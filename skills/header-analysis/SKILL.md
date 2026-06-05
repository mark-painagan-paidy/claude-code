---
name: header-analysis
description: Analyze email headers for authentication verification and routing analysis
invocation: user
---

# Email Header Analysis Skill

Perform detailed analysis of email headers to verify authentication (SPF, DKIM, DMARC), trace email routing, detect spoofing attempts, and assess email legitimacy.

## Usage

```
/header-analysis SOCSD-12345
```

Or provide headers directly:
```
/header-analysis <paste email headers>
```

## What it does

1. **Extract Email Headers**
   - Fetch headers from Jira ticket or direct input
   - Parse structured header fields
   - Identify key authentication headers

2. **Authentication Verification**
   - Analyze SPF (Sender Policy Framework) results
   - Verify DKIM (DomainKeys Identified Mail) signatures
   - Check DMARC (Domain-based Message Authentication) alignment
   - Review Authentication-Results header

3. **Email Routing Analysis**
   - Trace Received headers (email path)
   - Identify originating mail server
   - Map server hops and relay points
   - Verify TLS/encryption usage

4. **Sender Verification**
   - Compare From, Return-Path, and Reply-To
   - Check for domain alignment
   - Identify mail user agents
   - Detect spoofing indicators

5. **Security Assessment**
   - Flag authentication failures
   - Identify suspicious routing patterns
   - Detect header manipulation
   - Check for known malicious infrastructure

6. **Generate Report**
   - Summary of authentication results
   - Email flow visualization
   - Security verdict with confidence level
   - Actionable recommendations

## Analysis Framework

### 1. Authentication Headers

**Authentication-Results Header**
The primary source of authentication verification, added by receiving mail server:

```
Authentication-Results: mx.google.com;
  dkim=pass header.i=@domain.com header.s=selector;
  spf=pass smtp.mailfrom=sender@domain.com;
  dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=domain.com
```

**Key Fields:**
- `dkim=` - DKIM signature verification (pass/fail/none)
- `spf=` - SPF check result (pass/fail/softfail/neutral/none)
- `dmarc=` - DMARC policy check (pass/fail/none)

### 2. DKIM Signature Analysis

**DKIM-Signature Header**
Cryptographic signature proving message authenticity:

```
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=domain.com;
  s=selector; t=1234567890;
  bh=base64_body_hash;
  h=From:To:Subject:Date;
  b=base64_signature
```

**Fields to Check:**
- `d=` - Signing domain (should match From domain)
- `s=` - Selector (subdomain for DNS lookup)
- `bh=` - Body hash
- `b=` - Signature
- Result: `pass` = signature verified, `fail` = tampering or spoofing

### 3. SPF Verification

**Received-SPF Header**
Shows SPF check result:

```
Received-SPF: pass (google.com: domain of sender@domain.com designates
  192.0.2.1 as permitted sender) client-ip=192.0.2.1;
```

**SPF Results:**
- `pass` ✅ - Sending IP authorized
- `fail` ❌ - Sending IP not authorized (likely spoofed)
- `softfail` ⚠️ - Probably not authorized (weak policy)
- `neutral` ⚠️ - No policy statement
- `none` ⚠️ - No SPF record exists

**Verify with DNS:**
```bash
dig +short domain.com TXT | grep "v=spf1"
```

### 4. DMARC Policy

**From Authentication-Results:**
```
dmarc=pass (p=REJECT sp=REJECT dis=NONE)
```

**Policy Levels:**
- `p=reject` - Strongest: reject unauthenticated emails
- `p=quarantine` - Medium: flag/quarantine suspicious emails
- `p=none` - Weakest: monitor only, no enforcement
- `sp=` - Subdomain policy

**Verify with DNS:**
```bash
dig +short _dmarc.domain.com TXT
```

### 5. Email Routing (Received Headers)

**Received Headers** (read bottom-to-top for chronological order)

Each hop adds a Received header:
```
Received: from sender-server.com (sender-ip [192.0.2.1])
  by receiver-server.com with ESMTPS id xyz123
  for <recipient@example.com>
  (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384);
  Thu, 04 Jun 2026 10:00:00 -0700 (PDT)
```

**Analysis Points:**
- **First Received** (bottom) = originating server
- **Last Received** (top) = final delivery
- **Server IPs** = verify against known mail infrastructure
- **TLS version** = check encryption (TLS 1.2+ is good)
- **Delays** = unusual delays may indicate relay through spam servers

### 6. Sender Headers Comparison

**Critical Headers to Compare:**

| Header | Purpose | Spoofing Check |
|--------|---------|----------------|
| `From:` | Displayed sender | User sees this |
| `Return-Path:` | Bounce address | Should match From domain |
| `Reply-To:` | Reply destination | Check if different from From |
| `Sender:` | Actual sender | May differ for mailing lists |

**Red Flags:**
- ❌ From domain ≠ Return-Path domain
- ❌ Reply-To points to different domain (common in phishing)
- ❌ From name = "PayPal" but From address = "attacker@evil.com"

### 7. Suspicious Patterns

**Header Manipulation Indicators:**
- Missing or malformed Received headers
- Received headers with private IPs exposed
- Multiple conflicting Date headers
- Unusual or suspicious X-Mailer / User-Agent
- Message-ID format doesn't match domain
- Forged Received headers

**Routing Red Flags:**
- Email routed through unexpected countries
- Too many relay hops (>5-6 is suspicious)
- Residential/dynamic IPs in server chain
- Known spam/malware infrastructure IPs
- Missing intermediate hops

## Output Format

Post analysis results to ticket or stdout:

```markdown
## Email Header Analysis Results

**Authentication Verdict: [✅ VERIFIED | ⚠️ PARTIAL | ❌ FAILED | ⚪ INSUFFICIENT]**

---

### Authentication Summary

| Method | Result | Details |
|--------|--------|---------|
| **DKIM** | ✅/❌/⚠️ | Signing domain, selector, pass/fail reason |
| **SPF** | ✅/❌/⚠️ | Authorized IP, pass/fail reason |
| **DMARC** | ✅/❌/⚠️ | Policy level, alignment status |

---

### Email Routing

**Email Path:** (chronological order, oldest to newest)

1. **Origin:** `originating-server.com` (IP: 192.0.2.1)
   - First hop from sender's infrastructure
   
2. **Relay:** `smtp-relay.provider.com` (IP: 192.0.2.2)
   - TLS 1.3 encryption
   
3. **Destination:** `mx.recipient.com` (IP: 192.0.2.3)
   - Final delivery to mailbox

**TLS/Encryption:** ✅ TLS 1.3 (Strong encryption)

---

### Sender Information

| Field | Value |
|-------|-------|
| **From** | Sender Name <sender@domain.com> |
| **Return-Path** | <sender@domain.com> |
| **Reply-To** | <reply@domain.com> *(if different)* |
| **Message-ID** | <msg-id@domain.com> |

**Alignment Check:**
- ✅/❌ From domain matches Return-Path domain
- ✅/❌ Reply-To domain matches From domain (or N/A)
- ✅/❌ Message-ID format consistent with domain

---

### Key Findings

**🟢 Legitimate Indicators:**
- All authentication checks passed
- Email routed through expected infrastructure
- Proper TLS encryption used
- Sender domains properly aligned

**🔴 Suspicious Indicators:**
- SPF failed - sending IP not authorized
- DKIM signature invalid or missing
- Return-Path domain mismatch
- Suspicious relay servers in path

**⚠️ Concerns:**
- Weak DMARC policy (p=none)
- Reply-To different from From
- Unusual routing delays

---

### Technical Details

**Originating Server:**
- Hostname: server.domain.com
- IP Address: 192.0.2.1
- Reverse DNS: ✅/❌ Matches
- Infrastructure: GitHub / Google / AWS / etc.

**Authentication Headers:**
```
Authentication-Results: mx.google.com;
  dkim=pass header.i=@domain.com;
  spf=pass smtp.mailfrom=sender@domain.com;
  dmarc=pass (p=QUARANTINE sp=REJECT dis=NONE)
```

**DKIM Signature:**
```
DKIM-Signature: v=1; a=rsa-sha256; d=domain.com;
  s=selector; bh=...
```

---

### Verdict

**Overall Assessment:** ✅ LEGITIMATE / ⚠️ SUSPICIOUS / ❌ SPOOFED

**Confidence Level:** High / Medium / Low

**Reasoning:**
- Point-by-point explanation of verdict
- Key factors in decision
- What passed/failed

---

### Recommendations

**If Legitimate:**
- ✅ Email authentication verified
- Safe to trust sender identity
- Content may still require separate review

**If Suspicious/Failed:**
- ❌ Do not trust sender identity
- Do not click links or open attachments
- Report to security team
- Block sender if confirmed phishing

---

**Analyst:** Claude AI  
**Analysis Date:** YYYY-MM-DD HH:MM:SS TZ  
**Analysis Type:** Email Header Authentication & Routing
```

## Tools & Commands

### Header Parsing
- Bash/grep/awk - Extract specific headers
- Python email.parser - Parse RFC822 headers

### DNS Verification
```bash
# Check SPF
dig +short domain.com TXT | grep "v=spf1"

# Check DMARC
dig +short _dmarc.domain.com TXT

# Reverse DNS lookup
dig +short -x 192.0.2.1

# Check MX records
dig +short domain.com MX
```

### IP Reputation
```bash
# Reverse DNS
host 192.0.2.1

# WHOIS for IP ownership
whois 192.0.2.1 | grep -E "(OrgName|Country)"
```

### Atlassian (Jira)
- `mcp__atlassian__getJiraIssue` - Fetch ticket with email headers
- `mcp__atlassian__addCommentToJiraIssue` - Post analysis results

## Header Extraction Patterns

### From Jira Tickets
```bash
# Extract all headers from ticket description
grep -E "^[A-Z][a-zA-Z-]+:" ticket.txt

# Extract specific authentication headers
grep -E "Authentication-Results|DKIM-Signature|Received-SPF" ticket.txt
```

### Parse Authentication-Results
```bash
# Extract DKIM result
grep "dkim=" | sed 's/.*dkim=\([^ ;]*\).*/\1/'

# Extract SPF result
grep "spf=" | sed 's/.*spf=\([^ ;]*\).*/\1/'

# Extract DMARC result
grep "dmarc=" | sed 's/.*dmarc=\([^ ]*\).*/\1/'
```

### Parse Received Headers
```bash
# Get all Received headers (in order)
grep -n "^Received:" headers.txt

# Extract sending IPs
grep "Received:" | grep -oE "\[?[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\]?"

# Extract hostnames
grep "Received: from" | sed 's/Received: from \([^ ]*\).*/\1/'
```

## Decision Tree

```
1. Check Authentication-Results Header
   ├─ All pass (SPF, DKIM, DMARC)? → ✅ Continue to step 2
   ├─ Any fail? → ❌ SPOOFED/SUSPICIOUS
   └─ Missing? → ⚪ INSUFFICIENT - Need full headers

2. Verify Sender Alignment
   ├─ From = Return-Path domain? → ✅ Continue to step 3
   ├─ Mismatch? → ❌ SUSPICIOUS
   └─ Reply-To different domain? → ⚠️ FLAG for review

3. Analyze Email Routing
   ├─ Expected infrastructure? → ✅ Continue to step 4
   ├─ Suspicious hops/delays? → ⚠️ SUSPICIOUS
   └─ Unknown/residential IPs? → ❌ SUSPICIOUS

4. Check TLS/Encryption
   ├─ TLS 1.2+? → ✅ Continue to step 5
   ├─ Older TLS or plaintext? → ⚠️ CONCERN
   └─ Missing? → ⚠️ CONCERN

5. Final Assessment
   ├─ All checks pass? → ✅ VERIFIED LEGITIMATE
   ├─ Minor concerns only? → ⚠️ LIKELY LEGITIMATE
   └─ Auth failures or major red flags? → ❌ SPOOFED/PHISHING
```

## Verdict Guidelines

**✅ VERIFIED LEGITIMATE**
- SPF, DKIM, and DMARC all pass
- Sender domains properly aligned
- Email routed through expected infrastructure
- TLS encryption present
- No suspicious patterns

**⚠️ PARTIAL / SUSPICIOUS**
- Some authentication checks failed
- Weak DMARC policy (p=none)
- Minor alignment issues (Reply-To different)
- Unexpected but not malicious routing
- Requires manual review

**❌ FAILED / SPOOFED**
- SPF fail or DKIM fail
- Sender domain mismatch
- Known malicious infrastructure
- Header manipulation detected
- Clear spoofing attempt

**⚪ INSUFFICIENT**
- Full headers not provided
- Authentication-Results header missing
- Unable to verify without additional data
- Request complete headers from reporter

## Example Analysis

### Legitimate Email (GitHub)

**Input:** Email with these key headers:
```
Authentication-Results: mx.google.com;
  dkim=pass header.i=@github.com;
  spf=pass smtp.mailfrom=noreply@github.com;
  dmarc=pass (p=QUARANTINE sp=REJECT dis=NONE)
From: GitHub <noreply@github.com>
Return-Path: <noreply@github.com>
```

**Analysis:**
- ✅ DKIM PASS - Signed by github.com
- ✅ SPF PASS - Authorized GitHub SMTP server
- ✅ DMARC PASS - Strict policy (p=QUARANTINE)
- ✅ Sender alignment - From matches Return-Path
- ✅ Routed through legitimate GitHub infrastructure

**Verdict:** ✅ VERIFIED LEGITIMATE

---

### Spoofed Email

**Input:** Email with these headers:
```
Authentication-Results: mx.google.com;
  dkim=none;
  spf=fail;
  dmarc=fail
From: PayPal Security <service@paypal.com>
Return-Path: <phisher@evil-domain.com>
```

**Analysis:**
- ❌ DKIM NONE - No signature present
- ❌ SPF FAIL - Sending IP not authorized
- ❌ DMARC FAIL - Policy enforcement triggered
- ❌ Sender mismatch - Return-Path is different domain
- ❌ From domain spoofed

**Verdict:** ❌ CONFIRMED SPOOFING ATTEMPT

---

## Best Practices

1. **Always check Authentication-Results first** - This is the authoritative source
2. **Read Received headers bottom-to-top** - Email flow is chronological bottom-up
3. **Compare all sender-related headers** - From, Return-Path, Reply-To, Sender
4. **Verify DNS records** - Don't just trust headers, check SPF/DMARC at source
5. **Look for patterns** - Legitimate senders have consistent infrastructure
6. **Consider context** - Some legitimate emails fail auth (forwarding, mailing lists)
7. **Document unusual cases** - Build knowledge base of edge cases

## Common Edge Cases

### Legitimate Auth Failures

**Forwarded Emails:**
- SPF often fails (forwarding server not in original SPF)
- DMARC may fail due to SPF failure
- Check for "Forwarded" or "X-Forwarded" headers

**Mailing Lists:**
- May modify body (breaks DKIM)
- From vs Sender header difference
- List-* headers indicate mailing list

**Third-party Senders:**
- Marketing platforms (HubSpot, Mailchimp)
- SPF includes third-party servers
- DKIM signed by marketing platform domain

### Suspicious but Legitimate

**Different Reply-To:**
- Ticket systems use different reply addresses
- Support/no-reply addresses
- Verify Reply-To domain is affiliated

**Multiple Relays:**
- Large organizations have complex routing
- Cloud email gateways add hops
- All hops should be internal/expected infrastructure
