# Renami

A simple and easy to use desktop application that uses LLM to rename files based on their content. No command line needed, beginner friendly.

## Features

- AI-powered file name suggestions based on file content
- Customizable settings for API configuration, allowing for custom API keys, base URLs, and models
- Various file types supported: .jpg, .jpeg, .png, .docx, .pdf, .html (more to come)
- Drag-and-drop interface for easy file selection
- Batch processing of files

## Usage

1. Download the application from [Releases](https://github.com/Circloud/renami/releases/download/v1.1.0/renami-windows-portable-v1.1.0.zip)
2. **Unzip the file** and run `Renami.exe` in the unzipped folder
3. Click on the "Settings" button to configure the AI related settings, **currently only OpenAI is supported.**
4. Drag and drop files onto the application window or click to open file dialog
5. Program will extract file content and call AI to get a suggested new name
6. Review and confirm the suggested name

## TODO

- [x] Optimize settings dialog
- [ ] Add support for other AI API providers
- [ ] Support API connection test on settings view
- [ ] Optimize prompt for better renaming results
- [ ] Optimize the API calling logic to reduce batch processing time
- [ ] Test and add support for other file types
- [ ] Add support for customizing file naming conventions, e.g. camel case, snake case, etc.
- [ ] Add support for specific folder monitoring and auto-rename

## Privacy Considerations

Please note that when using this application:

- File contents are only sent to your configured AI service provider for name suggestions
- No file content is stored or transmitted to any other third-party services
- Your API key and other settings are stored locally on your device

## Acknowledgements

Thanks to the following libraries for making this possible:

- [MarkItDown](https://github.com/jxnl/markitdown)
- [OpenAI](https://openai.com)
- [tkinterdnd2](https://github.com/paul-musgrave/tkinterdnd2)