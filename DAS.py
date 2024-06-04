import time, threading
import os, signal
from dash import Dash, dcc, html, Input, Output, callback, State
from dash_daq import StopButton
import dash_bootstrap_components as dbc
import plotly, plotly.subplots
import serial, serial.serialutil

"""
1.  COM Port Selector
"""

def serial_monitor(port: str, baudrate: int) -> None:
    global ser, altitude, error_code
    ser = serial.Serial(port=port, baudrate=baudrate)
    while True:
        try:
            altitude = int(ser.readline().decode().strip())
            alt_data.append(altitude)
            with open("Altitude.csv", 'a') as file:
                print(time.strftime("%H:%M:%S,"), altitude, file=file)
        except serial.serialutil.SerialException as e:
            print("Arduino disconnected.")
            with open("Altitude.csv", 'a') as file:
                print("Arduino disconnected.", file=file)
            break
        except KeyboardInterrupt:
            print("User terminated operation.")
            with open("Altitude.csv", 'a') as file:
                print("User terminated operation.", file=file)
            break
    end_code(1, 1)
    os.kill(os.getpid(), signal.SIGINT)

@callback(Output("live-updates-text", "children"), Input("interval-component", "n_intervals"))
def update_altitude_value(n):
    style = {"padding":"15px", "fontSize":"60px"}
    return[html.Span(f'Altitude: {altitude}ft', style=style)]

@callback(Output("live-updates-graph", "figure"), Input("interval-component", "n_intervals"))
def update_graph_live(n):
    data['time'].append(time.strftime("%H:%M:%S"))
    data['altitude'].append(int(altitude))
    fig = plotly.subplots.make_subplots(rows=1, cols=1)
    fig['layout']['legend'] = {'x':0, 'y':0, 'xanchor':'left'}

    fig.append_trace(
        {
            'x':data['time'],
            'y':data['altitude'],
            'name':'Altitude',
            'mode':'lines+markers',
            'type':'scatter',
        }, 1, 1)
    return fig

@callback(Output("EOE-modal", "is_open"), Input("stop-button", "n_clicks"), State("test-modal", "is_open"))
def end_code(stop_pressed, is_open):
    print(stop_pressed)
    if stop_pressed and not is_open: return True

@callback(Output("stopbtn-output", "children"), Input("stop-button", "n_clicks"))
def end_execution(n_clicks):
    if n_clicks:
        with open("Altitude.csv", 'a') as file:
            print("User terminated operation.")
            print("User terminated operation.", file=file)
        time.sleep(0.2)
        os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    altitude = 0
    alt_data = []
    alt_data.append(altitude)
    thread_serial = threading.Thread(target=serial_monitor, args=("COM9", 9600))
    try:
        thread_serial.start()
    except KeyboardInterrupt:
        with open("Altitude.csv", 'a') as file:
            print("User terminated operation.")
            print("User terminated operation.", file=file)
            os.kill(os.getpid(), signal.SIGINT)
    except serial.serialutil.SerialException:
        with open("Altitude.csv", 'a') as file:
            print("Arduino disconneted.")
            print("Arduino disconnected.", file=file)
            os.kill(os.getpid(), signal.SIGINT)
    external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_css)
    data = {
        'time': [],
        'altitude': [],
    }
    app.layout = html.Div([
        html.Div([
                html.H4("Arduino Live Data Feed"),
                html.Div(id="live-updates-text"),
                dcc.Graph(id="live-updates-graph"),
                dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
            ]),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Server Shutdown."), close_button=True),
                dbc.ModalBody("User has terminated the process."),
            ], id="EOE-modal", size="sm", keyboard=False, backdrop=True, centered=True, is_open=False),
            StopButton(id="stop-button", n_clicks=0),
            html.Div(id="stopbtn-output"),
    ])
    print("Setup complete")
    app.run(debug=False, use_reloader=False)