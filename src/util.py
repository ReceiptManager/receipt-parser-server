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


