import subprocess
from abc import ABC, abstractmethod
from functools import wraps

# Command Pattern
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class FFmpegCommand(Command):
    def __init__(self, command):
        self.command = command

    def execute(self):
        subprocess.run(self.command)

# Observer Pattern
class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()

class LoadBinaryObserver:
    def update(self):
        print("Binary loaded successfully")

class ExecuteCommandObserver:
    def update(self):
        print("Command executed successfully")

# Singleton Pattern
class FFmpegLoader:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def load_binary(self):
        # Load binary implementation
        print("Binary loaded")

# Facade Pattern
class FFmpegFacade:
    def __init__(self):
        self.loader = FFmpegLoader()
        self.subject = Subject()
        self.subject.attach(LoadBinaryObserver())

    def load_binary(self):
        self.loader.load_binary()
        self.subject.notify()

    def execute_command(self, command):
        self.subject.attach(ExecuteCommandObserver())
        cmd = FFmpegCommand(command)
        cmd.execute()
        self.subject.notify()

# Decorator Pattern
def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Factory Pattern
class FFmpegCommandFactory:
    @staticmethod
    def create_command(command):
        return FFmpegCommand(command)

# Usage
ffmpeg_facade = FFmpegFacade()
ffmpeg_facade.load_binary()

@log_execution
def execute_ffmpeg_command(command):
    cmd = FFmpegCommandFactory.create_command(command)
    cmd.execute()

execute_ffmpeg_command([
    'ffmpeg',
    '-i',
    '/storage/emulated/0/Pictures/RDT_20200216_1834133821008713377834180.mp4',
    '-r',
    '10',
    '/storage/emulated/0/Pictures/vidosik.mp4'
])
