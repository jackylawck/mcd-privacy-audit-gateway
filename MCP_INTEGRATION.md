# 麦当劳 MCP 集成说明 (MCP Integration Specification)

## 1. 业务价值与定位
本项目定位为麦当劳 MCP 生态的企业级安全与隐私审计网关原型 (MCD-Privacy-Audit-Gateway MVP)。
在用户与麦当劳官方 MCP 工具交互时，提供双向治理：入站 (Inbound) 阶段针对用户自然语言输入执行 PII 敏感信息脱敏；出站 (Outbound) 阶段针对工具响应执行注入粗筛与不可信来源隔离 (Provenance Isolation)，防范间接提示注入 (Indirect Prompt Injection)。

## 2. 实际调用的麦当劳 MCP 能力
- **MCP Server 端点**: `https://mcp.mcd.cn`
- **协议类型**: `streamablehttp`
- **目标守护 Tools**:
  - `query-meals`
  - `query-meal-detail`
  - `query-nearby-stores`
  - `available-coupons`
  - `campaign-calendar`

## 3. 调用与处理链路
1. **入站清洗 (Inbound)**: 用户 Prompt 经由网关拦截，执行 PII 识别与动态遮蔽，生成脫敏哈希存证。
2. **MCP 转发 (Forwarding)**: 携带脱敏后参数与 Bearer Token，安全调用麦当劳官方 MCP 端点。
3. **出站治理 (Outbound)**: 拦截 MCP Tool 返回值，执行 Unicode 规范化与注入特征检测；若判定恶意则执行硬阻断，良性结果套用来源隔离标记。
4. **审计序列化 (Auditing)**: 结构化元数据送入审计流，绑定 SRE 容量契约生成不可篡改日志链。
