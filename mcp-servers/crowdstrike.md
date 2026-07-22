# CrowdStrike Falcon MCP Server

**Package**: `falcon-mcp`  
**Type**: UVX (Python)  
**Status**: ✅ Active

## Purpose

Integration with CrowdStrike Falcon for:
- Endpoint vulnerability scanning
- Host/device management
- Security detection queries
- Threat intelligence
- Real-time response (RTR)
- IOC management

## Configuration

```json
{
  "command": "uvx",
  "args": ["--from", "falcon-mcp", "falcon-mcp"],
  "env": {
    "FALCON_CLIENT_ID": "***",
    "FALCON_CLIENT_SECRET": "***",
    "FALCON_BASE_URL": "https://api.crowdstrike.com"
  }
}
```

## Available Tools (Common Ones)

### Vulnerability Management
- `falcon_search_vulnerabilities` - Search CVEs in environment
- `falcon_search_images_vulnerabilities` - Container image vulns
- `falcon_search_serverless_vulnerabilities` - Serverless vulns

### Host/Endpoint Management
- `falcon_search_hosts` - Search endpoints
- `falcon_get_host_details` - Get detailed host info
- `falcon_search_sensor_usage` - Sensor usage stats

### Detection & Response
- `falcon_search_detections` - Search security detections
- `falcon_get_detection_details` - Detailed detection info
- `falcon_search_indicators` - Search threat indicators
- `falcon_search_iocs` - Search indicators of compromise

### Real-Time Response (RTR)
- `falcon_init_rtr_session` - Start RTR session
- `falcon_execute_rtr_read_only_command` - Run read-only command
- `falcon_run_rtr_read_only_command_and_wait` - Run and wait for result
- `falcon_list_rtr_session_files` - List session files
- `falcon_delete_rtr_session` - Close RTR session

### Case Management
- `falcon_create_case` - Create security case
- `falcon_search_cases` - Search cases
- `falcon_get_cases` - Get case details
- `falcon_update_case` - Update case

### Quarantine
- `falcon_search_quarantined_files` - Search quarantined files
- `falcon_preview_quarantine_actions` - Preview actions
- `falcon_update_quarantined_files` - Update quarantine status

### IOC Management
- `falcon_add_ioc` - Add indicator of compromise
- `falcon_remove_iocs` - Remove IOCs
- `falcon_search_iocs` - Search IOCs

### Cloud Security (CSPM)
- `falcon_search_cspm_assets` - Search cloud assets
- `falcon_search_cspm_suppression_rules` - Suppression rules

## Usage in Skills

### vuln-check
**Purpose**: Check if CVE exists in environment

```python
# Search for specific CVE
falcon_search_vulnerabilities(
  filter: "cve.id:'CVE-2026-20230'",
  facet: "host_info",
  limit: 100
)

# Get remediation details
falcon_search_vulnerabilities(
  filter: "cve.id:'CVE-2026-20230'",
  facet: "remediation",
  limit: 100
)

# Get affected host details
falcon_get_host_details(ids: ["host_id_1", "host_id_2"])
```

## Authentication

Requires CrowdStrike API credentials:
- **Client ID**: OAuth2 client ID
- **Client Secret**: OAuth2 client secret
- **Base URL**: Regional API endpoint (e.g., `https://api.crowdstrike.com`)

Create API credentials in Falcon Console:
1. Support & Resources → API Clients and Keys
2. Add new API client
3. Assign scopes (read permissions recommended)
4. Copy Client ID and Secret

## Common Filters

### Vulnerability Search
```
cve.id:'CVE-2026-XXXXX'        - Specific CVE
status:'open'                  - Open vulnerabilities
severity:'CRITICAL'            - Critical severity
```

### Host Search
```
hostname:'SRV-*'               - Hostname pattern
platform_name:'Windows'        - OS platform
last_seen:>'2026-07-01'       - Recently seen
```

### Detection Search
```
status:'new'                   - New detections
severity:>='medium'            - Medium+ severity
max_severity:'critical'        - Critical detections
```

## Response Formats

### Vulnerability Result
```json
{
  "cve": {
    "id": "CVE-2026-XXXXX",
    "severity": "CRITICAL",
    "base_score": 9.8
  },
  "host_info": {
    "hostname": "SRV-PROD-01",
    "os": "Windows Server 2019"
  },
  "status": "open"
}
```

### Host Details
```json
{
  "device_id": "abc123...",
  "hostname": "SRV-PROD-01",
  "os_version": "Windows Server 2019",
  "local_ip": "10.0.1.50",
  "external_ip": "203.0.113.1",
  "last_seen": "2026-07-22T15:30:00Z",
  "agent_version": "7.14.16303"
}
```

## Usage Examples

### Check for critical vulnerabilities
```python
falcon_search_vulnerabilities(
  filter: "severity:'CRITICAL' AND status:'open'",
  limit: 50,
  sort: "created_timestamp.desc"
)
```

### Find Windows servers
```python
falcon_search_hosts(
  filter: "platform_name:'Windows' AND product_type_desc:'Server'",
  limit: 100
)
```

### Search recent detections
```python
falcon_search_detections(
  filter: "created_timestamp:>'2026-07-20T00:00:00Z'",
  limit: 50,
  sort: "created_timestamp.desc"
)
```

### Start RTR session for investigation
```python
# Initialize session
falcon_init_rtr_session(
  device_id: "abc123...",
  queue_offline: false
)

# Run command
falcon_execute_rtr_read_only_command(
  session_id: "session_id",
  base_command: "ps",
  command_string: "ps | grep suspicious"
)
```

## Best Practices

1. **Use filters**: Always filter queries to reduce API load
2. **Pagination**: Use `limit` and `offset` for large result sets
3. **Read-only first**: Use read-only commands before write operations
4. **Facets**: Use facets for grouped/aggregated data
5. **Error handling**: Check for rate limits (429) and retry

## Troubleshooting

**Authentication failed**: Verify Client ID/Secret are correct and not expired

**No results**: Check filter syntax, ensure hosts are reporting to Falcon

**Rate limit errors**: Reduce query frequency, implement backoff

**Permission denied**: Verify API client has required scopes

## Useful Facets

```
host_info         - Group by host
remediation       - Remediation guidance
cve               - CVE details
status            - Vulnerability status
severity          - Group by severity
```

## Related Documentation

- [Falcon API Documentation](https://falcon.crowdstrike.com/documentation/page/a2a7fc0e/crowdstrike-oauth2-based-apis)
- [Falcon MCP GitHub](https://github.com/CrowdStrike/falcon-mcp)
- [API Client Management](https://falcon.crowdstrike.com/support/api-clients-and-keys)
