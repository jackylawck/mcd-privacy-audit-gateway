# Security Policy (資訊安全政策)

## Supported Versions (版本支援範圍)

| Version | Supported          | Security Maintenance Status |
| :------ | :----------------- | :-------------------------- |
| 1.0.x   | :white_check_mark: | Active (Current MVP)        |
| < 1.0   | :x:                | Deprecated                  |

---

## Reporting a Vulnerability (安全性漏洞通報)

### English
We take the security and deterministic reliability of this gateway seriously. If you discover a security vulnerability, prompt injection bypass, or regulatory boundary gap, please **DO NOT** open a public issue.

Please report vulnerabilities privately via:
* **GitHub Private Vulnerability Reporting**: Navigate to the Security tab of this repository and select **"Report a vulnerability"**.
* **Direct Maintainer Contact**: Contact the repository owner directly through verified developer profiles.

Please include the following in your report:
1. Attack classification (e.g., Inbound PII Leakage, Outbound Filter Bypass, Denial of Service).
2. Minimal Reproducible Example (curl payload, input string, or environment configuration).
3. Evaluated impact across relevant privacy standards (GDPR, HK PDPO, or ISO/IEC 42001).

We commit to acknowledging receipts within 48 hours and validating mitigation timelines collaboratively.

### 繁體中文
我們高度重視本網關的資訊安全與確定性過濾效能。若您發現任何安全漏洞、隱私洩漏隱患或提示詞注入繞過途徑，**請勿直接建立公開 Issue**。

請透過以下私密管道通報：
* **GitHub 私密漏洞通報**：前往本倉庫的 **Security** 頁籤，點擊 **"Report a vulnerability"**。
* **開發者直接聯繫**：透過驗證之開發者個人檔案進行聯絡。

通報時請附上：
1. 威脅分類（如：入站個資漏檢、出站注入繞過、阻斷服務）。
2. 最小重現範例（Payload 字串或測試設定）。
3. 潛在影響評估（參照香港 Cap. 486、GDPR 或 ISO 標準）。

維護團隊將於 48 小時內確認收悉，並於確認後提供安全修補方案。

---

## Zero-Credential Commitment (零憑據政策)

1. This repository will never store, transmit, or request genuine API keys, Bearer tokens, or passwords.
2. Any hardcoded secret identified in repository history will be treated as an immediate P0 breach requiring irreversible credential revocation and Git history rewriting.
