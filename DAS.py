import time, threading
import os, signal
from dash import Dash, dcc, html, Input, Output, callback, State
from dash_daq import StopButton
import dash_bootstrap_components as dbc
import plotly, plotly.subplots
import serial, serial.serialutil, serial.tools.list_ports

"""
1.  COM Port Selector
if not selected: show_popup => State(COM_selected, com_modal_selected)
"""

"""
Reads values from serial port and updates 'altitude'.
"""
def serial_monitor(port: str, baudrate: int) -> None:
    global ser, altitude, error_code
    ser = serial.Serial(port=port, baudrate=baudrate)
    while True:
        try:
            altitude = int(ser.readline().decode().strip())
            alt_data.append(altitude)
        except serial.serialutil.SerialException as e:
            print("Arduino disconnected. <serial>")
            error_code = 1
            return
        except KeyboardInterrupt:
            print("User terminated operation. <serial>")
            error_code = 2
            return
        except ValueError:
            pass

"""
Displays any popup based on exception case encountered.
"""
@callback([
        Output("live-updates-graph", "figure"),
        Output("live-updates-text", "children"),
        Output("ard-modal", "is_open"),
        Output("int-modal", "is_open"),
    ], [
        Input("interval-component", "n_intervals"),
        Input("stop-button", "n_clicks")
    ], [
        State("int-modal", "is_open"),
        State("ard-modal", "is_open"),
    ])
def update_altitude_value(n_intervals, n_clicks, int_open, ard_open):
    
    style = {"padding":"15px", "fontSize":"60px"}
    data['time'].append(time.strftime("%H:%M:%S"))
    data['altitude'].append(altitude)
    with open("Altitude.csv", "a") as file:
        print(time.strftime("%H:%M:%S"), altitude, file=file)
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
    if n_clicks:
        thread_killer = threading.Thread(target=end_execution_1, args=(1, ))
        thread_killer.start()
        return fig, [html.Span("Altitude: {altitude}ft", style=style)], False, True
    if not error_code:
        return fig, [html.Span(f'Altitude: {altitude}ft', style=style)], False, False
    elif error_code==1:
        return fig, [html.Span(f'Altitude: {altitude}ft', style=style)], True, False
    elif error_code==2:
        return fig, [html.Span(f'Altitude: {altitude}ft', style=style)], False, True

"""
Ends execution of the program on user request.
"""
def end_execution_1(n_clicks):
    if n_clicks:
        with open("Altitude.csv", 'a') as file:
            print("User terminated operation. <button>")
            print("User terminated operation.", file=file)
        time.sleep(0.3)
        os.kill(os.getpid(), signal.SIGINT)

"""
Ends execution of the program on user request.
"""
@callback(Output("stopbtn-output", "children"), Input("interval-component", "n_intervals"))
def end_execution_2(n):
    if error_code:
        print(f"Error {error_code}")
        with open("Altitude.csv", 'a') as file:
            if error_code==1:
                print("Arduino connection has been lost.")
                print("Arduino connection has been lost.", file=file)
            elif error_code==2:
                print("User has terminated the process.")
                print("User has terminated the process.", file=file)
        time.sleep(0.25)
        os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    try:
        # initialisation of global/main variables
        altitude = 0
        alt_data = []
        alt_data.append(altitude)
        error_code = 0
        n = [str(x) for x in serial.tools.list_ports.comports()]
        data = {
            'time': [],
            'altitude': [],
        }
        thread_serial = threading.Thread(target=serial_monitor, args=("COM9", 9600))
        try:
            thread_serial.start()
        except KeyboardInterrupt:
            print("User interrupted operation.")
            os.kill(os.getpid(), signal.SIGINT)
        external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.BOOTSTRAP]
        # initialisation of Dash Webpage
        app = Dash(__name__, external_stylesheets=external_css)
        app.layout = html.Div([
            html.Div([
                    html.H4("Arduino Live Data Feed", style={"fontSize":"40px"}),
                    html.Div(id="live-updates-text"),
                    dcc.Graph(id="live-updates-graph"),
                    dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
            ]),
            StopButton(id="stop-button", n_clicks=0),
            html.Div(id="stopbtn-output"),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Server Shutdown.", style={"fontSize":"30px"}), close_button=True),
                dbc.ModalBody("The process has been terminated by the user.", style={"fontSize":"20px"}),
                ], id="int-modal", keyboard=False, backdrop=True, is_open=False),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Server Shutdown.", style={"fontSize":"30px"}), close_button=True),
                dbc.ModalBody("The Arduino connection is lost.", style={"fontSize":"20px"}),
                ], id="ard-modal", keyboard=False, backdrop=True, is_open=False),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Select COM Port", style={"fontSize":"30px"}), close_button=False),
                dcc.Dropdown(n, clearable=False) if not bool(n) else dbc.ModalBody("No COM ports are connected.", style={"fontSize":"20px"}),
            ], id="com-modal", keyboard=False, backdrop=True, is_open=False),
        ])
        print("Setup complete")
        app.run(debug=False, use_reloader=False)
    except KeyboardInterrupt:
        os.kill(os.getpid(), signal.SIGINT)
