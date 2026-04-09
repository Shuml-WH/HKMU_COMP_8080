from dash import Dash, dcc, html, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import mental_data

def appLayout(app: Dash) -> html.Div:
    return html.Div(
        [
            html.H1(
                "Mental Health Diagnosis & Treatment Dashboard", style={"background-color": "#41FFFF"}),
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
    )

    def update_patients_table(diagnosis_value, outcome_value):
        df_pat = mental_data.filter_patients(diagnosis_value, outcome_value)
        return df_pat.to_dict("records")


    # from Patient table,
    # output to Patient Detail Panel
    @app.callback(
        Output("patient-detail-panel", "children"),
        Input("patients-table", "selected_rows"),
        Input("patients-table", "data"),
    )

    def update_patient_details(selected_rows, table_data):
        if not selected_rows or not table_data:
            return html.Div("Select a patient from the table.")

        idx = selected_rows[0]
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
                html.P(f"Treatment Start Date: {detail['Treatment Start Date'].date()}"),
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
        fig.update_layout(xaxis_title="Outcome", yaxis_title="Number of patients")
        return fig
    

    # from filter diagnosis dropbar
    # to Summary graph Filter Diagnosis
    @app.callback(
        Output("severity-box", "figure"),
        Input("filter-diagnosis", "value"),
    )

    def update_severity_box(diagnosis_value):
        data = mental_data.get_score_distributions()
        if diagnosis_value and diagnosis_value != "All":
            data = data[data["Diagnosis"] == diagnosis_value]

        fig = px.box(
            data,
            x="Outcome",
            y="Symptom Severity (1-10)",
            color="Outcome",
            title="Symptom severity by outcome",
        )
        fig.update_layout(xaxis_title="Outcome", yaxis_title="Symptom Severity (1-10)")
        return fig
    




# to debug
if __name__ == "__main__":
    appLayout()