"""
calculator_tool.py
安全数学计算工具，Executor智能体可调用
自动清洗全角符号、提取纯数学表达式，避免eval报错
"""
import math
import re

def calculator(expression: str) -> str:
    """
    :param expression: 数学表达式字符串，支持输入整句话，自动提取计算部分
    """
    # 1. 全角符号转半角，清洗中文标点
    trans_table = str.maketrans({
        "：": ":",
        "，": ",",
        "（": "(",
        "）": ")",
        "＋": "+",
        "－": "-",
        "×": "*",
        "÷": "/",
        "＝": "="
    })
    clean_text = expression.translate(trans_table)

    # 2. 正则提取纯数学表达式（保留数字、小数点、运算符、括号）
    pattern = r'[\d\s\.\+\-\*\/\(\)]+'
    matches = re.findall(pattern, clean_text)
    if not matches:
        return "❌ 未能从输入中识别到有效的数学表达式"
    
    calc_expr = max(matches, key=len).strip()
    if not calc_expr:
        return "❌ 未能从输入中识别到有效的数学表达式"

    # 3. 安全eval计算
    safe_namespace = {
        "abs": abs,
        "round": round,
        "math": math,
        "pow": pow,
        "max": max,
        "min": min
    }
    try:
        result = eval(calc_expr, {"__builtins__": {}}, safe_namespace)
        return f"✅ 计算完成：{calc_expr} = {result}"
    except Exception as err:
        return f"❌ 计算器执行失败，错误：{str(err)}"
