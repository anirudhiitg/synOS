import pandas as pd
import numpy as np
from datetime import timedelta

def generate_task_data(days=90):
    start_date = pd.Timestamp('2026-07-01 00:00:00')
    tasks = []
    
    # 5 Forklifts, 5 Conveyors
    forklifts = [f'FL-0{i}' for i in range(1, 6)]
    conveyors = [f'CV-0{i}' for i in range(1, 6)]
    
    current_time = start_date
    end_date = start_date + timedelta(days=days)
    task_id_counter = 1000
    
    while current_time < end_date:
        # Generate a task every 1 to 2 minutes to simulate 24/7 continuous operation
        current_time += timedelta(seconds=np.random.randint(60, 120))
        
        # Determine Task Type and Robot
        is_pallet = np.random.choice([True, False])
        task_type = 'Pallet' if is_pallet else 'Material'
        robot_id = np.random.choice(forklifts) if is_pallet else np.random.choice(conveyors)
        
        # 1. System Latency: Time Assigned (5 to 30 seconds after creation)
        time_assigned = current_time + timedelta(seconds=np.random.randint(5, 30))
        
        # 2. FIFO Inefficiency: Empty Travel Time (3.5 to 5.5 minutes)
        # Represents robots deadheading across the facility due to naive chronological assignment
        travel_empty_seconds = np.random.randint(210, 330)
        time_arrived = time_assigned + timedelta(seconds=travel_empty_seconds)
        
        # 3. The Counter-Pattern: Shift Change Bottleneck
        # Shifts change at 6:00, 14:00, 22:00. Spikes wait time to 8-15 mins.
        hour = time_arrived.hour
        is_shift_change = hour in [5, 6, 13, 14, 21, 22] and (time_arrived.minute > 45 or time_arrived.minute < 30)
        
        if is_shift_change:
            station_wait_seconds = np.random.randint(480, 900) # 8 to 15 mins
        else:
            station_wait_seconds = np.random.randint(15, 45)   # Normal 15 to 45 secs
            
        time_pick = time_arrived + timedelta(seconds=station_wait_seconds)
        
        # 4. Loaded Travel Time: 2 to 4 minutes to storage/dispatch
        time_drop = time_pick + timedelta(seconds=np.random.randint(120, 240))
        
        tasks.append({
            'Task_ID': f'T-{task_id_counter}',
            'Task_Type': task_type,
            'Time_Created': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Time_Assigned': time_assigned.strftime('%Y-%m-%d %H:%M:%S'),
            'Robot_ID': robot_id,
            'Time_Robot_Arrived_Pick': time_arrived.strftime('%Y-%m-%d %H:%M:%S'),
            'Time_Pick_Complete': time_pick.strftime('%Y-%m-%d %H:%M:%S'),
            'Time_Drop_Complete': time_drop.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        task_id_counter += 1
        
    df = pd.DataFrame(tasks)
    df.to_csv('syncos_task_execution_log.csv', index=False)
    print(f"Generated {len(df)} tasks and saved to syncos_task_execution_log.csv")
    return df

if __name__ == "__main__":
    generate_task_data(90)