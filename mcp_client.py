import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    # 让客户端以子进程方式启动你的 server
    params = StdioServerParameters(command="uv", args=["run", "weather_server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("🔧 客户端自动发现的工具：", [t.name for t in tools.tools])

            result = await session.call_tool("get_weather", {"city": "杭州"})
            print("🌦️ 调用 get_weather(杭州)：", result.content[0].text)

asyncio.run(main())