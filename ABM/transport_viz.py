import mesa
import numpy as np

def agent_portrayal(agent):
    """Define how to portray each agent on the grid."""
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5
    }

    if agent.transport_mode == "car":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
    elif agent.transport_mode == "public_transit":
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
    elif agent.transport_mode == "bike":
        portrayal["Color"] = "green"
        portrayal["Layer"] = 3
    else:  # walking
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 4

    return portrayal

def create_server(model_class):
    """Create and return a server for the transportation model visualization."""
    # Create visualization elements
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 500, 500)
    
    # Create charts for different metrics
    mode_chart = mesa.visualization.ChartModule([
        {"Label": "Car_Users", "Color": "Red"},
        {"Label": "Transit_Users", "Color": "Blue"},
        {"Label": "Bike_Users", "Color": "Green"},
        {"Label": "Walk_Users", "Color": "Yellow"}
    ])
    
    time_chart = mesa.visualization.ChartModule([
        {"Label": "Average_Commute_Time", "Color": "Black"}
    ])
    
    cost_chart = mesa.visualization.ChartModule([
        {"Label": "Average_Commute_Cost", "Color": "Purple"}
    ])

    # Define model parameters that can be adjusted through the interface
    model_params = {
        "N": mesa.visualization.Slider(
            "Number of Agents",
            100,
            10,
            500,
            10,
            description="Number of commuters in the model"
        ),
        "width": 20,
        "height": 20
    }

    # Create and return server
    server = mesa.visualization.ModularServer(
        model_class,
        [grid, mode_chart, time_chart, cost_chart],
        "Transportation Choice Model",
        model_params
    )
    
    return server