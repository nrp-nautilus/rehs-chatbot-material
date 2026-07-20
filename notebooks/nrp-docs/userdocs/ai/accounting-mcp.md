# NRP Accounting MCP Server

Source: https://nrp.ai/documentation/userdocs/ai/accounting-mcp

# NRP Accounting MCP Server

The NRP Accounting MCP server provides read-only access to NRP accounting data stored in ClickHouse. It is intended for AI clients and tools that need to answer questions about namespace, institution, node, and resource usage.

## What users can ask

- Top namespaces, institutions, or nodes by GPU, CPU, memory, storage, FPGA, or network usage

- Active namespaces over a date range

- Namespace summaries and trends

- Top nodes for a namespace

- Filter discovery by namespace, institution, node, resource, PI, or node institution

## Best-supported tools

- get_latest_data_date : get the most recent ingested accounting date

- list_active_namespaces : list namespaces with observed usage in a date window

- list_filter_values : discover distinct filter values from actual usage rows

- top_resource_consumers : rank namespaces, institutions, or nodes for one resource

- get_usage_timeseries : return a daily trend for one namespace, institution, node, or node institution

- get_namespace_summary : summarize one namespace by resource and unit

- get_namespace_daily_trend : return a namespace trend view, defaulting to the last 30 days

- top_nodes_for_namespace : rank the highest-usage nodes for one namespace and one resource

- get_namespace_details : return namespace metadata, recent trend, and top nodes

- query_resource_usage : flexible escape hatch for custom aggregations

## Client access

### Native MCP

- Endpoint: https://nrp-accounting-mcp.nrp-nautilus.io/

- Best for clients that support MCP directly

- Exposed separately at the root endpoint

### OpenAPI bridge

- Endpoint: https://nrp-accounting-mcp.nrp-nautilus.io/openapi

- OpenAPI docs: https://nrp-accounting-mcp.nrp-nautilus.io/openapi/docs

- Best for tools like Open WebUI that need an OpenAPI-compatible tool server

- Requires a Bearer token using MCPO_API_KEY

OpenAPI authorization

Authorization: Bearer <MCPO_API_KEY>

## Defaults and behavior

- Most tools default to the latest ingested accounting day if no dates are supplied.

- Trend-oriented tools and list_active_namespaces default to the last 30 days.

- list_filter_values and list_active_namespaces return values observed in actual usage rows, not a static catalog.

- Discovery responses include total_count and is_truncated .

- Resource names should be canonical: gpu , cpu , memory , storage , fpga , network .

- Common aliases such as gpu_hours , gpu-hours , GPU hours , and cpu_core_hours are normalized automatically.

- Units are returned separately. For example, resource=gpu returns rows with unit=gpu_hours .

## Example prompts

- “What are the top 5 namespaces by GPU usage in the last 30 days in the NRP?”

- “List all namespaces with observed usage in the last month.”

- “Show GPU and CPU usage for namespace foo between 2026-03-22 and 2026-04-21 .”

- “Show the top nodes for namespace foo by GPU usage this week.”

## Prompt guidance

- Prefer focused asks like “top GPU namespaces” or “active namespaces last month” over generic “query usage.”

- Use canonical resource names like gpu and cpu in prompts.

- If you want a table, specify the columns and sorting you want.

- If a model needs highly reliable behavior, prefer native MCP over OpenAPI when the client supports it.

The implementation lives in:

- nrp_accounting_pipeline/mcp_server.py

- nrp_accounting_pipeline/accounting_queries.py

- README.md

Kubernetes manifests live under k8s/base , including:

- deployment-mcp.yaml

- deployment-openapi.yaml

- service-mcp.yaml

- service-openapi.yaml

- ingress-mcp.yaml

- configmap.yaml

- secret.yaml

Deployment shape:

- Deployment/nrp-accounting-mcp runs the native FastMCP HTTP server on port 8000 .

- Deployment/nrp-accounting-openapi runs mcpo as an MCP-to-OpenAPI bridge on port 8000 .

- Both are exposed through HAProxy ingress on nrp-accounting-mcp.nrp-nautilus.io .

- Ingress routes / to the native MCP service and /openapi to the OpenAPI bridge service.

- TLS is enabled for the ingress host.

Container and runtime details:

- Image: ghcr.io/djw8605/nrp-clickhouse:latest

- imagePullPolicy: Always is set to avoid stale cached images when using latest .

- The OpenAPI bridge is launched with:

```
mcpo --host 0.0.0.0 --port 8000 --root-path /openapi --api-key "$MCPO_API_KEY" -- python -m nrp_accounting_pipeline.mcp_server
```

Required secret and config values:

- CLICKHOUSE_HOST

- CLICKHOUSE_USER

- CLICKHOUSE_PASSWORD

- MCPO_API_KEY

- MCP_ALLOWED_HOSTS

- MCP_ALLOWED_ORIGINS

Admin notes:

- If the ingress hostname changes, update both the ingress host and the MCP allowed host/origin settings or the server will return 421 Invalid Host header .

- If Open WebUI returns 401 Missing or invalid Authorization header , configure its OpenAPI tool server with the Bearer token from MCPO_API_KEY .

- If a client gets empty results for gpu-hours , query resource=gpu instead. Aliases are normalized automatically, but canonical resource names are still preferred.
