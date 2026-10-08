from langgraph.graph import StateGraph,START,END
from src.langgraphAgenticAI.state.state import State
from src.langgraphAgenticAI.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphAgenticAI.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphAgenticAI.nodes.chatbot_with_tool import ChatbotWithToolNode
class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using Langgraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. the chatbot node is set as both the 
        entry and exit point of the graph.
        """
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advance chatbot graph with tools integration.
        This method creates a chatbot graph that includes both a chatbot node and tools node.
        It defines tools, initializes the chatbot with tool capabilities, and sets up
        conditional and direct edges between nodes.
        the chatbot node is set as the entry point.
        """
        tools=get_tools()
        tool_node=create_tool_node(tools)
        llm=self.llm
        obj_chatbot_with_tools=ChatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_with_tools.create_chatbot(tools)
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")

    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase=="Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase=="Chatbot with Web":
            self.chatbot_with_tools_build_graph()
        else:
            raise ValueError(f"Unknown usecase: {repr(usecase)}")
        return self.graph_builder.compile()