"""
文档读取工具模块
================
读取本地文档（PDF、Word、TXT、Markdown），供 Executor Agent 调用。

正式项目可以接入：
- PyPDF2 / pdfplumber：读取 PDF
- python-docx：读取 Word 文档
- Unstructured：多格式文档解析
"""

import os
from pathlib import Path


def read_local_doc(file_path: str) -> str:
    """
    读取本地文档内容
    ----------------
    输入：文件路径 file_path（相对或绝对路径）
    输出：文档纯文本内容
    
    正式项目支持格式：.txt / .md / .pdf / .docx
    """
    path = Path(file_path)

    if not path.exists():
        return f"⚠️ 文件不存在：{file_path}"

    # 纯文本文件直接读取
    if path.suffix in [".txt", ".md", ".py", ".json"]:
        try:
            content = path.read_text(encoding="utf-8")
            return f"📄 文件：{path.name}\n\n{content[:2000]}..."  # 截断防止太长
        except Exception as e:
            return f"⚠️ 读取失败：{e}"

    # PDF / Word 需要第三方库，Demo 阶段先返回提示
    elif path.suffix in [".pdf", ".docx"]:
        return (
            f"📄 文件：{path.name}\n"
            f"（{path.suffix} 格式，正式项目接入 pdfplumber / python-docx 后可读取内容）"
        )

    else:
        return f"⚠️ 不支持的文件格式：{path.suffix}"
