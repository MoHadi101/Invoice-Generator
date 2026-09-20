from cx_Freeze import setup, Executable
import sys

# ------------------------------------------------------------
# 1. Basis: GUI-Modus (kein Konsolenfenster)
# ------------------------------------------------------------
base = None
if sys.platform == "win32":
    base = "gui"   # <-- NICHT "Win32GUI", sondern "gui"!

# ------------------------------------------------------------
# 2. Dateien, die mit ins Programm kopiert werden
# ------------------------------------------------------------
include_files = [
    "invoice_template.docx",
    "icon.ico"            # Icon für .exe und Verknüpfung
]

# ------------------------------------------------------------
# 3. Desktop-Verknüpfung für den MSI-Installer
# ------------------------------------------------------------
shortcut_table = [
    ("DesktopShortcut",
     "DesktopFolder",
     "Invoice Generator",
     "TARGETDIR",
     "[TARGETDIR]InvoiceGenerator.exe",
     None, None, None, None, None, None, None)
]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
    "data": msi_data,
    "upgrade_code": "{22222222-3333-4444-5555-666666666666}",
    "add_to_path": False,
}

# ------------------------------------------------------------
# 4. Setup
# ------------------------------------------------------------
setup(
    name="InvoiceGenerator",
    version="1.0",
    description="Rechnungen aus Word-Vorlage generieren",
    author="Mohamad Al Hade",
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": [
                "os",
                "docxtpl",
                "jinja2",
                "lxml",
                "xml",
                "tkinter",
                "datetime"
            ],
            "include_msvcr": True,
        },
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(
            script="main.py",
            base=base,
            icon="icon.ico",          # Icon für die .exe
            target_name="InvoiceGenerator.exe"
        )
    ]
)