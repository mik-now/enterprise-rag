# Deploy Intel® Chatbot Toolkit

[← Docs index](../README.md)

Full deployment workflow: initialization, access, credentials, configuration, teardown.

## What gets installed

One command installs: model servers, vector database, NATS, Enhanced Data Preparation (EDP), system fingerprint, RAG microservices (retriever, reranker, prompt template, guardrails, LLM), Keycloak config, APISIX gateway, optional MCP gateway, UI, optional HPA.

## Prerequisites

The platform and Intel® Inference Toolkit must be installed first: [Platform Quickstart](https://github.com/intel/toolkit-manager/blob/main/docs/getting-started/quickstart.md). Hardware: [Prerequisites](../getting-started/prerequisites.md).

## Deployment workflow

> [!IMPORTANT]
> Run every command from the **Toolkit Manager** repo root, not from this repository. `init erag` clones this repository into `ext/enterprise.ai-erag` at a pinned revision.

### Step 1 - Initialize

```bash
./toolkit_manager.sh init erag [--env <name>] [--flavour <name>]
```

| Flavour | Use case |
|---|---|
| `chatqna` (default) | Conversational RAG |
| `docsum` | Document summarization |
| `audioqna` | Voice-based QA |
| `translation` | Language translation |
| `pl_chatqna` | Polish-language RAG |
| `chatqna_intel_gpu` | ChatQnA with the LLM on an Intel GPU (experimental) |

Seeds `env/<name>/config.erag.yaml` from the flavour's defaults. Model catalog (`models-rag.yaml`) is seeded at install time.

### Step 2 - Configure (optional)

Edit `env/<name>/config.erag.yaml`:

| Setting | Options | Default |
|---------|---------|---------|
| `pipeline_type` | `chatqna` \| `docsum` \| `translation` | `chatqna` |
| `pipeline_variant` | `base` \| `query-rewrite` \| `output_guard` \| `retrieve-rerank` \| `upload` | `base` |
| `inference_models` | List: `name` + `role` (`llm` \| `embedding` \| `reranking`) | `llama3-8b-awq`, `nomic-embed`, `bge-reranker-v2-m3` |
| `vector_databases_vector_store` | `redis-cluster` \| `mssql` \| `pgvector` | `redis-cluster` |
| `mcp_enabled` | `true` \| `false` | `true` for `chatqna`, `audioqna`, `pl_chatqna`; `false` otherwise |
| `hpa_enabled` | `true` \| `false` | `true` |

Gated models: `export HF_TOKEN="hf_..."`. Minimum hardware (≤60 cores / 128 GB): [Prerequisites - Deploying on Minimum Hardware](../getting-started/prerequisites.md#deploying-on-minimum-hardware).

### Step 3 - Deploy

```bash
./toolkit_manager.sh install erag [--env <name>]
```

Validates, deploys inference models, installs RAG components in dependency order, waits for readiness, writes credentials to `env/<name>/logs/rag/`. Takes 15-20 minutes.

Flags: `--env <name>`, `--only` (no deps), `--skip <names>`, `-- <ansible-args>`.

## Model serving

Models deploy automatically via `app_inference_models` during `install erag`. No manual `./model-manager` step needed.

Default (ChatQnA): `llama3-8b-awq` (LLM), `nomic-embed` (embedding), `bge-reranker-v2-m3` (reranking), all in `llm-inference` namespace. LLM via AI Gateway; embedding/reranking via KServe service names.

Customize: edit `inference_models` in `env/<name>/config.erag.yaml`. Each model must exist in `env/<name>/models-rag.yaml`.

## Access and credentials

### Access the UI

Gateway binds ports 80/443 on the cluster node via `hostPort`.

**On cluster node:**

```bash
echo "127.0.0.1 inteltoolkits.ai grafana.inteltoolkits.ai keycloak.inteltoolkits.ai s3.inteltoolkits.ai seaweedfs.inteltoolkits.ai" | sudo tee -a /etc/hosts
```

Base domain from `base_domain_name` in `env/<name>/global_config.yaml` (default: `inteltoolkits.ai`). Each subdomain explicit - wildcards unsupported in `/etc/hosts`.

**From another machine:** `ssh -L 443:localhost:443 user@<cluster-ip>`, then add same line to local `/etc/hosts`.

URLs: `https://inteltoolkits.ai` (RAG UI), `https://keycloak.inteltoolkits.ai`, `https://grafana.inteltoolkits.ai`, `https://seaweedfs.inteltoolkits.ai`, `https://s3.inteltoolkits.ai`.

> [!IMPORTANT]
> With the default self-signed certificates, visit `https://s3.<base_domain_name>` in your browser and accept the warning **before** ingesting documents. Without it, uploads fail in the browser with no error from the cluster.

### Credentials

Chatbot Toolkit accounts are in `env/<name>/logs/rag/` (one-time passwords; change after first login). The platform's Keycloak and Grafana accounts are in Kubernetes Secrets:

| Service | Username | Location |
|---------|----------|----------|
| UI admin/user/maintainer (realm `EnterpriseRAG`) | `erag-admin`, `erag-user`, `erag-maintainer` | default_credentials.txt |
| Keycloak admin console (realm `master`) | admin | `keycloak-admin-secret` Secret, namespace `keycloak` |
| Grafana, **Sign in with Keycloak** (realm `platform`) | platform-admin | `platform-bootstrap-admin` Secret, namespace `keycloak` (temporary; change at first login) |
| Grafana, local admin on the login form | admin | `grafana-admin-credentials` Secret, namespace `monitoring` |
| Vector store | (varies) | default_credentials.yaml |
| SeaweedFS S3 | (access/secret keys) | default_credentials.yaml |
| SeaweedFS Admin | (user/pass) | default_credentials.yaml |
| EDP Redis | default | default_credentials.yaml |
| EDP Postgres | edp | default_credentials.yaml |
| System Fingerprint Postgres | fingerprint / system_fingerprint | `fingerprint-postgresql-secret` K8s secret |
| NATS | NKey | `nats-auth` secret (auto-mounted) |

Secure credentials: `ansible-vault encrypt env/<name>/logs/rag/default_credentials.yaml`, then pass `-- --ask-vault-pass` on next install.

## Configure the deployment

Edit `env/<name>/config.erag.yaml` and re-run `./toolkit_manager.sh install erag --env <name>`. Updates only affected components. See: [Pipeline Configuration](pipelines.md), [Advanced Configuration Guide](../configuration/configuration.md).

## Data ingestion, UI and telemetry

Use **Data Ingestion** tab in **Admin Panel** (admin only; ChatQnA and AudioQnA only). User guides: [AudioQnA](../Intel_Chatbot_Toolkit_AudioQnA_User_Guide.pdf), [ChatQnA](../Intel_Chatbot_Toolkit_ChatQnA_User_Guide.pdf), [DocSum](../Intel_Chatbot_Toolkit_DocSum_User_Guide.pdf). Telemetry: [Telemetry Guide](../configuration/telemetry.md).

## Single sign-on and SharePoint integration

SSO and SharePoint share one Microsoft Entra ID app registration. Configure in `env/<name>/config.erag.yaml`:

```yaml
erag_keycloak_oidc_endpoint: ""       # enables SSO
erag_keycloak_oidc_alias: "enterprise-sso"
erag_keycloak_oidc_client_id: ""
erag_keycloak_oidc_client_secret: ""
erag_keycloak_oidc_tenant_id: ""      # additionally enables SharePoint
```

All empty = disabled. Partial config rejected. Apply: `./toolkit_manager.sh install erag --env <name>`. Full procedure: [Single Sign-On and SharePoint Integration](../configuration/sharepoint.md).

## Remove the installation

```bash
./toolkit_manager.sh teardown erag --env <name>
```

Removes components in reverse order; models undeployed automatically.

> [!WARNING]
> Teardown is environment-scoped. Tear down with the same `--env` you installed with: running it against another environment silently does nothing to the one you meant. `teardown erag` keeps the cluster, the platform, and Intel® Inference Toolkit; `teardown infrastructure` removes the cluster and everything on it.

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| **Test deployment** | ChatQnA: `cd .../ext/enterprise.ai-erag/deployment && ./scripts/test_connection.sh`. DocSum: `./scripts/test_docsum.sh`. Translation: `./scripts/test_translation.sh`. |
| **Debug tool** | [Debug Tool Guide](../faq-and-troubleshooting/troubleshooting.md) collects diagnostics. |
| **Status check** | `./toolkit_manager.sh status --env <name>` |
| **Pods stuck pending** | `kubectl describe pod <name> -n <namespace>`. Minimum hardware: verify [tuning steps](../getting-started/prerequisites.md#deploying-on-minimum-hardware). |
| **Models not deploying** | Gated models: `export HF_TOKEN="hf_..."` before install. |
| **Connection test fails** | Wait for all pods `Running` in pipeline namespace. |
| **Install fails** | Check `env/<name>/logs/install-erag-*.log`, then re-run (idempotent). |

## Related documentation

[Prerequisites](../getting-started/prerequisites.md), [Quickstart](../getting-started/quickstart.md), [Pipeline Configuration](pipelines.md), [Configuration Reference](../configuration/configuration.md), [Platform Documentation](https://github.com/intel/toolkit-manager/blob/main/docs/README.md).
