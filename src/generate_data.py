import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data(num_records=100):
    agents = ['John', 'Riya', 'Agent A', 'Agent B', 'Agent C', '']
    queues = ['Sales', 'Support']
    
    data = []
    
    start_time = datetime.strptime('10:00', '%H:%M')
    
    for i in range(num_records):
        call_id = 1000 + i + 1
        queue = random.choice(queues)
        
        # Decide if answered or abandoned
        # 10% chance of abandon
        if random.random() < 0.1:
            answered = 'No'
            abandoned = 'Yes'
            agent = ''
            duration = 0
            wait_time = random.randint(30, 300) # Waited 30s to 5m before hanging up
        else:
            answered = 'Yes'
            abandoned = 'No'
            # Assign agent based on queue to make it realistic
            if queue == 'Sales':
                possible_agents = ['John', 'Agent A', 'Agent B']
            else:
                possible_agents = ['Riya', 'Agent C']
            agent = random.choice(possible_agents)
            duration = random.randint(60, 600) # 1 min to 10 mins
            wait_time = random.randint(5, 60) # Picked up within a minute usually
            
        # Call time increments slightly
        current_time = start_time + timedelta(minutes=random.randint(0, 10))
        start_time = current_time
        
        data.append({
            'call_id': call_id,
            'agent': agent,
            'queue': queue,
            'duration': duration,
            'answered': answered,
            'abandoned': abandoned,
            'time': current_time.strftime('%H:%M'),
            'wait_time': wait_time
        })
        
    df = pd.DataFrame(data)
    df.to_csv('data/call_logs.csv', index=False)
    print(f"Generated {num_records} records in data/call_logs.csv")

if __name__ == "__main__":
    generate_data(200) # Generate 200 records
