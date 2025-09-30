import os
import sys
import subprocess
from google import genai
from google.genai import types

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
            return content
    except Exception as e:
        print(f"Error: {e}")


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="takes a file path and returns the content of the file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)