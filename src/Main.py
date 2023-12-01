#!/usr/bin/python3

# Load Gtk
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from MainWindow import MainWindow

win = None
# Uygulama aktif edildiğinde, ilk çalıştığında
def on_activate(app):
    global win

    if not win:
        # Yeni pencere oluştur
        win = MainWindow(app)

    # Ekranda göster
    win.present()


# Create a new application
app = Gtk.Application(application_id='tr.org.pardus.ornek-uygulama')
app.connect('activate', on_activate)

# Shortcuts for Actions
app.set_accels_for_action('win.new', ['<Ctrl>t'])
app.set_accels_for_action('win.open', ['<Ctrl>o'])
app.set_accels_for_action('win.save', ['<Ctrl>s'])
app.set_accels_for_action('win.save-as', ['<Ctrl><Shift>s'])

# Run the application
app.run(None)