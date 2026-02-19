---
name: mermaid
description: Use when user needs diagrams, visualizations, flowcharts, sequence diagrams, ERDs, class diagrams, or mentions Mermaid. Use when documenting system architecture, APIs, database schemas, or processes.
---

# Mermaid

Text-based diagrams that render in Markdown, GitHub, Obsidian, and most documentation platforms.

## Core Rules

1. **Quote all labels** containing special characters or spaces: `A["Node (with parens)"]`
2. **No emojis** in diagrams (compatibility and professionalism)
3. **Use short, descriptive IDs**: `api`, `db`, `userSvc` not `applicationProgrammingInterface`
4. **Use Catppuccin Frappe colors** for all styling (see Quick Color Reference below)

**REQUIRED SUB-SKILL:** Use `std-color-palette-frappe` for complete color palette reference.

## Quick Color Reference (Catppuccin Frappe)

| Purpose | Color | Hex |
|---------|-------|-----|
| Primary/Default | Blue | `#8caaee` |
| Success/Start | Green | `#a6d189` |
| Error/Stop | Red | `#e78284` |
| Warning | Yellow | `#e5c890` |
| Info/Highlight | Teal | `#81c8be` |
| Accent | Peach | `#ef9f76` |
| Text (on dark) | Text | `#c6d0f5` |
| Background | Base | `#303446` |
| Border/Stroke | Surface 1 | `#51576d` |

## Diagram Type Selection

| Need to show | Use | Reference |
|--------------|-----|-----------|
| Process, algorithm, decision tree | Flowchart | `references/flowcharts.md` |
| API flow, temporal interaction | Sequence | `references/sequence-diagrams.md` |
| Domain model, OOP design | Class | `references/class-diagrams.md` |
| Database schema, tables | ERD | `references/erd-diagrams.md` |
| System architecture (multi-level) | C4 | `references/c4-diagrams.md` |
| Styling, themes, config | Advanced | `references/advanced-features.md` |

## Quick Start

### Flowchart

```mermaid
flowchart TD
    Start([User visits]) --> Auth{Authenticated?}
    Auth -->|No| Login[Show login]
    Auth -->|Yes| Dashboard[Show dashboard]
    Login --> Auth

    style Start fill:#a6d189,stroke:#81c8be,color:#303446
    style Dashboard fill:#8caaee,stroke:#51576d,color:#c6d0f5
    classDef decision fill:#e5c890,stroke:#ef9f76,color:#303446
    class Auth decision
```

**Directions:** `TD` (top-down), `LR` (left-right), `BT`, `RL`

**Node shapes:**
- `[text]` rectangle
- `([text])` stadium/pill
- `{text}` diamond (decision)
- `[(text)]` cylinder (database)
- `[[text]]` subroutine

### Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API
    participant DB

    User->>+API: POST /login
    API->>+DB: Query user
    DB-->>-API: User data
    alt Valid credentials
        API-->>User: 200 + JWT
    else Invalid
        API-->>-User: 401
    end
```

**Arrows:** `->>` sync, `-->>` response, `-)` async

**Blocks:** `alt/else/end`, `opt/end`, `par/and/end`, `loop/end`

### Class Diagram

```mermaid
classDiagram
    Customer "1" --> "0..*" Order : places
    Order "1" *-- "1..*" LineItem : contains

    class Customer {
        +String email
        +placeOrder(cart)
    }

    class Order {
        +Decimal total
        +ship()
    }
```

**Relationships:**
- `--` association
- `*--` composition (child dies with parent)
- `o--` aggregation (child can exist alone)
- `<|--` inheritance
- `<|..` implementation

**Visibility:** `+` public, `-` private, `#` protected

### ERD

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : includes

    USER {
        uuid id PK
        string email UK
        string name
    }

    ORDER {
        uuid id PK
        uuid user_id FK
        decimal total
    }
```

**Cardinality:** `||` exactly one, `|o` zero or one, `}|` one or many, `}o` zero or many

### C4 Context

```mermaid
C4Context
    title System Context

    Person(user, "User", "Uses the app")
    System(app, "Application", "Main system")
    System_Ext(email, "Email Service", "Sends notifications")

    Rel(user, app, "Uses", "HTTPS")
    Rel(app, email, "Sends via", "SMTP")
```

**Elements:** `Person`, `System`, `System_Ext`, `Container`, `ContainerDb`, `Component`

## Styling with Frappe Colors

### Class-based Styling

```mermaid
flowchart LR
    A[Success]:::success
    B[Warning]:::warning
    C[Error]:::error
    D[Info]:::info

    A --> B --> C --> D

    classDef success fill:#a6d189,stroke:#81c8be,color:#303446
    classDef warning fill:#e5c890,stroke:#ef9f76,color:#303446
    classDef error fill:#e78284,stroke:#ea999c,color:#303446
    classDef info fill:#8caaee,stroke:#85c1dc,color:#303446
```

### Inline Styling

```mermaid
flowchart LR
    A[Normal]
    B[Highlighted]

    A --> B

    style B fill:#a6d189,stroke:#81c8be,color:#303446
```

### Theme Configuration

```mermaid
---
config:
  theme: base
  themeVariables:
    primaryColor: "#8caaee"
    primaryTextColor: "#c6d0f5"
    primaryBorderColor: "#51576d"
    lineColor: "#838ba7"
    secondaryColor: "#a6d189"
    tertiaryColor: "#e5c890"
    background: "#303446"
---
flowchart LR
    A --> B
```

**Themes:** `default`, `forest`, `dark`, `neutral`, `base`

**Look:** `classic` (default), `handDrawn` (sketch style)

## Common Mistakes

| Wrong | Correct |
|-------|---------|
| `A[Node (test)]` | `A["Node (test)"]` |
| `A --> B + C` | `A --> B` then `A --> C` |
| Unquoted label with `{}` | Quote it: `"label {data}"` |
| Random hex colors | Use Frappe palette colors |

## Export

- **GitHub/GitLab**: renders automatically in `.md` files
- **Mermaid Live**: https://mermaid.live (PNG/SVG export)
- **CLI**: `mmdc -i diagram.mmd -o output.png`
