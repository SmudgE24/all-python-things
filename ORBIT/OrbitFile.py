import os


# ============================================================
# ORBIT FILES
# ============================================================


def list_files(path="/Users/ethanbrown"):
    """
    Returns all files and folders in a directory.
    """

    try:

        items = os.listdir(path)

        if not items:
            return "Directory is empty."

        output = ""

        for item in items:

            full_path = os.path.join(path, item)

            if os.path.isdir(full_path):
                output += f"[DIR]  {item}\n"

            else:
                output += f"[FILE] {item}\n"

        return output

    except PermissionError:
        return "Error: Permission denied."

    except FileNotFoundError:
        return "Error: Directory does not exist."

    except Exception as e:
        return f"Error: {e}"


# ============================================================
# CURRENT DIRECTORY
# ============================================================

def current_directory(*args):

    return os.getcwd()


# ============================================================
# CHANGE DIRECTORY
# ============================================================

def change_directory(path):

    try:

        os.chdir(path)

        return f"Changed directory to:\n{os.getcwd()}"

    except FileNotFoundError:
        return "Error: Directory does not exist."

    except NotADirectoryError:
        return "Error: That is not a directory."

    except PermissionError:
        return "Error: Permission denied."

    except Exception as e:
        return f"Error: {e}"


# ============================================================
# MAKE DIRECTORY
# ============================================================

def make_directory(name):

    try:

        os.mkdir(name)

        return f"Created directory: {name}"

    except FileExistsError:
        return "Error: Directory already exists."

    except Exception as e:
        return f"Error: {e}"


# ============================================================
# CREATE FILE
# ============================================================

def create_file(name):

    try:

        with open(name, "x"):
            pass

        return f"Created file: {name}"

    except FileExistsError:
        return "Error: File already exists."

    except Exception as e:
        return f"Error: {e}"


# ============================================================
# DELETE
# ============================================================

def delete(path):

    try:

        if os.path.isfile(path):

            os.remove(path)

            return f"Deleted file: {path}"

        elif os.path.isdir(path):

            return "Error: That is a directory. Directory deletion is disabled."

        else:

            return "Error: File does not exist."

    except PermissionError:
        return "Error: Permission denied."

    except Exception as e:
        return f"Error: {e}"