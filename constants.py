# FSM Data
# FSM Data
CURRENT_STATE = "Temperature"
STATES = {
    'Temperature': 'state_icons/temperature.png',
    'Distance': 'state_icons/distance.png',
}

TEMPERATURE = {
    'CURRENT_TEMP': 0,
    'MAXIMUM_TEMP': 100,
}

DISTANCE = 30
BATTERY = [1, 2, 3, 4, 5]

LABEL_STYLE_SHEET = "color: blue; background-color: grey; selection-color: grey; selection-background-color: blue; border: 1px grey"
PBAR_LOW_PROGRESS = "QProgressBar::chunk {background-color: red;}"
PBAR_MED_PROGRESS = "QProgressBar::chunk {background-color: gold;}"
PBAR_HIGH_PROGRESS = "QProgressBar::chunk {background-color: green;}"

NUM_PLOTS = 5
PLOT_INCREMENTS = [1, 10]

GRAPH_IMG_NAME = "Graph.png"