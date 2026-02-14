import sys
import os
from dotenv import load_dotenv

# Load environment first
load_dotenv()

# Add the current directory to sys.path so we can import helper modules
sys.path.append(os.getcwd())

from helper.utils import summarize_webpage_content

def main():
    print("Testing summarize_webpage_content with fixed prompts...")
    content = "This is a simple test content that should be summarized. " * 50
    try:
        result = summarize_webpage_content(content)
        print("Function returned normally.")
        print(f"Result length: {len(result)}")
        if "Failed to summarize webpage" in result:
             print("Summary failed (caught exception).")
             print(result[:200])
        else:
             print("Summary success!")
             print(result[:200])
    except Exception as e:
        print(f"Exception propagated (unexpected): {e}")

if __name__ == "__main__":
    main()
