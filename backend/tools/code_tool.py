import sys
import subprocess
from langchain_core.tools import tool

@tool
def execute_python_code(code: str) -> str:
    """Executes a given python code string in a subprocess and returns the output or errors.
    Useful for calculating math, generating algorithms, or data processing.
    """
    try:
        # We use the venv's python executable
        python_exe = sys.executable 
        
        result = subprocess.run(
            [python_exe, "-c", code],
            capture_output=True,
            text=True,
            timeout=15 
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            return f"Code executed successfully.\nOutput:\n{output}" if output else "Code executed successfully with no output."
        else:
            return f"Code execution failed.\nError:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Code execution timed out after 15 seconds."
    except Exception as e:
        return f"Error executing code: {e}"
