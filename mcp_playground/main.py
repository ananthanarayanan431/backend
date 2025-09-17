
import asyncio


from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano-2025-08-07")

math_stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Users/ananthanarayanan/Desktop/backend/mcp_playground/servers/math_server.py"],
)

weather_server_url = "http://localhost:8000/sse" 

async def main():
    async with stdio_client(math_stdio_server_params) as (math_read,math_write), \
        sse_client(weather_server_url) as (whether_read, whether_write):
        
        async with ClientSession(read_stream=math_read, write_stream=math_write) as math_session, \
            ClientSession(read_stream=whether_read, write_stream=whether_write) as whether_session: 
            
            await math_session.initialize()
            await whether_session.initialize()
            print("Math session started!")
            print("Whether session stated")

            math_tools = await load_mcp_tools(session=math_session)
            whether_tools = await load_mcp_tools(session=whether_session)

            tools = math_tools + whether_tools
            agent = create_react_agent(llm,tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What’s the weather in Hyderabad and also 54+2*3?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
