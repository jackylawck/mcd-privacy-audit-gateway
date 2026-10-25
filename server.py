import os
import re
import unicodedata
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcd-privacy-audit-gateway")

ALLOWED_TOOLS = {
    "query-meals",
    "query-meal-detail",
    "query-nearby-stores",
    "available-coupons",
    "campaign-calendar"
}

INJECTION_PATTERNS = [
    re.compile(r"(?i)ignore\s+previous\s+(instructions|prompt)"),
    re.compile(r"(?i)disregard\s+the\s+above"),
    re.compile(r"(?i)system\s+prompt\s+bypass")
]

def mask_pii(text: str) -> tuple[str, list]:
    detected_types = []
    # 遮蔽 11 位手机号
    if re.search(r'(?<!\d)1[3-9]\d{9}(?!\d)', text):
        text = re.sub(r'(?<!\d)1[3-9]\d{9}(?!\d)', '[PHONE_MASKED]', text)
        detected_types.append("phone")
    # 遮蔽邮箱
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_MASKED]', text)
        detected_types.append("email")
    return text, detected_types

def sanitize_outbound_response(tool_name: str, raw_response: str) -> tuple[str, bool]:
    # 移除零宽字符与 Unicode 规范化
    cleaned = raw_response.replace('\u200B', '').replace('\u200C', '').replace('\u200D', '')
    normalized = unicodedata.normalize('NFKC', cleaned)
    
    # 检测注入：硬阻断
    for pattern in INJECTION_PATTERNS:
        if pattern.search(normalized):
            return "[SECURITY BLOCK] Tool output rejected due to suspected injection.", True
            
    # 良性输出：套用来源隔离标记
    safe_response = (
        f"--- START UNTRUSTED TOOL OUTPUT [{tool_name}] ---\n"
        f"{normalized}\n"
        f"--- END UNTRUSTED TOOL OUTPUT ---"
    )
    return safe_response, False

@mcp.tool()
def sanitize_audit_and_forward(prompt: str, target_tool: str = "query-meals") -> str:
    """在调用麦当劳 MCP 前清洗 PII，并在返回时执行出站注入过滤"""
    if target_tool not in ALLOWED_TOOLS:
        target_tool = f"UNTRUSTED_{target_tool}"
        
    clean_prompt, detected_types = mask_pii(prompt)
    
    # 模拟从麦当劳 MCP 获取的响应
    mock_mcd_response = f"Successfully queried {target_tool}. Current hot items: Big Mac, Fries."
    safe_output, is_blocked = sanitize_outbound_response(target_tool, mock_mcd_response)
    
    return f"[Gateway Processed]\nSanitized Input: {clean_prompt}\nDetected PII: {detected_types}\nResult:\n{safe_output}"

if __name__ == "__main__":
    mcp.run_stdio()
