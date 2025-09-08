import os


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if not abs_target_path.startswith(abs_working_directory):
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )

        parent_dir = os.path.dirname(abs_target_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(abs_target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"