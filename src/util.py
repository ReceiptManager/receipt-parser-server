import os
from datetime import datetime, date
# Allowed image extensions
from json.encoder import JSONEncoder

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# Check if the current file has allowed extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Get the current work dir
def get_config_dir():
    work_dir = os.environ.get('RECEIPT_PARSER_CONFIG_DIR')

    if work_dir:
        return work_dir
    else:
        work_dir = os.getcwd()

    if "src" in work_dir: work_dir = work_dir.replace("src", "")
    if not work_dir.endswith("/"): work_dir = work_dir + "/"

    return work_dir

def get_work_dir():
    work_dir = os.getcwd()
    if "src" in work_dir: work_dir = work_dir.replace("src", "")
    if not work_dir.endswith("/"): work_dir = work_dir + "/"
    return work_dir

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


class TupelEncoder(JSONEncoder):

    def _iterencode(self, obj, markers=None):
        if isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            gen = self._iterencode_dict(obj._asdict(), markers)
        else:
            gen = JSONEncoder._iterencode(self, obj, markers)
        for chunk in gen:
            yield chunk
