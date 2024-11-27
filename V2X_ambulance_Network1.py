#***********Read These comments before reading the file***************
#V2X for Network1-->We have used sumo software to make the simulation this code we have integrated with randomtrips file to achieve V2X simulation in SUMO software 
#We had assumed a car to be ambulance here as SUMO offers only cars in the simulations

import traci
import random
import time

# Path to SUMO configuration file
sumo_cmd = ["sumo-gui", "-c", "D:\Professional\Python_Sumo\File_Network1\Newyork.sumocfg"]

# Initialize the SUMO simulation
def start_simulation():
    traci.start(sumo_cmd)
    step = 0
    while step < 1000:  # Run the simulation for 1000 steps
        traci.simulationStep()  # Move simulation forward by one step
        
        handle_v2x("ambulance")  # Handle V2X communication for ambulance
        
        step += 1
    
    traci.close()  # Close the simulation after the run

# V2X logic for giving way to the ambulance
def handle_v2x(ambulance_id):
    # Get the position of the ambulance
    ambulance_position = traci.vehicle.getPosition(ambulance_id)
    ambulance_lane = traci.vehicle.getLaneID(ambulance_id)

    # Get the list of all vehicles in the simulation
    for veh_id in traci.vehicle.getIDList():
        if veh_id != ambulance_id:  # Skip the ambulance itself
            # Get the position and lane of the vehicle
            veh_position = traci.vehicle.getPosition(veh_id)
            veh_lane = traci.vehicle.getLaneID(veh_id)
            
            # Calculate distance from ambulance
            distance = ((veh_position[0] - ambulance_position[0])**2 +
                        (veh_position[1] - ambulance_position[1])**2)**0.5
            
            # If vehicle is within 50 meters of ambulance and in the same lane
            if distance < 50 and veh_lane == ambulance_lane:
                # Move the vehicle to the right lane to give space for ambulance
                traci.vehicle.changeLane(veh_id, max(0, traci.vehicle.getLaneIndex(veh_id) - 1), 30)
                
                # Optionally, you can reduce speed as well:
                # traci.vehicle.setSpeed(veh_id, traci.vehicle.getSpeed(veh_id) * 0.5)

# Add Vehicles Dynamically to the Simulation
def add_vehicles():
    # Create multiple vehicles and add them to the simulation
    num_vehicles = 100
    for i in range(num_vehicles):
        route = f"route{i % 5}"  # Example routes based on a pattern
        traci.vehicle.add(f"veh{i}", routeID=route, typeID="car", depart=random.uniform(0, 10))

# Main execution
if __name__ == "__main__":
    # Start SUMO simulation
    start_simulation()
