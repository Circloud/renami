from settings import Settings
from ai_service import AIService
from file_processor import FileProcessor
from main_window import MainWindow

def main():
    # Initialize components
    settings = Settings()
    ai_service = AIService(settings)
    file_processor = FileProcessor(settings, ai_service)

    # Initialize main window
    app = MainWindow(settings, file_processor, ai_service)
    app.mainloop()

if __name__ == "__main__":
    main()