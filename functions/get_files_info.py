import os
import sys

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