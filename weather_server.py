from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather-server")

@mcp.tool()
def get_weather(city:str)->str:
    table={"bg":"25","sh":"22"}
    return table.get(city,f"{city}暂无天气")

if __name__ == "__main__":
    mcp.run()    