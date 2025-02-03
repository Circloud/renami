from tkinter import ttk, StringVar, messagebox

class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent, text=""):
        super().__init__(parent)
        
        # Create variables for state
        self.text = text
        self.show = False
        
        # Create toggle button
        self.toggle_button = ttk.Button(
            self,
            text="▶ " + self.text,
            width=25,
            command=self.toggle
        )
        self.toggle_button.pack(pady=(5,20))
        
        # Create sub frame for content
        self.sub_frame = ttk.Frame(self)
    
    def toggle(self):
        """Toggle the visibility of the sub frame"""
        if self.show:
            self.sub_frame.pack_forget()
            self.toggle_button.configure(text="▶ " + self.text)
        else:
            self.sub_frame.pack(fill="x")
            self.toggle_button.configure(text="▼ " + self.text)
        self.show = not self.show

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, settings, ai_service, on_back):
        super().__init__(parent)

        # Initializing components
        self.settings = settings
        self.on_back = on_back
        self.ai_service = ai_service

        # Initialize StringVars for tracking changes
        self.setting_vars = {
            'llm_provider': StringVar(value=settings.get('llm_provider')),
            'openai_api_key': StringVar(value=settings.get('openai_api_key')),
            'openai_api_base_url': StringVar(value=settings.get('openai_api_base_url')),
            'openai_model': StringVar(value=settings.get('openai_model')),
            'deepseek_api_key': StringVar(value=settings.get('deepseek_api_key')),
            'deepseek_api_base_url': StringVar(value=settings.get('deepseek_api_base_url')),
            'deepseek_model': StringVar(value=settings.get('deepseek_model')),
            'gemini_api_key': StringVar(value=settings.get('gemini_api_key')),
            'gemini_api_base_url': StringVar(value=settings.get('gemini_api_base_url')),
            'gemini_model': StringVar(value=settings.get('gemini_model'))
        }
        
        # Add trace to variables
        for var in self.setting_vars.values():
            var.trace_add('write', self.on_setting_changed)

        # Initialize main frame
        self.main_frame = self.create_main_frame()
        
    def create_main_frame(self):
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)  # Make column 1 (content area) horizontally expandable
        self.grid_rowconfigure(0, weight=1)     # Make row 0 (content area and sidebar) vertically expandable

        # Create sidebar frame
        self.sidebar_frame = ttk.Frame(self, style='Sidebar.TFrame')
        self.sidebar_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=10)

        # Style configuration for sidebar
        style = ttk.Style()
        style.configure('Sidebar.TFrame', background='#f0f0f0')
        style.configure('SidebarBtn.TButton', padding=10)
                
        # Create content frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=1, sticky='nsew', padx=(0,10), pady=10)
        
        # Initialize settings sections
        self.sections = {
            'AI Service': self.create_ai_service_section,
            'About': self.create_about_section
        }

        # Create sidebar buttons
        for section in self.sections:
            btn = ttk.Button(
                self.sidebar_frame,
                text=section,
                style='SidebarBtn.TButton',
                command=lambda s=section: self.show_section(s)
            )
            btn.pack(fill='x', padx=5, pady=2)
            
        # Show initial section
        self.show_section('AI Service')
        
        # Create back button
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.button_frame, text="Back", command=self.on_back).pack(side='left', padx=5)

    def on_setting_changed(self, *args):
        """Called whenever a setting value changes"""
        # Create a new dictionary with current new settings values
        updated_settings = {}
        for key, var in self.setting_vars.items():
            updated_settings[key] = var.get()
        
        # Update settings with new values
        self.settings.update(updated_settings)

    def show_section(self, section):
        """Switch between different sections in same content frame"""
        # Clear widgets in content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Create new section content
        self.sections[section]() # Look up dictionary by section name and call corresponding function to create widgets

    def create_ai_service_section(self):
        """Create API settings section"""
        frame = ttk.LabelFrame(self.content_frame, text="AI Service Configuration")
        frame.pack(fill='x')
        
        # LLM Provider
        ttk.Label(frame, text="LLM Provider").pack(pady=(20,5))
        self.llm_provider_combo = ttk.Combobox(
            frame,
            width=62, # Set width to 62 to match the width of the entry field
            textvariable=self.setting_vars['llm_provider'],
            state='readonly'
            )
        self.llm_provider_combo['values'] = ('openai', 'deepseek', 'gemini')
        self.llm_provider_combo.pack(pady=(5, 20))
        
        # Create frame for llm provider-specific settings
        self.provider_settings_frame = ttk.Frame(frame)
        self.provider_settings_frame.pack(fill='x', padx=5, pady=5)
        
        # Bind the combobox selection event
        self.llm_provider_combo.bind('<<ComboboxSelected>>', self.show_provider_settings)
        
        # Initialize with current provider's settings
        self.show_provider_settings()
        
    def show_provider_settings(self, event=None):
        """Show the llm provider-specific settings forms based on selected provider"""
        # Clear existing settings
        for widget in self.provider_settings_frame.winfo_children():
            widget.destroy()
        
        # Get the selected llm provider to determine which provider-specific settings to show
        llm_provider = self.settings.get('llm_provider')

        # Create API key label
        ttk.Label(self.provider_settings_frame, text="API Key").pack(pady=5)

        # Create frame for API key entry and verify button
        entry_frame = ttk.Frame(self.provider_settings_frame)
        entry_frame.pack(anchor='center', pady=(5, 20))

        # Create API key entry
        self.api_key_entry = ttk.Entry(
            entry_frame, 
            show='*', 
            width=54,
            textvariable=self.setting_vars[f'{llm_provider}_api_key']
        )
        self.api_key_entry.pack(side='left')

        # Create verify button
        verify_button = ttk.Button(
            entry_frame,
            text="Verify",
            width=10,
            command=self.verify_credentials
        )
        verify_button.pack(side='left', padx=(0, 0))

        # Create collapsible frame for advanced settings
        advanced_settings_frame = CollapsibleFrame(self.provider_settings_frame, text="Advanced Settings")
        advanced_settings_frame.pack(fill="x", pady=(5, 20))
        
        # Create API base URL form inside collapsible frame
        ttk.Label(advanced_settings_frame.sub_frame, text="API Base URL").pack(pady=5)
        self.api_base_url_entry = ttk.Entry(
            advanced_settings_frame.sub_frame, 
            width=65, 
            textvariable=self.setting_vars[f'{llm_provider}_api_base_url']
        )
        self.api_base_url_entry.pack(pady=(5, 20))
        
        # Create model name form inside collapsible frame
        ttk.Label(advanced_settings_frame.sub_frame, text="Model Name").pack(pady=5)
        self.model_entry = ttk.Entry(
            advanced_settings_frame.sub_frame, 
            width=65, 
            textvariable=self.setting_vars[f'{llm_provider}_model']
        )
        self.model_entry.pack(pady=(5, 20))

    def verify_credentials(self):
        """Verify the credentials for the selected LLM provider"""
        success, message = self.ai_service.verify_credentials()
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def create_about_section(self):
        """Create about section with improved typography and layout"""
        # Main about frame
        frame = ttk.LabelFrame(self.content_frame, text="About")
        frame.pack(fill='x')
        
        # App title label
        title_label = ttk.Label(
            frame, 
            text="Renami",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(10, 15))
        
        # Description text label
        description_text = (
            "A simple and easy to use desktop application that uses LLM\n"
            "to rename files based on their content.\n"
            "No command line needed, beginner friendly."
        )
        description_label = ttk.Label(
            frame,
            text=description_text,
            justify='center',
            wraplength=400
        )
        description_label.pack(pady=(0, 15))
        
        # Version info label
        version_label = ttk.Label(
            frame,
            text="Version: 1.2.0",
            font=('Helvetica', 10)
        )
        version_label.pack(pady=(0, 10))