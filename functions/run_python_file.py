# functions/run_python_file.py

import os
import subprocess


from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        
        run_subprocess = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=abs_working_dir, text=True, timeout=30)

        output_str = ""
        if run_subprocess.returncode != 0:
            output_str += f"Process exited with code {run_subprocess.returncode}"

        if not run_subprocess.stdout and not run_subprocess.stderr:
            output_str += f"No output produced"
        else:
            output_str += f"STDOUT: {run_subprocess.stdout}"
            output_str += f"STDERR: {run_subprocess.stderr}"
        
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a single python file in a specified directory relative to the working directory, providing STDOUT, STDERR and run code",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments for the python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)