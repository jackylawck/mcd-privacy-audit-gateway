# 麦当劳 MCP 隐私与审计网关 - 威胁模型声明 (Threat Model)

本文档依照 Azure Well-Architected Framework (Security 支柱) 与 NIST AI RMF 规范，声明本项目的安全架构、已知边界与残余风险。本 MVP 旨在展示企业级 AI 治理组件的架构雏形，并未宣称可直接抵御所有高级对抗攻击。

## 1. 系统边界与信任根 (Trust Boundaries)
* **Producer (网关端)**：信任 Azure 托管身份 (Managed Identity) 提供不可否认的签名实体证明；信任 Inbound 正则清洗逻辑执行 PII 遮蔽。
* **Consumer (审计写入端)**：不信任 Producer，强制对每一笔事件执行 HMAC 签名校验与身份白名单比对；信任 Event Hub 提供绝对 FIFO 顺序以维持 `seq_no` 递增。
* **WORM Storage (不可变存储)**：信任 Terraform 基础设施契约实施 `allow_protected_append_writes_all = true`，使日志在保留期内具备物理上的不可篡改性。

## 2. 核心控制措施达成 (Implemented Controls)
* **零凭据提取 (Zero-Secret)**：完全移除环境变量与内存中的硬编码密钥，强校验采用 Managed Identity (MSI) 认证并限制为最小权限。
* **分布式幂等防重放 (Idempotency)**：Consumer 端引入内存去重机制防范 Event Hubs 的“至少一次 (At-least-once)”重放，避免审计链产生重复的 `sequence_no`。
* **分阶段 IaC (Phased IaC)**：基础设施采用分离部署策略，强制在代码层完成探测后再通过 Terraform 锁定 WORM 策略，避免不可逆锁定引发的配置瘫痪。

## 3. 已知边界与架构限制 (Known Limitations)

### 3.1 密码学限制：对称 HMAC 与密钥生命周期的矛盾 (P0 风险)
本 MVP 采用对称式 HMAC-SHA256 生成审计链签名。
* **残余风险**：一旦依照合规要求禁用旧版密钥，所有使用该密钥签名的历史日志将永久无法在链式结构中被验证。
* **运维契约与演进路线**：在迁移到非对称签名 (如 ECDSA P-256) 之前，**旧密钥在 WORM 保留期内不得禁用**；若合规要求强制禁用，必须先完成历史链的公钥化迁移或接受历史链验证失效的业务后果。

### 3.2 容量与高可用性限制 (单分区 SRE)
为确保审计链的严格连续性，Event Hub 被限制为单分区 (`partition_count = 1`)。
* **残余风险**：吞吐量硬上限为 ~1 MB/s 或 1000 EPS。
* **SRE 容忍度**：Consumer 端作为 Epoch Receiver，同一时刻仅有单实例活动。若 Consumer 崩溃，由于采用 `message_retention = 24h`，故障转移 (Failover) 的 MTTR 预算必须控制在 8 小时以内（保留期的 1/3），否则将因积压导致事件静默丢弃与审计断链。

### 3.3 Outbound 注入防御的局限性
当前出站防御基于正则表达式进行第一层粗筛。
* **控制行为**：
  * **检测到疑似注入**：硬阻断 (Hard Block)，返回固定安全告警，恶意原文绝对不进入 LLM 上下文。
  * **未检测到注入**：对良性输出强制套用不可信来源标记 (Provenance Isolation 标签)，降低（但不消除）LLM 被误导的概率。
* **残余风险**：无法抵御 2026 年主流的高级编码、语义规避与多轮注入。生产环境必须升级为结构化字段 Schema 校验优先、内容分类器预过滤为辅的深度隔离架构。

### 3.4 身份宣称的不可否认性依赖
网关写入日志的 `signer_identity` 直接读取自部署配置的 Managed Identity Client ID。
* **残余风险**：该字段的不可否认性完全依赖 Azure RBAC 对该身份的绑定，缺乏密码学层面的自证。
* **演进路线**：生产环境建议启用 OIDC 双向验证，或将身份验证信息与加密材料严格绑定。

### 3.5 分布式幂等与重放保护 (Idempotency)
本 MVP 当前在 Consumer 端使用内存集合 (Memory Cache) 执行 `request_id` 幂等去重。
* **残余风险**：Consumer 崩溃重启后，内存缓存清空。在 Event Hubs “至少一次 (At-least-once)” 语义下，可能导致重放事件产生重复的 `sequence_no`，进而引发验证器断链告警。
* **演进路线**：生产环境必须将幂等状态持久化依赖 (如 Redis 或 Checkpoint Store Metadata) 纳入 IaC 契约，并评估其可用性对审计链连续性的直接影响。
