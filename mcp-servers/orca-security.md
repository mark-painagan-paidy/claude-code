# Orca Security MCP Server

**Type**: HTTP (Remote MCP Server)  
**URL**: `https://mcp.orcasecurity.io`  
**Status**: ✅ Active

## Purpose

Integration with Orca Security for:
- Cloud security posture management (CSPM)
- Vulnerability assessment
- Asset inventory queries
- Risk analysis
- Compliance checks

## Configuration

```json
{
  "type": "http",
  "url": "https://mcp.orcasecurity.io"
}
```

## Available Tools

### Primary Tool
- `ask_orca` - Natural language queries about cloud security posture

## Usage

The Orca MCP server provides a conversational interface to query your cloud security data.

### Query Types

**Vulnerability Queries:**
```
"Am I vulnerable to CVE-2026-20230?"
"Show me all critical vulnerabilities"
"What assets are affected by CVE-2026-XXXXX?"
```

**Asset Queries:**
```
"List all cloud assets"
"Show me EC2 instances in production"
"What containers are running in my environment?"
```

**Risk Queries:**
```
"What are my highest risk assets?"
"Show me assets with critical findings"
"List assets with public exposure"
```

**Compliance Queries:**
```
"What compliance issues do I have?"
"Show me PCI-DSS violations"
"Are we compliant with SOC 2?"
```

## Usage in Skills

### vuln-check
**Purpose**: Check cloud environment for CVE exposure

```python
# Query Orca for CVE
ask_orca(query: "Am I vulnerable to CVE-2026-20230? Show me all affected assets.")

# Alternative query
ask_orca(query: "Show me assets affected by [vulnerability name]")
```

## Response Format

Orca returns structured responses with:
- Risk level assessment
- Affected asset counts
- Asset types
- Top affected assets (up to 10)
- Remediation guidance

Example response:
```
Risk Level: High

Affected Asset Types:
- Virtual Machines: 2
- Containers: 1

Top Affected Assets:
1. cisco-ucm-prod-01 (VM - AWS EC2) - Production
2. cisco-ucm-staging (VM - AWS EC2) - Staging
3. ucm-container-east (Container - EKS) - Development

Recommendation: Apply security patches immediately
```

## Authentication

Authentication is handled by the remote MCP server through OAuth/API tokens configured in the Orca platform. No local credentials needed in `mcp_config.json`.

## Query Best Practices

1. **Be specific**: Include CVE IDs, asset names, or specific risk levels
2. **Ask for details**: Request "show all affected assets" for comprehensive info
3. **Filter by environment**: Specify production/staging when relevant
4. **Request actionable info**: Ask for remediation steps

## Common Query Patterns

### Vulnerability Assessment
```
"Am I vulnerable to CVE-2026-XXXXX?"
"Show critical vulnerabilities in production"
"List all open CVEs affecting my infrastructure"
```

### Asset Inventory
```
"Show all EC2 instances with public IPs"
"List containers in my EKS clusters"
"What RDS databases are unencrypted?"
```

### Risk Analysis
```
"What are my top 10 highest risk assets?"
"Show assets with critical severity findings"
"List publicly exposed databases"
```

### Compliance
```
"Show PCI-DSS compliance violations"
"Are there any CIS benchmark failures?"
"What assets are non-compliant with SOC 2?"
```

## Response Interpretation

### Risk Levels
- **Critical**: Immediate action required
- **High**: High priority remediation
- **Medium**: Schedule remediation
- **Low**: Informational, address when possible

### Asset Types
- Virtual Machines (EC2, Azure VM, GCP Compute)
- Containers (ECS, EKS, AKS, GKE)
- Databases (RDS, DynamoDB, etc.)
- Storage (S3, Blob Storage, etc.)
- Serverless (Lambda, Functions)

## Integration with CrowdStrike

Orca focuses on **cloud infrastructure**, while CrowdStrike Falcon focuses on **endpoints**.

Use both in `vuln-check` skill:
- **Orca**: Check cloud VMs, containers, cloud services
- **CrowdStrike**: Check physical/virtual endpoints, workstations, servers

## Limitations

- Remote HTTP MCP server (requires internet connectivity)
- Query response time depends on Orca API performance
- Natural language processing may require query refinement
- Asset visibility limited to what Orca has scanned

## Troubleshooting

**No response**: Check internet connectivity to `mcp.orcasecurity.io`

**Authentication error**: Verify Orca platform API access is configured

**No assets found**: Ensure Orca has scanned your cloud environment recently

**Vague responses**: Rephrase query with more specific details (CVE ID, asset name)

## Example Queries

### Check specific CVE
```
ask_orca: "Am I vulnerable to CVE-2026-20230? Show me all affected assets with their risk levels."
```

### Find critical risks
```
ask_orca: "What are the top 5 critical vulnerabilities in my production environment?"
```

### Asset inventory
```
ask_orca: "List all EC2 instances in us-east-1 with their security findings."
```

### Compliance check
```
ask_orca: "Show me all PCI-DSS compliance violations and affected assets."
```

## Related Documentation

- [Orca Security Documentation](https://docs.orcasecurity.io/)
- [Orca API Reference](https://docs.orcasecurity.io/docs/api-reference)
- [MCP Integration Guide](https://docs.orcasecurity.io/docs/mcp-integration)
