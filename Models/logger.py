from DB.Methods import launch_db, append_log, get_logs, last_log_index


class Logger:
    def __init__(self, arg):
        launch_db(arg)

    @staticmethod
    def log(replica_id: int, label: str, data: str):
        append_log(replica_id, label, data)

    @staticmethod
    def get_logs(index):
        return get_logs(index)

    @staticmethod
    def index():
        return last_log_index()
