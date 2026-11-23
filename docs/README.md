# Intel® Chatbot Toolkit documentation

Start with the table. Each row is one job and one page. The sections under it are the same pages, grouped by folder, for when you already know the area.

> [!IMPORTANT]
> [Toolkit Manager](https://github.com/intel/toolkit-manager) installs and operates this toolkit. Clone **that** repository, run every command from its root, and `init erag` will fetch this one into `ext/` for you. See [Meet](overview/meet.md#where-the-pieces-live).

## Find a page

| I want to… | Page |
|---|---|
| Understand what the toolkit is and when to choose it | [Meet Intel® Chatbot Toolkit](overview/meet.md) |
| Check hardware and software before installing | [Prerequisites](getting-started/prerequisites.md) |
| Go from `init erag` to a working assistant | [Quick Start](getting-started/quickstart.md) |
| Install step by step, with endpoints and credentials | [Deploy Intel® Chatbot Toolkit](deployment/install-rag.md) |
| Pick a pipeline or switch between them | [Pipelines](deployment/pipelines.md) |
| Run on VMware vSphere | [Deploy on VMware](deployment/vmware.md) |
| Back up or restore a deployment | [Backup and Restore](deployment/backup-and-restore.md) |
| Find an option in `config.erag.yaml` | [Configuration](configuration/configuration.md) |
| Change the LLM, embedding or reranking model | [Models](configuration/models.md) |
| Add SSO, MFA or Active Directory | [Authentication](configuration/auth.md) |
| Ingest from SharePoint Online | [SharePoint](configuration/sharepoint.md) |
| Let AI agents use retrieval and ingestion | [MCP Integration](configuration/mcp.md) |
| Use an external S3 or NetApp ONTAP document store | [Object Store](configuration/object-store.md) |
| Create the AWS buckets, queue and user | [AWS S3 and SQS Setup](configuration/aws-s3.md) |
| Build the images and use my own registry | [Building Images](configuration/images.md) |
| Open Grafana and read the dashboards | [Telemetry](configuration/telemetry.md) |
| Size replicas, tune the vector database, autoscale | [Performance](configuration/performance.md) |
| See the components, roles and request flow | [Architecture](reference/architecture.md) |
| Look up an image and its Dockerfile | [Container Images](reference/container-images.md) |
| Understand mTLS and the Istio mesh | [Service Mesh](reference/service-mesh.md) |
| Look up a term | [Glossary](reference/glossary.md) |
| Get a short answer | [FAQ](faq-and-troubleshooting/frequently-asked-questions.md) |
| Fix something that is not working | [Troubleshooting](faq-and-troubleshooting/troubleshooting.md) |
| Learn each app's UI | [User guides](#user-guides) |

## Folders

| Folder | When you open it |
|---|---|
| `overview/` | Before you install: what the toolkit is |
| `getting-started/` | Requirements and the first install |
| `deployment/` | The full install, pipelines, VMware, backup and restore |
| `configuration/` | Settings you edit after the first install, integrations, telemetry and tuning |
| `reference/` | Architecture, images, the mesh and terms |
| `faq-and-troubleshooting/` | Answers |
| `assets/` | Images the guides use |
| `docs/` root | The app user guides (PDF); the deployed UIs link to these paths |

## First install

Do these in order: prerequisites, then the quick start.

| Guide | What it covers |
|---|---|
| [Meet Intel® Chatbot Toolkit](overview/meet.md) | What it is, why it exists, when to choose it, and which repository to start from |
| [Prerequisites](getting-started/prerequisites.md) | RAG hardware sizing, software access, and the limited single-user option |
| [Quick Start](getting-started/quickstart.md) | `init erag` to a working assistant, end to end |

## Deploy

Install the toolkit, pick a pipeline, and take it onto a partner platform.

| Guide | What it covers |
|---|---|
| [Deploy Intel® Chatbot Toolkit](deployment/install-rag.md) | Step-by-step install, endpoints, credentials, and teardown |
| [Pipelines](deployment/pipelines.md) | The six flavours, ChatQnA variants, and how to switch between them |
| [Deploy on VMware](deployment/vmware.md) | Running the chatbot on VMware vSphere |
| [Backup and Restore](deployment/backup-and-restore.md) | Enabling it, running a backup or restore, the pre-upgrade gate, and the identity realm |

## Configure

Edit `env/<name>/config.erag.yaml` and re-run `install erag`.

| Guide | What it covers |
|---|---|
| [Configuration](configuration/configuration.md) | Every option in `config.erag.yaml`, and how overrides resolve |
| [Models](configuration/models.md) | Changing the LLM, embedding, and reranking models; multilingual and accuracy features |
| [Authentication](configuration/auth.md) | Keycloak SSO with Microsoft Entra ID, multi-factor auth, and Active Directory federation |
| [SharePoint](configuration/sharepoint.md) | Ingesting from SharePoint Online, scheduled sync, and per-user site filtering |
| [MCP Integration](configuration/mcp.md) | Exposing retrieval and ingestion to AI agents over Model Context Protocol |
| [Object Store](configuration/object-store.md) | EDP storage backends, and serving documents from NetApp ONTAP S3 |
| [AWS S3 and SQS Setup](configuration/aws-s3.md) | Creating the buckets, queue, and IAM user for external S3 with the AWS CLI |
| [Building Images](configuration/images.md) | Building the component images locally and pointing the deployment at your registry |

## Operate

Watch it and tune it once it is running.

| Guide | What it covers |
|---|---|
| [Telemetry](configuration/telemetry.md) | The RAG Grafana dashboards and where to find logs |
| [Performance](configuration/performance.md) | Per-step resources, replica sizing, autoscaling, and vector-database tuning |

## Look things up

| Guide | What it covers |
|---|---|
| [Architecture](reference/architecture.md) | Components, roles, namespaces, pipeline composition, and request flow |
| [Container Images](reference/container-images.md) | Every image the deployment pulls, with its build context |
| [Service Mesh](reference/service-mesh.md) | How RAG namespaces join the Istio ambient mesh, and the current mTLS posture |
| [Glossary](reference/glossary.md) | Every term used in these guides, defined once |

## When something fails

| Guide | What it covers |
|---|---|
| [FAQ](faq-and-troubleshooting/frequently-asked-questions.md) | Short answers to the questions that come up most |
| [Troubleshooting](faq-and-troubleshooting/troubleshooting.md) | Common symptoms, their causes, and the debug tool |

## User guides

Feature and usage walkthroughs for each app, with screenshots. They are the PDFs at the `docs/` root; the apps' help links point there, so they don't move.

| Guide | App |
|---|---|
| [AudioQnA User Guide](Intel_Chatbot_Toolkit_AudioQnA_User_Guide.pdf) | Voice question answering |
| [ChatQnA User Guide](Intel_Chatbot_Toolkit_ChatQnA_User_Guide.pdf) | Conversational retrieval |
| [DocSum User Guide](Intel_Chatbot_Toolkit_DocSum_User_Guide.pdf) | Document summarization |

## Contribute

| Guide | What it covers |
|---|---|
| [Contributing](../CONTRIBUTING.md) | Reporting a problem or sending a change |
| [Pipelines reference](../deployment/pipelines/README.md) | Steps, variants and the composer, for adding a pipeline |
