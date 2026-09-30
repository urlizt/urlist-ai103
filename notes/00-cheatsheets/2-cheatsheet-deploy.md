# AI-103 Module 2 Cheatsheet: Implement generative AI and agentic solutions



## 1. Module Weight & Strategic Priority
- **Implement generative AI and agentic solutions: 30–35%** (largest module on the exam).
- Roughly a third of the exam; with Module 1 (25–30%) it is about 60% of your score, so a weak spot here is hard to recover from.

## 2. High-Level Skills Measured
- **Build generative applications by using Foundry**
  - Deploy/consume LLMs, small, code and multimodal models
  - RAG in an app; workflows, tool-augmented flows, multistep pipelines
  - Evaluate: fabrication (groundedness), relevance, quality, safety
  - Foundry SDKs/connectors; connect an app to a Foundry project
- **Build agents by using Foundry**
  - Roles, goals, conversation tracking, tool schemas
  - Retrieval + function calling + conversation memory
  - Tools: APIs, knowledge stores, search, Content Understanding, custom functions
  - Orchestrated multi-agent solutions
  - Autonomous/semi-autonomous workflows with approval controls
  - Monitoring, agent evaluation, error analysis
- **Optimize and operationalize generative AI systems**
  - Prompt engineering, model parameters
  - Reflection, chain-of-thought evaluation, self-critique loops
  - Observability: tracing, token analytics, safety signals, latency
  - Orchestrate multiple models/flows, hybrid LLM + rules
- **Preview vs GA (from your notes):** ⚠️ Work IQ = **Preview**; "some" Foundry tools are preview (notes don't say which); publish endpoint uses `api-version=2025-11-15-preview`. Study guide: preview features appear only if commonly used.
> [!IMPORTANT]
> **Coverage gap in your notes** (study-guide skills with **no** notes): evaluation (groundedness/relevance/safety evaluators), tracing/token analytics/observability, prompt engineering + parameter tuning depth, reflection/self-critique loops, conversation memory/context providers, hybrid LLM + rules, RAG-in-app code. **Notes with weak study-guide match** (lower priority): Work IQ, M365 publishing detail, A2A.

## 3. Revision Snapshot

### Agent types (Foundry Agent Service)
| Type | Defined by | Control | Use for |
|---|---|---|---|
| **Prompt agent** (declarative) | Config: model + instructions + tools | Medium | Fast prototyping |
| **Workflow agent** (declarative) | Multi-agent YAML / visual canvas | Medium | Orchestration without code |
| **Hosted agent** | Container + your code (**MAF** recommended) | Full | Custom logic |

### Portal vs VS Code
| | Portal | VS Code extension |
|---|---|---|
| Style | Visual, no-code | Code-first, YAML + Agent Designer (auto-synced) |
| Best | Prototyping, stakeholders | Git, bulk edits, templates, CI |

### Tools
| Tool | Purpose |
|---|---|
| **Code Interpreter** | Sandboxed Python (analysis, charts) |
| **File Search** | RAG over **uploaded files in a vector store** |
| **Azure AI Search** | Enterprise **existing index** |
| **Bing grounding / Web Search** | Live web |
| **OpenAPI** | REST APIs via OpenAPI spec; auth: anonymous / API key / managed identity |
| **Azure Functions** | Serverless; queue-triggered (input + output storage queue bindings) |
| **Function calling** | You define schema; **your code runs the function** |
| **MCP** | Protocol-based tool server; dynamic discovery |
| **Agent-to-Agent, SharePoint, Fabric, Deep Research, Computer Use, Browser Automation, Image Gen** | Additional catalog tools |
| **Logic Apps** | Low-code workflow tool |

- **Flow for any custom tool:** create function/spec → create tool object → attach via `tools=[...]` on the agent.
- More tools = more latency. Start with built-in. Tell the agent **when/how** to use each tool.

### MCP
- Client flow: server hosts `@mcp.tool` → client `list_tools()` → wrap as async funcs → `FunctionTool` → register on agent.
- Benefits: dynamic discovery, add/update tools **without redeploying** the agent, interoperability, standard auth.
- **Approval:** `always` (**default**) or `never`. If approval needed → response contains `mcp_approval_request` → you reply with `mcp_approval_response` (`approval_request_id` + `approve`).

### Foundry IQ (knowledge)
- Managed knowledge layer on **Azure AI Search**; agents connect via **MCP**; **one KB shared by many agents**, update once, all benefit.
- Add source flow: **Discover → Process (chunk + embed) → Index → Monitor** (auto reindex).
- RAG gives: **real-time updates, source transparency, factual grounding**.
- Good retrieval instructions = **always search, never use training data, exact citation format, fallback message**.
- Improve retrieval: **scoring profiles, semantic ranking, custom analyzers**.
- Evaluate: **grounding, citation, relevance, completeness**. Monitor: citation freq, fallback freq, query types, retrieval accuracy.

| Source | Access | Pick when |
|---|---|---|
| SharePoint **Remote** | Real-time | Simple, always current, M365 governance |
| SharePoint **Indexed** | Indexed | Advanced search / custom pipeline |
| Blob Storage | Direct | Files in Azure |
| OneLake | Direct | Fabric lakehouse |
| AI Search index | Indexed | Existing index |
| Web | Real-time | Public current info (Bing) |

### Deploy → Publish
- **Deploy** = internal (project). **Publish** = **Agent Application**: stable endpoint, **own Entra identity**, version updates don't change endpoint.
- Endpoint auth: **Entra ID only, no API keys**; caller needs RBAC role. **403 = missing RBAC**.
- ⚠️ **New identity → reassign RBAC** for tools/resources or tool calls fail after publishing.
- Endpoint is **stateless** → store conversation history client-side.
- **M365 publish:** portal (basic) vs **M365 Agents Toolkit** (advanced: custom SSO, middleware, CI/CD; `Teams/Copilot → Proxy App → Foundry Agent`).
- Scopes: **Shared** (instant, testing) vs **Organization** (admin approval, production).
- Prereqs: **Azure AI Project Manager** (project), **Azure AI User** (agent application), `Microsoft.BotService` provider registered, tenant allows custom apps.
- Publishing creates an **Azure Bot Service** resource.

### Foundry Workflows (visual)
- Patterns: **Sequential, Human-in-the-loop, Group chat**.
- Nodes: **Invoke** (agent), **Flow** (If/Else, Go To, For Each), **Data transformation** (Set/Reset Variable, Parse value), **Basic chat**, **End**.
- **Power Fx** formulas; variables = shared state; agents reusable across workflows.
- Code: `AIProjectClient` → create conversation → invoke workflow **by name** → stream events.

### Microsoft Agent Framework (MAF)
- Successor to **Semantic Kernel + AutoGen**. Code-first; recommended orchestration for **Hosted agents**. **Agent = reasons dynamically; Workflow = defines the process.**
- Blocks: model clients, **AgentSession**, context providers (memory), function tools, MCP clients, middleware, workflow orchestration.
- **Foundry = service-side history** (survives restarts); other providers = local in-memory history.
- Providers swappable (Foundry, Azure OpenAI, OpenAI, Anthropic, Bedrock, Ollama…), only client config changes.
- Auth: `DefaultAzureCredential` (CLI in dev, managed identity in prod). **No API keys.**
- Workflow parts: **Executors** (work), **Edges** (flow: direct, conditional, switch-case, fan-out, fan-in), **Events** (observability).
- Events: `WorkflowStartedEvent`, `WorkflowOutputEvent`, `WorkflowErrorEvent`, `ExecutorInvokeEvent`, `ExecutorCompleteEvent`, `RequestInfoEvent`.

### Orchestration patterns
| Pattern | Builder | Mental model | Exam clue |
|---|---|---|---|
| **Concurrent** | `ConcurrentBuilder` | Everyone at once | "Run several agents at the same time" |
| **Sequential** | `SequentialBuilder` | Pipeline | "Each builds on previous output" |
| **Group chat** | `GroupChatBuilder` | Managed discussion (human optional), **maker-checker** | "Manager controls who speaks next" |
| **Handoff** | (handoff) | Agent passes the baton | "**Agent** decides which specialist next" |
| **Magentic** | `MagenticBuilder` | Manager plans/replans, **task ledger** | "Open-ended, path unknown" |

- **Group chat manager call order:** `should_request_user_input` → `should_terminate` → `filter_results` (if ending) → `select_next_agent` (if continuing).
- Steps: chat client → define agents → build workflow → run → process outputs → extract final conversation.

### A2A
- **A2A = agent ↔ agent communication. MCP = agent ↔ tools.**
- **Agent Skill** (ID, name, description, tags, examples, I/O) · **Agent Card** (identity, endpoint, features, I/O modes, skills, auth) · **Agent Executor** (bridge: `execute`, `cancel`).
- Card at `/.well-known/agent-card.json`. Client: fetch card → init with base URL → send.
- Request: non-streaming (single response) vs streaming (incremental, async). Response: direct message vs **task object**.

### Security risks
- Leakage, **prompt injection**, unauthorized access, data poisoning, supply chain, autonomy errors, weak logging, model inversion.
- Mitigate: **RBAC, prompt filtering, sandboxing, logging, dependency audits, model validation**.

## 4. Code & API Call Reference
| Item | Purpose | Example Call / Value |
|---|---|---|
| `AIProjectClient` | Connect to Foundry project | `AIProjectClient(endpoint=..., credential=DefaultAzureCredential())` |
| `project_client.agents.create_version()` | Create agent version | `create_version(agent_name="x", definition=PromptAgentDefinition(model=, instructions=, tools=))` |
| `PromptAgentDefinition` | Declarative agent def | `model="gpt-4.1"`, `instructions="..."`, `tools=[...]` |
| `FunctionTool` | Function calling schema | `FunctionTool(name=, parameters={...}, description=, strict=True)` |
| `"additionalProperties": False` | Required with `strict=True` | inside `parameters` |
| `AzureFunctionTool` | Queue-triggered Azure Function | `AzureFunctionDefinition(input_binding=, output_binding=, function=)` |
| `AzureFunctionStorageQueue` | Queue binding | `queue_name`, `queue_service_endpoint` |
| `OpenApiTool` | OpenAPI tool | `OpenApiTool(openapi=OpenApiFunctionDefinition(name=, spec=, description=, auth=OpenApiAnonymousAuthDetails()))` |
| `jsonref.loads()` | Load spec file | `jsonref.loads(f.read())` |
| `MCPTool` | Remote MCP server | `MCPTool(server_label="github", server_url="https://api.githubcopilot.com/mcp/")` |
| `allowed_tools` | Limit MCP tools | `allowed_tools=["list_pull_requests"]` |
| `require_approval` | MCP approval mode | `"always"` (default) / `"never"` |
| `mcp_approval_request` / `mcp_approval_response` | Approval handshake | response has `approval_request_id` + `approve` |
| Foundry IQ KB URL | KB as MCP tool | `f"{search_endpoint}/knowledgebases/<kb-name>/mcp"` |
| `openai_client.responses.create()` | Call agent | `conversation=conversation.id, input="...", extra_body={"agent": {"name": agent.name, "type": "agent_reference"}}` |
| `response.output_text` | Read reply | `print(response.output_text)` |
| YAML `tools:` | Add tools in VS Code | `- type: code_interpreter` · `- type: bing_grounding` (`connection_id`) · `- type: file_search` (`vector_store_ids`) |
| Model params | Behaviour | `temperature` (randomness), `top_p` (diversity, default 1.0) |
| Published endpoint | Agent Application | `https://<resource>.services.ai.azure.com/api/projects/<proj>/applications/<app>/protocols/openai/responses?api-version=2025-11-15-preview` |
| Get token | Entra auth | `az account get-access-token --resource https://ai.azure.com` |
| `Authorization` header | Call endpoint | `Bearer <access-token>` (**no API key**) |
| `FastMCP("name")` | Build MCP server | `mcp = FastMCP("server-name")` |
| `@mcp.tool` | Expose tool | Schema from type hints + docstring |
| `session.list_tools()` / `session.call_tool(name, args)` | MCP client discover / invoke | wrap in async funcs |
| Workflow stream events | Foundry workflows | `response.completed` (workflow done), `response.output_item.done` (action done) |
| Power Fx | Workflow logic | `If(Local.Confidence > 0.8, "Proceed", "Escalate")`, `IsBlank()`, `IsEmpty()`, `ForAll()`, `Sum()`, `Count()`, `Concatenate()` |
| `AzureOpenAIChatClient` | MAF chat client | create client, then `create_agent` |
| `DefaultAzureCredential` | MAF/SDK auth | CLI (dev) / managed identity (prod) |
| `ConcurrentBuilder` / `SequentialBuilder` / `GroupChatBuilder` / `MagenticBuilder` | MAF orchestration | `.participants([...]).build()` |
| `run` vs `run_stream` | Non-streaming vs streaming | `get_outputs()` vs iterate `WorkflowOutputEvent` |
| `approval_mode` | MAF tool approval | on the tool decorator |
| `@tool` decorator / Annotated types / Pydantic | MAF tool schemas | explicit name + description |
| Agent as tool | MAF composition | one agent wrapped as a tool for another |
| Agent Card path | A2A discovery | `/.well-known/agent-card.json` |
| Work IQ | M365 data via CLI/MCP | `npm i -g @microsoft/workiq` · `workiq ask -q "..."` · `npx -y @microsoft/workiq mcp` · `workiq accept-eula` |

## 5. Important Distinctions & Exam Focus
- **Prompt vs Workflow vs Hosted agent** — config single agent / multi-agent orchestration / container with your code.
- **Declarative vs Hosted** — config-based (medium control) vs container-based (full control).
- **Agent vs Workflow** — agent decides dynamically; workflow defines the process.
- **Deploy vs Publish** — internal project availability vs external stable endpoint with own identity.
- **File Search vs Azure AI Search** — uploaded docs in vector store vs existing enterprise index.
- **File Search vs Code Interpreter** — retrieval (RAG) vs run Python.
- **Bing vs Azure AI Search** — live public web vs private indexed content.
- **Function calling vs Azure Function vs OpenAPI vs MCP** — your code / serverless queue-triggered / REST spec / protocol server with dynamic discovery.
- **MCP vs A2A** — agent-to-tool vs agent-to-agent.
- **MCP server vs client** — hosts/registers tools vs discovers/wraps/invokes them.
- **Foundry IQ vs Work IQ** — what the org knows (KB on AI Search) vs M365 Copilot data (CLI + MCP server).
- **SharePoint Remote vs Indexed** — real-time/simple vs indexed/custom pipeline.
- **Foundry portal publish vs M365 Agents Toolkit** — basic vs advanced (SSO, middleware, CI/CD proxy).
- **Shared vs Organization scope** — testing/no approval vs production/admin approval.
- **Sequential vs Handoff** — workflow fixes order vs agent picks next.
- **Group chat vs Magentic** — manager selects speaker in discussion vs manager plans via task ledger.
- **Concurrent vs Sequential** — parallel independent vs dependent pipeline.
- **Foundry workflows vs MAF workflows** — visual/declarative vs code-first (direction of travel: MAF).
- **Service-side vs local history** — Foundry persists; other providers in-memory.
- **`run` vs `run_stream`** — full result vs incremental.
- **Streaming vs non-streaming (A2A)** — incremental async vs single response.
- **Temperature vs Top-P** — randomness vs vocabulary diversity.
- **Designer vs YAML** — visual vs code; **auto-synced**.

## 6. Likely Exam Traps
- ⚠️ **Published agent = new identity**; dev permissions do **not** carry over → tools fail with auth errors. **Fix: reassign RBAC to agent identity.**
- ⚠️ Published endpoint = **Entra ID only, no API keys**. **403** → missing RBAC.
- Endpoint is **stateless**; client stores history.
- ⚠️ MCP `require_approval` **default = `always`**.
- MCP tools are **discovered dynamically**; adding tools needs **no agent redeploy**.
- `allowed_tools` restricts which MCP tools the agent may use.
- Vague instruction ("use the knowledge base") = inconsistent; must say **always search, never own knowledge, citation format, fallback**.
- Answers without citations = **not acceptable** for enterprise grounding.
- File Search ≠ Azure AI Search.
- **Temperature = randomness**, not "creativity mode".
- More tools = more latency; **start with built-in**.
- **Prompt injection is not solved by model choice alone.**
- `Microsoft.BotService` provider must be registered before M365 publishing.
- Org-scope M365 publish needs **admin approval**; users find it under "Built by your org".
- Work IQ: **Preview**, needs EULA accept, **admin consent in Entra**, respects user's existing permissions, stores no data.
- Foundry IQ **data quality** decides retrieval quality.
- Foundry portal is a poor fit when you need SSO/middleware → **Agents Toolkit**.
- Group chat manager: **order of method calls** is testable.
- MAF replaces **Semantic Kernel/AutoGen** ("next-gen").
- **MAF Foundry = service-side history**; local providers lose state on restart.
- Tool approval in MAF = `approval_mode`; in Foundry MCP = `require_approval`. Different APIs.
- Workflows: **Invoke** node can call an existing agent **or create a new one**.
- A2A **Agent Executor** is the bridge, not the client; `cancel` is optional.

> **Conflict 1: MCP `require_approval` type.** Notes 2.3 say string `"always"`/`"never"` in Key Terms but **boolean** in the "How to enable" section. Also written as `mcp_require_approval` vs `require_approval`. **Use the string form (`"always"`/`"never"`, default `"always"`)**; verify the parameter name in the SDK docs.
>
> **Conflict 2: Function calling "never manually invoke".** Notes 2.2 say you never call tools directly. That holds for service-executed tools (OpenAPI, Azure Function, MCP, built-ins). For **`FunctionTool`**, the model only *requests* the call; **your app runs the function and returns the result**. Verify in the docs before the exam.
>
> **Conflict 3: OpenAPI version.** Notes say "OpenAPI **3.0** specs" but the example spec is `"openapi": "3.1.0"`. Check which the docs require.
>
> **Conflict 4: "Tools must be added before deployment"** (notes 2.1 trap). Sounds too strict: agents are versioned via `create_version`, so tools can change in a new version. Treat as unverified.
>
> **Conflict 5: `create_version` params.** Snowfall example uses `name=`; others use `agent_name=`. Likely a typo in the notes; verify.
>
> **Conflict 6: MAF API names.** Notes mix `AgentSession`, `AzureOpenAIChatClient`, `run_stream`, `create_agent`. MAF is fast-moving and names have changed between releases; confirm against current docs.

## 7. Quick Recall Table
| Scenario | Correct Choice | Why |
|---|---|---|
| Q&A over PDFs users upload | **File Search** (vector store) | RAG over uploaded files |
| Query existing enterprise index | **Azure AI Search tool** | Already indexed |
| Latest public news | **Bing grounding / Web Search** | Live web |
| Charts / data analysis | **Code Interpreter** | Sandboxed Python |
| Same KB for many agents | **Foundry IQ** | Shared knowledge layer |
| Live SharePoint, simple setup | **SharePoint Remote** | Real-time, M365 governance |
| SharePoint with custom pipeline | **SharePoint Indexed** | Advanced search |
| Fabric lakehouse content | **OneLake** | Direct access |
| Call REST API with a spec | **OpenAPI tool** | Standard spec |
| Existing serverless backend | **Azure Functions tool** | Queue-triggered |
| Your own business logic in agent code | **Function calling** | You execute it |
| Tools change often, no redeploy | **MCP** | Dynamic discovery |
| Human sign-off before a tool call | **MCP `require_approval="always"`** (MAF: `approval_mode`) | Approval flow |
| Restrict which MCP tools | **`allowed_tools`** | Least privilege |
| Quick prototype / stakeholder review | **Foundry portal** | Visual, no-code |
| Git, bulk edits, templates | **VS Code YAML** | Code-first |
| Full code control, custom logic | **Hosted agent + MAF** | Container |
| Fixed step-by-step pipeline | **Sequential** | Ordered |
| Independent parallel opinions | **Concurrent** | Fan-out/fan-in |
| Debate / maker-checker / human in chat | **Group chat** | Manager selects speaker |
| Route to specialist dynamically | **Handoff** | Agent decides next |
| Open-ended, needs planning | **Magentic** | Task ledger, replanning |
| Approval or missing info mid-flow | **Human-in-the-loop workflow** | Pauses for input |
| Agents from different vendors talk | **A2A** | Standard protocol |
| Discover another agent's capabilities | **Agent Card** `/.well-known/agent-card.json` | Digital business card |
| Long-running remote agent task | **A2A streaming / task object** | Incremental |
| Publish to Teams/Copilot quickly | **Foundry portal publish** | Guided |
| Custom SSO / middleware / CI/CD | **M365 Agents Toolkit** proxy | Advanced |
| Test in Teams only | **Shared scope** | No admin approval |
| Tenant-wide production | **Organization scope** | Admin approval |
| Tools work in Foundry, fail after publish | **Reassign RBAC to agent identity** | New Entra identity |
| Agent doesn't reply in Teams | **Check Bot Service + logs** | Common cause |
| Ask M365 meetings/docs from terminal | **Work IQ CLI** | Copilot data |
| Trace/latency/token metrics | **Foundry metrics + App Insights** | Observability |

## Quick Exam Memory Block

```text
Use RAG when the model needs trusted or current knowledge.
Use fine-tuning when the model needs specialised behaviour or format.
Use tools when the model needs data or actions outside itself.
Use agents when the solution needs reasoning plus tool use across steps.
Keep agents narrow, secured, monitored, and auditable.
Use human approval for sensitive actions.
Use evaluation to check quality, relevance, groundedness, and safety.
Choose orchestration by control flow:
sequential = ordered stages
concurrent = parallel work
handoff = specialist transfer
group chat = shared collaboration
magentic = dynamic manager
```
