import openai

class AIService:
    def __init__(self, settings):
        self.settings = settings

    def get_suggestion(self, file_content, file_extension):
        try:
            with openai.OpenAI(
                api_key=self.settings.get('api_key'),
                base_url=self.settings.get('api_base_url')
            ) as client:

                system_prompt = """
                    You are an assistant that provides file naming suggestions based on the file content.
                    When asked to rename a file, you always follow the rules below:
                    1. Keep the original file extension
                    2. Only output file new file name without any other text
                    3. Since the content of the parsed files lacks a hierarchical structure, please make sure to come up with a file name that takes all the file content into account.
                """

                user_prompt = f"Please suggest a new name based on the following information: file extension: {file_extension}, file content: {file_content}"

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

                response = client.chat.completions.create(
                    model=self.settings.get('model'),
                    messages=messages,
                    temperature=0.7
                )

                print(f"\n\n\n-----------------\n\n\n# AI Service Response:\n\n{response.choices[0].message.content.strip()}")

            return True, response.choices[0].message.content.strip()
            
        except Exception as e:
            return False, f"AI Service Error: {str(e)}"