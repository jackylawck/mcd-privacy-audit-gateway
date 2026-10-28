# AI Governance, Privacy & Regulatory Compliance Statement
# AI 治理、私隱與法規合規性宣告聲明

> **Document Version**: 1.0.0  
> **Effective Date**: 2026-10-28  
> **Status**: Reference Architecture & MVP Operational Baseline  

---

## 1. Executive Summary & Architecture Scope (概述與架構邊界)

### English
**MCD-Privacy-Audit-Gateway** is an open-source, client-side privacy-enhancing proxy designed as an intermediate governance layer between end-user AI developer clients (MCP Clients) and remote Model Context Protocol (MCP) tool providers (specifically `https://mcp.mcd.cn`).

The gateway itself **does not contain, train, or host any artificial intelligence models, weights, or generative inference engines**. It operates strictly as a deterministic data filtering, normalization, and auditing middleware.

### 繁體中文
**MCD-Privacy-Audit-Gateway** 是一套開源客戶端隱私強化代理中介軟體，作為終端 AI 開發者客戶端（MCP Client）與遠端 MCP 服務提供商（麥當勞中國開放平台 `https://mcp.mcd.cn`）之間的治理屏障。

**本工具自身不包含、不訓練、亦不託管任何人工智能模型權重或生成式推論引擎**。其本質為純確定性（Deterministic）的資料過濾、文字正規化與雜湊審計中介層。

---

## 2. Regulatory Applicability Assessment (法規適用性評估矩陣)

| Regulatory Regime / Standard | Applicability Status | Compliance Posture & Demarcation |
| :--- | :---: | :--- |
| **EU AI Act (Regulation (EU) 2024/1689)** | **Not Directly Subject** (Boundary Control) | Does not qualify as an AI System under Art. 3(1). Acts as an external technical guardrail facilitating transparency obligations (Art. 50). |
| **EU GDPR (Regulation (EU) 2016/679)** | **Architecturally Aligned** | Implements Privacy by Design (Art. 25) and Data Minimization (Art. 5(1)(c)) via local-only masking without secondary retention. |
| **Hong Kong PDPO (Cap. 486)** | **Directly Aligned** | Complies with DPP 1 (Purpose and manner of collection) and DPP 4 (Security of personal data); adheres to PCPD AI Procurement & Usage Guidelines. |
| **China PIPL & CAC Regulations** | **Boundary Limited** | Not a provider under *Interim Measures for Generative AI Services*. Pre-masks client inputs before querying mainland endpoints. |
| **ISO/IEC 42001:2023 (AIMS)** | **Control Aligned** | Directly addresses AI data protection, boundary controls, and traceability controls (Annex A.6, A.7, A.8). |
| **ISO/IEC 27001:2022 & 27701:2019** | **Control Aligned** | Adheres to cryptographic separation, data sanitization, and PII protection operational standards. |

---

## 3. Data Flow & Zero-Retention Architecture (資料流與零留存架構)

```text
[End User Prompt]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ MCD-Privacy-Audit-Gateway (Local Client / Self-Hosted) │
│                                                        │
│  [1] Inbound PII Masking (Deterministic RegEx)         │
│  [2] Ephemeral Hash Generation (Zero-Plaintext Store)  │
│  [3] Forwarding Sanitized Query via Streamable HTTP    │
└──────────────────────────┬─────────────────────────────┘
                           │ Encrypted Payload (HTTPS)
                           ▼
               [Remote MCP Server (mcp.mcd.cn)]
                           │
                           ▼
┌──────────────────────────┴─────────────────────────────┐
│ MCD-Privacy-Audit-Gateway (Return Interception)        │
│                                                        │
│  [4] Unicode Normalization (NFKC & Zero-width Strip)   │
│  [5] Outbound Injection Coarse Screen (Hard Block)     │
│  [6] Provenance Tagging (--- UNTRUSTED TOOL OUTPUT ---)│
└──────────────────────────┬─────────────────────────────┘
                           │ Safe Annotated Output
                           ▼
                 [LLM Execution Context]

```

### Key Privacy Safeguards:

1. **Zero-Retention Principle**: Raw prompts, unmasked personal identifiers, and conversation transcripts are processed in-memory and discarded immediately upon request completion.
2. **Ephemeral Audit Evidence**: Audit records store cryptographically generated message digests (SHA-256 / HMAC) and classification flags rather than reconstructible plain text.
3. **No Cross-Border Telemetry**: The gateway does not transmit diagnostic, usage, or behavioral analytics to any third-party infrastructure.

---

## 4. ISO Management System Control Mapping (ISO 治理控制項對應)

### 4.1 ISO/IEC 42001:2023 (Artificial Intelligence Management System)

* **A.6.2 (AI System Life Cycle - Impact & Risk Assessment)**: Implements automated threat containment at the inference interface.
* **A.7.2 (Data for AI Systems - Data Quality & Governance)**: Ensures data minimization before external tool consumption.
* **A.8.4 (Traceability and Transparency)**: Tags tool outputs with provenance delimiters to distinguish model context from system instructions.

### 4.2 ISO/IEC 27701:2019 (Privacy Information Management System)

* **Clause 7.2.2 (Data Minimization)**: Automatically redacts national mobile phone patterns and email addresses.
* **Clause 7.2.8 (Integrity and Confidentiality)**: Restricts secret transmission by decoupling user identity tokens from log storage.

---

## 5. Disclaimer & Legal Safeguards (法律免責聲明與使用限制)

### English

1. **Prototype Disclaimer**: This software is released strictly as an educational, architectural Minimum Viable Product (MVP) under the MIT License. It does not constitute enterprise legal, regulatory, or cybersecurity compliance advice.
2. **Deterministic Limitations**: Regular-expression-based sanitization and pattern-based prompt injection detection cannot guarantee 100% interception of adversarial mutations, advanced semantic evasions, or obfuscated payloads.
3. **Third-Party Services**: Users remain exclusively responsible for obtaining lawful access tokens and adhering to the Terms of Service governing the McDonald's China MCP platform and underlying cloud providers.
4. **No Controller Liability**: The developer assumes no liability for regulatory infractions, data spills, or operational disruptions arising from downstream deployment or modification of this source code.

### 繁體中文

1. **架構原型免責聲明**：本軟體為依據 MIT 開源授權條款發布之教學與架構驗證原型（MVP），不構成任何企業級法律合規、法規遵循或資訊安全審查之保證。
2. **確定性過濾極限**：基於正則表達式之脫敏機制與出站特徵粗篩，無法保證 100% 抵禦進階對抗樣本、語意混淆或多輪間接提示注入。
3. **第三方平台義務**：使用者須自行確保其 MCP Token 之取得途徑完全合法，並持續遵守麥當勞中國開放平台及底層雲端服務之服務協定與資料使用規範。
4. **無資料控制者責任**：開發者不承擔任何因下游使用者不當部署、程式碼變更或外部數據傳輸所引發之監管裁罰、民事賠償或營運損失責任。
