import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from settings_view import SettingsFrame
import os
import threading
import asyncio

class MainWindow(TkinterDnD.Tk):
    def __init__(self, settings, file_processor, ai_service):
        super().__init__()

        # Initialize components
        self.settings = settings
        self.file_processor = file_processor
        self.ai_service = ai_service
        
        # Add processing status flag
        self.is_processing = False
        
        # Set window title and size
        self.title("Renami - AI File Renamer")
        
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
        self.supported_extensions = ('.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.jpg', '.jpeg', '.png', '.txt', '.md', '.json', '.csv', 'xml', '.html')
        self.displayed_supported_extensions = ('PDF', 'PowerPoint', 'Word', 'Excel', 'Images (JPG, PNG)', 'HTML', 'Text-based formats (Markdown, CSV, JSON, XML)')


        # Create container frame for switching between views
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)

        # Initialize main and settings frames
        self.main_frame = self.create_main_frame()
        self.settings_view = None # Lazy loaded (not created until needed)

        # Show main frame initially
        self.show_main_view()

    def create_main_frame(self):
        """Create primary view frame"""
        # Create main frame
        main_frame = ttk.Frame(self.container)

        # Create settings button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', padx=20, pady=10)

        # Create settings button within button frame
        self.settings_button = ttk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self.show_settings_view,
            width=15
        )
        self.settings_button.pack(side='right', padx=10)

        # Create drop frame
        self.drop_frame = ttk.Frame(main_frame)
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
            text="Supported file types: " + ", ".join(self.displayed_supported_extensions),
            font=('TkDefaultFont', 8, 'italic'),
            foreground='gray',
            background='white'
        )
        self.supported_file_types_label.pack(side='bottom', pady=(10))

        # Bind different drop events
        self.drop_label.bind("<Button-1>", self.on_click)
        self.drop_label.drop_target_register(DND_FILES) # Register drop label as drop target
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
        self.status_label = ttk.Label(main_frame, text="Ready", font=('TkDefaultFont', 10))
        self.status_label.pack(pady=10)

        return main_frame

    def show_main_view(self):
        """Show application main view"""
        if self.settings_view:
            self.settings_view.pack_forget()
        self.main_frame.pack(fill='both', expand=True)

    def show_settings_view(self):
        """Show application settings view"""
        # Hide main frame
        self.main_frame.pack_forget()

        # Lazy load settings frame if not already created
        if not self.settings_view:
            self.settings_view = SettingsFrame(
                self.container,
                self.settings,
                self.ai_service,
                on_back=self.show_main_view
            )
        self.settings_view.pack(fill='both', expand=True)

    def on_click(self, event=None):
        """Handle click event on drop zone label to open file dialog"""
        # Ignore click if already processing
        if self.is_processing:
            self._flash_label_warning(self.drop_label)
            return

        # Open file dialog to select files
        file_paths = filedialog.askopenfilename(
            title="Select files to rename",
            filetypes=[
                ("All supported files", " ".join(f"*{ext}" for ext in self.supported_extensions))
            ],
            multiple=True
        )

        if file_paths:
            # Start processing in a separate thread
            threading.Thread(target=self._files_processing_thread, args=(file_paths,)).start() # (file_paths,) here is a single item tuple for meeting requirements of args

    def on_drop(self, event):
        """Handle file drop event"""
        # Ignore drop if already processing
        if self.is_processing:
            self._flash_label_warning(self.drop_label)
            return

        # Get list of file paths from drop event
        file_paths = self.tk.splitlist(event.data)
        
        # Start processing in a separate thread
        threading.Thread(target=self._files_processing_thread, args=(file_paths,)).start() # (file_paths,) here is a single item tuple for meeting requirements of args

    def on_drag_enter(self, _):
        """Handle drag enter event"""
        # NOT WORKING AS EXPECTED, style not applied
        self.drop_label.configure(style='DropHover.TLabel')

    def on_drag_leave(self, _):
        """Handle drag leave event"""
        self.drop_label.configure(style='Drop.TLabel')

    def _flash_label_warning(self, label, miliseconds=500):
        """Flash the drop label red to indicate processing is in progress"""
        # Get current label color
        current_color = label.cget('foreground')
        # Change label color to red
        label.configure(foreground='red')
        # Schedule return to original color for flash effect
        self.after(miliseconds, lambda: label.configure(foreground=current_color))

    def _files_processing_thread(self, file_paths):
        """"Dedicated thread for file processing"""
        # Set processing flag
        self.is_processing = True

        # Update drop label
        self.after(0, lambda: [
            self.drop_label.configure(text="⏳ Processing files...\nPlease wait until finished"),
            self.drop_label.configure(foreground='gray')
        ])
        
        # Process files using asyncio.run
        results = asyncio.run(self.process_files(file_paths)) # blocking call - will wait until the process is finished before moving to the next line

        # Update status label AFTER processing
        self.after(0, self._update_final_status, results, file_paths)
        
        # Reset processing flag
        self.is_processing = False

        # Restore drop label
        self.after(0, lambda: [
            self.drop_label.configure(text="Drag and drop files here\nor click to select files"),
            self.drop_label.configure(foreground='black')
        ])

    def _update_final_status(self, results, file_paths):
        """Update final processing status after all files have been processed"""
        # Successful file count
        success_count = 0
        for result in results:
            if result:
                success_count += 1

        # Total file count
        total_count = len(file_paths)

        if success_count == total_count:
            self.status_label.configure(text=f"✅ Successfully processed all {total_count} file(s)", foreground="green")
        elif success_count > 0:
            self.status_label.configure(text=f"⚠️ Processed {success_count}/{total_count} file(s) successfully", foreground="orange")
        else:
            self.status_label.configure(text=f"❌ Failed to process all {total_count} file(s)", foreground="red")

    async def process_files(self, file_paths):
        """Process files concurrently and update processing status"""
        async def process_single_file(file_path):
            # Check if file exists
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found: {file_path}")
                return False

            # Check if file type is supported
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension not in self.supported_extensions:
                messagebox.showerror("Error", f"Unsupported file type: {file_extension}")
                self._flash_label_warning(self.supported_file_types_label, miliseconds=2000)
                return False

            # Check if API key is set
            llm_provider = self.settings.get("llm_provider")
            if not self.settings.get(f"{llm_provider}_api_key"):
                messagebox.showerror("Error", "Please set your API key first")
                self.show_settings_view()
                return False
        
            # Update status label before processing a single file
            self.after(0, self._update_processing_status, os.path.basename(file_path))

            # Call process_file method passed from file_processor
            success, message = await self.file_processor.rename_file(file_path)

            # Update status label after processing a single file
            self.after(0, self._update_processing_status, os.path.basename(file_path), success, message)

            return success
        
        # Create and gather concurrent tasks
        tasks = []
        for file_path in file_paths:
            task = asyncio.create_task(process_single_file(file_path))
            tasks.append(task)

        # Gather results
        return await asyncio.gather(*tasks, return_exceptions=True) # return_exceptions=True will not stop the process even if one of the tasks raises an exception

    def _update_processing_status(self, original_file_name, success=None, message=None):
        """Update status label before processing a file"""
        # Before processing (not received success status)
        if success is None:
            self.status_label.configure(text=f"Processing {original_file_name}...", foreground="black")
        # After processing
        elif success:
            self.status_label.configure(text=f"✅ Renamed to: {message}", foreground="green")
        else:
            self.status_label.configure(text=f"❌ Failed to rename: {message}", foreground="red")
            messagebox.showerror("Error", message)