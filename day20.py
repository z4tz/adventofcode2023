import os
from inputreader import aocinput
from collections import deque, Counter
import math


class Module:
    def __init__(self, name: str, destinations: list[str]):
        self.name = name
        self.destinations = destinations

    def receive(self, sender: str, pulse: str) -> tuple[str, bool, list[str]]:
        raise NotImplementedError

    def __repr__(self):
        return f'{self.__class__.__name__} {self.name} {self.destinations}'


class FlipFlop(Module):
    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
        self.state = False

    def receive(self, sender: str, pulse: str) -> tuple[str, bool, list[str]]:
        if not pulse:
            self.state = not self.state
            return self.name, self.state, self.destinations


class Conjunction(Module):
    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
        self.inputs = {}

    def add_input(self, input_name: str):
        self.inputs[input_name] = False

    def receive(self, sender: str, pulse: bool) -> tuple[str, bool, list[str]]:
        self.inputs[sender] = pulse
        return self.name, not all(self.inputs.values()), self.destinations


class Broadcast(Module):
    def receive(self, sender: str, pulse: bool) -> tuple[str, bool, list[str]]:
        return self.name, pulse, self.destinations


def pulse_counting(data: list[str]) -> tuple[int, int]:
    modules = {}
    conjunctions = []
    for line in data:
        sender, destinations = line.strip().split(' -> ')
        destinations = destinations.split(', ')
        if sender == 'broadcaster':
            modules[sender] = Broadcast(sender, destinations)
        elif sender.startswith('%'):
            modules[sender[1:]] = FlipFlop(sender[1:], destinations)
        elif sender.startswith('&'):
            modules[sender[1:]] = Conjunction(sender[1:], destinations)
            conjunctions.append(sender[1:])

    for module in modules:  # connect any module sending to conjunction modules
        for conjunction in conjunctions:
            if conjunction in modules[module].destinations:
                modules[conjunction].add_input(module)

    cycle_dependant = []  # get which modules send signals to the conjunction module below rx
    for module in modules.values():
        if 'rx' in module.destinations:
            cycle_dependant.extend(module.inputs.keys())

    signals = Counter()
    cycle_times = dict()
    for i in range(5000):
        actions = deque([('button', False, ['broadcaster'])])
        while actions:
            sender, signal, destinations = actions.pop()
            if i < 1000:  # part 1
                signals[signal] += len(destinations)
            if sender in cycle_dependant and signal:  # part 2
                cycle_times[sender] = i + 1
            for destination in destinations:
                try:
                    response = modules[destination].receive(sender, signal)
                except KeyError:
                    response = None
                if response:
                    actions.append(response)

    return signals[False] * signals[True], math.lcm(*cycle_times.values())


def main(day: int):
    data = aocinput(day)
    results = pulse_counting(data)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
