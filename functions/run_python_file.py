import os
import subprocess


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