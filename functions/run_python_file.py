import os
import sys
import subprocess
from google import genai
from google.genai import types

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
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n"
    except Exception as e:
        print(f"Error: executing Python file: {e}") 


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)