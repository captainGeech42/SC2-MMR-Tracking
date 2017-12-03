import time
import os


class Log:
    def __init__(self, filepath: str = None):
        self.filepath = filepath

    @staticmethod
    def get_timestamp()->str:
        return time.strftime("%H:%M:%S")

    def write_log_message(self, message: str, error: bool = False):
        log_type = "ERROR" if error else "INFO"
        msg = "{} {}: {}".format(self.get_timestamp(), log_type, message)
        print(msg)

        if self.filepath is not None:
            try:
                log_file = open(self.filepath, "a")
                log_file.write(msg + os.linesep)
                log_file.close()
            except OSError:
                fp = self.filepath
                self.filepath = None
                self.write_log_message(
                    "Could not write to log file '{}' (no more attempts will be made to write to this file)".format(fp),
                    True)
