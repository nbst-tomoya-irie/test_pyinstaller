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

        # Ave. Nav Speed
        ttk.Label(input_frame, text="Ave. Nav Speed (knot):").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.nav_speed_var = tk.StringVar(value="16.00")
        self.nav_speed_entry = ttk.Entry(input_frame, textvariable=self.nav_speed_var, width=10)
        self.nav_speed_entry.grid(row=0, column=1, padx=(10, 0), pady=5)

        # Utilization
        ttk.Label(input_frame, text="Utilization (%):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.utilization_var = tk.StringVar(value="75")
        self.utilization_entry = ttk.Entry(input_frame, textvariable=self.utilization_var, width=10)
        self.utilization_entry.grid(row=1, column=1, padx=(10, 0), pady=5)

        # Panama Ratio
        ttk.Label(input_frame, text="Panama Ratio (%):").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.panama_var = tk.StringVar(value="50")
        self.panama_entry = ttk.Entry(input_frame, textvariable=self.panama_var, width=10)
        self.panama_entry.grid(row=2, column=1, padx=(10, 0), pady=5)

        # Suez Ratio
        ttk.Label(input_frame, text="Suez Ratio (%):").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.suez_var = tk.StringVar(value="50")
        self.suez_entry = ttk.Entry(input_frame, textvariable=self.suez_var, width=10)
        self.suez_entry.grid(row=3, column=1, padx=(10, 0), pady=5)

        # Default button
        self.default_button = ttk.Button(input_frame, text="Default", command=self._reset_defaults)
        self.default_button.grid(row=4, column=0, columnspan=2, sticky="e", pady=(10, 0))

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

    def validate_range(self, value_str, name, low, high):
        try:
            v = float(value_str)
        except ValueError:
            self.append_message(f"[Error] Please enter a numeric value for {name}.")
            return None
        if not (low <= v <= high):
            self.append_message(f"[Error] {name} must be in the range {low} ~ {high}.")
            return None
        return v

    def _reset_defaults(self):
        self.nav_speed_var.set("16.00")
        self.utilization_var.set("75")
        self.panama_var.set("50")
        self.suez_var.set("50")

    def _toggle_entries(self):
        state = "disabled" if self.use_excel_var.get() else "normal"
        self.panama_entry.configure(state=state)
        self.suez_entry.configure(state=state)
        self.nav_speed_entry.configure(state=state)
        self.utilization_entry.configure(state=state)
        self.default_button.configure(state=state)

    def run_calculation(self):
        self.clear_messages()

        if self.use_excel_var.get():
            self.append_message("Use the Panama and Suez ratios set in the excel file")
            self.append_message("Running calculation...")
            self.run_button.configure(state="disabled")
            panama = None
            suez = None
            nav_speed = None
            utilization = None
        else:
            panama = self.validate_range(self.panama_var.get(), "Panama Ratio", 0.0, 100.0)
            suez = self.validate_range(self.suez_var.get(), "Suez Ratio", 0.0, 100.0)
            nav_speed = self.validate_range(self.nav_speed_var.get(), "Ave. Nav Speed", 0.0, 100.0)
            utilization = self.validate_range(self.utilization_var.get(), "Utilization", 0.0, 100.0)
            if any(v is None for v in (panama, suez, nav_speed, utilization)):
                return
            self.append_message(
                f"Panama Ratio: {panama:.2f}%, Suez Ratio: {suez:.2f}%, "
                f"Ave. Nav Speed: {nav_speed:.2f} knot, Utilization: {utilization:.2f}%"
            )
            panama /= 100.0
            suez /= 100.0
            utilization /= 100.0
            self.append_message("Running calculation...")
            self.run_button.configure(state="disabled")

        thread = threading.Thread(
            target=self._execute, args=(panama, suez, nav_speed, utilization), daemon=True
        )
        thread.start()

    def _execute(self, panama_ratio, suez_ratio, nav_speed, utilization):
        try:
            result = run_logic(panama_ratio, suez_ratio, nav_speed, utilization)
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
