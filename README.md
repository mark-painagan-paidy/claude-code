# Claude Code Skills

Custom Claude Code skills for SOC operations and security analysis.

## Overview

This repository contains custom skills for [Claude Code](https://claude.ai/code) designed to enhance SOC (Security Operations Center) workflows, particularly for phishing email analysis and threat intelligence.

## Available Skills

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

The phishing-analysis skill requires the Atlassian MCP server for Jira integration. Add to your Claude Code settings:

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

## Skill Structure

```
skills/
└── phishing-analysis/
    └── SKILL.md          # Main skill definition
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

### Permissions

The skills may prompt for permission to:
- Run DNS queries via `dig`
- Execute WHOIS lookups
- Make HTTP requests via `curl`
- Access Jira tickets via MCP
- Post comments to Jira tickets

## Usage Examples

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
