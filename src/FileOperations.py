import gi
gi.require_version('Gtk', '4.0')
from gi.repository import GLib, Gio

def get_name(file):
    info = file.query_info("standard::display-name", Gio.FileQueryInfoFlags.NONE)
    if info:
        return info.get_attribute_string("standard::display-name")
    else:
        return file.get_basename()

def read_file(file, on_finish_callback):
    file.load_contents_async(None, _read_file_finish, on_finish_callback)

def _read_file_finish(file, result, on_finish_callback):
    contents = file.load_contents_finish(result)

    if not contents[0]:
        path = file.peek_path()
        on_finish_callback(file, "", f"Unable to open {path}: {contents[1]}")
        return

    try:
        on_finish_callback(file, contents[1].decode('utf-8'), "")

    except UnicodeError as err:
        path = file.peek_path()
        on_finish_callback(file, "", f"Unable to load the contents of {path}: the file is not encoded with UTF-8")

# = Save File    
def save_file(file, text, on_finish_callback):
    # Start the asynchronous operation to save the data into the file
    file.replace_contents_async(str.encode(text),
                                    None,
                                    False,
                                    Gio.FileCreateFlags.NONE,
                                    None,
                                    _save_file_finish,
                                    on_finish_callback)

def _save_file_finish(file, result, on_finish_callback):
    (success, new_etag) = file.replace_contents_finish(result)

    on_finish_callback(file, success, new_etag)