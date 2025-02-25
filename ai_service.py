import openai
from functools import wraps
import asyncio

class AIService:
    def __init__(self, settings):
        self.settings = settings

    # Internal method starts with _
    def _log(self, title, message):
        """Utility method for debugging purposes"""
        print(f"\n\n\n-----------------\n\n\n# {title}:\n\n{message}")

    # Internal method starts with _
    def _get_client(self):
        """Create and return an OpenAI client with current settings"""
        llm_provider = self.settings.get('llm_provider')
        self._log(f"AIService get_client LLM Provider", llm_provider)
        
        return openai.AsyncOpenAI(
            api_key=self.settings.get(f'{llm_provider}_api_key'),
            base_url=self.settings.get(f'{llm_provider}_api_base_url')
        )

    # Internal method starts with _
    def _handle_openai_errors(func):
        """Decorator to handle OpenAI API errors for verify_credentials and get_suggestion"""
        @wraps(func) # Preserve the original function's metadata like function name, docstring, etc.
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except openai.AuthenticationError as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: Invalid API key"
            except openai.APITimeoutError as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: API timeout"
            except openai.APIConnectionError as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: Base URL or network configuration error"
            except openai.NotFoundError as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: Model name or base url error"
            except openai.RateLimitError as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: Request rate limit exceeded"
            except openai.APIError as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: Unexpected error"
            except Exception as e:
                self._log(f"AIService {func.__name__} Error", e)
                return False, "AI Service Error: Unexpected error"
        return wrapper

    @_handle_openai_errors
    async def verify_credentials(self):
        """Verify if the API credentials are valid by making a minimal API call"""
        llm_provider = self.settings.get('llm_provider')

        try:
            async with self._get_client() as client:
                async def make_request():
                    response = await client.chat.completions.create(
                        model=self.settings.get(f"{llm_provider}_model"),
                        messages=[{"role": "user", "content": "Test"}],
                        max_tokens=1
                    )
                    return response

                timeout_sec = 6
                response = await asyncio.wait_for(make_request(), timeout=timeout_sec) # Set a forced fixed timeout

            if response:
                self._log(f"AIService verify_credentials Result", response.choices[0].message.content.strip())
                return True, "Credentials verified successfully"

        except asyncio.TimeoutError:
            error_msg = f"API timeout after {timeout_sec} seconds"
            self._log("AIService verify_credentials Error", error_msg)
            return False, f"AI Service Error: {error_msg}"

    @_handle_openai_errors
    async def get_suggestion(self, file_content, file_extension):
        """Get AI suggestion for file naming based on content"""
        llm_provider = self.settings.get('llm_provider')
        naming_language = self.settings.get('naming_language')
        naming_convention = self.settings.get('naming_convention')
        custom_instruction = self.settings.get('custom_instruction')

        if naming_language == 'en':
            if naming_convention == 'with-spaces':
                naming_convention_prompt = f"Capitalize the first letter of each word and separate words with spaces, e.g. This Is New File Name"
            elif naming_convention == 'pascal-case':
                naming_convention_prompt = "PascalCase: Capitalize the first letter of each word without spaces in between, e.g. ThisIsNewFileName"
            elif naming_convention == 'camel-case':
                naming_convention_prompt = "camelCase: Except for the first word being in lowercase, the first letter of each subsequent word is capitalized, with no spaces in between., e.g. thisIsNewFileName"
            elif naming_convention == 'snake-case':
                naming_convention_prompt = "snake_case: Lowercase each word and separate words with underscores, e.g. this_is_new_file_name"
            elif naming_convention == 'kebab-case':
                naming_convention_prompt = "kebab-case: Lowercase each word and separate words with hyphens, e.g. this-is-new-file-name"
            elif naming_convention == 'not-applicable':
                naming_convention_prompt = "This is not applicable, please ignore this requirement temporarily."

        else:
            naming_convention_prompt = "This is not applicable, please ignore this requirement temporarily."

        system_prompt = f"""
        You are an assistant that provides file naming suggestions based on the file content.
        When asked to rename a file, you always adhere to the following rules:
        1. ONLY output the suggested new file name without any additional text.
        2. Do not add any file extension to the new file name
        3. Since the content of the parsed files lacks a hierarchical structure, please make sure to come up with a file name that takes all the file content into account.
        4. Avoid using any invalid characters in new file name.
        5. Use {naming_language} for naming the file.
        6. Follow the naming convention: {naming_convention_prompt}
        ---
        Custom Instruction: {custom_instruction}
        """

        user_prompt = f"Please suggest a new file name (without extension) based on the following file content: {file_content}"

        async with self._get_client() as client:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = await client.chat.completions.create(
                model=self.settings.get(f'{llm_provider}_model'),
                messages=messages,
                temperature=0.7,
                max_tokens=50
            )

            suggestion = response.choices[0].message.content.strip()
            self._log(f"AIService get_suggestion Result", suggestion)
            return True, suggestion