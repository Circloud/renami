# Renami

A simple and easy to use desktop application that uses LLM to rename files based on their content. No command line needed, beginner friendly.

## Features

- AI-powered file name suggestions based on file content
- Customizable settings for API configuration, allowing for custom API keys, base URLs, and models
- Various file types supported: .pdf, .docx, .doc, .pptx, .ppt, .xlsx, .xls, .jpg, .jpeg, .png, .txt, .md, .json, .csv, xml, .html
- Drag-and-drop interface for easy file selection
- Batch processing of files

## Usage

1. Download the latest version of the application from [Releases](https://github.com/Circloud/renami/releases)
2. **Unzip the file** and run `Renami.exe` in the unzipped folder
3. Click on the "Settings" button to configure the AI related settings.
4. Drag and drop files onto the application window or click to open file dialog
5. Program will extract file content and call LLM API to get a suggested new name

## TODO

- [x] Optimize settings dialog
- [x] Refine prompt for better renaming results
- [x] Add support for multiple LLM API providers
- [x] Optimize UI on settings view
- [x] Better handle API call errors (e.g. excessive request delay, api key error, rate limit error, etc.)
- [x] Support API connection test on settings view
- [x] Test and add support for other file types
- [ ] Add support for customizing file naming conventions, e.g. camel case, snake case, etc.
- [ ] Add support for multi-language renaming
- [ ] Refactor ai_service.py to make it more maintainable
- [ ] Refactor config.json to nested structure to replace current hardcoded llm providers
- [ ] Refactor API base URL formatting logic (move to settings_view.py)
- [ ] Introduce async function to handle API calls (both verify credentials and rename)
- [ ] Optimize the API calling logic to reduce batch processing time
- [ ] Refine API calling for structured output
- [ ] v2.0.0 plan: Add support for specific folder monitoring and auto-rename

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