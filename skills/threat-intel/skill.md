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

### 8. Internal CTI Slack Channel
- **Channel ID**: `C04M2SB3EBD` (https://exco.slack.com/archives/C04M2SB3EBD)
- **Method**: Use `mcp__slack__slack_read_channel` (primary) and `mcp__slack__slack_search_public_and_private` (secondary)
- **Primary Strategy**: Read recent messages (last 100-200 messages, ~3-7 days)
  - Most intelligence is in **file attachments** (CSA reports, JPCERT advisories)
  - Parse message text and file metadata for relevant content
  - Look for patterns: "CSA-", "CSDR-", "JPCERT", ".jp", breach names, company names
- **Search Strategies** (if needed for deeper analysis):
  1. Broad geographic: `japan OR japanese OR .jp OR JPCERT OR APAC OR Asia OR China OR Korea OR "South Korea" OR "North Korea"`
  2. Breach/incident keywords: `breach OR ransomware OR "data breach" OR leak OR compromised OR hacked OR extortion OR stolen`
  3. APT groups: `APT10 OR APT40 OR Lazarus OR APT41 OR Tick OR "Stone Panda" OR "Bronze Butler" OR MenuPass OR Kimsuky OR APT37`
  4. Critical infrastructure: `fortinet OR FortiGate OR cisco OR "supply chain" OR vulnerability OR CVE OR zero-day OR 0day`
  5. File search: Search with `content_types="files"` to find PDF/HTML reports
- **Filter Priority**:
  1. JPCERT/CC advisories (Japan CERT - highest priority)
  2. CrowdStrike reports mentioning Japan, APAC, or relevant threat actors
  3. Breach incidents affecting Asian companies or .jp domains
  4. APT campaigns with APAC targeting
  5. Critical vulnerabilities in widely-used infrastructure
- **Output**: Include report IDs (CSA-#, CSDR-#), JPCERT advisories, timestamps, and key findings

### 9. Security Vendor Intelligence
- CrowdStrike Blog: Search for "Japan" or APT groups targeting Japan
- Mandiant/Google TAG: APT groups targeting APAC region, Japan-specific breaches
- JPCERT/CC: Japan Computer Emergency Response Team advisories

### 10. CrowdStrike Falcon (if available)
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

1. **Fetch intelligence**: Query all sources in parallel
   - Use WebFetch for external sources (CISA, BleepingComputer, etc.)
   - Use `mcp__slack__slack_read_channel` and `mcp__slack__slack_search_public_and_private` for internal CTI Slack channel
2. **Scan CTI Slack Channel**: Specifically search the internal CTI channel (`C04M2SB3EBD`) for:
   - Recent messages mentioning Japan, Japanese organizations, or .jp domains
   - Breach reports, ransomware incidents, or data leaks
   - APT activity targeting Japan or APAC region
   - Any threat intelligence shared by the team that matches filtering criteria
3. **Generate report**: Compile and format the threat intelligence report
4. **Post to Slack**: Automatically post the complete report to Slack channel `C0BA3Q4NS6B` using `mcp__slack__slack_send_message`
5. **Confirm delivery**: Provide the Slack message link to the user

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

## 💬 Internal CTI Channel Highlights
[Recent intelligence from internal CTI Slack channel related to Japan, breaches, or relevant threats]

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
2. **Internal CTI Slack Scanning**:
   - **PRIMARY METHOD**: Use `mcp__slack__slack_read_channel` with channel_id `C04M2SB3EBD` to fetch last 100-200 messages
   - **Parse message content for**:
     - CrowdStrike report IDs: CSA-######, CSDR-######
     - JPCERT advisories: AT######, WR######
     - File attachments (HTML reports from Slackbot)
     - Keywords: Japan, Japanese, JPCERT, APAC, Asia, breach, ransomware, APT groups, FortiGate, Cisco, zero-day
     - Company/victim names in breach reports
   - **SECONDARY METHOD**: Use `mcp__slack__slack_search_public_and_private` for deep searches:
     - Geographic: `"japan OR japanese OR .jp OR JPCERT OR APAC in:<#C04M2SB3EBD> after:YYYY-MM-DD"`
     - Incidents: `"breach OR ransomware OR leak OR compromised in:<#C04M2SB3EBD> after:YYYY-MM-DD"`
     - APT actors: `"APT10 OR APT40 OR Lazarus OR APT41 OR Kimsuky in:<#C04M2SB3EBD> after:YYYY-MM-DD"`
     - Files: Use `content_types="files"` to search report attachments
   - **Extract and report**:
     - Report IDs and titles (e.g., "CSA-260773: Brazil Emergency Alert System Breach")
     - JPCERT advisory numbers and summaries
     - Key findings from CrowdStrike reports relevant to Japan/APAC
     - Breach victims, threat actors, TTPs mentioned
     - Include Slack message timestamps for reference
3. **Error handling**: If a source is unavailable, note it but continue with others
4. **Deduplication**: Remove duplicate CVEs/IOCs across sources, including duplicates from internal Slack channel
5. **Prioritization Rules**:
   - PRIMARY: Any threat targeting Japan (all sectors, including breaches)
   - SECONDARY: FinTech threats ONLY if Japan-related
   - EXCLUDE: General FinTech threats without Japan connection
6. **Breach Focus**: Prioritize data breaches, ransomware incidents, compromises in Japan
7. **Freshness**: Include timestamps to show recency of intelligence
8. **Actionability**: For each threat, include: severity, affected products/organizations, mitigation steps
9. **Slack Integration**: After generating the report, automatically post to Slack channel `C0BA3Q4NS6B` using the `mcp__slack__slack_send_message` tool

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
