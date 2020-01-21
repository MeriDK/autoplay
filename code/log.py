from datetime import datetime


class Log:
    def __init__(self, path):
        self.path = path

    def log(self, line):
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} {line}\n')
