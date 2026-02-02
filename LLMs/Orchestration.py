from agents import  Agent, WebSearchTool, function_tool


@function_tool
def save_results(output):

     db.insert({"output": output, "timestamp": datetime.time()})

     return "File saved"


search_agent = Agent(

    name= "Search Agent",

    instructions="Help the user search the internet and save results if asked.",
    tools=[WebSearchTool(),save_results],

)