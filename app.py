import os

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
from src.langgraphAgenticAI.main import load_langgraph_agenticai_app
if __name__=="__main__":
    load_langgraph_agenticai_app()