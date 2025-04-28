import os
import pathlib

def get_tools():
    tools = [
        {
            "name": "list_directory",
            "description": "List all files and directories in the current working directory",
            "input_schema": {
                "type": "object",
                "properties": {
                    "relpath": {
                        "type": "string",
                        "description": "Relative path to dir within dir.  Just return '.' if wanting to look at current dir."
                    }
                }
            }
        },
        {
            "name": "read_file",
            "description": "Read the contents of a file in the current working directory. You NEED to provide a filename",
            "input_schema": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read, including extension"
                    }
                },
                "required": ["filename"]
            }
        },
        {
            "name": "write_file",
            "description": "Write content to a file in the current working directory. Creates a new file or overwrites an existing one.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to write to, including extension"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    }
                },
                "required": ["filename", "content"]
            }
        }
    ]
    return tools

def list_directory(dir="."):
    current_dir = pathlib.Path.cwd()
    target_dir = current_dir / dir

    items = list(current_dir.iterdir())
    files = []
    directories = []

    for item in items:
        if item.is_file():
            files.append(item.name)
        elif item.is_dir():
            directories.append(item.name)

    return {
        "current_directory": str(current_dir),
        "files": files,
        "directories": directories,
        "total_items": len(files) + len(directories)
    }

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    return {
        "filename": filename,
        "content": content
    }

def write_file(filename, content):
    print("writing file: ", filename)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "filename": filename,
            "status": "success",
            "bytes_written": len(content),
            "message": f"Successfully wrote to {filename}"
        }
    except Exception as e:
        return {
            "filename": filename,
            "status": "error",
            "message": f"Error writing to file: {str(e)}"
        }
