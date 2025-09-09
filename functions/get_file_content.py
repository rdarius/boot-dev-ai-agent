import os
from functions.config import MAX_FILE_CONTENT_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file, truncated if too large, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        abs_working_directory = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if not abs_target_path.startswith(abs_working_directory):
            return (
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(abs_target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if len(content) > MAX_FILE_CONTENT_CHARS:
            truncated = content[:MAX_FILE_CONTENT_CHARS]
            return truncated + f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_CHARS} characters]'
        else:
            return content

    except Exception as e:
        return f"Error: {e}"