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

                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides file naming suggestions based on the file content.When asking to rename a file, you always keep the original file extension and only output file new file name without any other text."
                    },
                    {
                        "role": "user",
                        "content": f"Please suggest a new name based on the following information: file extension: {file_extension}, file content: {file_content}"
                    }
                ]

                response = client.chat.completions.create(
                    model=self.settings.get('model'),
                    messages=messages,
                    temperature=0.7
                )

                print(f"\n\n\n-----------------\n\n\nAI Service Response: {response.choices[0].message.content.strip()}")

            return True, response.choices[0].message.content.strip()
            
        except Exception as e:
            return False, f"AI Service Error: {str(e)}"