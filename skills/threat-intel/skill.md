---
skill: threat-intel
description: Fetch cyber threat intelligence relevant to Japan, including breaches and Japan-related FinTech threats
trigger: Use when the user asks for threat intelligence, CTI updates, security threats, breaches, or latest vulnerabilities affecting Japan
---

# Threat Intelligence Skill

Fetch and analyze cyber threat intelligence from multiple sources, filtered for:
- **Geographic Focus**: Japan (APT groups, threat actors, campaigns, breaches targeting Japan)
- **Industry Focus**: FinTech threats ONLY if they involve Japan or Japanese organizations
- **Breach Focus**: Data breaches, security incidents, compromises affecting any sector in Japan

## Sources

Query the following sources in parallel:

### 1. CISA Known Exploited Vulnerabilities (KEV)
- URL: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
- Filter: All critical/high severity (these affect all industries including FinTech)
- Focus: Vulnerabilities being actively exploited

### 2. BleepingComputer News
- URL: `https://www.bleepingcomputer.com/`
- Filter: Recent security news, breaches, vulnerabilities
- Focus: Japan-related incidents, breaches, APT campaigns, or Japan-FinTech threats

### 3. The Hacker News
- URL: `https://thehackernews.com/`
- Filter: Latest cybersecurity news and breaches
- Focus: Japan-related threats, breaches, APT activity, or Japan-FinTech incidents

### 4. NVD Recent CVEs (Japan/Critical Infrastructure)
- URL: `https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=20`
- Filter: Critical/High severity CVEs
- Focus: Highlight any Japan-specific or widely exploited vulnerabilities

### 5. AlienVault OTX - Japan Pulses
- URL: `https://otx.alienvault.com/api/v1/pulses/subscribed`
- Search: `https://otx.alienvault.com/api/v1/search/pulses?q=japan`
- Note: Requires OTX API key (free tier available)

### 6. URLhaus Recent Malware URLs
- URL: `https://urlhaus.abuse.ch/downloads/json_recent/`
- Filter: Extract URLs with .jp domains or Japan-hosted infrastructure
- Focus: Malware distribution targeting Japan

### 7. ThreatFox Recent IOCs
- URL: `https://threatfox.abuse.ch/export/json/recent/`
- Filter: Look for Japan-related campaigns or infrastructure
- Focus: IOCs from APT groups known to target Japan

### 8. Security Vendor Intelligence
- CrowdStrike Blog: Search for "Japan" or APT groups targeting Japan
- Mandiant/Google TAG: APT groups targeting APAC region, Japan-specific breaches
- JPCERT/CC: Japan Computer Emergency Response Team advisories

### 9. CrowdStrike Falcon (if available)
Query your Falcon tenant for:
- Recent detections in your environment
- Threat actor intelligence matching Japan profile
- IOCs and indicators from Japan-related campaigns

## Filtering Criteria

**PRIMARY: Japan-related threats (ALL sectors):**
- APT groups: APT10 (MenuPass), APT40, Lazarus Group, APT41, Tick (Bronze Butler), Stone Panda
- Geographic targeting: Japan, Japanese organizations (domestic and overseas operations)
- Breaches: Any data breach, security incident, or compromise affecting Japanese companies or .jp infrastructure
- Language: Japanese-language phishing, documents
- Infrastructure: .jp domains, Japan-hosted C2, attacks originating from or targeting Japan

**SECONDARY: FinTech threats (ONLY if Japan-related):**
- **RULE**: Only include FinTech/financial sector threats if they explicitly involve Japan or Japanese organizations
- Industries: Banking, Financial Services in Japan, Payment processors operating in Japan
- Japanese FinTech companies, cryptocurrency exchanges operating in Japan
- Attack types: BEC, wire fraud, SWIFT attacks targeting Japanese financial institutions
- Technologies: Core banking systems used in Japan, payment gateways serving Japanese market

**Breach Intelligence Focus:**
- Data breaches affecting Japanese companies (any industry)
- Compromised Japanese infrastructure (.jp domains, Japan-hosted servers)
- Ransomware incidents in Japan
- Supply chain attacks affecting Japanese organizations
- Credential leaks from Japanese services

## Workflow

1. **Fetch intelligence**: Query all sources in parallel using WebFetch
2. **Generate report**: Compile and format the threat intelligence report
3. **Post to Slack**: Automatically post the complete report to Slack channel `C0BA3Q4NS6B` using `mcp__slack__slack_send_message`
4. **Confirm delivery**: Provide the Slack message link to the user

## Output Format

Structure the report as:

```markdown
# Threat Intelligence Report
**Generated**: [timestamp]
**Focus**: Japan | Breaches | Japan-FinTech

## 🚨 Critical Alerts
[High-priority threats requiring immediate attention]

## 💥 Recent Breaches & Incidents
[Data breaches, ransomware incidents, compromises affecting Japanese organizations or infrastructure]

## 🎯 Japan-Targeted Threats
[APT campaigns, malware, attacks specifically targeting Japan or Japanese organizations]

## 🏦 Japan FinTech Threats (if applicable)
[Financial sector threats ONLY if they involve Japan or Japanese financial institutions]

## 📊 Recent Vulnerabilities
[CVEs and exploited vulnerabilities with Japan relevance]

## 🔍 Indicators of Compromise (IOCs)
[Malicious IPs, domains, file hashes from Japan-related campaigns]

## 📰 Intelligence Reports
[Links to detailed reports from BleepingComputer, The Hacker News, security vendors]

## 🔗 Sources
[List all sources queried with timestamps]
```

## Implementation Notes

1. **Parallel fetching**: Use WebFetch for all HTTP sources simultaneously
2. **Error handling**: If a source is unavailable, note it but continue with others
3. **Deduplication**: Remove duplicate CVEs/IOCs across sources
4. **Prioritization Rules**:
   - PRIMARY: Any threat targeting Japan (all sectors, including breaches)
   - SECONDARY: FinTech threats ONLY if Japan-related
   - EXCLUDE: General FinTech threats without Japan connection
5. **Breach Focus**: Prioritize data breaches, ransomware incidents, compromises in Japan
6. **Freshness**: Include timestamps to show recency of intelligence
7. **Actionability**: For each threat, include: severity, affected products/organizations, mitigation steps
8. **Slack Integration**: After generating the report, automatically post to Slack channel `C0BA3Q4NS6B` using the `mcp__slack__slack_send_message` tool

## Usage

```bash
# Fetch latest threat intelligence (automatically posts to Slack)
/threat-intel

# Can be scheduled for daily updates (will auto-post to Slack each time)
/loop 24h /threat-intel
```

## Slack Integration

**Automatic Posting**: Every time this skill runs, it will automatically post the threat intelligence report to:
- **Slack Channel**: `C0BA3Q4NS6B` (https://exco.slack.com/archives/C0BA3Q4NS6B)
- **Format**: Formatted markdown report with sections for easy reading
- **Sections**: Critical alerts, breaches, Japan threats, IOCs, and recommended actions

The report will be posted using the Slack MCP integration (`mcp__slack__slack_send_message`).

## Setup Instructions

**Required:**
- Slack MCP server must be configured (appears to be already set up based on your mcp_config.json)

**Optional:**
- AlienVault OTX: Register at https://otx.alienvault.com
- Add to environment: `OTX_API_KEY=your_key_here`

Most sources work without authentication.
