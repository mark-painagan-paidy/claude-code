#!/usr/bin/env python3
"""
Jira PII Scanner
Scans Jira issues for potential PII (emails, phone numbers, SSNs, credit cards, etc.)
"""

import re
import json
import sys
from typing import List, Dict, Any, Set
from datetime import datetime
import argparse

# Try to import requests, provide helpful error if missing
try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("Error: 'requests' library not found. Install it with: pip install requests")
    sys.exit(1)


class PIIPattern:
    """PII pattern definitions with regex and descriptions"""

    PATTERNS = {
        'email': {
            'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'description': 'Email address',
            'severity': 'HIGH'
        },
        'phone_us': {
            'regex': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            'description': 'US Phone number',
            'severity': 'HIGH'
        },
        'phone_intl': {
            'regex': r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            'description': 'International phone number',
            'severity': 'HIGH'
        },
        'ssn': {
            'regex': r'\b\d{3}-\d{2}-\d{4}\b',
            'description': 'US Social Security Number',
            'severity': 'CRITICAL'
        },
        'credit_card': {
            'regex': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'description': 'Credit card number',
            'severity': 'CRITICAL'
        },
        'ip_address': {
            'regex': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'description': 'IP address',
            'severity': 'MEDIUM'
        },
        'passport': {
            'regex': r'\b[A-Z]{1,2}\d{6,9}\b',
            'description': 'Passport number',
            'severity': 'CRITICAL'
        },
        'address': {
            'regex': r'\b\d{1,5}\s+[\w\s]{1,50}\s+(?:street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln|drive|dr|court|ct)\b',
            'description': 'Street address',
            'severity': 'MEDIUM'
        }
    }


class JiraPIIScanner:
    """Scanner for detecting PII in Jira issues"""

    def __init__(self, jira_url: str, username: str, api_token: str, max_results: int = 100):
        self.jira_url = jira_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, api_token)
        self.max_results = max_results
        self.session = requests.Session()
        self.session.auth = self.auth
        self.findings: List[Dict[str, Any]] = []

    def search_issues(self, jql: str = "") -> List[Dict[str, Any]]:
        """Search Jira issues using JQL"""
        issues = []
        start_at = 0

        if not jql:
            jql = "ORDER BY created DESC"

        while True:
            url = f"{self.jira_url}/rest/api/3/search"
            params = {
                'jql': jql,
                'startAt': start_at,
                'maxResults': min(self.max_results, 100),  # API limit is 100 per request
                'fields': 'summary,description,comment,created,reporter,assignee,status'
            }

            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                issues.extend(data.get('issues', []))

                total = data.get('total', 0)
                start_at += len(data.get('issues', []))

                print(f"Fetched {start_at}/{min(total, self.max_results)} issues...", file=sys.stderr)

                if start_at >= total or start_at >= self.max_results:
                    break

            except requests.exceptions.RequestException as e:
                print(f"Error fetching issues: {e}", file=sys.stderr)
                break

        return issues

    def scan_text(self, text: str, context: str) -> List[Dict[str, Any]]:
        """Scan text for PII patterns"""
        if not text:
            return []

        findings = []

        for pattern_name, pattern_info in PIIPattern.PATTERNS.items():
            matches = re.finditer(pattern_info['regex'], text, re.IGNORECASE)

            for match in matches:
                # Create a snippet with context (30 chars before and after)
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                snippet = text[start:end].replace('\n', ' ').strip()

                findings.append({
                    'type': pattern_name,
                    'description': pattern_info['description'],
                    'severity': pattern_info['severity'],
                    'match': match.group(),
                    'context': context,
                    'snippet': f"...{snippet}..."
                })

        return findings

    def scan_issue(self, issue: Dict[str, Any]) -> None:
        """Scan a single issue for PII"""
        issue_key = issue['key']
        fields = issue.get('fields', {})

        issue_findings = []

        # Scan summary
        summary = fields.get('summary', '')
        issue_findings.extend(self.scan_text(summary, 'Summary'))

        # Scan description
        description = fields.get('description', '')
        if isinstance(description, dict):
            # New Jira format (Atlassian Document Format)
            description = self._extract_text_from_adf(description)
        issue_findings.extend(self.scan_text(description, 'Description'))

        # Scan comments
        comments = fields.get('comment', {}).get('comments', [])
        for idx, comment in enumerate(comments):
            comment_body = comment.get('body', '')
            if isinstance(comment_body, dict):
                comment_body = self._extract_text_from_adf(comment_body)

            comment_findings = self.scan_text(comment_body, f'Comment #{idx + 1}')
            issue_findings.extend(comment_findings)

        # If we found PII, add to overall findings
        if issue_findings:
            self.findings.append({
                'issue_key': issue_key,
                'summary': summary,
                'url': f"{self.jira_url}/browse/{issue_key}",
                'status': fields.get('status', {}).get('name', 'Unknown'),
                'created': fields.get('created', ''),
                'reporter': fields.get('reporter', {}).get('displayName', 'Unknown'),
                'pii_found': issue_findings,
                'pii_count': len(issue_findings)
            })

    def _extract_text_from_adf(self, adf: Dict[str, Any]) -> str:
        """Extract plain text from Atlassian Document Format"""
        if not isinstance(adf, dict):
            return str(adf)

        text_parts = []

        def extract_recursive(node):
            if isinstance(node, dict):
                if node.get('type') == 'text':
                    text_parts.append(node.get('text', ''))

                for key in ['content', 'nodes']:
                    if key in node:
                        content = node[key]
                        if isinstance(content, list):
                            for item in content:
                                extract_recursive(item)
                        else:
                            extract_recursive(content)

        extract_recursive(adf)
        return ' '.join(text_parts)

    def generate_report(self, output_format: str = 'text') -> str:
        """Generate a report of findings"""
        if output_format == 'json':
            return json.dumps(self.findings, indent=2)

        # Text report
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("JIRA PII SCAN REPORT")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 80)
        report_lines.append(f"\nTotal issues scanned: {len(self.findings)}")

        if not self.findings:
            report_lines.append("\n✓ No PII patterns detected!")
            return '\n'.join(report_lines)

        # Severity summary
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0}
        for finding in self.findings:
            for pii in finding['pii_found']:
                severity_counts[pii['severity']] += 1

        report_lines.append(f"\nPII Findings Summary:")
        report_lines.append(f"  CRITICAL: {severity_counts['CRITICAL']}")
        report_lines.append(f"  HIGH:     {severity_counts['HIGH']}")
        report_lines.append(f"  MEDIUM:   {severity_counts['MEDIUM']}")
        report_lines.append(f"  TOTAL:    {sum(severity_counts.values())}")

        # Detailed findings
        report_lines.append("\n" + "=" * 80)
        report_lines.append("DETAILED FINDINGS")
        report_lines.append("=" * 80)

        for finding in sorted(self.findings, key=lambda x: -x['pii_count']):
            report_lines.append(f"\n[{finding['issue_key']}] {finding['summary']}")
            report_lines.append(f"URL: {finding['url']}")
            report_lines.append(f"Status: {finding['status']} | Reporter: {finding['reporter']}")
            report_lines.append(f"PII Instances Found: {finding['pii_count']}")
            report_lines.append("-" * 80)

            # Group by type
            pii_by_type = {}
            for pii in finding['pii_found']:
                pii_type = pii['description']
                if pii_type not in pii_by_type:
                    pii_by_type[pii_type] = []
                pii_by_type[pii_type].append(pii)

            for pii_type, pii_list in pii_by_type.items():
                report_lines.append(f"\n  [{pii_list[0]['severity']}] {pii_type} ({len(pii_list)} instance(s))")
                for pii in pii_list[:3]:  # Show first 3 instances
                    report_lines.append(f"    Location: {pii['context']}")
                    report_lines.append(f"    Snippet: {pii['snippet']}")
                if len(pii_list) > 3:
                    report_lines.append(f"    ... and {len(pii_list) - 3} more")

        return '\n'.join(report_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Scan Jira issues for PII (emails, phone numbers, SSNs, etc.)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan all issues (up to 1000)
  python jira-pii-scanner.py --url https://yourcompany.atlassian.net --user your@email.com --token YOUR_API_TOKEN

  # Scan specific project
  python jira-pii-scanner.py --url https://yourcompany.atlassian.net --user your@email.com --token YOUR_API_TOKEN --jql "project = PROJ"

  # Scan recent issues
  python jira-pii-scanner.py --url https://yourcompany.atlassian.net --user your@email.com --token YOUR_API_TOKEN --jql "created >= -30d"

  # Output as JSON
  python jira-pii-scanner.py --url https://yourcompany.atlassian.net --user your@email.com --token YOUR_API_TOKEN --format json > report.json

API Token: Generate at https://id.atlassian.com/manage-profile/security/api-tokens
        """
    )

    parser.add_argument('--url', required=True, help='Jira instance URL (e.g., https://yourcompany.atlassian.net)')
    parser.add_argument('--user', required=True, help='Jira username/email')
    parser.add_argument('--token', required=True, help='Jira API token')
    parser.add_argument('--jql', default='', help='JQL query to filter issues (default: all issues)')
    parser.add_argument('--max-results', type=int, default=1000, help='Maximum number of issues to scan (default: 1000)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')

    args = parser.parse_args()

    # Initialize scanner
    print(f"Initializing Jira PII Scanner...", file=sys.stderr)
    print(f"Target: {args.url}", file=sys.stderr)
    print(f"Max results: {args.max_results}", file=sys.stderr)

    scanner = JiraPIIScanner(args.url, args.user, args.token, args.max_results)

    # Search issues
    print(f"\nSearching issues with JQL: {args.jql or 'ORDER BY created DESC'}", file=sys.stderr)
    issues = scanner.search_issues(args.jql)
    print(f"Found {len(issues)} issues to scan\n", file=sys.stderr)

    # Scan each issue
    print("Scanning for PII patterns...", file=sys.stderr)
    for idx, issue in enumerate(issues, 1):
        if idx % 10 == 0:
            print(f"Scanned {idx}/{len(issues)} issues...", file=sys.stderr)
        scanner.scan_issue(issue)

    print(f"\nScan complete! Found PII in {len(scanner.findings)} issues.\n", file=sys.stderr)

    # Generate report
    report = scanner.generate_report(args.format)

    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == '__main__':
    main()
