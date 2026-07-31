---
name: sd-status
description: Generate Service Desk status report grouped by assignee
invocation: user
---

# Service Desk Status Report Skill

Generate a comprehensive Service Desk status report from the Jira SE board, formatted for posting to Slack. Groups tickets by assignee and shows current status, update dates, and due dates.

## Usage

```
/sd-status
```

Or with optional Slack posting:

```
/sd-status --post
```

## What it does

1. **Query Jira Service Desk Board**
   - Fetch all active tickets from SE board queue (queue ID: 122)
   - Filter for tickets that need action or are in progress
   - Exclude resolved/closed tickets

2. **Group Tickets by Assignee**
   - Organize tickets by current assignee
   - Count tickets per assignee
   - Sort assignees alphabetically

3. **Extract Ticket Details**
   - Ticket key (SE-XXXX)
   - Summary/title
   - Request type (AWS Access, Security Help, WAF Change, etc.)
   - Current status (In Progress, Waiting for customer, Waiting for support)
   - Last updated date
   - Due date (if applicable)

4. **Format Report**
   - Generate Slack-friendly markdown format
   - Include assignee mentions (@username)
   - Show ticket counts
   - Group by "Needs your action" sections
   - Link to tickets for easy access

5. **Optional: Post to Slack**
   - Post formatted report to configured Slack channel
   - Default: `#sec-team` channel or configured in environment

## Report Format

The generated report follows this structure:

```
Service Desk Status:

@Assignee Name — X ticket(s) ·
Needs your action:
• SE-XXXX: Ticket Summary · Request Type · Status · Updated: YYYY-MM-DD · [Due: YYYY-MM-DD]
  https://paidy-portal.atlassian.net/browse/SE-XXXX
• SE-YYYY: Another Ticket · Request Type · Status · Updated: YYYY-MM-DD
  https://paidy-portal.atlassian.net/browse/SE-YYYY

@Next Assignee — Y ticket(s) ·
Needs your action:
...
```

### Format Details

- **Header:** "Service Desk Status:" with optional timestamp
- **Assignee Line:** `@Name — X ticket(s) ·` with Slack mention format
- **Section:** "Needs your action:" for actionable tickets
- **Ticket Bullet:** `•` bullet point with ticket key, summary, metadata on first line
- **Ticket Link:** Indented URL on second line for easy clicking
- **Separator:** Blank line between assignees only (no blank line between tickets of same assignee)

### Status Categories

Tickets shown are those requiring action:
- **In Progress** - Actively being worked on
- **Waiting for customer** - Awaiting response from requester
- **Waiting for support** - Awaiting internal action
- **Open/New** - Unassigned or newly created

Excluded statuses:
- Resolved
- Closed
- Done
- Cancelled

## Jira Query

The skill uses JQL (Jira Query Language) to fetch tickets:

```jql
project = SE 
AND status IN ("In Progress", "Waiting for customer", "Waiting for support", "Open", "To Do", "Reopened")
ORDER BY assignee ASC, updated DESC
```

This query:
- Uses positive filtering (IN) instead of negative (NOT IN) for better performance
- Includes both assigned and unassigned tickets
- Orders by assignee first (unassigned tickets appear first), then by last updated

### Request Type Mapping

Common SE project request types:
- **AWS Access** - AWS account/permission requests
- **Security Help** - General security assistance
- **WAF Change** - Web Application Firewall modifications
- **Offboarding** - Employee offboarding security tasks
- **Onboarding** - Employee onboarding security setup
- **Merchant Security Questionnaire** - Vendor security assessments
- **Service Request** - General service requests
- **Vulnerability Management** - CVE/vulnerability handling

## Technical Implementation

### Jira API Calls

1. **Search Issues** - `mcp__atlassian__searchJiraIssuesUsingJql`
   ```javascript
   {
     "cloudId": "paidy-portal.atlassian.net",
     "jql": "project = SE AND status IN (\"In Progress\", \"Waiting for customer\", \"Waiting for support\", \"Open\", \"To Do\", \"Reopened\") ORDER BY assignee ASC, updated DESC",
     "fields": [
       "summary",
       "status",
       "assignee",
       "updated",
       "duedate",
       "issuetype",
       "customfield_10802"  // Request type
     ],
     "maxResults": 100
   }
   ```

2. **Get Assignee Info** - Extract from issue object
   - `fields.assignee.displayName` - Full name for grouping
   - `fields.assignee.accountId` - For Slack mention mapping

### Slack Formatting

**Ticket Link Format:**
```
https://paidy-portal.atlassian.net/browse/SE-XXXX
```

**Slack Mention Format:**
```
@Username
```

**Status Indicators:**
- In Progress → Show as-is
- Waiting for customer → Append "Waiting for customer" superscript
- Waiting for support → Append "Waiting for support" superscript

**Date Format:**
- Updated: `YYYY-MM-DD` (ISO format)
- Due: `YYYY-MM-DD` (only shown if due date exists)

### Grouping Logic

```javascript
// Group tickets by assignee (handle unassigned tickets)
const grouped = tickets.reduce((acc, ticket) => {
  const assignee = ticket.fields.assignee?.displayName || "Unassigned";
  if (!acc[assignee]) {
    acc[assignee] = [];
  }
  acc[assignee].push(ticket);
  return acc;
}, {});

// Sort assignees alphabetically (Unassigned first if present)
const sortedAssignees = Object.keys(grouped).sort((a, b) => {
  if (a === "Unassigned") return -1;
  if (b === "Unassigned") return 1;
  return a.localeCompare(b);
});
```

### Status Filtering

Include only tickets in these statuses:
- Open
- In Progress
- Waiting for customer
- Waiting for support
- Reopened
- To Do

Exclude:
- Resolved
- Closed
- Done
- Cancelled
- Won't Do

## Example Output

```
Service Desk Status:

@Ashish Thirunagari — 5 ticket(s) ·
Needs your action:
• SE-4446: [PRE-APPROVED] - [AWS Access Request] - Exception Access (AWS Bedrock for Claude usage) · OIT: AWS Request · Waiting for support · Updated: 2026-07-13
  https://paidy-portal.atlassian.net/browse/SE-4446
• SE-4442: [PRE-APPROVED] - [AWS Access Request] - Exception Access · OIT: AWS Request · Waiting for customer · Updated: 2026-07-10
  https://paidy-portal.atlassian.net/browse/SE-4442
• SE-4428: [PRE-APPROVED] - [AWS Access Request] - Exception Access · OIT: AWS Request · Waiting for customer · Updated: 2026-07-10
  https://paidy-portal.atlassian.net/browse/SE-4428
• SE-4418: GitHub token usage · IT Help · In Progress · Updated: 2026-07-09
  https://paidy-portal.atlassian.net/browse/SE-4418
• SE-4441: [PRE-APPROVED] - [AWS Access Request] - New Account · OIT: AWS Request · Waiting for support · Updated: 2026-07-08
  https://paidy-portal.atlassian.net/browse/SE-4441

@Darryl Sim — 1 ticket(s) ·
Needs your action:
• SE-4339: Merchant Security Questionnaire · IT Help · Waiting for customer · Updated: 2026-06-08
  https://paidy-portal.atlassian.net/browse/SE-4339

@Jason Keyes — 1 ticket(s) ·
Needs your action:
• SE-4403: Check new installed library in Docker image is okay · IT Help · Waiting for customer · Updated: 2026-07-09
  https://paidy-portal.atlassian.net/browse/SE-4403

@Mark Painagan — 2 ticket(s) ·
Needs your action:
• SE-4447: Web Application Firewall Change Request · Service Request with Approvals · Waiting for support · Updated: 2026-07-13
  https://paidy-portal.atlassian.net/browse/SE-4447
• SE-4445: Web Application Firewall Change Request · Service Request with Approvals · Waiting for customer · Updated: 2026-07-13
  https://paidy-portal.atlassian.net/browse/SE-4445

@Wahyu Nuryanto — 1 ticket(s) ·
Needs your action:
• SE-4437: [Chikako Sato] - Automated SEC ticket for Off boarding · IT Help · Waiting for customer · Due: 2026-07-16 · Updated: 2026-07-07
  https://paidy-portal.atlassian.net/browse/SE-4437
```

## Configuration

### Environment Variables

Set these in your shell environment or `.env` file:

```bash
# Slack channel for posting reports (optional)
SD_STATUS_SLACK_CHANNEL="#sec-team"

# Jira board queue ID (default: 122)
SD_STATUS_QUEUE_ID="122"

# Maximum tickets to fetch (default: 100)
SD_STATUS_MAX_RESULTS="100"
```

### Slack Username Mapping

Map Jira display names to Slack usernames for mentions:

```javascript
const slackMentionMap = {
  "Ashish Thirunagari": "@Ashish Thirunagari",
  "Darryl Sim": "@Darryl Sim",
  "Jason Keyes": "@Jason Keyes",
  "Mark Painagan": "@Mark Painagan",
  "Wahyu (ワ ユ)": "@Wahyu (ワ ユ)",
  "Akshay TU": "@Akshay TU"
  // Add more mappings as needed
};
```

## Usage Scenarios

### 1. Daily Stand-up
```bash
/sd-status
```
Generate current status for team review during daily sync.

### 2. Shift Handoff
```bash
/sd-status --post
```
Post status to Slack when handing off SD duty to next team member.

### 3. Weekly Review
```bash
/sd-status
```
Review ticket distribution and aging for workload balancing.

### 4. Manager Check-in
```bash
/sd-status
```
Quick overview of team's current workload and bottlenecks.

## Best Practices

1. **Run Before Posting to Slack**
   - Review generated report first without `--post` flag
   - Verify all tickets are captured correctly
   - Check for any stale or misassigned tickets

2. **Regular Schedule**
   - Run at beginning of SD duty shift
   - Post updates when significant changes occur
   - Document handoff notes in Slack thread

3. **Ticket Aging**
   - Flag tickets not updated in >7 days
   - Highlight tickets approaching due dates
   - Escalate blocked tickets

4. **Workload Distribution**
   - Monitor ticket counts per assignee
   - Identify bottlenecks or overload
   - Reassign as needed for balance

## Troubleshooting

### No Tickets Returned

**Possible Causes:**
- All tickets resolved/closed
- JQL filter too restrictive
- Queue ID incorrect

**Solution:**
- Verify queue URL: `https://paidy-portal.atlassian.net/jira/servicedesk/projects/SE/queues/custom/122`
- Check JQL in Jira directly
- Adjust status filters if needed

### Missing Assignees

**Possible Causes:**
- Unassigned tickets filtered out
- Assignee field empty

**Solution:**
- Include unassigned section: `AND assignee IS EMPTY`
- Review ticket assignment process

### Slack Mentions Not Working

**Possible Causes:**
- Username mapping incorrect
- Slack workspace settings

**Solution:**
- Update `slackMentionMap` with correct usernames
- Verify Slack display names match Jira

### Rate Limiting

**Possible Causes:**
- Too many API calls
- Jira/Slack API limits hit

**Solution:**
- Add delay between API calls
- Reduce `maxResults` parameter
- Cache results for repeated queries

## Future Enhancements

- [ ] Add SLA/aging indicators (🔴 overdue, 🟡 approaching due, 🟢 on track)
- [ ] Include ticket priority in report
- [ ] Add trend analysis (ticket count change vs. previous report)
- [ ] Support filtering by request type or status
- [ ] Generate charts/metrics for leadership reporting
- [ ] Automate posting via scheduled cron job
- [ ] Add email report option
- [ ] Include customer satisfaction scores
- [ ] Link to relevant runbooks per request type
- [ ] Add ticket velocity metrics (time to resolve)

---

**Skill Version:** 1.0.0  
**Last Updated:** 2026-07-13  
**Maintainer:** Security Engineering Team
