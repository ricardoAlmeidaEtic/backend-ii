from typing import List, Protocol

class Observer(Protocol):
    def update(self, state: str):
        raise NotImplementedError

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
        self._state: str = ""

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state: str):
        self._state = state
        self.notify()

class ConcreteObserverA:
    def update(self, state: str):
        print(f"ConcreteObserverA received state: {state}")

class ConcreteObserverB:
    def update(self, state: str):
        print(f"ConcreteObserverB received state: {state}")

# Example usage
if __name__ == "__main__":
    subject = Subject()

    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()

    subject.attach(observer_a)
    subject.attach(observer_b)

    subject.set_state("State 1")
    subject.set_state("State 2")