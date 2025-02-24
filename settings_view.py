from tkinter import ttk, StringVar, messagebox
import asyncio
from version import get_version
import webbrowser
import threading

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
            'gemini_api_key': StringVar(value=settings.get('gemini_api_key')),
            'gemini_api_base_url': StringVar(value=settings.get('gemini_api_base_url')),
            'gemini_model': StringVar(value=settings.get('gemini_model')),
            'doubao_api_key': StringVar(value=settings.get('doubao_api_key')),
            'doubao_api_base_url': StringVar(value=settings.get('doubao_api_base_url')),
            'doubao_model': StringVar(value=settings.get('doubao_model')),
            'openai_compatible_api_key': StringVar(value=settings.get('openai_compatible_api_key')),
            'openai_compatible_api_base_url': StringVar(value=settings.get('openai_compatible_api_base_url')),
            'openai_compatible_model': StringVar(value=settings.get('openai_compatible_model')),
            'naming_language': StringVar(value=settings.get('naming_language')),
            'naming_convention': StringVar(value=settings.get('naming_convention'))
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
            'Naming Rules': self.create_naming_rules_section,
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
        """Create API settings section for configuring LLM providers"""
        # Main container frame
        frame = ttk.LabelFrame(self.content_frame, text="AI Service Configuration")
        frame.pack(fill='x')

        # ===== LLM Provider Setting =====
        # Internal-display name mapping for llm providers
        self.llm_provider_name_map = {
            'openai': 'OpenAI Official',
            'gemini': 'Google Gemini Official',
            'doubao': 'ByteDance Doubao Official',
            'openai_compatible': 'OpenAI Compatible (Most Third-party Services)'
        }

        # Create LLM provider combobox
        ttk.Label(frame, text="LLM Provider").pack(pady=(20,5))
        self.llm_provider_combo = ttk.Combobox(
            frame,
            width=62,
            state='readonly'
        )

        # Show display name in combobox
        self.llm_provider_combo['values'] = [self.llm_provider_name_map[name] for name in self.llm_provider_name_map]
        self.llm_provider_combo.pack(pady=(5, 20))

        # Initialize combobox with display name from config
        current_internal_name = self.setting_vars['llm_provider'].get()
        self.llm_provider_combo.set(self.llm_provider_name_map[current_internal_name])

        # ===== Provider-specific Settings =====
        # Container for provider-specific settings
        self.provider_settings_frame = ttk.Frame(frame)
        self.provider_settings_frame.pack(fill='x')

        # Initialize default provider-specific settings
        self.show_provider_settings()

        def on_provider_selected(event):
            # Map display name to internal name
            selected_display_name = self.llm_provider_combo.get()
            selected_internal_name = next(k for k, v in self.llm_provider_name_map.items() if v == selected_display_name)
            # Store internal name to StringVar
            self.setting_vars['llm_provider'].set(selected_internal_name)
            # Update provider-specific settings
            self.show_provider_settings()

        # Update StringVar and show provider-specific settings when combobox is changed
        self.llm_provider_combo.bind('<<ComboboxSelected>>', on_provider_selected)

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
        self.verify_button = ttk.Button(
            entry_frame,
            text="Verify",
            width=10,
            command=self.verify_credentials
        )
        self.verify_button.pack(side='left', padx=(0, 0))

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
        # Disable verify button while verifying
        self.verify_button.configure(state='disabled')

        def verification_thread():
            # Run verification in a separate thread
            success, message = asyncio.run(self.ai_service.verify_credentials())
            # Update the UI with verification result (After verification finished)
            self.after(0, self._update_verification_result, success, message)

        # Start the verification thread
        threading.Thread(target=verification_thread, daemon=True).start()

    def _update_verification_result(self, success, message):
        # Check if verify button still exists (maybe destroyed when switching to another section)
        if self.verify_button.winfo_exists():
            self.verify_button.configure(state='normal')
            
        # Show messagebox with verification result
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def create_naming_rules_section(self):
        """Create naming rules section to configure naming rules"""
        # Main naming rules frame
        frame = ttk.LabelFrame(self.content_frame, text="Naming Rules")
        frame.pack(fill='x')

        # ===== Naming Language Setting =====
        # Create file naming language label
        ttk.Label(frame, text="File Naming Language").pack(pady=(20,5))

        # Internal-display name mapping for naming languages
        self.naming_language_name_map = {
            "en": "English",
            "zh-Hans": "Chinese (Simplified)"
        }

        # Create combobox for file naming language
        self.naming_language_combo = ttk.Combobox(
            frame,
            width=62,
            state='readonly'
        )

        # Show display name in combobox
        self.naming_language_combo['values'] = [self.naming_language_name_map[lang] for lang in self.naming_language_name_map]
        self.naming_language_combo.pack(pady=(5, 20))

        # Initialize combobox with display name from config
        current_internal_name = self.setting_vars['naming_language'].get()
        self.naming_language_combo.set(self.naming_language_name_map[current_internal_name])

        # ===== Naming Language-specific Settings =====
        # Create frame for naming language-specific settings
        self.naming_language_settings_frame = ttk.Frame(frame)
        
        def on_naming_language_selected(event):
            # Map display name to internal name
            selected_display_name = self.naming_language_combo.get()
            selected_internal_name = next(k for k, v in self.naming_language_name_map.items() if v == selected_display_name)
            # Store internal name to StringVar
            self.setting_vars['naming_language'].set(selected_internal_name)
            # Update naming language-specific settings
            self.show_naming_language_settings(selected_internal_name)
        
        # Update StringVar when combobox is changed
        self.naming_language_combo.bind('<<ComboboxSelected>>', on_naming_language_selected)

        # Show current naming language settings
        self.show_naming_language_settings(self.setting_vars['naming_language'].get())

    def show_naming_language_settings(self, naming_language):
        """Show the naming language-specific settings frame based on selected naming language"""
        # Clear existing settings
        for widget in self.naming_language_settings_frame.winfo_children():
            widget.destroy()

        if naming_language == 'en':
            # Show the language-specific settings frame
            self.naming_language_settings_frame.pack(fill='x')
            
            self.naming_convention_map = {
                "with-spaces": "With Spaces",
                "pascal-case": "PascalCase",
                "camel-case": "camelCase",
                "snake-case": "snake_case",
                "kebab-case": "kebab-case",
                "not-applicable": "N/A"
            }

            # Create combobox for naming convention
            ttk.Label(self.naming_language_settings_frame, text="Naming Convention").pack(pady=5)
            self.naming_convention_combo = ttk.Combobox(
                self.naming_language_settings_frame,
                width=62,
                state='readonly'
            )

            # Show display name in combobox
            self.naming_convention_combo['values'] = list(self.naming_convention_map.values())
            self.naming_convention_combo.pack(pady=(5,20))
            
            # Initialize combobox with display name from config
            current_internal_name = self.setting_vars['naming_convention'].get()
            self.naming_convention_combo.set(self.naming_convention_map[current_internal_name])

            # Update StringVar when combobox is changed
            def on_naming_convention_selected(event):
                # Map display name to internal name
                selected_display_name = self.naming_convention_combo.get()
                selected_internal_name = next(k for k, v in self.naming_convention_map.items() if v == selected_display_name)
                # Store internal name to StringVar
                self.setting_vars['naming_convention'].set(selected_internal_name)

            self.naming_convention_combo.bind('<<ComboboxSelected>>', on_naming_convention_selected)
            
        elif naming_language == 'zh-Hans':
            # Hide language-specific settings frame
            self.naming_language_settings_frame.pack_forget()

    def create_about_section(self):
        """Create about section to show general information about the application"""
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
            text=f"Version: {get_version()}",
            font=('Helvetica', 10)
        )
        version_label.pack(pady=(0, 10))

        # GitHub link label
        github_link = "https://github.com/Circloud/renami"
        github_link_label = ttk.Label(
            frame,
            text=f"Available at {github_link}",
            font=('Helvetica', 9),
            foreground='#666666',
            cursor="hand2"  # Changes cursor to hand when hovering
        )
        github_link_label.bind("<Button-1>", lambda e: webbrowser.open(github_link))
        github_link_label.pack(pady=(5, 10))