# AI-103 Module 4 Cheatsheet: Vision, Video, Content Understanding, Document Intelligence, AI Search

## 1. Module Weight & Strategic Priority
- Your Module 4 notes span **two** exam domains:
  - **Implement computer vision solutions: 10–15%** → notes 4.1–4.5
  - **Implement information extraction solutions: 10–15%** → notes 4.6–4.8 (plus Content Understanding from 4.4/4.5)
- Combined **20–30%**, about the same as Module 1 (25–30%) but less than Module 2 (30–35%). Individually each domain is a small slice, so **breadth of service-selection questions** matters more than depth.

## 2. High-Level Skills Measured
**Computer vision (10–15%)**
- Image generation from text and reference media; video generation from text/reference media
- Image-editing workflows (inpainting, mask-based edits, prompt edits); editing generated videos
- Multimodal understanding: captions (concise/detailed, multi-image), visual Q&A grounded in evidence, alt-text
- **Content Understanding** for visual characteristics; **single-task vs pro-mode** pipelines
- Video analysis; identify objects/components/regions in images or video
- Responsible AI for multimodal: unsafe visual filters, **indirect prompt injection via text in images**, visual policy (watermarks, prohibited symbols, brand rules)

**Information extraction (10–15%)**
- Ingest/index documents, images, audio, video
- **Semantic, hybrid, vector search** for grounding
- Enrichment with custom/built-in skills (text, images, layout)
- RAG ingestion flow incl. **OCR**; connect retrieval to workflows and agent tools
- Multimodal extraction (OCR + layout + fields); clean grounded output for agents/RAG via **Content Understanding**; analyzers for structured/markdown output

**Preview vs GA:** your notes don't flag any. Notes claim **DALL-E 3 retired March 4, 2026**; `gpt-image-1/2` current.

> **Coverage gaps previously flagged (now addressed in this cheatsheet):**
> - AI Search vector, hybrid, semantic search and integrated vectorization
> - Image editing (inpainting, masks, `images.edit`) and reference-media image generation
> - Content Understanding pro mode vs single-task
> - Alt-text/accessibility captions, object/region detection
> - Responsible AI for multimodal (prompt injection in images, visual policy rules)
> - Connecting retrieval to agents/workflows (Foundry IQ from Module 2 is the link)
>
> These are now covered in sections 3–7 below.

## 3. Revision Snapshot

### Which service for which job
| Need | Service |
|---|---|
| Understand images + text (Q&A, reasoning over charts) | **Multimodal model**: `gpt-4.1`, `gpt-4.1-mini`, `Phi-4-multimodal-instruct` |
| Create images from text | **GPT-image**: `gpt-image-1`, `gpt-image-2`; also `FLUX.1-Kontext-pro` |
| Edit images (inpainting, masks) | **GPT-image** via `images.edit()` |
| Create video | **Sora 2 / Sora 2 Pro** |
| Unstructured (doc/image/audio/video) → structured fields, JSON/markdown | **Content Understanding** |
| Forms/invoices/receipts, OCR + layout + fields | **Document Intelligence** |
| Index, enrich, search, RAG grounding, knowledge mining | **Azure AI Search** |
| Semantic similarity search | Embedding model (`text-embedding-3-large`), not a chat model |

### Vision chat
- Multimodal user message = **multi-part** (text + image). Image as **web URL** or **Base64 data URL**.
- Test in Foundry **Chat playground**.

### Image generation
- Text → image; **GPT-image returns Base64**. Higher `quality` = more cost/time.
- **Content filter can block** prompts/outputs; app must handle policy errors.
- Prefer **Entra ID/keyless** auth; never hard-code keys.
- Playground: Foundry **Images playground** (gives Python + cURL code).

### Image Editing (Inpainting, Masks, Prompt Edits)
- **Inpainting**: model takes an original image + a **mask** (an image that marks the region to edit) + prompt. The mask area is regenerated; the rest is preserved.
- **Outpainting**: extend beyond the original canvas.
- **Compositing**: combine elements using mask-guided edits.
- API: `client.images.edit()` — parameters: `image` (string or array, required), `mask` (string, optional), `prompt`, `model`, `n`, `size`, `quality`, `output_format`, `output_compression`, `background`.
- Mask format: PNG, **same dimensions** as the original image.
- `background` values: `transparent`, `opaque`, `auto`. If `transparent`, `output_format` must be `png` (default) or `webp`.
- Editing uses **GPT-image-1 series** models.
- Reference-media image generation: provide reference image(s) alongside prompt to condition output on visual input.

### Sora 2 (video)
- Modes: **text→video, image→video, remix, audio in output**.
- Sizes: `1280x720` (landscape), `720x1280` (portrait). Durations: **4 / 8 / 12 s**.
- **Async: Create → Poll → Download.** Download only when `completed`; available **24 hours**.
- Reference image: JPEG/PNG/WebP, **must match target resolution**, **faces rejected**.
- Job states: `queued`, `in_progress`, `completed`, `failed`, `cancelled`.
- **Remix**: use `videos.remix()` with an existing video ID + focused prompt. (Notes also show `remix_video_id` as a `create()` parameter — confirm against current docs; safe recall is “existing video ID + focused prompt”.)

### Alt-Text and Accessibility Captions
- **Alt text** = HTML attribute on `<img>` tags; describes image content in plain text.
- Improves accessibility for screen readers (Microsoft Narrator, JAWS, NVDA) and image SEO.
- **Azure AI Vision Image Analysis** offers captioning models that generate one-sentence descriptions — usable as AI-generated alt text.
- Microsoft products (PowerPoint, Word, Edge) use Image Analysis captions to generate alt text.
- **Confidence threshold**: advised **0.4** — only accept captions above this level for accurate alt text.
- Image Analysis 4.0 is deprecated; retirement **25 September 2028**. Migrate to available alternatives.

### Content Understanding (CU)
- Foundry Tool: docs, images, audio, video → structured output (**Markdown for search/RAG, JSON fields for automation**).
- **Analyzer** = how content is processed. **Schema** = fields wanted.
- Prebuilt: `prebuilt-image`, `prebuilt-receipt`, `prebuilt-invoice`, `prebuilt-idDocument`. Custom: own `fieldSchema`, `baseAnalyzerId`.
- Field `method`: **extract** (find existing), **classify** (predefined categories), **generate** (produce from analysis).
- Result: `fields` (value + **confidence 0–1** + **source/grounding**), `markdown`, metadata, OCR/layout.
- Confidence guide: **≥0.9 automate · 0.7–0.9 consider review · <0.7 manual verify**.
- **Content Understanding Studio** = build/test/refine analyzers, create versions.
- Needs deployed models: **GPT-4.1, GPT-4.1-mini, text-embedding-3-large**.
- **Analysis is async** (create analyzer too): operation ID/poller.

### Content Understanding: Pro Mode vs Single-Task (Standard) Mode
| Feature | Single-Task (Standard) | Pro Mode |
|---|---|---|
| Complexity | Low | High |
| Cost | Lower | Higher |
| Latency | Faster | Slower |
| Contextual understanding | Limited | Advanced (multi-step reasoning) |
| Workflow orchestration | Minimal | Extensive |
| Multi-file input | No (single file) | **Yes** — multiple documents simultaneously |
| External knowledge bases | No | **Yes** — linking, enrichment, validation |
| Use cases | Straightforward field extraction from one file | Contract validation, inconsistency detection, complex reasoning across files |

- Default: all analyzers operate in **standard mode** unless pro is configured.
- Pro mode is designed for advanced scenarios requiring **multi-step reasoning and cross-file analysis**.

### Responsible AI for Multimodal: Indirect Prompt Injection via Text in Images
- **Prompt injection**: malicious instructions that manipulate model behaviour (override system instructions, extract data, bypass safeguards).
- **Direct injection**: attacker types malicious text directly into the prompt.
- **Indirect injection**: malicious instruction is **hidden inside external content** the AI processes — web pages, documents, PDFs, emails, **images**, screenshots, videos.
- **Why images are dangerous**: multimodal models can OCR text from images, interpret screenshots, understand diagrams, process video frames. Attackers hide instructions in images (backgrounds, tiny fonts, low-contrast text, subtitles, signage in frames).
- **OCR risk**: OCR extracts text from images → extracted text is sent to LLM → LLM interprets it as instructions → executes unintended behaviour.
- **Azure AI Content Safety** — protection:
  - **Prompt Shields**: detects and blocks both direct user prompt attacks and **indirect attacks** embedded in documents or images.
  - **Multimodal API** (`imageWithText`): analyses text and images **together**, not in silos, using the Florence foundation model to detect nuanced harm.
  - **OCR-then-classify** architectural pattern: run OCR on every inbound image and route extracted text through the same injection/content classifiers as typed input.
- **Defence pattern**: treat all text extracted from images/video as untrusted input — never pass directly to the model without classification.
- **Visual policy** (from study guide): watermarks, prohibited symbols, brand rules.

### Document Intelligence (DI)
- OCR + deep learning: text (incl. handwriting), key-value pairs, tables, selection marks, structure, bounding boxes.
- **Read** = text/handwriting/language. **Layout** = Read + tables + selection marks + structure. *(Note: in newer DI versions, key-value extraction may be a separate feature/add-on rather than part of Layout — verify.)*
- **Prebuilt** = no training (invoice, receipt, ID, bank statement, check, pay stub, contract, tax, mortgage…). **Try prebuilt first.**
- **Custom template** = fixed layout, fast/cheap. **Custom neural** = varying layouts, slower/costlier.
- **Custom classifier** = identifies doc type. **Composed model** = combines custom models and routes to the right one.
- Studio: label → train → test. Start with **≥5–6 sample forms**.
- **Authentication**: exam favours **keyless** (`DefaultAzureCredential` / managed identity). The older `DocumentAnalysisClient` + `AzureKeyCredential` shown in notes is Form Recognizer-style; newer SDKs support keyless and different client names.

### Azure AI Search
- Pipeline: **Data source → Indexer → document cracking → skillset (enrichment) → index → search**; optional **knowledge store**.
- **Index ≠ original data**: searchable JSON with extracted/generated fields.
- Built-in skills: language, OCR, entities, key phrases, translation, PII, image captions/tags. **Custom skill** = often Azure Function (e.g., call Document Intelligence).
- Field attributes: **key, searchable, filterable, sortable, facetable, retrievable**.
- Query: **simple** vs **full Lucene** (regex, advanced). `$filter` (OData), `$orderby`, `facet`.
- **Knowledge store projections: objects (JSON), tables, files (images)** for analytics/ETL/reuse.

### AI Search: Vector, Hybrid, Semantic Search & Integrated Vectorization
*(Biggest gap — study guide lists these explicitly under grounding)*

**Vector search**
- Stores numerical embeddings; query is vectorized and matched by similarity (kNN).
- Algorithms: **HNSW** (Hierarchical Navigable Small World — fast approximate, best for most scenarios) vs **exhaustive KNN** (brute-force scan, more accurate but slower).
- HNSW params: `efSearch` (query-time efficiency/accuracy, default 500), `efConstruction` (index-time neighbours), `m` (bi-directional links, 4–10).
- Vector fields: must be **searchable** and **retrievable**, but **cannot** be filterable, sortable, or facetable.
- Metrics: cosine, dotProduct, euclidean.

**Hybrid search**
- Combines **keyword (full-text) + vector** queries in a single request.
- Both queries execute **in parallel**.
- Results merged and reordered using **Reciprocal Rank Fusion (RRF)** — automatically applied by AI Search on hybrid queries.
- Hybrid + **semantic ranking** outperforms pure vector search for queries with named entities / exact phrases (per Microsoft benchmarks).

**Semantic search (semantic ranker)**
- Query-side feature that re-ranks initial BM25 or RRF results using Microsoft language understanding models.
- Extends the query execution pipeline in three ways (L1/L2/L3 ranking).
- Returns `@search.rerankerScore` (0.00–4.00) alongside `@search.score`.
- Set `queryType: "semantic"` and a `semanticConfigurationName` in the query.
- In hybrid semantic queries, filters and semantic ranking apply to **text content only**, not to vectors.

**Integrated vectorization**
- Adds **data chunking + text-to-vector embedding** to skills in indexer-based indexing — skips writing chunking/embedding pipeline code.
- Skillset flow: **Text Split skill** (or Document Layout skill) for chunking → **Azure OpenAI Embedding skill** (`#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill`) or **Azure Vision multimodal embedding skill** (`#Microsoft.Skills.Vision.VectorizeSkill`, preview) for vectorization.
- Chunking properties: `method` (semantic/fixed), `unit` (tokens), `maximumLength` (e.g. 500).
- `dimensions` must match the embedding model output.
- Requires an index with vector fields + vector search configuration (`vectorSearch` section in index definition).
- **Foundry IQ** (Module 2) is built on top of AI Search as the managed knowledge layer for agents.

## 4. Code & API Call Reference
| Item | Purpose | Example Call / Value |
|---|---|---|
| `client.responses.create()` | Vision chat (Responses API) | `model="gpt-4.1", input=[{"role":"user","content":[{"type":"input_text","text":"..."},{"type":"input_image","image_url":data_url}]}]` |
| `client.chat.completions.create()` | Vision chat (Chat Completions) | content types **`text`** and **`image_url`** |
| `developer` role | System-style instructions in Responses | `{"role":"developer","content":"..."}` |
| Base64 data URL | Send local image | `f"data:image/{fmt};base64,{b64}"` (or web URL) |
| `response.output_text` | Read Responses reply | `print(response.output_text)` |
| `AzureOpenAI(...)` | Client for image generation | `client = AzureOpenAI(...)` |
| `client.images.generate()` | Generate image | `model="gpt-image-1", prompt=, size="1024x1024", quality="high", n=1` |
| `client.images.edit()` | Edit image (inpainting) | `model="gpt-image-1", image=open(...), mask=open(...), prompt="..."` |
| Image params | Output control | `quality` low/medium/high · `n` · `output_format` PNG/JPEG · `background` (transparent) · `output_compression` (JPEG) |
| Save image | Decode result | `base64.b64decode(img.data[0].b64_json)` |
| `client.videos.create()` | Start Sora job | `model="sora-2", prompt=, size="1280x720", seconds="4"` |
| `input_reference` | Image → video first frame | image file (JPEG/PNG/WebP) |
| `videos.remix()` | Remix existing video | `client.videos.remix(video_id=..., prompt="...")` (also `remix_video_id` as create param — confirm) |
| `client.videos.retrieve()` | Poll status | `client.videos.retrieve(video.id)` |
| `client.videos.download_content()` | Download | `download_content(video.id, variant="video")` then `.write_to_file("output.mp4")` |
| `pip install azure-ai-contentunderstanding` | CU SDK | Python 3.9+ |
| `ContentUnderstandingClient` | CU client | endpoint + `AzureKeyCredential` or `DefaultAzureCredential` |
| `begin_create_analyzer()` | Create analyzer (async) | `poller = client.begin_create_analyzer(...); poller.result()` |
| `begin_analyze()` | Analyze content (async) | `client.begin_analyze(analyzer_id=, inputs=[AnalysisInput(url=...)])` |
| `poller.result()` | Get final result | `result = poller.result()` |
| Analyzer JSON | Define analyzer | `baseAnalyzerId`, `fieldSchema.fields.<name>.{type, method}`, `models`, `config` |
| `content.fields` | Read extracted fields | each has `type`, `value`, `confidence`, `source` |
| CU REST create | Create analyzer | **PUT** `/contentunderstanding/analyzers/{analyzer}` → `Operation-Location` |
| CU REST analyze | Submit content | **POST** `/contentunderstanding/analyzers/{analyzer}:analyze` (URL) or `:analyzeBinary` (file) → Operation ID |
| CU REST results | Poll results | **GET** `/contentunderstanding/analyzerResults/{operation-id}` |
| `DocumentAnalysisClient` | DI client (legacy) | Prefer **keyless**: `DocumentAnalysisClient(endpoint=, credential=DefaultAzureCredential())` |
| `begin_analyze_document_from_url()` | DI analyze | `task = client.begin_analyze_document_from_url(model_id, formUrl); result = task.result()` |
| AI Search query params | Search | `search`, `queryType` (simple/full/semantic), `searchFields`, `select`, `searchMode`, `$filter`, `$orderby`, `facet` |
| Vector query params | Vector search | `vectorQueries=[{"kind":"vector","vector":[...],"fields":"contentVector","k":5}]` |
| Hybrid query | Keyword + vector | Combine `search` and `vectorQueries` in one request; RRF applied automatically |
| Semantic query | Semantic ranking | `queryType="semantic"`, `semanticConfiguration="my-semantic-config"` → `@search.rerankerScore` |
| Integrated vectorization skills | Chunk + embed | `#Microsoft.Skills.Text.SplitSkill`, `#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill`, `#Microsoft.Skills.Vision.VectorizeSkill` (preview) |
| Vector index config | Define vector search | `vectorSearch: { algorithms: [...], profiles: [...] }` in index definition |
| Field attributes | Index schema | `key`, `searchable`, `filterable`, `sortable`, `facetable`, `retrievable` |
| `$orderby` example | Sort | `last_modified desc` |
| Knowledge store | Persist enrichment | projections: objects / tables / files |
| Prompt Shields | Detect indirect injection | Azure AI Content Safety — `shieldPrompt` API or `imageWithText` multimodal API |

## 5. Important Distinctions & Exam Focus
- **Multimodal model vs embedding model vs text-only model** — sees images+text / finds by meaning (vector search) / text only.
- **Vision (understand) vs GPT-image (create)** — `responses.create` with `input_image` vs `images.generate`.
- **Responses API vs Chat Completions** — `input_text`/`input_image` vs `text`/`image_url`.
- **Image generation vs video generation** — sync-style call returning Base64 vs **async job** (create/retrieve/download).
- **Image generation vs image editing** — `images.generate()` vs `images.edit()` with mask.
- **Inpainting vs outpainting vs compositing** — edit inside mask / extend canvas / combine elements.
- **`input_reference` vs remix** — image as first frame vs modify an existing video (video ID).
- **Content Understanding vs Document Intelligence** — generative multi-modal (docs, images, audio, video) with extract/classify/generate vs OCR/layout/form-specialist for documents with prebuilt/custom models.
- **Content Understanding vs OCR** — CU also classifies and generates; not just text.
- **Analyzer vs schema** — how content is processed vs which fields to output.
- **`extract` vs `classify` vs `generate`** — find / categorize / produce.
- **Confidence vs grounding (source)** — how reliable vs where in the source.
- **`analyze` vs `analyzeBinary`** — URL vs file bytes.
- **Prebuilt vs custom analyzer/model** — common docs, no training vs your fields/layouts.
- **Standard vs pro mode (CU)** — single file, low complexity vs multi-file, advanced reasoning.
- **Read vs Layout** — text vs text + tables/selection marks/structure.
- **Custom template vs custom neural** — fixed layout vs varying layout.
- **Custom classifier vs composed model** — identifies type vs routes to the right extractor.
- **Indexer vs index vs skillset** — pipeline engine / searchable output / enrichment steps.
- **Search index vs knowledge store** — for searching vs for analytics/ETL reuse.
- **Searchable vs filterable vs facetable** — full-text / exact filter / refinement categories.
- **Vector vs hybrid vs semantic search** — pure vector kNN / keyword+vector with RRF / semantic ranker re-ranks.
- **Integrated vectorization vs manual chunking/embedding** — built-in skills vs custom code.
- **Simple vs full (Lucene) query** — basic vs regex/advanced.
- **AI Search vs Document Intelligence** — orchestration/search layer vs specialist extractor called via **custom skill**.
- **Direct vs indirect prompt injection** — user types attack vs hidden in external content (images, docs).
- **OCR-then-classify vs trusting OCR output** — treat extracted text as untrusted, run classifiers.
- **Alt-text vs caption** — HTML attribute for accessibility vs generated description (can be used as alt-text).

## 6. Likely Exam Traps
- ⚠️ **Video and CU analysis are asynchronous.** `create()` / `begin_analyze()` starts work; results come later. Download only when `completed`.
- ⚠️ **Reference image must match target resolution**; **faces rejected**.
- Sora `seconds` allowed: **4, 8, 12 only**; `seconds="4"` is a string in the example.
- **Completed videos expire after 24 hours.**
- **DALL-E 3 retired** (notes: March 4, 2026); answers pointing to it are wrong. Use `gpt-image-*`.
- **Wrong content type per API:** `input_image` (Responses) vs `image_url` (Chat Completions).
- Image generation can be **content-filtered**; don't assume an image is returned.
- **Inpainting mask must be PNG and same dimensions as original image.**
- **`background: transparent` requires `output_format` PNG or WEBP.**
- **`prebuilt-*` ID must match doc type** (receipt vs invoice vs idDocument).
- **CU prebuilt analyzer names vary** between notes 4.4 and 4.6 — verify against current docs.
- CU **needs GPT-4.1, GPT-4.1-mini, text-embedding-3-large deployed** first.
- **Analyzer creation is also async** (`begin_create_analyzer`).
- **Low confidence (<0.7) → human review**, not auto-process.
- CU **Studio** = build/test analyzers; **API/SDK** = run in apps.
- **Pro mode supports multi-file; standard does not.**
- DI: **use prebuilt before custom**; template for fixed layouts, neural for varied.
- DI **classifier only classifies**; it does not extract fields.
- **Layout may not extract key-value pairs in newer DI versions** — verify.
- **DI SDK: prefer keyless (`DefaultAzureCredential`) over `AzureKeyCredential`.**
- **Index is not your source data**; **indexer ≠ skillset**.
- **Filterable ≠ searchable**; a field must be **facetable** to build facets, **sortable** for `$orderby`.
- **Vector fields cannot be filterable, sortable, or facetable.**
- **Hybrid search uses RRF automatically** — no manual merging needed.
- **Semantic ranker returns `@search.rerankerScore` (0–4), not `@search.score`.**
- Knowledge store is **not** a search index.
- Content Understanding is **not** image generation and **not** just OCR.
- **Indirect prompt injection via images** — OCR extracts text, LLM treats it as instructions. Use Prompt Shields / multimodal API / OCR-then-classify.
- **Alt-text confidence threshold: 0.4** — below this, do not use as alt-text.
- Keyless (**Entra ID**) auth preferred; hard-coded API keys are the wrong answer.
- **Sora remix**: notes show both `remix_video_id` and `videos.remix()`. Confirm which the docs use; safe recall is “existing video ID + focused prompt”.

> **Conflict 1: Remix mechanism.** Notes 4.3 show both `remix_video_id` (a `create()` parameter) and `videos.remix()`. Confirm which the docs use for Sora 2; the safe recall is "**existing video ID + focused prompt**".
>
> **Conflict 2: Document Intelligence SDK.** Notes use `DocumentAnalysisClient` + `begin_analyze_document_from_url()` + `AzureKeyCredential`. That is the **older Form Recognizer-style SDK**; newer Document Intelligence SDKs use different client/method names and support **keyless auth** (`DefaultAzureCredential`). Exam favours keyless.
>
> **Conflict 3: Layout and key-value pairs.** Notes list key-value pairs under **Layout**; in newer DI versions key-value extraction is a separate feature/add-on. Verify before relying on it.
>
> **Conflict 4: Prebuilt analyzer names.** Notes 4.4 list `prebuilt-image` etc.; 4.6 uses `baseAnalyzerId: "prebuilt-document"`. CU prebuilt names have been changing across versions; verify.
>
> **Conflict 5: Retirement date.** DALL-E 3 "retired March 4, 2026" is from your notes; the study guide doesn't mention it. Treat as note-only until confirmed.

## 7. Quick Recall Table
| Scenario | Correct Choice | Why |
|---|---|---|
| Describe/reason about an uploaded chart or photo | **Multimodal model** (`gpt-4.1`) + `input_image` | Understands images |
| Semantic search over text | **Embedding model** | Vector search by meaning |
| Generate a product image from text | **`gpt-image-*` + `images.generate()`** | Image creation |
| Edit part of an image (inpainting) | **`images.edit()` + mask** | Mask-guided regeneration |
| Image needs transparent background | **`background`** param | Supported by GPT-image |
| Generate 8-second landscape clip | **Sora 2**, `1280x720`, `seconds="8"` | Supported size/duration |
| Start video from a specific image | **`input_reference`** (match resolution, no faces) | First-frame control |
| Tweak an existing generated video | **Remix** (existing video ID) | Preserves structure |
| Video job not ready yet | **Poll `videos.retrieve()`** until `completed` | Async |
| Extract fields from receipts/invoices/IDs (common types) | **Document Intelligence prebuilt** or **CU prebuilt** | No training |
| Extract from images, audio, video, and docs in one service | **Content Understanding** | Multimodal |
| Field value must be a category (new/used/damaged) | **`classify`** | Predefined values |
| Field value is a description written by the model | **`generate`** | Produced from analysis |
| Need to know *where* a value came from | **Grounding / `source`** | Region in source |
| Value confidence 0.75 | **Human review** | Medium band |
| Custom analyzer design/testing without code | **Content Understanding Studio** | Graphical tool |
| Content is a URL vs file bytes (CU REST) | **`:analyze`** vs **`:analyzeBinary`** | Input type |
| Multi-file analysis with advanced reasoning | **Content Understanding pro mode** | Supports multi-file, orchestration |
| Text + handwriting only | **DI Read** | Text extraction |
| Need tables + selection marks | **DI Layout** | Structure |
| Company forms, same layout | **Custom template** | Fast, cheap |
| Company forms, layouts vary | **Custom neural** | Flexible |
| Mixed incoming document types | **Custom classifier / composed model** | Identify + route |
| Ingest files, run OCR/entities, make searchable | **AI Search indexer + skillset** | Enrichment pipeline |
| Call Document Intelligence during indexing | **Custom skill (Azure Function)** | Extends pipeline |
| Advanced query with regex | **`queryType=full` (Lucene)** | Full syntax |
| Let users narrow results by category | **Facetable field + `facet`** | Refinement UI |
| Reuse enriched data for analytics/Power BI/ETL | **Knowledge store** (objects/tables/files) | Persist beyond index |
| Ground an agent/RAG on enriched content | **AI Search index** (+ CU markdown) | Search + grounding |
| Semantic similarity search over vectors | **Vector search (HNSW)** | kNN over embeddings |
| Combine keyword + vector search | **Hybrid search + RRF** | Best of both, auto-merged |
| Re-rank results with language understanding | **Semantic ranker (`queryType="semantic"`)** | Returns `@search.rerankerScore` |
| Auto-chunk and embed during indexing | **Integrated vectorization skills** | Text Split + Embedding skill |
| Generate alt text for accessibility | **Image Analysis caption + confidence ≥0.4** | Screen reader support |
| Prevent hidden instructions in images | **Prompt Shields / OCR-then-classify** | Indirect prompt injection defence |
| DI authentication | **DefaultAzureCredential (keyless)** | Exam favours keyless |
| Sora remix | **`videos.remix()` with video ID** | Confirm against docs |