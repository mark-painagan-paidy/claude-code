---
skill: vuln-check
description: Check if a specific vulnerability (CVE) exists in your environment using Orca Security and CrowdStrike
trigger: Use when the user asks to check for a CVE, vulnerability exposure, or affected endpoints in the environment
---

# Vulnerability Check Skill

Check if a specific vulnerability (CVE) or security issue exists in your environment by querying both Orca Security and CrowdStrike Falcon platforms.

## Purpose

This skill helps you quickly determine:
- Whether your environment is vulnerable to a specific CVE
- Which assets/endpoints are affected
- Severity and risk level of exposure
- Remediation status across platforms

## Usage

```bash
# Check for a specific CVE
/vuln-check CVE-2026-20230

# Check for a vulnerability by name
/vuln-check "FortiGate credential leak"

# Check with additional context
/vuln-check CVE-2026-12569 "PTC Windchill"
```

## Input Parameters

The skill accepts:
- **CVE ID** (required): CVE-YYYY-##### format (e.g., CVE-2026-20230)
- **Additional context** (optional): Product name, vulnerability description, or keywords

## Workflow

### 1. Parse Input
- Extract CVE ID from user input
- Identify additional context (product names, keywords, library names)
- Validate CVE format or library name

### 2. Search GitHub Organization (paidy)
For CVE or library name (e.g., libssh2, log4j, spring):
- **Get all repositories**: Use `gh repo list paidy --limit 1000` to get all org repos
- **Search in multiple file types**:
  - Dockerfiles: `yum update`, `apt install`, `apk add` commands
  - Dependency files: `package-lock.json`, `yarn.lock`, `Gemfile.lock`, `pom.xml`, `build.gradle`, `requirements.txt`, `go.mod`, `Cargo.lock`
  - Docker compose: `docker-compose.yml`, `docker-compose.yaml`
  - CI/CD configs: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`
- **Search strategy**: For each repo, check via GitHub API (`gh api repos/paidy/{repo}/contents/{file}`)
- **Output**: List of repositories containing the vulnerable library/package

### 3. Query Orca Security
Use `mcp__orca__ask_orca` to check cloud environment:
- Query: "Am I vulnerable to [CVE-ID]? Show me all affected assets."
- Alternative: "Show me assets affected by [vulnerability name]"
- Orca returns: Risk level, affected asset types, and top results

### 4. Query CrowdStrike Falcon
Use `mcp__crowdstrike__falcon_search_vulnerabilities` to check endpoints:

**Step 1**: Search for the CVE with host info
```
filter: "cve.id:'CVE-YYYY-#####'"
facet: "host_info"
limit: 100
```

**Step 2**: If results found, get remediation details
```
filter: "cve.id:'CVE-YYYY-#####'"
facet: "remediation"
limit: 100
```

**Step 3**: Get detailed CVE information
```
filter: "cve.id:'CVE-YYYY-#####'"
facet: "cve"
limit: 10
```

### 5. Get Affected Host Details
For each affected host ID from CrowdStrike:
- Use `mcp__crowdstrike__falcon_get_host_details` to get full context
- Extract: hostname, OS, IP addresses, last seen, agent version

### 5. Generate Consolidated Report

Output format:

```markdown
# Vulnerability Assessment Report
**CVE**: [CVE-ID]
**Generated**: [timestamp]

---

## 📋 Summary

**Vulnerability**: [CVE description]
**Severity**: [CVSS score and rating]
**Status**: [Exploited in the wild? / Patch available?]

**Exposure Summary**:
- Orca Security: [# affected assets] | Risk Level: [Critical/High/Medium/Low]
- CrowdStrike: [# affected endpoints]
- **Total Unique Assets**: [combined count]

---

## ☁️ Orca Security - Cloud Assets

**Risk Level**: [risk level from Orca]

**Affected Asset Types**:
[List asset types with counts]

**Top Affected Assets** (up to 10):
1. [Asset name] - [Asset type] - [Additional context]
2. ...

---

## 💻 CrowdStrike - Endpoints

**Total Affected Endpoints**: [count]

**Breakdown by Platform**:
- Windows: [count]
- Linux: [count]
- macOS: [count]

**Vulnerability Status**:
- Open: [count]
- Closed: [count]
- In Progress: [count]

### Affected Endpoints

| Hostname | OS | IP Address | Agent Version | Status | Last Seen |
|----------|-----|-----------|---------------|--------|-----------|
| [hostname] | [os] | [ip] | [version] | [status] | [timestamp] |

---

## 🔧 Remediation Information

**From CrowdStrike**:
- [Remediation guidance]
- [Patch information]
- [Workarounds if available]

**Recommended Actions**:
1. [Priority action items]
2. [Patching recommendations]
3. [Mitigation steps]

---

## 🔗 References

- CVE Details: https://cve.mitre.org/cgi-bin/cvename.cgi?name=[CVE-ID]
- NIST NVD: https://nvd.nist.gov/vuln/detail/[CVE-ID]
- CrowdStrike Console: [Link to affected assets]
- Orca Security Console: [Link to findings]
```

## Error Handling

### CVE Not Found
If the vulnerability is not detected in either platform:
```markdown
✅ **Good News**: No affected assets found for [CVE-ID]

**Orca Security**: No vulnerable assets detected
**CrowdStrike**: No affected endpoints found

**Note**: This may mean:
- Your environment is not vulnerable
- Assets are patched/remediated
- Detection signatures not yet available
- CVE does not apply to your asset types
```

### API Errors
Handle connection or authentication issues:
- Log the error
- Report which service is unavailable
- Provide partial results from available services

### Invalid CVE Format
If input doesn't match CVE pattern:
```markdown
❌ Invalid CVE format. Please use: CVE-YYYY-##### (e.g., CVE-2026-20230)
```

## Implementation Notes

1. **Parallel Queries**: Run Orca and CrowdStrike queries in parallel for speed
2. **Pagination**: Handle large result sets (>100 endpoints) with pagination
3. **Deduplication**: If an asset appears in both platforms, note it clearly
4. **Context Enrichment**: Cross-reference with CISA KEV if CVE is in the catalog
5. **Caching**: Cache CVE metadata (CVSS, description) to reduce external API calls
6. **Severity Mapping**: Normalize severity ratings between platforms

## Advanced Features

### Check Multiple CVEs
```bash
/vuln-check CVE-2026-20230,CVE-2026-20245,CVE-2025-67038
```
Generate a combined report for multiple vulnerabilities.

### Filter by Status
```bash
/vuln-check CVE-2026-20230 --status=open
```
Only show unpatched/open vulnerabilities.

### Export Results
Automatically save report to file:
```bash
/vuln-check CVE-2026-20230 --export
```

## Integration with Other Skills

- **threat-intel**: After generating a threat intelligence report, use this skill to check if any reported CVEs affect your environment
- **Security Review**: Include vulnerability checks as part of security assessments

## Example Queries

```bash
# Quick CVE check
/vuln-check CVE-2026-20230

# Check with product context
/vuln-check CVE-2026-20245 Cisco SD-WAN

# Check FortiGate credential leak
/vuln-check CVE-2026-50751 FortiGate

# Check multiple related CVEs
/vuln-check CVE-2026-34910,CVE-2026-34909,CVE-2026-34908
```

## Output Example

```markdown
# Vulnerability Assessment Report
**CVE**: CVE-2026-20230
**Generated**: 2026-06-26 16:30 JST

---

## 📋 Summary

**Vulnerability**: Cisco Unified Communications Manager - SSRF
**Severity**: CVSS 8.6 (High)
**Status**: ⚠️ Actively exploited in the wild

**Exposure Summary**:
- Orca Security: 3 affected assets | Risk Level: High
- CrowdStrike: 12 affected endpoints
- **Total Unique Assets**: 15

---

## ☁️ Orca Security - Cloud Assets

**Risk Level**: High

**Affected Asset Types**:
- Virtual Machines: 2
- Containers: 1

**Top Affected Assets**:
1. cisco-ucm-prod-01 - VM (AWS EC2) - Production
2. cisco-ucm-staging - VM (AWS EC2) - Staging
3. ucm-container-east - Container (EKS) - Development

---

## 💻 CrowdStrike - Endpoints

**Total Affected Endpoints**: 12

**Breakdown by Platform**:
- Windows: 8
- Linux: 4
- macOS: 0

**Vulnerability Status**:
- Open: 10
- Closed: 2
- In Progress: 0

### Affected Endpoints

| Hostname | OS | IP Address | Agent Version | Status | Last Seen |
|----------|-----|-----------|---------------|--------|-----------|
| SRV-CISCO-PROD01 | Windows Server 2019 | 10.0.1.50 | 7.14.16303 | Open | 2026-06-26 15:45 |
| SRV-CISCO-PROD02 | Windows Server 2019 | 10.0.1.51 | 7.14.16303 | Open | 2026-06-26 15:42 |
| cisco-linux-node1 | RHEL 8.5 | 10.0.2.10 | 7.14.16303 | Closed | 2026-06-26 14:20 |

---

## 🔧 Remediation Information

**From CrowdStrike**:
- Upgrade to Cisco Unified CM 12.5(1)SU8 or later
- Apply security patch from Cisco Advisory
- Workaround: Restrict access to management interface

**Recommended Actions**:
1. **Immediate**: Patch all production systems (8 endpoints) by Jun 28, 2026
2. **High Priority**: Apply workarounds to internet-facing instances
3. **Monitor**: Check for exploitation indicators in logs

---

## 🔗 References

- CVE Details: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-20230
- NIST NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-20230
- CISA KEV: Listed (Due Date: 2026-06-28)
- Cisco Advisory: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-cucm-ssrf-###
```

## Notes

- Ensure both Orca Security and CrowdStrike MCP servers are configured
- Results are real-time snapshots; re-run for updated status
- Large environments may require pagination handling
- Some CVEs may only appear in one platform depending on asset coverage
