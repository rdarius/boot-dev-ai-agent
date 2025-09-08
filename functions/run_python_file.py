import os
import subprocess


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