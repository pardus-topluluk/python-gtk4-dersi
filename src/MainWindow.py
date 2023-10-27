import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.setup_window()

        self.setup_ui()
    
    # == SETUPS ==
    def setup_window(self):
        self.set_default_size(400, 300)
        self.set_title("Merhaba Dünya")

    def setup_headerbar(self):
        pass

    def setup_ui(self):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=50,
            margin_top=7,
            margin_start=7,
            margin_end=7,
            margin_bottom=7,
        )

        label = Gtk.Label(
            label="Bu benim ilk uygulamam",
            css_classes=["title-1", "success", "dim-label"] # <h1>
        )

        btn = Gtk.Button(
            label="Merhaba!",
            css_classes=["pill"]
        )
        btn.connect("clicked", self.on_btn_merhaba_clicked)

        box.append(label)
        box.append(btn)

        self.set_child(box)
    
    # == FUNCTIONS ==

    # == CALLBACKS ==
    def on_btn_merhaba_clicked(self, btn):
        print("Merhaba, butona bastığınız için teşekkürler.")