import os
import sys
import subprocess
from google import genai
from google.genai import types


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

    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)