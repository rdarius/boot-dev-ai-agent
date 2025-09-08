from functions.run_python_file import run_python_file


def run_tests():
    cases = [
        ("calculator", "main.py", []),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", []),
        ("calculator", "../main.py", []),
        ("calculator", "nonexistent.py", []),
    ]

    for working_dir, file_path, args in cases:
        if args:
            print(f'run_python_file("{working_dir}", "{file_path}", {args}):')
        else:
            print(f'run_python_file("{working_dir}", "{file_path}"):')

        result = run_python_file(working_dir, file_path, args)

        print("Result:")
        for line in result.splitlines():
            print(" " + line)

        print()


if __name__ == "__main__":
    run_tests()