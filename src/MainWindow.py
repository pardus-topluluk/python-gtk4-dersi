import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

import FileOperations

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.setup_variables()

        self.setup_actions()

        self.setup_window()

        self.setup_headerbar()

        self.setup_ui()
    
    # == SETUPS ==
    def setup_variables(self):
        self._current_working_file = None

    def setup_actions(self):
        new_action = Gio.SimpleAction(name="new")
        new_action.connect("activate", self.on_action_win_new_activated)
        self.add_action(new_action)
    
        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.on_action_win_open_activated)
        self.add_action(open_action)

        save_action = Gio.SimpleAction(name="save")
        save_action.connect("activate", self.on_action_win_save_activated)
        self.add_action(save_action)

        save_as_action = Gio.SimpleAction(name="save-as")
        save_as_action.connect("activate", self.on_action_win_save_as_activated)
        self.add_action(save_as_action)

    def setup_window(self):
        self.set_default_size(600, 400)
        self.set_title("Metin Editörü")

    def setup_headerbar(self):
        btn_new = Gtk.Button(
            icon_name="document-new-symbolic",
            action_name="win.new",
            tooltip_text="Creates a new empty document."
        )
        btn_open = Gtk.Button(
            icon_name="document-open-symbolic",
            action_name="win.open",
            tooltip_text="Open a file."
        )
        btn_save = Gtk.Button(
            icon_name="document-save-symbolic",
            action_name="win.save",
            tooltip_text="Save the current file."
        )
        btn_save_as = Gtk.Button(
            icon_name="document-save-as-symbolic",
            action_name="win.save-as",
            tooltip_text="Save the current file as different file."
        )

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        box.append(btn_new)
        box.append(btn_open)
        box.append(btn_save)
        box.append(btn_save_as)

        headerbar = Gtk.HeaderBar()
        headerbar.pack_start(box)

        self.set_titlebar(headerbar)


    def setup_ui(self):
        self.text_view = Gtk.TextView(
            monospace=True,
            left_margin=7,
            right_margin=7
        )
        scrolled_window = Gtk.ScrolledWindow(child=self.text_view)

        self.set_child(scrolled_window)
    
    # == FUNCTIONS ==
    def get_textview_text(self):
        buffer = self.text_view.get_buffer()

        # Retrieve the iterator at the start of the buffer
        start = buffer.get_start_iter()
        # Retrieve the iterator at the end of the buffer
        end = buffer.get_end_iter()
        # Retrieve all the visible text between the two bounds
        return buffer.get_text(start, end, False)
    
    def set_textview_text(self, text):
        buffer = self.text_view.get_buffer()

        # TextView'in metnini verdiğimiz parametreye eşitle
        buffer.set_text(text)

        # İmleci başa al
        start = buffer.get_start_iter()
        buffer.place_cursor(start)

    # == CALLBACKS ==
    def on_action_win_new_activated(self, action, params):
        self.set_textview_text("")
        self.set_title("Metin Editörü")
        self._current_working_file = None
    
    def on_action_win_open_activated(self, action, params):
        self._open_file_chooser = Gtk.FileChooserNative(
            title="Open File",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel",
        )

        self._open_file_chooser.connect("response", self.on_open_dialog_response)
        self._open_file_chooser.show()
    
    def on_open_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            FileOperations.read_file(dialog.get_file(), self.on_file_read)
        
        # Dialog'u kaldırıyoruz
        self._open_file_chooser = None
    
    def on_file_read(self, file, content, err):
        if err:
            print(f"Error: {err}")
            return
        
        self.set_textview_text(content)

        filename = FileOperations.get_name(file)
        self.set_title(filename)

        # Set current working file
        self._current_working_file = file

    def on_action_win_save_activated(self, action, params):
        if self._current_working_file:
            text = self.get_textview_text()

            FileOperations.save_file(self._current_working_file, text, self.on_file_saved)
        else:
            # If there is no file to work on, open "Save as..." dialog
            self.activate_action("win.save-as")
    
    def on_action_win_save_as_activated(self, action, params):
        self._save_file_chooser = Gtk.FileChooserNative(
            title="Save File",
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE,
            accept_label="_Save",
            cancel_label="_Cancel",
        )

        self._save_file_chooser.connect("response", self.on_save_dialog_response)
        self._save_file_chooser.show()
    
    def on_save_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            text = self.get_textview_text()

            FileOperations.save_file(dialog.get_file(), text, self.on_file_saved)
        
        # Dialog'u kaldırıyoruz
        self._save_file_chooser = None
    
    def on_file_saved(self, file, success, new_etag):
        if success:
            filename = FileOperations.get_name(file)
            self.set_title(filename)

            self._current_working_file = file