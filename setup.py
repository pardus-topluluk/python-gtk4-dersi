#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import subprocess

APP_NAME = "pardus-ornek-uygulama"
APP_ID = "tr.org.pardus.ornek-uygulama"
TRANSLATIONS_FOLDER = "po"


def compile_translations():
    mo = []
    for po_file in os.listdir(TRANSLATIONS_FOLDER):
        if po_file.endswith(".po"):
            language = po_file.split('.po')[0]

            os.makedirs(
                f"{TRANSLATIONS_FOLDER}/{language}/LC_MESSAGES", exist_ok=True)

            mo_file = f"{TRANSLATIONS_FOLDER}/{language}/LC_MESSAGES/{APP_NAME}.mo"

            msgfmt_cmd = f'msgfmt "{TRANSLATIONS_FOLDER}/{po_file}" -o "{mo_file}"'
            print(mo_file, po_file, msgfmt_cmd)
            subprocess.call(msgfmt_cmd, shell=True)

            mo.append((f"/usr/share/locale/{language}/LC_MESSAGES",
                       [mo_file]))
    return mo


data_files = [
    ("/usr/share/applications/", [f"{APP_ID}.desktop"]),
    (f"/usr/share/pardus/{APP_NAME}/src", [
        "src/Main.py",
        "src/MainWindow.py",
        "src/FileOperations.py",
    ]),
    ("/usr/bin/", [f"{APP_NAME}"]),
    ("/usr/share/icons/hicolor/scalable/apps/", [f"{APP_NAME}.svg"])
] + compile_translations()

setup(
    name=f"{APP_NAME}",
    version="0.1.0",
    packages=find_packages(),
    scripts=[f"{APP_NAME}"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Emin Fedar",
    author_email="emin.fedar@pardus.org.tr",
    description="My Text Editor is a simple text editor.",
    license="GPLv3",
    keywords="",
    url="https://github.com/pardus-topluluk/python-gtk4-dersi",
)
