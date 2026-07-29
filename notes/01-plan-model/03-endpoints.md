flowchart TD
    A[Application Layer] --> B[Select SDK]
    B --> C[Authentication]
    C --> D[Chat API]
    D --> E[Endpoint]
    E --> F[Model & Response]

    subgraph Application
        A1[Web]
        A2[Mobile]
        A3[Scripts]
    end
    A --> Application

    subgraph Select SDK
        B1[Foundry SDK]
        B2[OpenAI SDK]
    end
    B --> Select SDK

    subgraph Authentication
        C1[Entra ID]
        C2[API Key / Token]
    end
    C --> Authentication

    subgraph Chat API
        D1[Responses API]
        D2[ChatCompletions API]
    end
    D --> Chat API

    subgraph Endpoint
        E1[Project Endpoint - Agents & Data]
        E2[Azure OpenAI Endpoint - Model Inference]
    end
    E --> Endpoint
