---
name: phishing-takedown
description: Submit phishing sites for takedown to JP-CERT and Google Safe Browsing
invocation: user
---

# Phishing Takedown Skill

Submit confirmed phishing sites for takedown to JP-CERT (Anti-Phishing Council Japan) and Google Safe Browsing. This skill extracts phishing URLs from SOCSD tickets or accepts direct URL input, then provides submission guidance for both reporting channels.

## Usage

**From SOCSD Ticket:**
```
/phishing-takedown SOCSD-12345
```

**Direct URL:**
```
/phishing-takedown https://evil-phishing-site.com
```

**Multiple URLs:**
```
/phishing-takedown SOCSD-12345 https://phishing-url1.com https://phishing-url2.com
```

## What it does

1. **Extract Phishing URLs**
   - Fetch details from SOCSD ticket if provided
   - Extract all URLs from ticket description or accept direct input
   - Identify primary phishing domain and related URLs
   - Validate URL format and accessibility

2. **Gather Submission Information**
   - Extract sender email address (attacker's email)
   - Collect screenshots/evidence from ticket attachments
   - Note any IOCs (domains, IPs, email addresses)
   - Compile victim impact details

3. **JP-CERT Submission Preparation**
   - Format data for Anti-Phishing Council Japan form
   - Prepare required fields (Brand, URL, Evidence)
   - Generate submission instructions

4. **Google Safe Browsing Submission**
   - Format data for Google's phishing report form
   - Prepare URL and additional context
   - Generate submission instructions

5. **Documentation**
   - Post takedown submission summary to original SOCSD ticket
   - Record submission timestamps and reference numbers
   - Track URLs submitted for takedown
   - Update ticket status/labels if needed

## Reporting Channels

### 1. JP-CERT (Anti-Phishing Council Japan)

**Submission URL:** https://www.antiphishing.jp/registration.html

**Required Information:**
- **Brand Name:** Paidy
- **Phishing URL:** Full URL of the phishing site
- **Discovery Date:** When the phishing site was discovered
- **Evidence:** Screenshots, email samples, or other proof
- **Reporter Information:** Contact details

**Submission Process:**
1. Open the JP-CERT registration form
2. Select or enter "Paidy" as the targeted brand
3. Enter the full phishing URL
4. Upload evidence (screenshots, email headers)
5. Provide discovery date and reporter contact info
6. Submit the form

**Response Time:** Typically 1-3 business days for initial acknowledgment

---

### 2. Google Safe Browsing

**Submission URL:** https://safebrowsing.google.com/safebrowsing/report_phish/

**Required Information:**
- **Phishing URL:** Full URL of the malicious site
- **Additional Context:** Optional details about the phishing attempt

**Submission Process:**
1. Open Google Safe Browsing report form
2. Enter the phishing URL in the provided field
3. Add any additional context (optional)
4. Complete CAPTCHA verification
5. Submit the report

**Response Time:** Google typically processes reports within hours and adds to blocklist if confirmed

**Note:** Google Safe Browsing feeds into Chrome, Firefox, and Safari's phishing protection

---

## Output Format

When executed, the skill provides:

```markdown
## Phishing Takedown Submission Report

**Source:** SOCSD-12345 (or Direct Input)
**Submission Date:** YYYY-MM-DD HH:MM:SS TZ

---

### Phishing URLs Identified

1. **Primary Phishing Site:** https://evil-phishing-site.com/login
   - **Status:** Active/Down
   - **Infrastructure:** Hosting provider, IP address
   - **First Seen:** YYYY-MM-DD

2. **Related URLs:**
   - https://evil-phishing-site.com/verify
   - https://evil-phishing-site.com/update

---

### Attacker Information

- **Sender Email:** attacker@evil-domain.com
- **Phishing Domain:** evil-phishing-site.com
- **Hosting IP:** 192.0.2.1
- **Registrar:** Registrar name
- **Name Servers:** NS records

---

### Takedown Submission Instructions

#### 1. Submit to JP-CERT (Anti-Phishing Council Japan)

**Submission URL:** https://www.antiphishing.jp/registration.html

**Form Fields:**
- **Brand Name (ブランド名):** Paidy
- **Phishing URL (フィッシングサイトURL):** 
  ```
  https://evil-phishing-site.com/login
  ```
- **Discovery Date (発見日):** YYYY-MM-DD
- **Evidence (証拠):** Attach screenshot from ticket or use evidence below
- **Reporter Info (報告者情報):** [Your contact details]

**Evidence Summary:**
- Email sent from: attacker@evil-domain.com
- Subject line: [Subject from ticket]
- Impersonates: Paidy billing/login page
- Targets: Paidy customers/users

**Action Required:**
1. ✅ Open JP-CERT form: https://www.antiphishing.jp/registration.html
2. ✅ Fill in the form with the information above
3. ✅ Upload screenshot evidence (see ticket attachments)
4. ✅ Submit the form
5. ✅ Save confirmation/reference number

---

#### 2. Submit to Google Safe Browsing

**Submission URL:** https://safebrowsing.google.com/safebrowsing/report_phish/

**Form Fields:**
- **URL to report:**
  ```
  https://evil-phishing-site.com/login
  ```
- **Additional information (optional):**
  ```
  Phishing site impersonating Paidy (paidy.com) payment service. 
  Harvests user credentials. Reported by customer on YYYY-MM-DD.
  Related phishing email from: attacker@evil-domain.com
  ```

**Action Required:**
1. ✅ Open Google Safe Browsing report form: https://safebrowsing.google.com/safebrowsing/report_phish/
2. ✅ Paste the phishing URL
3. ✅ Add context in the optional field (see above)
4. ✅ Complete CAPTCHA
5. ✅ Submit the report

**Repeat for related URLs:**
- https://evil-phishing-site.com/verify
- https://evil-phishing-site.com/update

---

### Submission Tracking

| Service | URL | Submitted | Status | Reference |
|---------|-----|-----------|--------|-----------|
| JP-CERT | https://evil-phishing-site.com/login | YYYY-MM-DD HH:MM | Pending | [Add ref#] |
| Google Safe Browsing | https://evil-phishing-site.com/login | YYYY-MM-DD HH:MM | Pending | - |

**Next Steps:**
1. Complete manual submissions to JP-CERT and Google Safe Browsing using the instructions above
2. Record reference numbers in the tracking table
3. Monitor phishing site status (use `/phishing-analysis` or manual checks)
4. Follow up with takedown services if site remains active after 48-72 hours
5. Update original SOCSD ticket with takedown completion status

---

**Note:** This skill prepares submission instructions and gathers required information. Manual submission to JP-CERT and Google Safe Browsing is required as both services use web forms with CAPTCHA verification.

---

**Analyst:** Claude AI  
**Report Generated:** YYYY-MM-DD HH:MM:SS TZ
```

---

## Integration with SOCSD Tickets

### Fetching from Jira

When a SOCSD ticket ID is provided:

1. **Retrieve Ticket Details**
   ```
   mcp__atlassian__getJiraIssue(issueIdOrKey: "SOCSD-12345")
   ```

2. **Extract Phishing Data**
   - Email body from description
   - URLs from ticket description and comments
   - Attacker email from custom field (`customfield_10834`)
   - Request Category to confirm phishing classification
   - Attachments (screenshots, email evidence)

3. **Post Takedown Report**
   ```
   mcp__atlassian__addCommentToJiraIssue(
     issueIdOrKey: "SOCSD-12345",
     body: [Takedown submission report]
   )
   ```

4. **Update Ticket Fields (Optional)**
   - Add "Takedown Requested" label
   - Update Request Category to "Takedown Request" if needed
   - Set custom field for takedown tracking

---

## URL Analysis Commands

### Validate URLs
```bash
# Test if phishing site is still active
curl -sL -o /dev/null -w "%{http_code}\n" "https://phishing-site.com"

# Get redirect chain
curl -sL -I "https://phishing-site.com" | grep -i "location\|http"
```

### Domain Information
```bash
# WHOIS lookup
whois phishing-domain.com | grep -E "(Registrar|Creation|Name Server)"

# DNS resolution
dig +short phishing-domain.com A

# Check hosting IP
dig +short phishing-domain.com A | xargs -I {} whois {} | grep -E "(OrgName|Country)"
```

### Screenshot Evidence
- Check ticket attachments for existing screenshots
- Note screenshot filenames for reference in submissions
- If screenshots missing, recommend using browser screenshot tools

---

## Tools & Commands Used

### Atlassian (Jira)
- `mcp__atlassian__getJiraIssue` - Fetch SOCSD ticket details
- `mcp__atlassian__addCommentToJiraIssue` - Post takedown report
- `mcp__atlassian__editJiraIssue` - Update ticket labels/fields

### URL Analysis
- `curl` - Test URL accessibility and status
- `dig` - DNS lookups
- `whois` - Domain registration information

### Evidence Gathering
- Parse ticket description for URLs
- Extract email headers and sender info
- Identify IOCs (domains, IPs, email addresses)

---

## Workflow Integration

### Typical Use Case

1. **Phishing Report Received** → Analyzed with `/phishing-analysis SOCSD-12345`
2. **Verdict: Confirmed Phishing** → Decision to request takedown
3. **Execute Takedown Skill** → `/phishing-takedown SOCSD-12345`
4. **Manual Submissions** → Analyst submits to JP-CERT & Google using provided instructions
5. **Track Status** → Monitor for site takedown (24-72 hours)
6. **Follow-up** → Escalate if site remains active after 72 hours

---

## Best Practices

1. **Verify Phishing Confirmation**
   - Only submit URLs confirmed as malicious
   - Run `/phishing-analysis` first if verdict unclear
   - Avoid false positives (impacts reputation with takedown services)

2. **Timely Submission**
   - Submit within 1-2 hours of confirmation
   - Faster submission = faster takedown = fewer victims

3. **Complete Evidence**
   - Include screenshots showing phishing content
   - Provide email headers if available
   - Document brand impersonation clearly

4. **Track Submissions**
   - Record submission date/time in ticket
   - Save reference numbers from JP-CERT
   - Monitor for follow-up requests

5. **Monitor Takedown Success**
   - Check URL status after 24, 48, and 72 hours
   - Re-submit if site still active after 72 hours
   - Document takedown completion in ticket

6. **Report Multiple URLs**
   - Submit all related phishing URLs from same campaign
   - Include redirect chains and alternate domains
   - Note if multiple domains point to same content

---

## Future Enhancements

**Potential additions to this skill:**

1. **Automated Submission (API Integration)**
   - Google Safe Browsing API (if access granted)
   - Automated form submission tools
   - Selenium/Playwright for web form automation

2. **Takedown Vendor Integration**
   - Integration with third-party takedown services
   - Vendor-specific submission formats
   - Status tracking via vendor APIs

3. **Screenshot Automation**
   - Automated screenshot capture of phishing sites
   - Thumbnail generation for reports
   - Evidence archival

4. **Status Monitoring**
   - Automated checks for site takedown status
   - Notifications when site is confirmed down
   - Metrics on takedown success rates

5. **Bulk Submission**
   - Handle multiple tickets at once
   - Batch submission for related campaigns
   - Campaign tracking across multiple URLs

---

## Troubleshooting

**Issue:** URL is already down when executing skill
- **Solution:** Document in ticket and mark as already resolved

**Issue:** URL returns error or doesn't resolve
- **Solution:** Include in submission with note about current status

**Issue:** Screenshots not available in ticket
- **Solution:** Provide instructions for analyst to capture, or use web archive

**Issue:** Uncertain if URL is truly phishing
- **Solution:** Run `/phishing-analysis` first for verdict before takedown

**Issue:** JP-CERT form is in Japanese
- **Solution:** Use browser translation, or follow field mapping in this guide

**Issue:** Google Safe Browsing CAPTCHA blocks automation
- **Solution:** Manual submission required; skill provides formatted submission text

---

## Related Skills

- `/phishing-analysis` - Analyze suspected phishing emails before takedown
- `/header-analysis` - Verify email authentication headers
- (Future) `/phishing-status` - Check takedown status of reported URLs

---

## References

- **JP-CERT Anti-Phishing Council:** https://www.antiphishing.jp/
- **Google Safe Browsing:** https://safebrowsing.google.com/
- **APWG (Anti-Phishing Working Group):** https://apwg.org/
- **Phishing Response Best Practices:** https://www.cisa.gov/phishing
