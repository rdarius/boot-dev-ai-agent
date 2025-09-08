from functions.get_file_content import get_file_content


def run_tests():
    cases = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]

    for working_dir, file_path in cases:
        print(f'get_file_content("{working_dir}", "{file_path}"):')

        result = get_file_content(working_dir, file_path)

        print("Result:")
        # Indent each line of output
        for line in result.splitlines():
            print(" " + line)

        print()  # Blank line between cases


if __name__ == "__main__":
    run_tests()