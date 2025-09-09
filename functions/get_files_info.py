import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        abs_working_directory = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if not abs_target_path.startswith(abs_working_directory):
            return (
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )

        if not os.path.isdir(abs_target_path):
            return f'Error: "{directory}" is not a directory'

        results = []
        for entry in os.listdir(abs_target_path):
            entry_path = os.path.join(abs_target_path, entry)
            try:
                is_dir = os.path.isdir(entry_path)
                size = os.path.getsize(entry_path)
                results.append(
                    f"- {entry}: file_size={size} bytes, is_dir={str(is_dir)}"
                )
            except Exception as e:
                results.append(f"- {entry}: Error accessing file info ({e})")

        return "\n".join(results)

    except Exception as e:
        return f"Error: {e}"