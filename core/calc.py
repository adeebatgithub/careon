import math


def next_even(n):
    return n if n % 2 == 0 else n + 1


class Calculator:
    def __init__(self, occasion: float, observed_time: float, performance: int, relaxation: int, demand: int):
        self.occasion = occasion
        self.observed_time = observed_time
        self.performance = performance
        self.relaxation = relaxation
        self.demand = demand

    def normal_time(self):
        return self.occasion * self.observed_time * (self.performance / 100)

    def standard_time(self):
        return self.normal_time() * (1 + self.relaxation / 100)

    def takt_time(self):
        return 480 / self.demand

    def total_time(self):
        return self.standard_time() * self.demand

    def number_of_workers(self, factor: int = 1):
        return (self.standard_time() / self.takt_time()) * factor


def body_cuff_cutting(demand: int):
    body = Calculator(
        occasion=1 / 1400,
        observed_time=30,
        performance=100,
        relaxation=15,
        demand=demand
    )
    cuff = Calculator(
        occasion=1 / 25,
        observed_time=40 / 60,
        performance=100,
        relaxation=15,
        demand=demand
    )
    return {
        "required": ((body.standard_time() + cuff.standard_time()) / body.takt_time()) * 3,
        "default": 4,
        "_std_time": body.standard_time() + cuff.standard_time(),
    }


def welcrow_cutting(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=0.03,
        performance=100,
        relaxation=15,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 1,
        "_std_time": calc.standard_time(),
    }


def welcrow_attachment(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=10 / 60,
        performance=95,
        relaxation=17,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(factor=2),
        "default": 6,
        "_std_time": calc.standard_time(),
    }


def reinforcement_attachment(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=15 / 60,
        performance=100,
        relaxation=15,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(factor=2),
        "default": 6,
        "_std_time": calc.standard_time(),
    }


def tie_attachment(demand: int, nos: int):
    if nos == 1:
        observed_time = 11 / 60
    elif nos == 2:
        observed_time = 0.32
    else:
        print("tie: not a valid nos")
        return

    calc = Calculator(
        occasion=1,
        observed_time=observed_time,
        performance=90,
        relaxation=15,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(factor=2),
        "default": 12,
        "_std_time": calc.standard_time(),
    }


def sleeve_attachment(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=42 / 60,
        performance=105,
        relaxation=16,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 24,
        "_std_time": calc.standard_time(),
    }


def neck_tie_attachment(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=0.25,
        performance=95,
        relaxation=18,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 6,
        "_std_time": calc.standard_time(),
    }


def cuff_attachment(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=11 / 60,
        performance=100,
        relaxation=15,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 6,
        "_std_time": calc.standard_time(),
    }


def thread_cutting(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=14 / 60,
        performance=85,
        relaxation=16,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 6,
        "_std_time": calc.standard_time(),
    }


def taging(demand: int):
    calc = Calculator(
        occasion=1,
        observed_time=20 / 60,
        performance=80,
        relaxation=15,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 8,
        "_std_time": calc.standard_time(),
    }


def folding(demand: int, folding_type: int):
    if folding_type == 1:
        observed_time = 35 / 60
        factor = 2
    elif folding_type == 0:
        observed_time = 0.83
        factor = 1
    else:
        return

    calc = Calculator(
        occasion=1,
        observed_time=observed_time,
        performance=90,
        relaxation=17,
        demand=demand
    )

    if folding_type == 1:
        return {
            "required": next_even(calc.number_of_workers(factor=factor)),
            "default": 24,
            "_std_time": calc.standard_time(),
        }
    return {
        "required": calc.number_of_workers(),
        "default": 24,
        "_std_time": calc.standard_time(),
    }


def packing(demand: int):
    calc = Calculator(
        occasion=1 / 100,
        observed_time=2,
        performance=85,
        relaxation=16,
        demand=demand
    )
    return {
        "required": calc.number_of_workers(),
        "default": 2,
        "_std_time": calc.standard_time(),
    }


def number_of_workers(demand: int, nos_tie: int, folding_type: int, attached: int):
    number_of_workers_activity = {
        "body_cuff_cutting": body_cuff_cutting(demand),
        "welcrow_cutting": welcrow_cutting(demand),
        "welcrow_attachment": welcrow_attachment(demand),
        "reinforcement_attachment": reinforcement_attachment(demand) if attached == 1 else {"default": 0,
                                                                                            "required": 0},
        "tie_attachment": tie_attachment(demand, nos_tie),
        "sleeve_attachment": sleeve_attachment(demand),
        "neck_tie_attachment": neck_tie_attachment(demand),
        "cuff_attachment": cuff_attachment(demand),
        "thread_cutting": thread_cutting(demand),
        "tagging": taging(demand),
        "folding": folding(demand, folding_type),
        "packing": packing(demand)
    }
    return number_of_workers_activity

def total_number_of_workers(demand: int, nos_tie: int, folding_type: int, attached: int):
    number_of_workers_activity = number_of_workers(demand, nos_tie, folding_type, attached)
    total_number_of_workers_activity = {k:math.ceil(v.get("required")) for k, v in number_of_workers_activity.items()}
    for activity in ("welcrow_attachment", "reinforcement_attachment", "tie_attachment"):
        if activity in total_number_of_workers_activity:
            total_number_of_workers_activity[activity] = next_even(total_number_of_workers_activity[activity])
    return sum(total_number_of_workers_activity.values()), number_of_workers_activity


if __name__ == "__main__":
    kwargs = {
        "demand": 1,
        "nos_tie": 1,
        "folding_type": 1,
        "attached": 1,
    }

    w1 = total_number_of_workers(**kwargs)