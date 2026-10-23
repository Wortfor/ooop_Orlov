"""Main application window."""

import tkinter as tk
from tkinter import ttk
from .client_tab import ClientTab
from .server_tab import ServerTab


class App(tk.Tk):
    """Main window with tabs."""

    def __init__(self):
        super().__init__()
        self.title("HTTP Client & Server")
        self.geometry("900x700")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        self.client_tab = ClientTab(notebook)
        self.server_tab = ServerTab(notebook)
        notebook.add(self.client_tab, text="Client")
        notebook.add(self.server_tab, text="Server")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self.server_tab.server:
            self.server_tab.server.stop()
        self.destroy()
