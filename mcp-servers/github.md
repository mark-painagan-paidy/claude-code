# GitHub MCP Server

**Package**: `@modelcontextprotocol/server-github`  
**Type**: NPX (Node.js)  
**Status**: ✅ Active

## Purpose

Integration with GitHub for:
- Repository management
- Code search
- Issue and PR operations
- File operations
- Branch management

## Configuration

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

## Available Tools

### Repository Operations
- `search_repositories` - Search GitHub repositories
- `create_repository` - Create new repository
- `fork_repository` - Fork a repository

### File Operations
- `get_file_contents` - Read file contents from repo
- `create_or_update_file` - Create/modify files
- `push_files` - Batch file operations

### Code Search
- `search_code` - Search code across repositories
- `search_issues` - Search issues and pull requests
- `search_users` - Search GitHub users

### Issue Management
- `create_issue` - Create new issue
- `update_issue` - Update existing issue
- `get_issue` - Get issue details
- `list_issues` - List repository issues
- `add_issue_comment` - Add comment to issue

### Pull Request Operations
- `create_pull_request` - Create new PR
- `get_pull_request` - Get PR details
- `list_pull_requests` - List repository PRs
- `get_pull_request_files` - Get PR file changes
- `get_pull_request_comments` - Get PR comments
- `get_pull_request_reviews` - Get PR reviews
- `create_pull_request_review` - Create PR review
- `merge_pull_request` - Merge PR
- `update_pull_request_branch` - Update PR branch

### Branch Operations
- `create_branch` - Create new branch
- `list_commits` - List repository commits

## Authentication

Requires GitHub Personal Access Token (PAT) with appropriate scopes:
- `repo` - Full control of private repositories
- `read:org` - Read org membership
- `workflow` - Update GitHub Actions workflows

Create PAT at: https://github.com/settings/tokens

## Usage in Skills

### vuln-check
**Purpose**: Search GitHub organization for vulnerable dependencies

```bash
# Get all repos in organization
gh repo list paidy --limit 1000

# Search for vulnerable library in files
search_code(
  q: "libssh2 org:paidy filename:Dockerfile",
  per_page: 100
)

# Check specific file
get_file_contents(
  owner: "paidy",
  repo: "repo-name",
  path: "package.json"
)
```

## Common Search Queries

### Code Search
```
"log4j org:paidy"                      - Search for log4j in org repos
"filename:Dockerfile apt install"      - Dockerfiles with apt install
"filename:package.json express"        - package.json with express
"extension:yml github/workflows"       - GitHub Actions workflows
```

### Issue/PR Search
```
"is:open is:issue label:security"      - Open security issues
"is:pr author:username is:merged"      - Merged PRs by user
"is:issue created:>2026-07-01"        - Recent issues
```

### Repository Search
```
"org:paidy archived:false"             - Active org repos
"topic:security org:paidy"             - Security-related repos
"fork:true org:paidy"                  - Forked repos
```

## File Operations Examples

### Read file
```
get_file_contents(
  owner: "mark-painagan-paidy",
  repo: "claude-code",
  path: "skills/vuln-check/skill.md"
)
```

### Create/Update file
```
create_or_update_file(
  owner: "mark-painagan-paidy",
  repo: "claude-code",
  path: "conversations/2026-07-22_new-topic.md",
  content: "file content here",
  message: "Add new conversation dump",
  branch: "main"
)
```

### Batch file push
```
push_files(
  owner: "mark-painagan-paidy",
  repo: "claude-code",
  branch: "main",
  files: [
    {path: "file1.md", content: "..."},
    {path: "file2.md", content: "..."}
  ],
  message: "Batch update"
)
```

## Issue/PR Examples

### Create issue
```
create_issue(
  owner: "mark-painagan-paidy",
  repo: "claude-code",
  title: "Add new skill for X",
  body: "## Description\n\n...",
  labels: ["enhancement", "skill"]
)
```

### Create pull request
```
create_pull_request(
  owner: "mark-painagan-paidy",
  repo: "claude-code",
  title: "Update threat-intel skill",
  body: "## Changes\n\n- Enhanced CTI integration",
  head: "feature-branch",
  base: "main"
)
```

## Rate Limits

GitHub API rate limits:
- **Authenticated**: 5,000 requests/hour
- **Search API**: 30 requests/minute
- **Code Search**: 10 requests/minute

Use search queries efficiently and cache results when possible.

## Best Practices

1. **Use specific searches**: Filter by org, filename, extension
2. **Batch operations**: Use `push_files` for multiple file updates
3. **Search code first**: Before reading files, search to find them
4. **Handle rate limits**: Implement retry logic with backoff
5. **Use PAT securely**: Never commit tokens to repositories

## Repository Access

With your PAT, you have access to:
- **Personal repos**: All repositories under `mark-painagan-paidy`
- **Organization repos**: Repos in organizations you're a member of (e.g., `paidy`)
- **Public repos**: All public repositories on GitHub

## Common Workflows

### Find vulnerable dependencies
1. Search code: `search_code(q: "CVE-2026-XXXXX org:paidy")`
2. Get file contents: `get_file_contents()` for matches
3. Check dependency versions
4. Create issues for affected repos

### Update files across repos
1. Search repositories: `search_repositories(q: "org:paidy archived:false")`
2. For each repo, update file: `create_or_update_file()`
3. Create PR: `create_pull_request()`

### Monitor security issues
1. Search issues: `search_issues(q: "is:issue label:security is:open org:paidy")`
2. Get issue details: `get_issue()`
3. Add comments with analysis: `add_issue_comment()`

## Troubleshooting

**Authentication failed**: Verify PAT is valid and has correct scopes

**Rate limit exceeded**: Wait for rate limit reset, implement backoff

**File not found**: Check file path, branch name, repository access

**Permission denied**: Verify PAT has `repo` scope for private repos

## Related Documentation

- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub Search Syntax](https://docs.github.com/en/search-github/searching-on-github)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
