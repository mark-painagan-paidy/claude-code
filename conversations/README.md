# Conversation Dumps

This directory contains conversation histories from Claude Code sessions for reference and context continuity.

## Purpose

When working on projects or troubleshooting issues across multiple Claude sessions, you can dump important conversations here to:
- Maintain context across sessions
- Reference past solutions and approaches
- Document decision-making processes
- Build a knowledge base of your work

## File Naming Convention

Use descriptive names with dates:
```
YYYY-MM-DD_topic-description.md
```

Examples:
- `2026-07-22_security-canvas-automation.md`
- `2026-07-22_skills-repo-setup.md`
- `2026-07-15_phishing-analysis-workflow.md`

## Template

Each conversation dump should include:

```markdown
# [Topic Title]

**Date**: YYYY-MM-DD
**Session Duration**: X hours/minutes
**Tags**: #security, #automation, #analysis, etc.

## Context

Brief description of what we were working on and why.

## Key Discussion Points

- Point 1
- Point 2
- Point 3

## Solutions/Implementations

### [Solution Name]

Description of what was implemented, code snippets, commands used, etc.

### [Solution Name 2]

More details...

## Files Modified/Created

- `/path/to/file1` - Description
- `/path/to/file2` - Description

## Commands/Tools Used

```bash
# Example commands
command1
command2
```

## Outcomes

What was accomplished, what worked, what didn't.

## Follow-up Items

- [ ] Todo item 1
- [ ] Todo item 2

## References

- Link to PR
- Link to documentation
- Link to related issues
```

## Usage

### Saving a Conversation

When you want to save a conversation:
```
"Dump this conversation to the conversations folder as 'YYYY-MM-DD_topic-name.md'"
```

Claude will create a markdown file summarizing:
- What we discussed
- What was implemented
- Key commands and code
- Outcomes and next steps

### Referencing Past Conversations

In a new session, you can say:
```
"Check the conversations folder for context about [topic]"
```

or

```
"Review the conversation dump from 2026-07-22 about security canvas automation"
```

## Organization

You can create subdirectories by topic:

```
conversations/
├── security/
│   ├── 2026-07-22_canvas-automation.md
│   └── 2026-07-15_phishing-workflow.md
├── infrastructure/
│   └── 2026-07-10_github-actions.md
└── analysis/
    └── 2026-07-05_threat-intel-setup.md
```

## Tips

1. **Be specific**: Include enough detail that you can understand the context months later
2. **Include code/commands**: Actual commands and code snippets are more useful than descriptions
3. **Note decisions**: Document why certain approaches were chosen
4. **Link artifacts**: Include links to PRs, Jira tickets, Slack threads, etc.
5. **Regular dumps**: Don't wait too long - dump conversations while they're fresh
