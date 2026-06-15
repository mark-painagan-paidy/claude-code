# Claude Code Skills

Custom Claude Code skills for SOC operations and security analysis.

## Overview

This repository contains custom skills for [Claude Code](https://claude.ai/code) designed to enhance SOC (Security Operations Center) workflows, particularly for phishing email analysis and threat intelligence.

## Available Skills

### 🛡️ Threat Intelligence (CTI)

Automated cyber threat intelligence gathering focused on Japan, breaches, and Japan-related FinTech threats. Fetches intelligence from multiple OSINT sources and posts reports to Slack.

**Features:**
- Multi-source intelligence gathering (BleepingComputer, The Hacker News, CISA KEV, JPCERT/CC)
- Japan-focused threat monitoring (APT groups, breaches, incidents)
- Breach intelligence (data breaches, ransomware, compromises)
- Japan-FinTech threat tracking (only if Japan-related)
- Automatic Slack integration for report delivery
- IOC extraction and vulnerability tracking

**Sources:**
- BleepingComputer & The Hacker News (latest security news)
- CISA Known Exploited Vulnerabilities (KEV)
- JPCERT/CC (Japan Computer Emergency Response Team)
- URLhaus & ThreatFox (malware IOCs)
- CrowdStrike & Mandiant threat intelligence

**Usage:** 
```bash
/threat-intel                    # Generate report and post to Slack
/loop 24h /threat-intel         # Daily automated reports
```

[View detailed documentation →](skills/threat-intel/skill.md)

---

### 🎣 Phishing Analysis

Automated phishing email analysis that integrates with Jira Service Desk tickets.

**Features:**
- Domain and DNS reputation checks (SPF, DMARC, WHOIS)
- URL analysis and redirect tracking
- Email authentication verification
- Infrastructure identification
- Automated verdict generation
- Results posted directly to Jira tickets

**Usage:** `/phishing-analysis SOCSD-12345`

[View detailed documentation →](skills/phishing-analysis/SKILL.md)

---

### 📧 Header Analysis

Email header analysis for authentication verification and routing analysis.

**Usage:** `/header-analysis`

[View detailed documentation →](skills/header-analysis/)

## Installation

### Prerequisites

- Claude Code CLI, Desktop app, or Web interface
- Atlassian MCP server configured (for Jira integration)
- Access to SOC Service Desk Jira project

### Setup Instructions

1. **Clone this repository:**
   ```bash
   git clone https://github.com/mark-painagan-paidy/claude-code-skills.git
   cd claude-code-skills
   ```

2. **Copy skills to Claude Code directory:**
   ```bash
   cp -r skills/* ~/.claude/skills/
   ```

3. **Verify installation:**
   ```bash
   ls ~/.claude/skills/
   ```

4. **Restart Claude Code** (if using CLI or Desktop app)

5. **Test the skill:**
   Type `/skills` in Claude Code to see available skills

### MCP Server Configuration

Skills require various MCP servers for integrations:

**For phishing-analysis (Jira integration):**
```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-atlassian"]
    }
  }
}
```

**For threat-intel (Slack integration):**
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"]
    }
  }
}
```

## Skill Structure

```
skills/
├── threat-intel/
│   └── skill.md          # Threat intelligence gathering
├── phishing-analysis/
│   └── SKILL.md          # Phishing email analysis
└── header-analysis/
    └── skill.md          # Email header analysis
```

Each skill follows the Claude Code skill format:
- Frontmatter with metadata (name, description, invocation)
- Detailed instructions and analysis framework
- Tool and command references
- Example usage and output formats

## Requirements

### System Tools
- `dig` - DNS lookups
- `whois` - Domain registration info
- `curl` - URL testing and HTTP requests

### MCP Servers
- **Atlassian MCP** - Jira integration for ticket management
- **Slack MCP** - Slack integration for threat intelligence reports

### Permissions

The skills may prompt for permission to:
- Run DNS queries via `dig`
- Execute WHOIS lookups
- Make HTTP requests via `curl`
- Access Jira tickets via MCP
- Post comments to Jira tickets

## Usage Examples

### Threat Intelligence

```bash
# Generate and post threat intelligence report to Slack
/threat-intel

# Schedule daily automated reports
/loop 24h /threat-intel
```

The skill will:
1. Fetch intelligence from multiple sources (BleepingComputer, The Hacker News, CISA, JPCERT/CC)
2. Filter for Japan-related threats, breaches, and APT activity
3. Extract IOCs and vulnerability information
4. Generate comprehensive CTI report
5. Automatically post report to configured Slack channel

### Phishing Analysis

```bash
# Analyze a phishing report in Jira
/phishing-analysis SOCSD-33563
```

The skill will:
1. Fetch the ticket details from Jira
2. Extract email headers, URLs, and content
3. Perform DNS and domain analysis
4. Test URL reputation and redirects
5. Generate a comprehensive analysis report
6. Post findings as a comment to the ticket

### Header Analysis

```bash
# Analyze email headers for authentication
/header-analysis
```

The skill will analyze email headers for SPF, DKIM, DMARC verification and routing information.

## Contributing

Feel free to:
- Add new skills for SOC operations
- Improve existing analysis frameworks
- Enhance documentation
- Report issues or suggest features

### Adding New Skills

1. Create a new directory under `skills/`
2. Add a `SKILL.md` file with proper frontmatter
3. Document the skill's purpose, usage, and requirements
4. Test thoroughly before committing

## License

This project is provided as-is for internal use and learning purposes.

## Author

**Mark Painagan**  
SOC Analyst | Security Operations

## Acknowledgments

- Built for [Claude Code](https://claude.ai/code) by Anthropic
- Integrates with Atlassian Jira via MCP
- Uses standard security analysis tools and frameworks

---

**Last Updated:** June 2026
