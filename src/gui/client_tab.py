"""Client tab."""

import json
import threading
import tkinter as tk
from tkinter import ttk
from ..client.http_client import HttpClient, HttpError
from ..net.tcp_client import ConnectionError, TimeoutError
from ..http.url import ParseError
from .widgets import HeaderTable


class ClientTab(ttk.Frame):
    """GUI tab for HTTP client."""

    def __init__(self, master):
        super().__init__(master)
        self.client = HttpClient()
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)
        ttk.Label(top, text="URL:").pack(side="left")
        self.url_var = tk.StringVar(value="http://example.com")
        ttk.Entry(top, textvariable=self.url_var, width=60).pack(side="left", padx=5)
        self.method_var = tk.StringVar(value="GET")
        ttk.Combobox(
            top, textvariable=self.method_var, values=["GET", "POST"], width=8
        ).pack(side="left")

        hdr_frame = ttk.LabelFrame(self, text="Headers")
        hdr_frame.pack(fill="x", padx=5, pady=5)
        self.headers = HeaderTable(hdr_frame)
        self.headers.pack(fill="both", expand=True, padx=5, pady=5)

        body_frame = ttk.LabelFrame(self, text="Request Body (POST)")
        body_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.body_text = tk.Text(body_frame, height=5)
        self.body_text.pack(fill="both", expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=5, pady=5)
        self.send_btn = ttk.Button(btn_frame, text="Send", command=self._send)
        self.send_btn.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self._clear).pack(
            side="left", padx=5
        )

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(btn_frame, textvariable=self.status_var).pack(side="left", padx=20)

        resp_frame = ttk.LabelFrame(self, text="Response")
        resp_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.response_text = tk.Text(resp_frame, height=15)
        self.response_text.pack(fill="both", expand=True, padx=5, pady=5)

    def _clear(self):
        self.body_text.delete("1.0", tk.END)
        self.response_text.delete("1.0", tk.END)
        self.status_var.set("Ready")

    def _send(self):
        self.send_btn.config(state="disabled")
        self.status_var.set("Sending...")
        self.response_text.delete("1.0", tk.END)
        threading.Thread(target=self._do_request, daemon=True).start()

    def _do_request(self):
        try:
            url = self.url_var.get().strip()
            method = self.method_var.get().upper()
            headers = self.headers.get_headers()
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            else:
                body = self.body_text.get("1.0", tk.END).strip()
                ctype = headers.pop("Content-Type", "text/plain")
                resp = self.client.post(url, body.encode(), ctype, headers=headers)
            self.after(0, self._show_response, resp)
        except (ConnectionError, TimeoutError, ParseError, HttpError) as exc:
            self.after(0, self._show_error, str(exc))
        except Exception as exc:
            self.after(0, self._show_error, f"Error: {exc}")

    def _show_response(self, resp):
        self.send_btn.config(state="normal")
        self.status_var.set(f"Status: {resp.status} {resp.reason}")
        parts = [f"HTTP {resp.version} {resp.status} {resp.reason}", ""]
        for name, value in resp.headers.items():
            parts.append(f"{name}: {value}")
        parts.append("")
        try:
            body = resp.body.decode("utf-8")
        except UnicodeDecodeError:
            body = repr(resp.body)
        if "json" in resp.headers.get("Content-Type", "").lower():
            try:
                body = json.dumps(json.loads(body), indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                pass
        parts.append(body)
        self.response_text.insert("1.0", "\n".join(parts))

    def _show_error(self, message):
        self.send_btn.config(state="normal")
        self.status_var.set("Error")
        self.response_text.insert("1.0", f"ERROR: {message}")
