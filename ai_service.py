import openai

class AIService:
    def __init__(self, settings):
        self.settings = settings

    def verify_credentials(self):
        """Verify if the API credentials are valid by making a minimal API call"""
        # Get the LLM provider to use provider-specific settings
        llm_provider = self.settings.get('llm_provider')
        print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials LLM Provider:\n\n{llm_provider}")
        
        with openai.OpenAI(
            api_key=self.settings.get(f'{llm_provider}_api_key'),
            base_url=self.settings.get(f'{llm_provider}_api_base_url')
        ) as client:
            
            try:
                # Make a minimal API call to verify the credentials
                response = client.chat.completions.create(
                    model=self.settings.get(f'{llm_provider}_model'),
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Response:\n\n{response.choices[0].message.content.strip()}")
                return True, "Connection successful"
                
            except openai.AuthenticationError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Error:\n\n{e}")
                return False, "AI Service Error: Invalid API key"
            
            except openai.APITimeoutError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Error:\n\n{e}")
                return False, "AI Service Error: API timeout"
            
            except openai.APIConnectionError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Error:\n\n{e}")
                return False, "AI Service Error: Base URL or network configuration error"
            
            except openai.NotFoundError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Error:\n\n{e}")
                return False, "AI Service Error: Model name or base url error"
            
            except openai.RateLimitError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Error:\n\n{e}")
                return False, "AI Service Error: Request rate limit exceeded"

            except openai.APIError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService verify_credentials Error:\n\n{e}")
                return False, "AI Service Error: Unexpected error"

    def get_suggestion(self, file_content, file_extension):
        # Get the LLM provider to use provider-specific settings
        llm_provider = self.settings.get('llm_provider')
        print(f"\n\n\n-----------------\n\n\n# AIService LLM Provider:\n\n{llm_provider}")

        # Define general system and user prompts
        system_prompt = """
        You are an assistant that provides file naming suggestions based on the file content.
        When asked to rename a file, you always follow the rules below:
        1. Keep the original file extension
        2. Only output file new file name without any other text
        3. Since the content of the parsed files lacks a hierarchical structure, please make sure to come up with a file name that takes all the file content into account.
        """

        user_prompt = f"Please suggest a new name based on the following information: file extension: {file_extension}, file content: {file_content}"

        with openai.OpenAI(
            api_key=self.settings.get(f'{llm_provider}_api_key'),
            base_url=self.settings.get(f'{llm_provider}_api_base_url')
        ) as client:

            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
            
            try:
                response = client.chat.completions.create(
                    model=self.settings.get(f'{llm_provider}_model'),
                    messages=messages,
                    temperature=0.7
                )

                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Response:\n\n{response.choices[0].message.content.strip()}")

                return True, response.choices[0].message.content.strip()
            
            except openai.AuthenticationError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Error:\n\n{e}")
                return False, "AI Service Error: Invalid API key"
            
            except openai.APITimeoutError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Error:\n\n{e}")
                return False, "AI Service Error: API timeout"
            
            except openai.APIConnectionError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Error:\n\n{e}")
                return False, "AI Service Error: Base URL or network configuration error"
            
            except openai.NotFoundError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Error:\n\n{e}")
                return False, "AI Service Error: Model name or base url error"
            
            except openai.RateLimitError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Error:\n\n{e}")
                return False, "AI Service Error: Request rate limit exceeded"

            except openai.APIError as e:
                print(f"\n\n\n-----------------\n\n\n# AIService get_suggestion Error:\n\n{e}")
                return False, "AI Service Error: Unexpected error"