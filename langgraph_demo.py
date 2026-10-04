import re, json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from chat import get_llm

llm = get_llm()


# ---- 工具（第 9 课同款）----
def get_weather(city):
    table = {"北京": "晴 25°C", "上海": "多云 28°C", "杭州": "小雨 22°C"}
    return table.get(city, f"{city}暂无天气数据")


def calculator(expr):
    if not all(c in "0123456789+-*/. " for c in expr):
        return "表达式含非法字符"
    return eval(expr, {"__builtins__": {}}, {})


# ---- 状态：贯穿全程的数据包 ----
class State(TypedDict):
    question: str
    action: str
    args: dict
    result: str
    answer: str


# ---- 节点 ①：LLM 判断该调哪个工具 ----
def extract(state):
    prompt = f"""判断问题需要调用哪个工具，只输出 JSON：
{{"tool": "get_weather 或 calculator", "args": {{"对应参数": "值"}}}}
工具：get_weather(city)，calculator(expr)
问题：{state["question"]}"""
    raw = llm.invoke(prompt).content
    data = json.loads(re.search(r"\{.*\}", raw, re.S).group())
    return {"action": data["tool"], "args": data["args"]}


# ---- 节点 ②：执行真实工具 ----
def act(state):
    if state["action"] == "get_weather":
        return {"result": get_weather(state["args"]["city"])}
    if state["action"] == "calculator":
        return {"result": calculator(state["args"]["expr"])}
    return {"result": "未知工具"}


# ---- 节点 ③：LLM 组织最终回答 ----
def respond(state):
    prompt = f"用户问：{state['question']}。工具查询结果是：{state['result']}。请用一句自然的话回答用户。"
    return {"answer": llm.invoke(prompt).content}


# ---- 搭图：节点 + 边 ----
graph = StateGraph(State)
graph.add_node("extract", extract)
graph.add_node("act", act)
graph.add_node("respond", respond)
graph.add_edge(START, "extract")
graph.add_edge("extract", "act")
graph.add_edge("act", "respond")
graph.add_edge("respond", END)

# ---- 编译：加检查点 + 在 act 前设人工确认断点 ----
app = graph.compile(checkpointer=MemorySaver(), interrupt_before=["act"])

# ---- 跑：第一次调用停在断点，确认后恢复 ----
config = {"configurable": {"thread_id": "demo-1"}}  # thread_id = 这条对话的"存档编号"

state = app.invoke({"question": "北京天气怎么样？"}, config)
print("⏸️ 执行停在 act 节点前（模拟人工确认，检查点已存档）")
print("   当前已提取：", state["action"], state["args"])

# 人工确认后，从断点继续（传 None 表示继续）
state = app.invoke(None, config)
print("✅ 从断点恢复完成，最终回答：", state["answer"])
