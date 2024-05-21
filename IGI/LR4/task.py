from abc import ABC, abstractmethod
'''task module'''

class Task(ABC):
    '''task module'''
    @staticmethod
    @abstractmethod
    def complete_task():
        pass