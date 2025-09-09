import os
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    args = dict(function_call_part.args or {})

    args["working_directory"] = "./calculator"

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = f"Error executing function: {e}"

    tool_response = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name, response={"result": function_result}
            )
        ],
    )

    if verbose:
        print(f"-> {tool_response.parts[0].function_response.response}")

    return tool_response