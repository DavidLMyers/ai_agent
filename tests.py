from functions.get_files_info import get_files_info, get_file_content, write_file, run_python_file

run_python_file("calculator", "main.py")
run_python_file("calculator", "main.py", ["3 + 5"])
run_python_file("calculator", "tests.py")
run_python_file("calculator", "../main.py")
run_python_file("calculator", "nonexistent.py")