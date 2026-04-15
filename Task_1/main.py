from dash import Dash
import dash_bootstrap_components as dbc
import dashMentalLayout

def main():
    app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
    app.title = "Mental Health Management Dashboard"
    app.layout = dashMentalLayout.appLayout(app)
    dashMentalLayout.register_callbacks(app)
    app.run(debug=False)

if __name__ == "__main__":
    main()
