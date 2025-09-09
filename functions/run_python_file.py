import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if not abs_target_path.startswith(abs_working_directory):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.exists(abs_target_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed = subprocess.run(
            ["python3", abs_target_path] + args,
            cwd=abs_working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        result_parts = []
        if completed.stdout.strip():
            result_parts.append("STDOUT:\n" + completed.stdout.strip())
        if completed.stderr.strip():
            result_parts.append("STDERR:\n" + completed.stderr.strip())
        if completed.returncode != 0:
            result_parts.append(f"Process exited with code {completed.returncode}")

        if not result_parts:
            return "No output produced."

        return "\n".join(result_parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"