import mesa
from transport_model import TransportationModel

def agent_portrayal(agent):
    """Define how to portray each agent on the grid."""
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Layer": 0
    }

    if agent.transport_mode == "car":
        portrayal["Color"] = "red"
    elif agent.transport_mode == "public_transit":
        portrayal["Color"] = "blue"
    elif agent.transport_mode == "bike":
        portrayal["Color"] = "green"
    else:  # walking
        portrayal["Color"] = "yellow"

    return portrayal

# Create visualization elements
grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# Charts for different metrics
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

# Model parameters
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

# Create and launch server
server = mesa.visualization.ModularServer(
    TransportationModel,
    [grid, mode_chart, time_chart, cost_chart],
    "Transportation Choice Model",
    model_params
)

server.port = 8521
server.launch()