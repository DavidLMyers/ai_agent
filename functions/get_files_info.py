import os
import sys
import subprocess
from google import genai
from google.genai import types

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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
