# MCP Servers Configuration

This directory documents the Model Context Protocol (MCP) servers configured for Claude Code integration.

## Active MCP Servers

### 1. **Slack** 💬
- **Package**: `@modelcontextprotocol/server-slack`
- **Type**: NPX (Node.js)
- **Purpose**: Slack workspace integration for reading channels, searching messages, posting updates, managing canvases
- **Status**: ✅ Active

**Capabilities:**
- Search public/private channels
- Read channel messages and threads
- Send messages and drafts
- Create and update canvases
- Manage reactions
- Read user profiles
- Schedule messages

**Key Tools:**
- `slack_read_channel` - Read messages from channels
- `slack_search_public` / `slack_search_public_and_private` - Search messages
- `slack_send_message` - Post messages
- `slack_read_canvas` / `slack_update_canvas` / `slack_create_canvas` - Canvas management
- `slack_read_thread` - Read thread replies
- `slack_read_user_profile` - Get user information

**Configuration:**
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "NODE_EXTRA_CA_CERTS": "/Users/mark.painagan/.claude/certs/combined-ca-bundle.pem"
  }
}
```

---

### 2. **GitHub** 🐙
- **Package**: `@modelcontextprotocol/server-github`
- **Type**: NPX (Node.js)
- **Purpose**: GitHub repository and issue management
- **Status**: ✅ Active

**Capabilities:**
- Repository management
- Issue and PR operations
- File content reading/writing
- Code search
- Branch management
- Commit operations

**Key Tools:**
- `search_repositories` - Search GitHub repos
- `search_code` - Search code across repos
- `get_file_contents` - Read file contents
- `create_or_update_file` - Modify files
- `create_issue` / `update_issue` - Issue management
- `create_pull_request` - Create PRs
- `list_commits` - View commit history
- `search_issues` - Search issues and PRs

**Configuration:**
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "NODE_EXTRA_CA_CERTS": "/Users/mark.painagan/.claude/certs/combined-ca-bundle.pem",
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_***"
  }
}
```

**Authentication**: Personal Access Token (PAT) required

---

### 3. **CrowdStrike Falcon** 🦅
- **Package**: `falcon-mcp`
- **Type**: UVX (Python)
- **Purpose**: CrowdStrike Falcon endpoint security and threat intelligence
- **Status**: ✅ Active

**Capabilities:**
- Vulnerability scanning
- Host/endpoint management
- Detection searching
- IOC (Indicators of Compromise) management
- Real-time response (RTR) sessions
- Threat intelligence queries
- Case management
- Shield (CSPM) monitoring

**Key Tools:**
- `falcon_search_vulnerabilities` - Search for CVEs in environment
- `falcon_get_host_details` - Get endpoint information
- `falcon_search_detections` - Search security detections
- `falcon_search_hosts` - Find hosts/endpoints
- `falcon_search_indicators` - Search threat indicators
- `falcon_search_iocs` - Search IOCs
- `falcon_init_rtr_session` - Start remote response session
- `falcon_search_cspm_assets` - Search cloud assets
- `falcon_create_case` - Create security cases

**Configuration:**
```json
{
  "command": "uvx",
  "args": ["--from", "falcon-mcp", "falcon-mcp"],
  "env": {
    "FALCON_CLIENT_ID": "***",
    "FALCON_CLIENT_SECRET": "***",
    "FALCON_BASE_URL": "https://api.crowdstrike.com"
  }
}
```

**Authentication**: API Client ID/Secret required

---

### 4. **Orca Security** 🐋
- **Type**: HTTP (Remote MCP Server)
- **URL**: `https://mcp.orcasecurity.io`
- **Purpose**: Cloud security posture management and vulnerability assessment
- **Status**: ✅ Active

**Capabilities:**
- Cloud asset vulnerability scanning
- Risk assessment
- Compliance checking
- Cloud security posture queries

**Key Tools:**
- `ask_orca` - Natural language queries about cloud security posture

**Configuration:**
```json
{
  "type": "http",
  "url": "https://mcp.orcasecurity.io"
}
```

**Authentication**: OAuth/API authentication handled by remote server

---

## Configuration File Location

**macOS/Linux**: `~/.claude/mcp_config.json`

## Adding New MCP Servers

To add a new MCP server:

1. Edit `~/.claude/mcp_config.json`
2. Add server configuration under `mcpServers` key
3. Restart Claude Code
4. Verify with `/mcp` command

Example:
```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "npx",
      "args": ["-y", "@your/mcp-server-package"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

## Certificate Configuration

Custom CA certificates are configured for corporate proxy/SSL inspection:
- **Location**: `/Users/mark.painagan/.claude/certs/combined-ca-bundle.pem`
- **Used by**: Slack, GitHub MCP servers
- **Purpose**: Trust corporate SSL certificates

## Usage in Skills

MCP servers are extensively used in custom skills:

- **threat-intel**: Uses Slack MCP to read CTI channel, post reports
- **phishing-analysis**: Uses Atlassian (Jira) MCP for ticket management
- **header-analysis**: Uses Atlassian MCP for email header analysis
- **vuln-check**: Uses Orca Security and CrowdStrike MCPs
- **update-security-report**: Uses Slack MCP for canvas updates

## Troubleshooting

### MCP Server Not Loading
1. Check server is listed: `/mcp` command
2. Verify credentials in `mcp_config.json`
3. Check Claude Code logs: `~/.claude/logs/`
4. Restart Claude Code

### Authentication Errors
- Verify API keys/tokens are valid and not expired
- Check environment variables are properly set
- Ensure network connectivity to remote servers

### Tool Not Found
- Run `/mcp` to see available tools
- Use `ToolSearch` to load deferred tool schemas
- Check MCP server is successfully connected

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit API keys/tokens to Git**
   - Use `.gitignore` for config files with secrets
   - Rotate tokens if accidentally exposed
   
2. **Use least-privilege access**
   - GitHub PAT: Limit scopes to necessary permissions
   - CrowdStrike API: Use read-only credentials when possible
   
3. **Audit MCP access**
   - Review what data MCP servers can access
   - Monitor usage in Claude Code logs
   
4. **Corporate compliance**
   - Ensure MCP usage complies with company policies
   - Use approved authentication methods

## MCP Registry

Official MCP servers: https://github.com/modelcontextprotocol/servers

Community MCP servers:
- **Atlassian**: Jira/Confluence integration
- **Filesystem**: Local file operations
- **PostgreSQL**: Database queries
- **AWS**: AWS service management
- And many more...

## Version Information

- **Claude Code**: Compatible with MCP protocol
- **Node.js MCP Servers**: Installed via `npx` (always latest)
- **Python MCP Servers**: Installed via `uvx` (always latest)
- **HTTP MCP Servers**: Remote-hosted, version managed by provider

## Related Documentation

- [MCP Protocol Specification](https://github.com/modelcontextprotocol/specification)
- [Building MCP Servers](https://github.com/modelcontextprotocol/servers/blob/main/DEVELOPMENT.md)
- [Claude Code MCP Guide](https://docs.anthropic.com/claude/docs/mcp)
