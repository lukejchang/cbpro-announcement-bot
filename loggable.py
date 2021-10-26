from datetime import datetime


class Loggable:
    log_name = "Unknown"

    def log(self, string):
        now_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{now_str}] [{self.log_name}] {string}")
