import os
import sys
import subprocess

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        if not full_path.startswith(working_directory):
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(full_path):
            raise Exception(f'Error: "{directory}" is not a directory')
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            print(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
    except Exception as e:
        print(f"Error: {e}")


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not full_path.startswith(working_directory):
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(full_path):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        with open(full_path, 'r') as f:
            content = f.read()
            if len(content) > 10000:
                content = content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
            print(content)
    except Exception as e:
        print(f"Error: {e}")
    
def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not full_path.startswith(working_directory):
            raise Exception(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        with open(full_path, 'w') as f:
            f.write(content)
        print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        print(f"Error: {e}")

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        real_working_directory = os.path.realpath(working_directory)
        real_full_path = os.path.realpath(full_path)
        if not real_full_path.startswith(real_working_directory + os.sep):
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        full_path = os.path.realpath(full_path)
        if not os.path.isfile(full_path):
            raise Exception(f'File "{file_path}" not found')
        if not file_path.endswith('.py'):
            raise Exception(f'"{file_path}" is not a Python file')
        command = [sys.executable, full_path]
        if args:
            command += args
        completed_process = subprocess.run(command, cwd=working_directory, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed_process.returncode != 0:
            raise Exception(f'Process exited with code {completed_process.returncode}')
        stdout = completed_process.stdout.decode('utf-8') if completed_process.stdout else "No output produced."
        stderr = completed_process.stderr.decode('utf-8') if completed_process.stderr else "No output produced."
        print(f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
    except Exception as e:
        print(f"Error: executing Python file: {e}") 

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")