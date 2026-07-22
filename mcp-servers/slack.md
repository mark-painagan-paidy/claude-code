# Slack MCP Server

**Package**: `@modelcontextprotocol/server-slack`  
**Type**: NPX (Node.js)  
**Status**: ✅ Active

## Purpose

Integration with Slack workspace for:
- Reading channels and messages
- Searching conversations
- Posting messages and updates
- Managing Slack canvases
- User profile lookups

## Configuration

```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "NODE_EXTRA_CA_CERTS": "/Users/mark.painagan/.claude/certs/combined-ca-bundle.pem"
  }
}
```

## Available Tools

### Message Operations
- `slack_send_message` - Send message to channel/user
- `slack_send_message_draft` - Send message draft
- `slack_schedule_message` - Schedule future message
- `slack_read_channel` - Read messages from channel
- `slack_read_thread` - Read thread replies
- `slack_search_public` - Search public channels
- `slack_search_public_and_private` - Search all accessible channels

### Canvas Operations
- `slack_create_canvas` - Create new canvas
- `slack_read_canvas` - Read canvas content (markdown)
- `slack_update_canvas` - Update canvas sections

### User Operations
- `slack_read_user_profile` - Get user profile info
- `slack_search_users` - Search users by name

### Channel Operations
- `slack_search_channels` - Search channels by name
- `slack_list_channel_members` - List channel members

### Reaction Operations
- `slack_add_reaction` - Add emoji reaction
- `slack_get_reactions` - Get reactions on message

### Other
- `slack_read_file` - Read file contents
- `slack_search_emojis` - Search custom emojis

## Usage in Skills

### threat-intel
**Purpose**: Read CTI channel for intelligence, post reports

```bash
# Read recent CTI channel messages
slack_read_channel(channel_id: "C04M2SB3EBD", limit: 200)

# Search for Japan-related threats
slack_search_public_and_private(query: "japan OR JPCERT in:<#C04M2SB3EBD>")

# Post threat intelligence report
slack_send_message(channel_id: "C0BA3Q4NS6B", text: report)
```

### update-security-report
**Purpose**: Update weekly security monitoring canvas

```bash
# Search for canvas by title
slack_search_public(query: "type:canvases \"Weekly Security Monitoring Report\"", content_types: "files")

# Read canvas content
slack_read_canvas(canvas_id: "F0BKT2Z1K32")

# Update canvas sections
slack_update_canvas(
  canvas_id: "F0BKT2Z1K32",
  sections: [
    {edit_type: "replace", section_id: "...", content: "..."}
  ]
)
```

## Authentication

Authenticated via OAuth during initial MCP setup. Token stored securely by Claude Code.

## Key Channels Referenced

- **CTI Channel**: `C04M2SB3EBD` (https://exco.slack.com/archives/C04M2SB3EBD)
- **Security Updates**: `C0BA3Q4NS6B` (https://exco.slack.com/archives/C0BA3Q4NS6B)

## Search Modifiers

```
in:#channel-name        - Search specific channel
from:@username          - Filter by author
after:YYYY-MM-DD       - Date filter
type:canvases          - Search canvases
has:link               - Messages with links
content_types="files"  - Search files only
```

## Canvas Markdown Format

Canvas uses Canvas-flavored Markdown:
- Headers: `#`, `##`, `###` (max 3 levels)
- User mentions: `![](@U15CTCJ83)`
- Channel mentions: `![](#C15CTCJ83)`
- Links: `[text](url)` (no angle brackets)
- Date headings: `![](slack_date:YYYY-MM-DD)`
- Callouts: `::: {.callout}\n...\n:::`

## Best Practices

1. **Reading channels**: Start with smaller limits, increase if needed
2. **Searching**: Use specific modifiers to narrow results
3. **Canvas updates**: Always read canvas first to get current section IDs
4. **Rate limiting**: Batch operations when possible

## Troubleshooting

**Canvas section ID errors**: Section IDs change after every update. Always read canvas before updating.

**Search no results**: Try broader query, check channel access permissions.

**Authentication expired**: Re-authenticate via `/mcp` dialog.

## Examples

### Post formatted message
```
slack_send_message(
  channel_id: "C0BA3Q4NS6B",
  text: "# Report\n\n**Status**: Complete\n- Item 1\n- Item 2"
)
```

### Search for recent security incidents
```
slack_search_public_and_private(
  query: "incident OR breach OR ransomware after:2026-07-01",
  sort: "timestamp",
  sort_dir: "desc"
)
```

### Read thread with context
```
slack_read_thread(
  channel_id: "C04M2SB3EBD",
  thread_ts: "1721234567.123456"
)
```
