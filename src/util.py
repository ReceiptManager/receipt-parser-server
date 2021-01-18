from datetime import datetime, date
import os

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Check if the current file has allowed extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Get the current work dir
def get_work_dir():
    dir = os.getcwd()

    if "src" in dir: dir = dir.replace("src", "")
    if not dir.endswith("/"): dir = dir + "/"

    return dir

# Save return. Convenient function to return not null
def save_ret(component):
    if not component: return ""
    return component

# Serialize date object
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError("Type %s not serializable" % type(obj))

def get_last_modified_file(search_dir):
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]  # add path to each file
    files.sort(key=lambda x: -os.path.getmtime(x))
    os.chdir("../../")

    if not files:
        return None

    return files[0]