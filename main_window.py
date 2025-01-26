import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from settings_dialog import SettingsDialog
import os

class MainWindow(TkinterDnD.Tk):
    def __init__(self, settings, file_processor):
        super().__init__()

        # Initialize components
        self.settings = settings
        self.file_processor = file_processor
        
        # Set window title and size
        self.title("AI Renamer")
        
        # Withdraw window initially to prevent flash
        self.withdraw()
        
        # Set default size
        self.geometry("800x600")
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"800x600+{x}+{y}")
        
        # Show the window in its final position (centered)
        self.deiconify()

        # Supported file types
        self.supported_extensions = ('.jpg', '.jpeg', '.png', '.docx', '.pdf', '.html')

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill='x', padx=20, pady=10)

        # Create settings button within button frame
        self.settings_button = ttk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            width=15
        )
        self.settings_button.pack(side='right', padx=10)

        # Create drop frame
        self.drop_frame = ttk.Frame(self.main_frame)
        self.drop_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Create drop zone label
        self.drop_label = ttk.Label(
            self.drop_frame,
            text="Drag and drop files here\nor click to select files",
            padding=50,
            style='Drop.TLabel',
        )
        self.drop_label.pack(fill='both', expand=True)

        # Create supported file types label inside drop zone
        self.supported_file_types_label = ttk.Label(
            self.drop_label,
            text="Supported file types: " + ", ".join(self.supported_extensions),
            font=('TkDefaultFont', 8, 'italic'),
            foreground='gray',
            background='white'
        )
        self.supported_file_types_label.pack(side='bottom', pady=(10))

        # Bind different drop events
        self.drop_label.bind("<Button-1>", self.on_click)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_label.dnd_bind("<<DragEnter>>", self.on_drag_enter)
        self.drop_label.dnd_bind("<<DragLeave>>", self.on_drag_leave)

        # Create custom styles for drop zone label
        style = ttk.Style()
        style.configure('Drop.TLabel',
                        relief='solid',
                        borderwidth=2,
                        background='white',
                        anchor='center')
        style.configure('DropHover.TLabel',
                        relief='solid',
                        borderwidth=2,
                        background='lightgray',
                        anchor='center')
        
        # Create status label
        self.status_label = ttk.Label(self.main_frame, text="Ready", font=('TkDefaultFont', 10))
        self.status_label.pack(pady=10) 
    
    def open_settings(self):
        """Show settings window"""
        settings_dialog = SettingsDialog(self, self.settings)

        # Make the dialog modal
        self.wait_window(settings_dialog)

    def on_click(self, event=None):
        """Handle click event on drop zone label to open file dialog"""
        # Open file dialog to select files
        file_paths = filedialog.askopenfilename(
            title="Select files to rename",
            filetypes=[
                ("All supported files", " ".join(f"*{ext}" for ext in self.supported_extensions))
            ],
            multiple=True
        )

        for file_path in file_paths:
            self.handle_processing(file_path)

    def on_drop(self, event):
        """Handle file drop event"""
        # Get file paths from event
        file_paths = self.tk.splitlist(event.data)
        for file_path in file_paths:
            self.handle_processing(file_path)

    def on_drag_enter(self, _):
        """Handle drag enter event"""
        self.drop_label.configure(style='DropHover.TLabel')

    def on_drag_leave(self, _):
        """Handle drag leave event"""
        self.drop_label.configure(style='Drop.TLabel')

    def handle_processing(self, file_path):
        """Process files and update status label"""

        # Check if file exists
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return

        # Check if file type is supported
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in self.supported_extensions:
            messagebox.showerror("Error", f"Unsupported file type: {file_extension}")
            return

        # Check if API key is set
        if not self.settings.get("api_key"):
            messagebox.showerror("Error", "Please set your API key in settings before renaming files")
            self.open_settings()
            return
        
        # Update status label before processing
        self.status_label.configure(text=f"Processing {os.path.basename(file_path)}...", foreground="black")
        self.update()

        # Call process_file method passed from file_processor
        success, message = self.file_processor.process_file(file_path)

        # Update status label based on processing result
        if success:
            self.status_label.configure(text=f"✅ {message}", foreground="green")
        else:
            self.status_label.configure(text=f"❌ {message}", foreground="red")
            messagebox.showerror("Error", message)