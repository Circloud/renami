import tkinter as tk
from tkinter import ttk

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, settings):
        super().__init__(parent)

        # Initializing
        self.settings = settings

        # Set window title and size
        self.title("Settings")
        self.geometry("400x300")

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Create form for API key, base URL and model name
        ttk.Label(self, text="API Key").pack(pady=5)
        self.api_key_entry = ttk.Entry(self, show='*', width=50)
        self.api_key_entry.insert(0, self.settings.get('api_key', ''))
        self.api_key_entry.pack(pady=5)

        ttk.Label(self, text="API Base URL").pack(pady=5)
        self.api_base_url_entry = ttk.Entry(self, width=50)
        self.api_base_url_entry.insert(0, self.settings.get('api_base_url', ''))
        self.api_base_url_entry.pack(pady=5)

        ttk.Label(self, text="Model Name").pack(pady=5)
        self.model_entry = ttk.Entry(self, width=50)
        self.model_entry.insert(0, self.settings.get('model'))
        self.model_entry.pack(pady=5)

        # Create buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(side='bottom', pady=20)

        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save", command=self.save).pack(side='left', padx=5)

        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def save(self):
        """Save the settings and close the window"""
        # Update settings with new values
        self.settings.update({
            'api_key': self.api_key_entry.get(),
            'api_base_url': self.api_base_url_entry.get(),
            'model': self.model_entry.get()
        })
        self.result = True
        self.destroy()

    def cancel(self):
        """Close the dialog window without saving"""
        self.result = False
        self.destroy()