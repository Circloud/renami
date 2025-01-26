import json

class Settings:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
    
    def load(self):
        """Load settings from config file"""
        with open(self.config_file, 'r') as f:
                settings = json.load(f)

                # Ensure the API base URL ends with /v1
                if settings.get('api_base_url'):
                    if not settings['api_base_url'].endswith('/v1'):
                        settings['api_base_url'] = settings['api_base_url'].rstrip('/') + '/v1'
                return settings
        
    def save(self, settings):
        """Save settings to config file"""
        with open(self.config_file, 'w') as f:
            json.dump(settings, f)

    def get(self, key, default=None):
        """Get a setting value"""
        return self.load().get(key, default)
    
    def update(self, new_settings):
        """Update settings with new values"""
        current_settings = self.load()
        current_settings.update(new_settings)
        self.save(current_settings)