# 麦当劳 MCP 安全合规与防篡改审计网关 MVP (MCD-Privacy-Audit-Gateway)

面向麦当劳 MCP 生态的企业级安全网关雏形。提供双向防护 (Inbound PII 遮蔽 + Outbound 注入粗筛阻断)，并基于 Azure Managed Identity、Event Hubs 单分区序列化及 Append Blob WORM 原则，构建具备严格 SRE 容量契约的不可变审计链。

本项目为架构原型（MVP），非生产就绪版本；完整控制边界、容错逻辑与残余风险见下文文档。

- 🛡️ [查看完整威胁模型与边界声明 (Threat Model)](./THREAT_MODEL.md)
- 📋 [查看麦当劳 MCP 集成说明](./MCP_INTEGRATION.md)
- 📜 [参赛原创与合规声明](./CONTEST_DECLARATION.md)

## 核心特性
- **双向治理**: 入站 PII 动态遮蔽，出站 Indirect Prompt Injection 粗筛与来源隔离。
- **零凭据依赖**: 基于 Azure Managed Identity，避免硬编码密钥。
- **可审计设计**: 契约对标 NIST AI RMF 与 OWASP LLM Top 10。

## 快速启动
```bash
pip install mcp
python server.py

```

```

---

### 第三步：點亮 Star
在倉庫頁面右上角點擊 **Star**（確保 Star 數大於 0）[cite: 1]。

---

### 第四步：前往官方 Issue 報名
前往官方競賽 Issues 頁面：
👉 `[https://github.com/M-China/mcd-developer-innovation-challenge/issues](https://github.com/M-China/mcd-developer-innovation-challenge/issues)`[cite: 1]

點擊 **New Issue**，填入以下內容並送出：

* **標題：**
  ```text
  【参赛申请】分布式隐私合规与防篡改审计网关 MVP (Azure/SRE 架构实践)

```

* **正文：**
```text
【参赛申请】
项目名称：分布式隐私合规与防篡改审计网关 (MCD-Privacy-Audit-Gateway)
项目地址：https://github.com/jackylawck/mcd-privacy-audit-gateway
项目简介：面向麦当劳 MCP 生态的企业级安全网关雏形。提供双向防护 (Inbound PII 遮蔽 + Outbound 注入粗筛阻断)，并基于 Azure Managed Identity、Event Hubs 单分区序列化及 Append Blob WORM 原则，构建具备严格 SRE 容量契约的不可变审计链。本项目为架构原型（MVP），非生产就绪版本；完整控制边界、容错逻辑与残余风险见 THREAT_MODEL.md。

```



送出後約 1–3 分鐘重整頁面，查看官方機器人回覆。若有任何驗證反饋，可隨時發送截圖處理。
