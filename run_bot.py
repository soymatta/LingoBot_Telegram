import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os


class BotHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_bot()

    def start_bot(self):
        if self.process:
            self.process.kill()
            time.sleep(1)  # Esperar a que el proceso anterior termine
        print("🔄 Iniciando el bot...")
        self.process = subprocess.Popen([sys.executable, "bot.py"])

    def on_modified(self, event):
        if event.src_path.endswith("bot.py"):
            print("📝 Cambios detectados en bot.py")
            self.start_bot()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    path = "."  # Directorio actual
    event_handler = BotHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.kill()
    observer.join()


if __name__ == "__main__":
    main()
