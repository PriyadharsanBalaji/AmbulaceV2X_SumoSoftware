#***********Read These comments before reading the file***************
#V2X along with Lane Management System for Network2-->We have used sumo software to make the simulation this code we have integrated with randomtrips file to achieve V2X simulation in SUMO software 
#We had assumed a car to be ambulance here as SUMO offers only cars in the simulations
#Seperate Lane for ambulance will be given beforehand using this system ,we have attached the photoes of an ambulance(assuming ambulance as a car) going in a seperate lane without vehicles for a specific radius in the documentation

import traci
import random

# SUMO configuration file
#Here I have pasted the location in which my files are present in my laptop for doing simulations
sumo_cmd = ["sumo-gui", "-c", "D:\Professional\Python_Sumo\FileNetwork2\map.sumocfg"]

# Ambulance parameters
ambulance_id = "ambulance"
ambulance_speed = 15  # Desired speed for the ambulance (m/s)
clearance_radius = 50  # Distance in meters for vehicles to clear the path

# Simulation steps
simulation_steps = 1000

def start_simulation():
    """Start the SUMO simulation."""
    traci.start(sumo_cmd)
    print("Simulation started...")
    
    # Add the ambulance at the start of the simulation
    add_ambulance()
    
    # Run the simulation step-by-step
    for step in range(simulation_steps):
        traci.simulationStep()  # Advance the simulation
        
        # Handle V2X for traffic management
        v2x_traffic_management(ambulance_id)
        
        # Adjust ambulance behavior dynamically
        manage_ambulance_lane(ambulance_id)
        
        if step % 100 == 0:  # Log every 100 steps
            print(f"Simulation step: {step}")
    
    traci.close()
    print("Simulation finished.")

def add_ambulance():
    """Add the ambulance to the simulation."""
    # Define the ambulance route and add it to the simulation
    route_id = "ambulance_route"
    traci.route.add(route_id, edges=["edge1", "edge2", "edge3", "edge4", "edge5"])
    traci.vehicle.add(ambulance_id, routeID=route_id, typeID="ambulance")
    traci.vehicle.setSpeed(ambulance_id, ambulance_speed)
    print(f"Ambulance {ambulance_id} added to the simulation.")

def v2x_traffic_management(ambulance_id):
    """
    V2X logic to manage traffic for the ambulance.
    - Nearby vehicles detect the ambulance and clear the path.
    """
    # Get ambulance's position and lane
    ambulance_position = traci.vehicle.getPosition(ambulance_id)
    ambulance_lane_id = traci.vehicle.getLaneID(ambulance_id)
    
    # Get all vehicles in the simulation
    vehicle_ids = traci.vehicle.getIDList()
    
    for veh_id in vehicle_ids:
        if veh_id == ambulance_id:
            continue  # Skip the ambulance itself
        
        # Get vehicle's position and lane
        vehicle_position = traci.vehicle.getPosition(veh_id)
        vehicle_lane_id = traci.vehicle.getLaneID(veh_id)
        
        # Calculate distance to the ambulance
        distance = ((vehicle_position[0] - ambulance_position[0]) ** 2 +
                    (vehicle_position[1] - ambulance_position[1]) ** 2) ** 0.5
        
        # If the vehicle is within the clearance radius and in the same lane
        if distance <= clearance_radius and vehicle_lane_id == ambulance_lane_id:
            # Move the vehicle to the adjacent lane
            current_lane_index = traci.vehicle.getLaneIndex(veh_id)
            target_lane_index = max(0, current_lane_index - 1)  # Move to the rightmost lane
            traci.vehicle.changeLane(veh_id, target_lane_index, 30)
            
            # Optionally reduce the speed of the vehicle
            traci.vehicle.setSpeed(veh_id, max(0, traci.vehicle.getSpeed(veh_id) * 0.5))
            print(f"Vehicle {veh_id} cleared path for the ambulance.")

def manage_ambulance_lane(ambulance_id):
    """
    Dynamically manage the ambulance's lane and speed.
    - Adjust lane or speed if obstacles are detected ahead.
    """
    # Get the ambulance's current lane and speed
    ambulance_lane_id = traci.vehicle.getLaneID(ambulance_id)
    ambulance_speed = traci.vehicle.getSpeed(ambulance_id)
    
    # Get leader vehicle in the current lane
    leader_id, leader_dist = traci.vehicle.getLeader(ambulance_id, 50) or (None, float("inf"))
    
    if leader_id:
        # If a leader vehicle is detected within 50 meters, change lanes or reduce speed
        current_lane_index = traci.vehicle.getLaneIndex(ambulance_id)
        num_lanes = traci.lane.getNumberOfLanes(traci.vehicle.getRoadID(ambulance_id))
        
        if current_lane_index + 1 < num_lanes:
            # Change to the left lane if possible
            traci.vehicle.changeLane(ambulance_id, current_lane_index + 1, 30)
            print(f"Ambulance changed to lane {current_lane_index + 1} to avoid leader {leader_id}.")
        else:
            # If no lane change is possible, reduce speed
            reduced_speed = max(ambulance_speed * 0.5, 5)  # Reduce to 50% of current speed
            traci.vehicle.setSpeed(ambulance_id, reduced_speed)
            print(f"Ambulance reduced speed to {reduced_speed} due to leader {leader_id}.")

def add_random_vehicles(num_vehicles=100):
    """
    Add random vehicles to the simulation.
    - Vehicles are assigned random routes and departure times.
    """
    for i in range(1, num_vehicles + 1):
        vehicle_id = f"veh{i}"
        route_id = random.choice(["route1", "route2", "route3", "route4", "route5"])
        depart_time = random.uniform(0, 50)
        
        traci.route.add(route_id, edges=["edge1", "edge2", "edge3"])
        traci.vehicle.add(vehicle_id, routeID=route_id, typeID="car", depart=depart_time)
        print(f"Vehicle {vehicle_id} added with route {route_id} and depart time {depart_time:.2f}.")

if __name__ == "__main__":
    # Start the simulation
    start_simulation()