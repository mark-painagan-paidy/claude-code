# Atlassian MCP Server (Jira & Confluence)

**Type**: Cloud-connected (via claude.ai)  
**Status**: ✅ Active

## Purpose

Integration with Atlassian products for:
- Jira issue/ticket management
- Confluence page reading/editing
- Project metadata queries
- Comments and worklogs
- Issue transitions and workflows

## Configuration

Atlassian MCP is connected through your claude.ai account via OAuth. No local configuration needed in `mcp_config.json`.

**Connected Workspace**: paidy-portal.atlassian.net

## Available Tools

### Jira - Issue Operations
- `mcp__atlassian__getJiraIssue` - Get issue details
- `mcp__atlassian__createJiraIssue` - Create new issue
- `mcp__atlassian__editJiraIssue` - Update issue fields
- `mcp__atlassian__addCommentToJiraIssue` - Add comment to issue
- `mcp__atlassian__addWorklogToJiraIssue` - Add work log entry
- `mcp__atlassian__transitionJiraIssue` - Transition issue status

### Jira - Search & Query
- `mcp__atlassian__searchJiraIssuesUsingJql` - Search with JQL
- `mcp__atlassian__getVisibleJiraProjects` - List accessible projects
- `mcp__atlassian__getJiraProjectIssueTypesMetadata` - Get project metadata
- `mcp__atlassian__getJiraIssueTypeMetaWithFields` - Get issue type fields
- `mcp__atlassian__getTransitionsForJiraIssue` - Get available transitions

### Jira - Links
- `mcp__atlassian__createIssueLink` - Link issues together
- `mcp__atlassian__getIssueLinkTypes` - Get available link types
- `mcp__atlassian__getJiraIssueRemoteIssueLinks` - Get remote links

### Confluence - Page Operations
- `mcp__atlassian__getConfluencePage` - Read page content
- `mcp__atlassian__createConfluencePage` - Create new page
- `mcp__atlassian__updateConfluencePage` - Update existing page
- `mcp__atlassian__getConfluencePageDescendants` - Get child pages

### Confluence - Comments
- `mcp__atlassian__createConfluenceInlineComment` - Add inline comment
- `mcp__atlassian__createConfluenceFooterComment` - Add footer comment
- `mcp__atlassian__getConfluencePageInlineComments` - Get inline comments
- `mcp__atlassian__getConfluencePageFooterComments` - Get footer comments
- `mcp__atlassian__getConfluenceCommentChildren` - Get comment replies

### Confluence - Search & Navigation
- `mcp__atlassian__getConfluenceSpaces` - List Confluence spaces
- `mcp__atlassian__getPagesInConfluenceSpace` - List pages in space
- `mcp__atlassian__searchConfluenceUsingCql` - Search with CQL

### General
- `mcp__atlassian__search` - Universal search
- `mcp__atlassian__getAccessibleAtlassianResources` - List resources
- `mcp__atlassian__atlassianUserInfo` - Get user information
- `mcp__atlassian__lookupJiraAccountId` - Lookup user by email
- `mcp__atlassian__fetch` - Generic API fetch

## Usage in Skills

### phishing-analysis
**Purpose**: Fetch SOCSD tickets, update fields, post analysis

```javascript
// Get ticket details
mcp__atlassian__getJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345"
})

// Update custom fields
mcp__atlassian__editJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345",
  fields: {
    "customfield_10805": {"value": "Phishing Report"},
    "customfield_11136": {"value": "Internal (Paidy Employee)"},
    "customfield_10834": "attacker@evil.com",
    "customfield_10836": {"value": "Email"},
    "customfield_10837": [
      {"value": "Impersonation"},
      {"value": "Malicious domain/url"}
    ]
  }
})

// Post analysis comment
mcp__atlassian__addCommentToJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345",
  comment: "## Phishing Analysis Results\n\n..."
})
```

### header-analysis
**Purpose**: Fetch email headers from tickets, post analysis

```javascript
// Get ticket with email headers
mcp__atlassian__getJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-33563"
})

// Post header analysis
mcp__atlassian__addCommentToJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-33563",
  comment: "## Email Header Analysis Results\n\n..."
})
```

## Common Jira Projects

- **SOCSD**: SOC Service Desk (phishing reports, security incidents)
- Access other projects via `getVisibleJiraProjects()`

## JQL (Jira Query Language) Examples

### Search issues
```
project = SOCSD AND status = Open
created >= -7d AND assignee = currentUser()
labels = phishing AND resolution = Unresolved
project = SOCSD ORDER BY created DESC
```

### Common JQL operators
- `=`, `!=`, `>`, `>=`, `<`, `<=`
- `IN (value1, value2)`
- `NOT IN (value1, value2)`
- `IS EMPTY`, `IS NOT EMPTY`
- `~` (contains text)

## Custom Field Mapping (SOCSD)

### Request Category (`customfield_10805`)
**Type**: Single select
```json
{"value": "Phishing Report"}
```
Options: Phishing Report, Spam, Internal Email, Phishing Exercise, Test, Takedown Request, Non-phishing Related Concern

### Customer Type (`customfield_11136`)
**Type**: Single select
```json
{"value": "Internal (Paidy Employee)"}
```
Options: Internal (Paidy Employee), External (Paidy Customers)

### Attacker's Email Address (`customfield_10834`)
**Type**: Text field
```json
"attacker@example.com"
```

### Phishing Medium (`customfield_10836`)
**Type**: Single select
```json
{"value": "Email"}
```
Options: Email, SMS

### Phishing Techniques (`customfield_10837`)
**Type**: Multi-select
```json
[
  {"value": "Impersonation"},
  {"value": "Malicious domain/url"}
]
```
Options: Impersonation, Malicious domain/url, Malicious Attachment, Marketing Email, Legitimate Email, Phishing Exercise, Account Concern, Billing Concern, Paidy Partner, Test

## Issue Transitions

Get available transitions:
```javascript
mcp__atlassian__getTransitionsForJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345"
})
```

Transition issue:
```javascript
mcp__atlassian__transitionJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345",
  transition: {
    id: "31"  // Transition ID from getTransitions
  }
})
```

## CQL (Confluence Query Language) Examples

### Search pages
```
type = page AND space = SEC
title ~ "security" AND lastModified >= now("-7d")
creator = currentUser() AND space = TEAM
```

## Field Value Formats

### Single-select fields
```json
{"value": "Option Name"}
```

### Multi-select fields
```json
[
  {"value": "Option 1"},
  {"value": "Option 2"}
]
```

### Text fields
```json
"plain text string"
```

### User fields
```json
{"accountId": "user-account-id"}
```

### Date fields
```json
"2026-07-22"
```

## Best Practices

1. **Always get issue first**: Use `getJiraIssue()` to get current state before editing
2. **Get field metadata**: Use `getJiraIssueTypeMetaWithFields()` to discover available fields
3. **Check custom field IDs**: Custom fields use IDs like `customfield_10805`
4. **Format values correctly**: Single-select uses `{"value": "..."}`, text uses plain string
5. **Use JQL for batch queries**: More efficient than fetching issues one by one
6. **Verify transitions**: Get available transitions before attempting transition

## Troubleshooting

**Field not found**: Check custom field ID with `getJiraIssueTypeMetaWithFields()`

**Invalid field value**: Verify format (single-select vs text vs multi-select)

**Transition failed**: Check available transitions with `getTransitionsForJiraIssue()`

**Permission denied**: Verify your Atlassian account has access to the project

**CloudId error**: Use `"paidy-portal.atlassian.net"` as cloudId

## Authentication

Authentication handled via OAuth through claude.ai. No manual token management needed.

To reconnect:
1. Use `/mcp` command in Claude Code
2. Select Atlassian
3. Re-authenticate if needed

## Common Workflows

### Analyze phishing ticket
1. Get ticket: `getJiraIssue("SOCSD-12345")`
2. Extract email content from description
3. Perform analysis (DNS, URLs, headers)
4. Update custom fields: `editJiraIssue()`
5. Post analysis: `addCommentToJiraIssue()`

### Search for similar issues
1. Build JQL query: `project = SOCSD AND labels = phishing`
2. Search: `searchJiraIssuesUsingJql()`
3. Get details: `getJiraIssue()` for each
4. Compare patterns

### Document findings in Confluence
1. Search space: `getPagesInConfluenceSpace()`
2. Create page: `createConfluencePage()`
3. Add analysis content with markdown
4. Link to Jira issues

## Example: Complete Phishing Analysis

```javascript
// 1. Get ticket
const issue = await mcp__atlassian__getJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345"
});

// 2. Extract email content
const emailContent = issue.fields.description;

// 3. Perform analysis
// ... (DNS lookups, URL checks, etc.)

// 4. Update ticket fields
await mcp__atlassian__editJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345",
  fields: {
    "customfield_10805": {"value": "Phishing Report"},
    "customfield_11136": {"value": "Internal (Paidy Employee)"},
    "customfield_10834": "phisher@evil.com",
    "customfield_10836": {"value": "Email"},
    "customfield_10837": [
      {"value": "Impersonation"},
      {"value": "Malicious domain/url"}
    ]
  }
});

// 5. Post analysis results
await mcp__atlassian__addCommentToJiraIssue({
  cloudId: "paidy-portal.atlassian.net",
  issueIdOrKey: "SOCSD-12345",
  comment: `## Phishing Analysis Results

**Verdict**: ❌ CONFIRMED PHISHING

### Key Findings
- Domain typosquatting detected
- SPF check failed
- Known malicious infrastructure

### Recommendations
- Block sender domain
- Add URLs to blocklist
- Notify affected users`
});
```

## Related Documentation

- [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Confluence Cloud REST API](https://developer.atlassian.com/cloud/confluence/rest/v1/)
- [JQL Reference](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/)
- [CQL Reference](https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/)
