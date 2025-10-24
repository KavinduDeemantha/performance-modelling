import random
import statistics
import matplotlib.pyplot as plt

simulation_time = 8 * 60  # total simulation time in minutes (8 hours)
passenger_arrival_rate = 1 / 0.5  # passengers per 30 seconds(avg every 30 seconds)

# Scenarios for the simulation
scenarios = [
    {"name": "A", "bus_interval": 20, "bus_capacity": 40},
    {"name": "B", "bus_interval": 15, "bus_capacity": 40},
    {"name": "C",  "bus_interval": 15,  "bus_capacity": 30},
]

# Simulation function
def simulate_scenario(bus_interval, bus_capacity):
    time = 0
    next_passenger_arrival = random.expovariate(passenger_arrival_rate) # time of next passenger arrival
    next_bus_arrival = bus_interval

    queue = []
    waiting_times = []
    bus_occupancies = []
    queue_lengths = []

    while time < simulation_time:
        # check the next event whether passenger arrival or bus arrival
        if next_passenger_arrival < next_bus_arrival:
            # Passenger arrives
            time = next_passenger_arrival
            queue.append(time)
            next_passenger_arrival += random.expovariate(passenger_arrival_rate)
        else:
            # Bus arrives
            time = next_bus_arrival
            boarded = 0

            # Board passengers until bus full or queue empty
            while queue and boarded < bus_capacity:
                arrival_time = queue.pop(0)
                waiting_times.append(time - arrival_time)
                boarded += 1

            # Record metrics
            bus_occupancies.append(boarded)
            queue_lengths.append(len(queue))
            next_bus_arrival += bus_interval

    # Compute statistics

    avg_wait = statistics.mean(waiting_times) if waiting_times else 0
    avg_queue = statistics.mean(queue_lengths) if queue_lengths else 0
    avg_occupancy = statistics.mean(bus_occupancies) if bus_occupancies else 0

    return avg_wait, avg_queue, avg_occupancy, waiting_times, queue_lengths

# Run simulations for each scenario
results = []

for scenario in scenarios:
    avg_wait, avg_queue, avg_occupancy, wait_times, queues = simulate_scenario(
        scenario["bus_interval"], scenario["bus_capacity"]
    )
    results.append({
        "Scenario": scenario["name"],
        "Avg_Wait": avg_wait,
        "Avg_Queue": avg_queue,
        "Avg_Occupancy": avg_occupancy
    })

# Print results
print("\n--- Simulation Results (8 hours) ---")
for r in results:
    print(f"\nScenario: {r['Scenario']}")
    print(f"Average Wait Time: {r['Avg_Wait']:.2f} minutes")
    print(f"Average Queue Length: {r['Avg_Queue']:.2f} passengers")
    print(f"Average Bus Occupancy: {r['Avg_Occupancy']:.2f} passengers")

# Bar chart for Average Wait Time
plt.figure(figsize=(10,5))
plt.bar([r['Scenario'] for r in results], [r['Avg_Wait'] for r in results], color='skyblue')
plt.title("Average Passenger Wait Time by Scenario")
plt.ylabel("Minutes")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# Bar chart for Average Queue Length
plt.figure(figsize=(10,5))
plt.bar([r['Scenario'] for r in results], [r['Avg_Queue'] for r in results], color='orange')
plt.title("Average Queue Length by Scenario")
plt.ylabel("Passengers")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# Bar chart for Average Bus Occupancy
plt.figure(figsize=(10,5))
plt.bar([r['Scenario'] for r in results], [r['Avg_Occupancy'] for r in results], color='green')
plt.title("Average Bus Occupancy by Scenario")
plt.ylabel("Passengers per Bus")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()