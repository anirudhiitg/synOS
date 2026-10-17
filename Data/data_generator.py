import pandas as pd
import numpy as np
from datetime import datetime, timedelta

NUM_TASKS = 5000
START_DATE = datetime(2026, 10, 1)
END_DATE = START_DATE + timedelta(days=7)

FL_ROBOTS = [f"FL-0{i}" for i in range(1, 6)]
CV_ROBOTS = [f"CV-0{i}" for i in range(1, 6)]
ZONES = ['Dispatch_Zone', 'Aisle_1', 'Aisle_2', 'Aisle_3', 'Charging_Bay', 'Storage_Zone']
# Weighted probabilities for locations (Dispatch and Aisle 1 are busier)
ZONE_WEIGHTS = [0.35, 0.25, 0.15, 0.10, 0.05, 0.10] 

# 1. Generate Task Execution Log with Normal Distributions
task_data = []
current_time = START_DATE

for i in range(1, NUM_TASKS + 1):
    task_id = f"T-{1000 + i}"
    # Slight imbalance: 55% Pallets, 45% Material
    task_type = np.random.choice(['Pallet', 'Material'], p=[0.55, 0.45])
    robot_id = np.random.choice(FL_ROBOTS) if task_type == 'Pallet' else np.random.choice(CV_ROBOTS)
    
    # Task arrival gaps based on time of day (busier during the day)
    hour = current_time.hour
    base_gap = 60 if 8 <= hour <= 18 else 180 
    time_created = current_time + timedelta(seconds=abs(np.random.normal(base_gap, 20)))
    
    # Durations using bell curves
    time_assigned = time_created + timedelta(seconds=abs(np.random.normal(30, 10)))
    time_arrived = time_assigned + timedelta(seconds=abs(np.random.normal(120, 40)))
    time_picked = time_arrived + timedelta(seconds=abs(np.random.normal(45, 15)))
    time_dropped = time_picked + timedelta(seconds=abs(np.random.normal(300, 60)))
    
    task_data.append([
        task_id, task_type, robot_id, time_created, time_assigned, 
        time_arrived, time_picked, time_dropped
    ])
    current_time = time_created

df_tasks = pd.DataFrame(task_data, columns=[
    'Task_ID', 'Task_Type', 'Robot_ID', 'Time_Created', 'Time_Assigned', 
    'Time_Robot_Arrived_Pick', 'Time_Pick_Complete', 'Time_Drop_Complete'
])
df_tasks.to_csv('syncos_task_execution_log.csv', index=False)

# 2. Generate Fleet State Log with Battery Tracking
fleet_data = []
log_id_counter = 1

for robot in FL_ROBOTS + CV_ROBOTS:
    current_time = START_DATE
    battery = 100.0
    state = 'Idle'
    
    while current_time < END_DATE:
        log_id = f"L-{10000 + log_id_counter}"
        
        # Battery and State Logic
        if battery <= 15.0 or (state == 'Charging' and battery < 95.0):
            state = 'Charging'
            zone = 'Charging_Bay'
            battery = min(100.0, battery + 10.0) # Charge by 10% per tick
        else:
            # 80% chance of moving, 10% blocked, 10% idle
            state = np.random.choice(['Moving_Loaded', 'Moving_Empty', 'Blocked_Traffic', 'Idle'], p=[0.5, 0.3, 0.1, 0.1])
            zone = np.random.choice(ZONES, p=ZONE_WEIGHTS)
            battery = max(0.0, battery - np.random.normal(2.0, 0.5)) # Drain by ~2% per tick
            
        fleet_data.append([log_id, current_time, robot, state, zone, round(battery, 1)])
        
        current_time += timedelta(minutes=5)
        log_id_counter += 1

df_fleet = pd.DataFrame(fleet_data, columns=[
    'Log_ID', 'Timestamp', 'Robot_ID', 'Current_State', 'Location_Zone', 'Battery_Level_Pct'
])
df_fleet = df_fleet.sort_values(['Timestamp', 'Robot_ID']).reset_index(drop=True)
df_fleet.to_csv('syncos_fleet_state_log.csv', index=False)

print("Realistic synthetic data generated.")