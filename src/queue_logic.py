import random

class Agent:
    def __init__(self, name, status='Available'):
        self.name = name
        self.status = status # Available, Busy, Offline

class Queue:
    def __init__(self, name, agents):
        self.name = name
        self.agents = [Agent(a) for a in agents]
        self.calls_waiting = 0

    def get_status(self):
        return {
            "queue_name": self.name,
            "agents_available": len([a for a in self.agents if a.status == 'Available']),
            "agents_busy": len([a for a in self.agents if a.status == 'Busy']),
            "calls_waiting": self.calls_waiting
        }

    # Simulate random activity
    def update_simulation(self):
        # Randomly change agent status
        for agent in self.agents:
            if random.random() < 0.3: # 30% chance to change status
                agent.status = random.choice(['Available', 'Busy'])
        
        # Randomly add/remove calls from waiting
        change = random.choice([-1, 0, 1, 2])
        self.calls_waiting = max(0, self.calls_waiting + change)

# Initialize Queues
sales_queue = Queue("Sales", ["John", "Agent A", "Agent B"])
support_queue = Queue("Support", ["Riya", "Agent C"])

def get_all_queues_status():
    sales_queue.update_simulation()
    support_queue.update_simulation()
    return [sales_queue.get_status(), support_queue.get_status()]
