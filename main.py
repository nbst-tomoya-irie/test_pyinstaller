"""
Simple Hello World application for testing PyInstaller
"""
import tkinter as tk
from tkinter import ttk
import threading

from logic_calculation import run as run_logic


class LngSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LNG Trade Flow Simulation")
        self.root.resizable(False, False)

        # --- 入力エリア ---
        input_frame = ttk.LabelFrame(root, text="Parameter Settings", padding=10)
        input_frame.pack(padx=10, pady=(10, 5), fill="x")

        # Panama Ratio
        ttk.Label(input_frame, text="Panama Ratio (0.0 ~ 1.0):").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.panama_var = tk.StringVar(value="0.5")
        self.panama_entry = ttk.Entry(input_frame, textvariable=self.panama_var, width=10)
        self.panama_entry.grid(row=0, column=1, padx=(10, 0), pady=5)

        # Suez Ratio
        ttk.Label(input_frame, text="Suez Ratio (0.0 ~ 1.0):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.suez_var = tk.StringVar(value="0.5")
        self.suez_entry = ttk.Entry(input_frame, textvariable=self.suez_var, width=10)
        self.suez_entry.grid(row=1, column=1, padx=(10, 0), pady=5)

        # --- Extension canal_usage_config ---
        ext_frame = ttk.LabelFrame(root, text="Extension canal_usage_config", padding=10)
        ext_frame.pack(padx=10, pady=(5, 5), fill="x")

        self.use_excel_var = tk.BooleanVar(value=False)
        self.use_excel_check = ttk.Checkbutton(
            ext_frame,
            text="Use the Panama and Suez ratios set in the excel file",
            variable=self.use_excel_var,
            command=self._toggle_entries,
        )
        self.use_excel_check.pack(anchor="w")

        # --- Run Button ---
        self.run_button = ttk.Button(root, text="Run", command=self.run_calculation)
        self.run_button.pack(pady=10)

        # --- Message Display Area ---
        msg_frame = ttk.LabelFrame(root, text="Messages", padding=10)
        msg_frame.pack(padx=10, pady=(5, 10), fill="both", expand=True)

        self.message_text = tk.Text(msg_frame, height=12, width=60, state="disabled")
        scrollbar = ttk.Scrollbar(msg_frame, orient="vertical", command=self.message_text.yview)
        self.message_text.configure(yscrollcommand=scrollbar.set)
        self.message_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def append_message(self, msg):
        self.message_text.configure(state="normal")
        self.message_text.insert("end", msg + "\n")
        self.message_text.see("end")
        self.message_text.configure(state="disabled")

    def clear_messages(self):
        self.message_text.configure(state="normal")
        self.message_text.delete("1.0", "end")
        self.message_text.configure(state="disabled")

    def validate_ratio(self, value_str, name):
        try:
            v = float(value_str)
        except ValueError:
            self.append_message(f"[Error] Please enter a numeric value for {name}.")
            return None
        if not (0.0 <= v <= 1.0):
            self.append_message(f"[Error] {name} must be in the range 0.0 ~ 1.0.")
            return None
        return v

    def _toggle_entries(self):
        state = "disabled" if self.use_excel_var.get() else "normal"
        self.panama_entry.configure(state=state)
        self.suez_entry.configure(state=state)

    def run_calculation(self):
        self.clear_messages()

        if self.use_excel_var.get():
            self.append_message("Use the Panama and Suez ratios set in the excel file")
            self.append_message("Running calculation...")
            self.run_button.configure(state="disabled")
            panama = None
            suez = None
        else:
            panama = self.validate_ratio(self.panama_var.get(), "Panama Ratio")
            suez = self.validate_ratio(self.suez_var.get(), "Suez Ratio")
            if panama is None or suez is None:
                return
            self.append_message(f"Panama Ratio: {panama}, Suez Ratio: {suez}")
            self.append_message("Running calculation...")
            self.run_button.configure(state="disabled")

        thread = threading.Thread(
            target=self._execute, args=(panama, suez), daemon=True
        )
        thread.start()

    def _execute(self, panama_ratio, suez_ratio):
        try:
            result = run_logic(panama_ratio, suez_ratio)
            self.root.after(0, self.append_message, result)
            self.root.after(0, self.append_message, "Completed.")
        except Exception as e:
            self.root.after(0, self.append_message, f"[Error] {e}")
        finally:
            self.root.after(0, lambda: self.run_button.configure(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    app = LngSimulatorApp(root)
    root.mainloop()
