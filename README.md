# AI Renamer

A desktop application that uses AI to rename files based on their content.

## Features

- AI-powered file name suggestions based on file content
- Customizable settings for API configuration, allowing for custom API keys, base URLs, and models
- Various file types supported: .jpg, .jpeg, .png, .docx, .pdf, .html (more to come)
- Drag-and-drop interface for easy file selection
- Batch processing of files

## Usage

1. Launch the application by running `main.py`
2. Drag and drop files onto the application window or click to open file dialog
3. Program will extract file content and call AI to get a suggested new name
4. Review and confirm the suggested name

## TODO

- [ ] Optimize the API calling logic to reduce batch processing time
- [ ] Add support for other AI API providers
- [ ] Test and add support for other file types
- [ ] Add support for customizing file naming conventions, e.g. camel case, snake case, etc.
- [ ] Refactor settings dialog
- [ ] Add support for specific folder monitoring and auto-rename

## Privacy Considerations

Please note that when using this application:

- File contents are only sent to your configured AI service provider for name suggestions
- No file content is stored or transmitted to any other third-party services
- Your API key and other settings are stored locally on your device

## Acknowledgements

Thanks to the following libraries and services for making this possible:

- [MarkItDown](https://github.com/jxnl/markitdown)
- [OpenAI](https://openai.com)
- [tkinterdnd2](https://github.com/paul-musgrave/tkinterdnd2)