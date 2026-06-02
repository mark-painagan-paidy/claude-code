---
name: phishing-analysis
description: Analyze phishing emails reported in SOC Service Desk tickets
invocation: user
---

# Phishing Analysis Skill

Analyze phishing emails reported in Jira SOC Service Desk (SOCSD) tickets and post detailed analysis results back to the ticket.

## Usage

```
/phishing-analysis SOCSD-12345
```

## What it does

1. **Fetch Ticket Details**
   - Retrieve ticket from SOC Service Desk (SOCSD)
   - Extract email content from description
   - Identify sender, recipient, URLs, and attachments

2. **Domain Analysis**
   - Extract sender domain from email headers
   - Run WHOIS lookup for domain registration info
   - Check DNS records (SPF, DMARC, MX)
   - Verify domain age and registrar reputation
   - Identify authorized sending services

3. **URL Reputation Analysis**
   - Extract all URLs from email body
   - Test each URL for resolution and redirects
   - Identify hosting infrastructure
   - Check for suspicious patterns (URL shorteners, typosquatting)
   - Document redirect chains

4. **Email Authentication Assessment**
   - Review SPF records for authorized senders
   - Check DMARC policy strictness
   - Identify marketing platforms in SPF (HubSpot, SendGrid, etc.)
   - Note if full headers are needed for verification

5. **Generate Analysis Report**
   - Compile findings into structured format
   - Assign verdict with confidence level
   - List legitimate vs suspicious indicators
   - Provide actionable recommendations

6. **Post Results to Ticket**
   - Add comprehensive analysis as comment
   - Include technical details for SOC review
   - Flag verification steps if headers needed
   - Suggest remediation actions

## Analysis Framework

### 1. Sender Domain Analysis

**Email Headers**
- Extract sender address (From/差出人)
- Extract Reply-To address (返信先)
- Compare From vs Reply-To for mismatches
- Verify domain ownership (WHOIS lookup)

**DNS & Authentication Records**
- Check SPF records: `dig +short <domain> TXT`
- Check DMARC policy: `dig +short _dmarc.<domain> TXT`
- Check MX records: `dig +short <domain> MX`
- Verify authorized sending services (HubSpot, SendGrid, etc.)

**Domain Reputation**
- Domain age and creation date
- Registrar (legitimate registrars: MarkMonitor, CSC, etc.)
- Registrant organization
- Name servers (AWS, Cloudflare, etc.)

**Typosquatting Detection**
- Check for character substitutions (l→1, o→0)
- Look for extra/missing characters
- Check for similar TLDs (.com vs .co, .net)
- Verify against known legitimate domains

### 2. URL Analysis

**URL Extraction**
- Extract all URLs from email body
- Identify tracking links vs direct links
- Note URL shorteners (bit.ly, tinyurl, etc.)

**URL Reputation Checks**
- Test URL resolution: `dig +short <domain> A`
- Check HTTP response: `curl -sL -o /dev/null -w "%{http_code} %{redirect_url}\n"`
- Follow redirect chains to final destination
- Identify hosting infrastructure (CDN, cloud providers)

**Suspicious Patterns**
- Base64 encoded URLs
- Data URIs (data:text/html)
- IP addresses instead of domains
- Non-standard ports
- Unusual subdomains

### 3. Email Authentication Verification

**Request Full Headers**
- Ask reporter to provide full email headers
- Look for `Authentication-Results:` header
- Check SPF/DKIM/DMARC pass/fail status
- Verify `Return-Path:` matches sender domain
- Review `Received:` header chain

**DKIM Signature**
- Look for `DKIM-Signature:` header
- Verify signing domain matches sender
- Check selector and body hash

**Message Routing**
- Review `Received:` headers for suspicious hops
- Verify originating server IPs
- Check for mail relay abuse

### 4. Content Analysis

**Language & Grammar**
- Urgency or threat language
- Poor grammar or translation artifacts
- Inconsistent formatting

**Requests**
- Asking for credentials
- Payment information requests
- Urgent action required
- Unexpected attachments

**Brand Impersonation**
- Logo usage and quality
- Email template matching
- Brand voice consistency

### 5. Infrastructure Analysis

**Hosting Information**
- Identify CDN usage (Cloudflare, Akamai)
- Check cloud hosting (AWS, Azure, GCP)
- Marketing platforms (HubSpot, Mailchimp)
- Note IP addresses and ranges

**SSL/TLS Certificate**
- Check certificate validity
- Verify certificate issuer
- Check domain match

### Output Format

Post a comment to the ticket with:

```markdown
## Phishing Analysis Results

**Verdict: [CONFIRMED PHISHING | SUSPICIOUS | LEGITIMATE | INCONCLUSIVE]**

---

### Email Header Information
- **From:** sender@domain.com
- **Reply-To:** replyto@domain.com
- **To:** recipient@domain.com
- **Date:** YYYY-MM-DD HH:MM:SS TZ
- **Subject:** Email subject line

---

### Domain Information

**Primary Domain:** domain.com
- **Registrant:** Company Name
- **Registrar:** Registrar Name
- **Created:** YYYY-MM-DD
- **Name Servers:** NS records

**Subdomain/Marketing Domain:** subdomain.domain.com
- **Infrastructure:** Hosting provider
- **IPs:** IP addresses
- **CDN:** CDN provider if applicable

---

### Email Authentication

**SPF (Sender Policy Framework):**
```
SPF record content
```
- ✅/❌ Authorized sending services identified

**DMARC Policy:**
```
DMARC record content
```
- Policy: none/quarantine/reject
- Strictness level

**Mail Infrastructure:**
- Primary: Mail provider
- Marketing: Marketing platform
- Other authorized: Additional services

---

### URL Analysis

**URLs Found:** [count]

**Sample URL Analysis:**
1. `https://example.com/path`
   - **Resolves to:** IP or redirect destination
   - **HTTP Status:** 200/404/etc
   - **Infrastructure:** Hosting info
   - **Assessment:** ✅ Legitimate / ❌ Suspicious

---

### Key Indicators

**🟢 Legitimate Indicators:**
- Finding 1 with explanation
- Finding 2 with explanation

**🔴 Suspicious Indicators:**
- Finding 1 with explanation
- Finding 2 with explanation

**⚠️ Concerns:**
- Finding 1 with explanation

---

### Verification Steps Needed

If authentication cannot be fully verified from ticket alone:

- [ ] Request full email headers from reporter
- [ ] Check `Authentication-Results:` header for SPF/DKIM/DMARC
- [ ] Verify `Return-Path:` and `Received:` headers
- [ ] Confirm DKIM signature if present

---

### Recommended Actions

**Immediate:**
- [ ] Action item 1
- [ ] Action item 2

**Follow-up:**
- [ ] Action item 3
- [ ] Action item 4

**If Phishing Confirmed:**
- [ ] Block sender domain in email gateway
- [ ] Add URLs to blocklist
- [ ] Notify affected users
- [ ] Report to abuse@domain or relevant authority

---

**Analyst:** Claude AI  
**Analysis Date:** YYYY-MM-DD HH:MM:SS TZ
```

## Tools & Commands Used

### Atlassian (Jira)
- `mcp__atlassian__getJiraIssue` - Fetch ticket details
- `mcp__atlassian__addCommentToJiraIssue` - Post analysis results

### DNS & Domain Analysis
- `dig +short <domain> TXT` - Check SPF records
- `dig +short _dmarc.<domain> TXT` - Check DMARC policy
- `dig +short <domain> MX` - Check mail servers
- `dig +short <domain> A` - Resolve domain to IPs
- `whois <domain>` - Domain registration info

### URL Testing
- `curl -sL -o /dev/null -w "%{http_code} %{redirect_url}\n" <url>` - Test HTTP response
- `curl -sL -I <url>` - Follow redirects and show headers

### Optional External Services
- `WebFetch` - Fetch and analyze web content (if needed)

## Technical Implementation Notes

### DNS Checks Pattern
```bash
# Check SPF
dig +short domain.com TXT | grep -E "spf|dmarc"

# Check DMARC
dig +short _dmarc.domain.com TXT

# Check MX records
dig +short domain.com MX

# Resolve domain
dig +short domain.com A

# WHOIS lookup
whois domain.com | grep -E "(Creation Date|Registrant|Registrar:|Name Server)"
```

### URL Analysis Pattern
```bash
# Test URL response
curl -sL -o /dev/null -w "%{http_code} %{redirect_url}\n" "URL"

# Follow redirects
curl -sL -I "URL" | grep -i "location\|http"
```

### Authentication Record Interpretation

**SPF Record:**
- `include:` - Authorized sending services
- `~all` - Soft fail (common, acceptable)
- `-all` - Hard fail (strict policy)
- `?all` - Neutral (weak policy)
- `+all` - Pass all (VERY SUSPICIOUS - allows anyone to send)

**DMARC Policy:**
- `p=none` - Monitoring only (weak)
- `p=quarantine` - Suspect emails quarantined (good)
- `p=reject` - Reject failing emails (strongest)
- `pct=100` - Policy applies to 100% of emails

**Authorized Senders to Recognize:**
- Google: `_spf.google.com`
- Microsoft 365: `spf.protection.outlook.com`
- SendGrid: `sendgrid.net`
- Mailgun: `mailgun.org`
- HubSpot: `*.hubspotemail.net`
- Mailchimp: `servers.mcsv.net`
- Zendesk: `mail.zendesk.com`

## Example Usage

### Basic Usage
```
/phishing-analysis SOCSD-33563
```

Analyzes ticket SOCSD-33563 containing a phishing report and posts structured findings.

### Example Analysis Output

For a ticket reporting a suspicious Paidy billing email:

**Execution Steps:**
1. Fetch SOCSD-33563 ticket details
2. Extract sender: `noreply@paidy.com`
3. Extract URLs: Multiple `marketing.paidy.com/e3t/...` links
4. Run DNS checks on `paidy.com`:
   - SPF: Includes HubSpot (7854719.spf05.hubspotemail.net)
   - DMARC: p=quarantine (strict policy)
   - WHOIS: Owned by PayPal Inc., registered 2010
5. Test URL resolution: Resolves to HubSpot infrastructure
6. Generate verdict: LEGITIMATE (with caveat to verify charge)
7. Post comprehensive analysis to ticket

**Posted Comment Would Include:**
- ✅ Domain legitimately owned by PayPal Inc.
- ✅ HubSpot authorized in SPF records
- ✅ Strict DMARC policy (p=quarantine)
- ✅ Long-established domain (2010)
- ⚠️ User reports unrecognized charge
- Recommendation: Verify charge directly through Paidy app/website

---

## Decision Tree

```
1. Check Sender Domain
   ├─ Typosquatting detected? → ❌ CONFIRMED PHISHING
   ├─ Unknown/suspicious domain? → ⚠️ SUSPICIOUS
   └─ Legitimate domain? → Continue to step 2

2. Check DNS Records
   ├─ No SPF/DMARC? → ⚠️ SUSPICIOUS
   ├─ SPF allows everyone (+all)? → ❌ SUSPICIOUS
   └─ Proper authentication? → Continue to step 3

3. Check URLs
   ├─ Malicious destination? → ❌ CONFIRMED PHISHING
   ├─ URL shorteners/suspicious? → ⚠️ SUSPICIOUS
   └─ Legitimate infrastructure? → Continue to step 4

4. Content Analysis
   ├─ Credential harvesting? → ❌ CONFIRMED PHISHING
   ├─ Urgent/threatening? → ⚠️ SUSPICIOUS
   └─ Normal content? → Continue to step 5

5. Final Assessment
   ├─ Headers needed? → ⚪ INCONCLUSIVE - Request headers
   ├─ All checks pass? → ✅ LEGITIMATE
   └─ Mixed signals? → ⚠️ SUSPICIOUS - Investigate further
```

---

## Verdict Guidelines

**✅ LEGITIMATE**
- Domain owned by legitimate company
- Proper SPF/DMARC configuration
- URLs resolve to expected infrastructure
- No suspicious patterns
- May still note concerns (e.g., unrecognized charge)

**⚠️ SUSPICIOUS**
- Some red flags present
- Authentication weak but not absent
- URLs redirect through unknown services
- Content has concerning elements
- Recommend caution and further investigation

**❌ CONFIRMED PHISHING**
- Clear typosquatting or domain spoofing
- Malicious URLs confirmed
- Credential harvesting detected
- Known phishing indicators present
- Immediate blocking recommended

**⚪ INCONCLUSIVE**
- Insufficient information from ticket alone
- Full email headers required
- External verification needed
- Request additional data from reporter
