---
description: Update weekly security monitoring report canvas with new numbers, comparing against previous week's data and generating rephrased Key Takeaways and Executive Summary
tags: [slack, canvas, security, reporting]
---

# Update Security Report Canvas

This skill updates a weekly security monitoring report canvas with:
1. Week-over-week comparisons
2. Rephrased Key Takeaways highlighting significant changes
3. Rephrased Executive Summary with context and analysis
4. Preserved detailed report data section

## Usage

User should provide:
- The canvas title/date of the CURRENT report to update (e.g., "29th June - 5th July 2026")
- The canvas title/date of the PREVIOUS week to compare against (e.g., "22 - 28 June 2026")

The skill will:
1. Find both canvases by title
2. Read the detailed numbers from both
3. Calculate week-over-week changes
4. Generate completely rephrased content with comparisons
5. Update the current canvas

## Steps

1. **Find the canvases**
   - Search for the current week's canvas by title
   - Search for the previous week's canvas by title
   - Read both canvases to get all numbers

2. **Extract and compare metrics**
   From both canvases, extract:
   - SOC: Total alerts, mitigated, false positives, no impact, phishing
   - reCAPTCHA: Web %, iOS %, Android % block rates
   - Web Attacks: Total auth requests, rate limited, blocked
   - ZScaler: Total threats, malicious content, phishing, XSS/suspicious, adware/spyware
   - Phishing: Employee reports, consumer reports, takedowns

3. **Calculate changes**
   For each metric, calculate:
   - Absolute change (new - old)
   - Percentage change ((new - old) / old * 100)
   - Trend direction (up/down/stable)

4. **Generate rephrased Key Takeaways**
   Create 4 bullet points covering:
   - Most significant SOC/alert changes
   - Notable threat vector changes (ZScaler, reCAPTCHA)
   - Infrastructure performance highlights
   - Zero incident achievement (if applicable)
   
   Use varied phrasing like:
   - "normalized", "stabilized", "surged", "escalated", "moderated"
   - "dropped X%", "climbed X%", "jumped", "fell"
   - Different emojis each time

5. **Generate rephrased Executive Summary**
   For each of 5 sections, write analysis with:
   - Reference to previous week's numbers for context
   - Highlight significant changes with percentages
   - Explain trends and implications
   - Use varied vocabulary and sentence structure
   
   Sections:
   - **Security Monitoring**: Alert volume, mitigation, precision, incidents
   - **reCAPTCHA Monitoring**: Web/iOS/Android trends, threat actor patterns
   - **Web Attacks Monitoring**: Traffic volume, blocking/rate-limiting
   - **ZScaler Monitoring**: Perimeter threats breakdown, emerging patterns
   - **Phishing Monitoring**: Employee/consumer reports, takedowns, brand protection

6. **Update the canvas**
   - Update Key Takeaways section
   - Update Executive Summary section
   - Ensure DETAILED REPORT DATA section is preserved at bottom
   - If numbers section is missing, restore it from the current canvas data

## Important Notes

- Always preserve the detailed numbers section at the bottom
- Use completely different phrasing each time (not just number replacements)
- Include week-over-week context in narrative
- Highlight both improvements and escalations
- Use specific percentages when significant (>20% change)
- Keep writing concise and executive-friendly
- Maintain the same emoji theme/style as original canvas

## Error Handling

- If canvas not found, ask user to verify the title
- If numbers are incomplete, ask user to confirm the data
- If comparison canvas has different format, adapt analysis accordingly
