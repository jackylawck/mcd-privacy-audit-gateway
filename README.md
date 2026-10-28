# 麦当劳 MCP 安全合规与防篡改审计网关 MVP (MCD-Privacy-Audit-Gateway)

面向麦当劳 MCP 生态的企业级安全网关雏形。提供双向防护 (Inbound PII 遮蔽 + Outbound 注入粗筛阻断)，并基于 Azure Managed Identity、Event Hubs 单分区序列化及 Append Blob WORM 原则，构建具备严格 SRE 容量契约的不可变审计链。

本项目为架构原型（MVP），非生产就绪版本；完整控制边界、法律合规声明、容错逻辑与残余风险请参阅下方核心文档。

## 核心文档与治理规范

- 🛡️ [查看完整威胁模型与边界声明 (Threat Model)](./THREAT_MODEL.md)
- ⚖️ [查看 AI 治理、私隐与全球合规性声明 (Governance & Compliance)](./GOVERNANCE_AND_COMPLIANCE.md)
- 🔒 [查看信息安全与漏洞通报政策 (Security Policy)](./SECURITY.md)
- 🏗️ [查看架构设计与密钥轮换 SOP (Architecture)](./docs/ARCHITECTURE.md)
- 📋 [查看麦当劳 MCP 集成说明](./MCP_INTEGRATION.md)
- 📜 [参赛原创与合规声明](./CONTEST_DECLARATION.md)

## 核心特性

- **双向治理**: 入站 PII 动态遮蔽，出站 Indirect Prompt Injection 粗筛与来源隔离。
- **零凭据依赖**: 基于 Azure Managed Identity，避免硬编码密钥。
- **可审计设计**: 契约对标 NIST AI RMF 与 OWASP LLM Top 10。
- **全球合规对齐**: 架构设计映射 ISO/IEC 42001/27001/27701 控制项，符合香港《个人资料（私隐）条例》(PDPO) 与 GDPR 数据最小化原则。

## 快速启动

```bash
pip install mcp
python server.py
