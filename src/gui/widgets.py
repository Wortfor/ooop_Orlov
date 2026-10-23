"""Reusable GUI widgets."""

import tkinter as tk
from tkinter import ttk


class HeaderTable(ttk.Frame):
    """Table for HTTP headers (name -> value)."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._build()

    def _build(self):
        self.tree = ttk.Treeview(
            self, columns=("name", "value"), show="headings", height=5
        )
        self.tree.heading("name", text="Header")
        self.tree.heading("value", text="Value")
        self.tree.column("name", width=150)
        self.tree.column("value", width=300)
        self.tree.pack(fill="both", expand=True)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Add", command=self._add_dialog).pack(
            side="left", padx=2
        )
        ttk.Button(btn_frame, text="Remove", command=self._remove).pack(
            side="left", padx=2
        )

    def _add_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("New Header")
        ttk.Label(dlg, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, padx=5)
        ttk.Label(dlg, text="Value:").grid(row=1, column=0, padx=5, pady=5)
        val_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=val_var).grid(row=1, column=1, padx=5)

        def ok():
            if name_var.get():
                self.tree.insert("", "end", values=(name_var.get(), val_var.get()))
            dlg.destroy()

        ttk.Button(dlg, text="OK", command=ok).grid(
            row=2, column=0, columnspan=2, pady=5
        )

    def _remove(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def get_headers(self) -> dict:
        result = {}
        for item in self.tree.get_children():
            name, value = self.tree.item(item)["values"]
            result[str(name)] = str(value)
        return result
