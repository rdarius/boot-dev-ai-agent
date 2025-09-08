from functions.get_files_info import get_files_info


def run_tests():
    cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]

    for working_dir, directory in cases:
        print(f'get_files_info("{working_dir}", "{directory}"):')

        result = get_files_info(working_dir, directory)

        if directory == ".":
            print("Result for current directory:")
        else:
            print(f"Result for '{directory}' directory:")

        # Indent each line of result
        for line in result.splitlines():
            print(f" {line}")

        print()  # Extra newline between test cases


if __name__ == "__main__":
    run_tests()