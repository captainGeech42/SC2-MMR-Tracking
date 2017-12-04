import time
import os


class Log:
    filepath = None

    @staticmethod
    def get_timestamp() -> str:
        return time.strftime("%H:%M:%S")

    @staticmethod
    def write_log_message(message: str, error: bool = False):
        log_type = "ERROR" if error else "INFO"
        msg = "{} {}: {}".format(Log.get_timestamp(), log_type, message)
        print(msg)

        if Log.filepath is not None:
            try:
                log_file = open(Log.filepath, "a")
                log_file.write(msg + os.linesep)
                log_file.close()
            except OSError:
                fp = Log.filepath
                Log.filepath = None
                Log.write_log_message(
                    "Could not write to log file '{}' (no more attempts will be made to write to this file)".format(fp),
                    True)
