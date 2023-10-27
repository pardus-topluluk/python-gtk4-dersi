#!/usr/bin/python3

# Load Gtk
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from MainWindow import MainWindow

# Uygulama aktif edildiğinde, ilk çalıştığında
def on_activate(app):
    # Yeni pencere oluştur
    win = MainWindow(app)

    # Ekranda göster
    win.present()

# Create a new application
app = Gtk.Application(application_id='tr.org.pardus.ornek-uygulama')
app.connect('activate', on_activate)

# Run the application
app.run(None)