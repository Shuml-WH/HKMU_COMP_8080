from dash import Dash, dcc, html, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import mental_data


def appLayout(app: Dash) -> html.Div:
    return html.Div(
        [
            html.H1(
                "Mental Health Diagnosis & Treatment Dashboard", style={
                    "background-color": "#0f172a", "color": "#ffffff", "height": "10vh",
                    "display" : "flex", "align-items": "center",  # flex, to align the text
                    "position": "sticky", "top": "0", "width": "100%", "zIndex": "1000",  # sticking the top Header component while scrolling down
                    "WebkitMaskImage": "linear-gradient(to bottom, black 85%, transparent 100%)", "maskImage": "linear-gradient(to bottom, black 85%, transparent 100%)"  # color fade
                    }), 
            html.Hr(),
            dbc.Container(
                [
                    # Dropdown bar components
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(id="filter-diagnosis", 
                                             options=[{"label": "All", "value": "All"}]
                                             + [{"label": x, "value": x} for x in mental_data.listDiagnosis],
                                             value="All",
                                             placeholder="Filter by Diagnosis",
                                             ),
                                             width=4,
                                             ),
                            dbc.Col(
                                dcc.Dropdown(id="filter-outcome",
                                             options=[{"label": "All", "value": "All"}]
                                             + [{"label": y, "value": y} for y in mental_data.listOutcome],
                                             value="All",),
                                             width=4,
                                             ),

                            dbc.Col(
                                dcc.Input(
                                            id="filter-patient-id",
                                            type="number",
                                            placeholder="Filter by Patient ID",
                                        ),
                                        width=4,
                            ),
                        ]
                    ),
                    html.Br(),


                    # Patient table & details
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5("Patients"),
                                    dash_table.DataTable(id="patients-table",
                                                         columns=[{"name": "Patient ID", "id": "Patient ID"},
                                                                  {"name": "Age", "id": "Age"},
                                                                  {"name": "Gender", "id": "Gender"},
                                                                  {"name": "Diagnosis", "id": "Diagnosis"},
                                                                  {"name": "Outcome", "id": "Outcome"},
                                                                  ],
                                                        page_size=10,
                                                        row_selectable="single",
                                                        style_table={"height": "400px", "overflowY": "auto"},
                                                        ),
                                    html.Button("Clear selection", id="clear-selection-btn"),
                                ],
                                width=6,
                            ),


                            dbc.Col(
                                [
                                    html.H5("Patient Details"),
                                    html.Div(id="patient-detail-panel"),
                                ],
                                width=6,
                            ),
                        ]
                    ),
                    html.Hr(),

                    
                    # Add New Patient area
                    html.H5("Add New Patient"),
                    dbc.Row(
                            [
                                dbc.Col(dcc.Input(id="new-patient-id", type="number", placeholder="Patient ID"), width=2),
                                dbc.Col(dcc.Input(id="new-age", type="number", placeholder="Age"), width=2),
                                # dbc.Col(dcc.Input(id="new-gender", type="text", placeholder="Gender"), width=2),
                                # dbc.Col(dcc.Input(id="new-diagnosis", type="text", placeholder="Diagnosis"), width=2),
                                # dbc.Col(dcc.Input(id="new-outcome", type="text", placeholder="Outcome"), width=2),
                                dbc.Col(
                                        dcc.Dropdown(
                                            id="new-gender",
                                            options=[
                                                {"label": "Male", "value": "Male"},
                                                {"label": "Female", "value": "Female"},
                                            ],
                                            placeholder="Gender",
                                        ),
                                        width=2,
                                    ),

                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="new-diagnosis",
                                            options=[{"label": x, "value": x} for x in mental_data.listDiagnosis],
                                            placeholder="Diagnosis",
                                        ),
                                        width=2,
                                    ),

                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="new-outcome",
                                            options=[{"label": y, "value": y} for y in mental_data.listOutcome],
                                            placeholder="Outcome",
                                        ),
                                        width=2,
                                    ),

                                dbc.Col(html.Button("Add Patient", id="add-patient-btn"), width=2),

                            ]
                    ),
                    html.Div(id = "add-patient-message"),
                    html.Hr(),


                    # Summary graphs
                    dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id="outcome-bar"),width=6,),
                                dbc.Col(dcc.Graph(id="severity-box"),width=6,),
                            ]
                    ),
                ]#, style = {"background-color": "#001145"}
            ),
        ]
    )





# Callbacks function for interactive charts
def register_callbacks(app: Dash):
    # from Filter diagnosis and output dropbar
    # output to Patient table
    @app.callback(
        Output("patients-table", "data"),
        Input("filter-diagnosis", "value"),
        Input("filter-outcome", "value"),
        Input("filter-patient-id", "value"),
        Input("add-patient-btn", "n_clicks"),
    )

    def update_patients_table(diagnosis_value, outcome_value, patient_id_value, n_clicks):
        df_pat = mental_data.filter_patients(diagnosis_value, outcome_value, patient_id_value)
        return df_pat.to_dict("records")




    # from Patient table,
    # output to Patient Detail Panel
    @app.callback(
        Output("patient-detail-panel", "children"),
        Input("patients-table", "selected_rows"),
        Input("patients-table", "data"),
    )

    # selected_rows: a list of indices in Dash DataTable,  table_data: a list of dictionaries (current data)
    def update_patient_details(selected_rows, table_data):
        if not selected_rows or not table_data:
            return html.Div("Select a patient from the table.")

        idx = selected_rows[0]  # selected_rows is a list of indices of the selected rows, [0] is the index of the first (and only) selected row
        row = table_data[idx]
        patient_id = int(row["Patient ID"])
        detail = mental_data.get_patient_detail(patient_id)
        
        if detail is None:
            return html.Div("No detail found.")
        
        # Return html layouts, return to Patient Detail Panel
        return html.Div(
            [
                html.P(f"Patient ID: {detail['Patient ID']}"),
                html.P(f"Age: {detail['Age']}    Gender: {detail['Gender']}"),
                html.P(f"Diagnosis: {detail['Diagnosis']}"),
                html.P(f"Outcome: {detail['Outcome']}"),
                html.Hr(),
                html.P(f"Symptom Severity: {detail['Symptom Severity (1-10)']}"),
                html.P(f"Mood Score: {detail['Mood Score (1-10)']}"),
                html.P(f"Sleep Quality: {detail['Sleep Quality (1-10)']}"),
                html.P(f"Stress Level: {detail['Stress Level (1-10)']}"),
                html.P(f"Treatment Progress: {detail['Treatment Progress (1-10)']}"),
                html.Hr(),
                html.P(f"Medication: {detail['Medication']}"),
                html.P(f"Therapy Type: {detail['Therapy Type']}"),
                html.P(f"Treatment Start Date: {detail['Treatment Start Date']}"),
                html.P(f"Treatment Duration (weeks): {detail['Treatment Duration (weeks)']}"),
                html.P(f"AI-Detected Emotional State: {detail['AI-Detected Emotional State']}"),
                html.P(f"Adherence to Treatment (%): {detail['Adherence to Treatment (%)']}"),
            ]
        )
    

    
    # Clear Radio selection button
    @app.callback(
        Output("patients-table", "selected_rows"),
        Input("clear-selection-btn", "n_clicks"),
        State("patients-table", "selected_rows"),
        prevent_initial_call=True,
        )
    
    def clear_selection(n_clicks, selected_rows):
            # Clear everything
            return []



    # from Filter Diagnosis dropbar,
    # to Summary Graph outcome bar
    @app.callback(
        Output("outcome-bar", "figure"),
        Input("filter-diagnosis", "value"),
    )

    def update_outcome_bar(diagnosis_value):
        data = mental_data.get_summary_all()
        if diagnosis_value and diagnosis_value != "All":
            data = data[data["Diagnosis"] == diagnosis_value]

        fig = px.bar(
            data,
            x="Outcome",
            y="n_patients",
            color="Outcome",
            title="Number of patients by outcome",
            text="n_patients",
            hover_data=["Diagnosis"]
        )
        fig.update_layout(xaxis_title="Outcome", yaxis_title="Number of patients",  
        paper_bgcolor="#d9e2f0", plot_bgcolor="#0f172a")
        return fig
    

    # from filter diagnosis dropbar
    # to Summary graph Filter Diagnosis
    @app.callback(
        Output("severity-box", "figure"),
        Input("filter-diagnosis", "value"),
        Input("filter-outcome", "value")
    )

    def update_severity_box(diagnosis_value, outcome_value):
        data = mental_data.get_score_distributions()

        if diagnosis_value and diagnosis_value != "All":
            data = data[data["Diagnosis"] == diagnosis_value]

        if outcome_value and outcome_value != "All":
            data = data[data["Outcome"] == outcome_value]

        # fig = px.box(
        #     data,
        #     x="Outcome",
        #     y="Symptom Severity (1-10)",
        #     color="Outcome",
        #     title="Symptom severity by outcome",
        # )
        #fig.update_layout(xaxis_title="Outcome", yaxis_title="Symptom Severity (1-10)")

        fig = px.box(
            data,
            x="Diagnosis",
            y="Age",
            color="Diagnosis",
            title="Age distribution by diagnosis",
        )
        fig.update_layout(xaxis_title="Diagnosis", yaxis_title="Age",  
        paper_bgcolor="#d9e2f0", plot_bgcolor="#0f172a")

        return fig
    

    # from add patient rows
    @app.callback(
    Output("add-patient-message", "children"),
    Output("new-patient-id", "value"),
    Output("new-age", "value"),
    Output("new-gender", "value"),
    Output("new-diagnosis", "value"),
    Output("new-outcome", "value"),
    Input("add-patient-btn", "n_clicks"),
    State("new-patient-id", "value"),
    State("new-age", "value"),
    State("new-gender", "value"),
    State("new-diagnosis", "value"),
    State("new-outcome", "value"),
    prevent_initial_call=True,
)
    def add_new_patient(n_clicks, patient_id, age, gender, diagnosis, outcome):
        if patient_id is None or age is None or not gender or not diagnosis or not outcome:
            return "Please fill in all patient fields.", patient_id, age, gender, diagnosis, outcome

        try:
            mental_data.add_patient(patient_id, age, gender, diagnosis, outcome)
            return f"Patient {int(patient_id)} added successfully.", None, None, None, None, None  # None = Placeholder for other columns in the csv
        except ValueError as e:
            return str(e), patient_id, age, gender, diagnosis, outcome




# to debug
if __name__ == "__main__":
    appLayout()