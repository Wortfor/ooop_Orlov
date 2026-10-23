"""Server tab."""

import queue
import time
import tkinter as tk
import webbrowser
from tkinter import ttk
from ..server.http_server import HttpServer
from ..server.router import Router
from ..server import handlers


class ServerTab(ttk.Frame):
    """GUI tab for HTTP server."""

    def __init__(self, master):
        super().__init__(master)
        self.server: HttpServer | None = None
        self.log_queue: queue.Queue = queue.Queue()
        self._build()
        self._poll_log()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)
        ttk.Label(top, text="Port:").pack(side="left")
        self.port_var = tk.StringVar(value="8080")
        ttk.Entry(top, textvariable=self.port_var, width=8).pack(side="left", padx=5)
        self.start_btn = ttk.Button(top, text="Start", command=self._start)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(
            top, text="Stop", command=self._stop, state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        self.indicator = tk.Canvas(top, width=20, height=20)
        self.indicator.pack(side="left", padx=10)
        self._dot = self.indicator.create_oval(2, 2, 18, 18, fill="red")
        ttk.Button(top, text="Open in Browser", command=self._open_browser).pack(
            side="left", padx=5
        )
        ttk.Button(top, text="Clear Log", command=self._clear_log).pack(
            side="left", padx=5
        )

        log_frame = ttk.LabelFrame(self, text="Request Log")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_tree = ttk.Treeview(
            log_frame, columns=("time", "method", "path", "status"), show="headings"
        )
        self.log_tree.heading("time", text="Time")
        self.log_tree.heading("method", text="Method")
        self.log_tree.heading("path", text="Path")
        self.log_tree.heading("status", text="Status")
        self.log_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def _on_request(self, method, path, status):
        self.log_queue.put((time.strftime("%H:%M:%S"), method, path, status))

    def _poll_log(self):
        try:
            while True:
                entry = self.log_queue.get_nowait()
                self.log_tree.insert("", 0, values=entry)
        except queue.Empty:
            pass
        self.after(200, self._poll_log)

    def _start(self):
        try:
            port = int(self.port_var.get())
        except ValueError:
            return
        router = Router()
        router.route("GET", "/echo", handlers.handle_echo_get)
        router.route("POST", "/echo", handlers.handle_echo_post)
        router.route("GET", "/time", handlers.handle_time)
        router.route("GET", "/headers", handlers.handle_headers)
        self.server = HttpServer(router, log_callback=self._on_request)
        self.server.start(port)
        self.indicator.itemconfig(self._dot, fill="green")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

    def _stop(self):
        if self.server:
            self.server.stop()
            self.server = None
        self.indicator.itemconfig(self._dot, fill="red")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def _open_browser(self):
        webbrowser.open(f"http://localhost:{self.port_var.get()}/")

    def _clear_log(self):
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
