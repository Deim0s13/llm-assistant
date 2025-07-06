# 🗄️ Prompt-Building Flow with Memory

```mermaid
flowchart TB
    subgraph Settings
        A1[settings.json] -->|memory.enabled| C
        A2 -->|context.max_history_turns| C
    end
    subgraph Runtime
        B1[current user message] --> C
        B2[live chat history] --> C
        B3[🔁 Memory store<br>(utils.memory)] --> C
    end
    subgraph prepare_context()
        C[Assemble & trim<br>prompt context] --> D[Model generate()]
    end

C -->|out| E[Assistant reply]
E -.->|save()| B3
