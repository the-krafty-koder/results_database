import dash_core_components as dcc
import dash, pickle, pandas as pd,dash_table
import dash_html_components as html
import pandas as pd
from django.shortcuts import redirect
from django_plotly_dash import DjangoDash
from plotly import tools
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.dependencies import Input,Output
from submission.models import *
from django.shortcuts import redirect
from processing.functions import get_data,get_student_name
from .models import Subject

results = "None"
timer = 0
class get_tables():

    def get_dataframe(self,subjects,stream):
        df = pd.DataFrame({"Number":[i for i in range(1,len(stream.students)+1)],"Student Name":[student.student_name for student in stream.students],"Adm":[student.admission for student in stream.students]})
        for sub in subjects:
            df[sub] = 0
        return df

    def get_submit_app(self,stream):
        try:
            subjects = [sub.name for sub in Subject.objects.all()]
            data = self.get_dataframe(subjects,stream)
            columns = ([{'name': sub, 'id': sub, 'type':'numeric'} for sub in data.columns])
        except IndexError:
            subjects = ["Maths","English","Kiswahili","Physics","Chemistry","Biology","Geography","History","Business","CRE"]
            data = [dict(Model=i, **{subj: 0 for subj in subjects}) for i in range(1, 50)]
            columns = ([{'name' : 'Number', 'id':'Number'}] + [{'name' : 'Adm No', 'id':'Adm No', 'type':'numeric'},
                                                    {'name' : 'Student Name', 'id':'Student Name', 'type':'text'}] +
            [{'name': sub, 'id': sub, 'type':'numeric'} for sub in subjects])

        submit_app = DjangoDash("submission_table")
        submit_app.layout = html.Div(children = [

            dash_table.DataTable(
                id="table_example",
                columns=columns,

                data=data.to_dict("rows"),
                style_data={'whitespace':'normal'},
                style_table={
                    'maxHeight':'600px',
                    'overflowY': 'scroll',
                    'max_rows_in_viewport':40,
                },
                style_cell={
                        'whiteSpace': 'normal'
                },
                style_cell_conditional=[
                                {'if': {'column_id': 'Student Name'},
                                 'width': '150px'},
                                {'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'},],
                style_header={
                    'backgroundColor': 'rgb(224, 230, 255)',
                    'fontWeight': 'bold',
                    'color':'rgb(4, 57, 201)',
                },
                style_as_list_view=True,
                editable= True,

            ),
            html.Button(id='submit-button', n_clicks=0,  children= "Done"),
            html.Div(id = "output", children= "Proceed to Submit form below"),
        ])
        @submit_app.callback(
            Output('output', 'children'),
            [Input('submit-button', 'n_clicks'),
             Input('table_example', 'data'),
             Input('table_example', 'columns')])
        def save_data(click, rows, column):
            if click > 0:

                exam_results = pd.DataFrame(rows, columns=[c['name'] for c in column])

                global results
                results = exam_results

                global timer
                timer = timer + 1
                return "Data submitted"
        return submit_app


    def get_streamview_app(self,stream):

        subjects = ["Mathematics","English","Kiswahili","Physics","Chemistry","Biology","Geography","History","Business","CRE","French"]
        streamview_app = DjangoDash("streamview_table")
        streamview_app.layout = html.Div(children = [
            html.Div([
                dcc.Dropdown(
                        id='exam-dropdown',
                        options=[{'label': i.exam_name, 'value': i.exam_name} for i in stream.exams],
                        value=stream.exams[0].exam_name
                ),
            ]),
            html.Div([
                html.Div(id='streamview_table',style={'marginBottom': 50, 'marginTop': 50}),
            ]),
        ])
        @streamview_app.callback(
            Output('streamview_table', 'children'),
            [Input('exam-dropdown', 'value'),])
        def update_graph(exam_name):
            results = stream.get_exam(exam_name).results
            return dash_table.DataTable(
                id="table_example",
                columns=(
                    [{'name': sub, 'id': sub, 'type':'numeric'} for sub in results.columns]
                ),

                data=results.to_dict('rows'),
                style_data={'whitespace':'normal'},
                style_table={
                    'maxHeight':'600px',
                    'overflowY': 'scroll',
                    'max_rows_in_viewport':40,
                },
                style_cell={
                        'whiteSpace': 'normal'
                },
                style_cell_conditional=[
                                {'if': {'column_id': 'Student Name'},
                                 'width': '150px'},
                                {'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'},],
                style_header={
                    'backgroundColor': 'rgb(224, 230, 255)',
                    'fontWeight': 'bold',
                    'color':'rgb(4, 57, 201)',
                },
                style_as_list_view=True,


            )

        return streamview_app

    def get_lineplot(self):
        fig = go.Figure(data=go.Scatter(
                    x=["CAT 1","CAT 2","CAT 3","CAT 4","CAT 5","CAT 6"],
                    y=[450,700,600,550,350,690],
                    name="Perfomance Over Time",
                    mode="lines+markers",
                    showlegend=False
                ))
        fig['layout'].update(
                    autosize=False,
                    height=180,
                    width=650,
                    margin=dict(l=0, r=0, t=0, b=0),
                    yaxis=dict(showline=False, tickmode="auto", nticks=6),
                    xaxis=dict(showline=True),
                )
        lineplot1 = DjangoDash("lineplot1")
        lineplot1.layout = html.Div(children=[
            dcc.Graph(figure=fig, id="Subplot Graph")]
        )
        return lineplot1

    def get_students_db(self,stream):
        students_data = pd.DataFrame([get_data(student) for student in stream.students])
        students_db_app = DjangoDash("students_db")
        students_db_app.layout = html.Div(children = [
            dcc.Location(id='url'),
            dash_table.DataTable(
                id="students_db",
                columns=(
                    [{'name': sub, 'id': sub, 'type':'numeric'} for sub in students_data.columns]
                ),

                data=students_data.to_dict('rows'),
                style_data={'whitespace':'normal'},
                style_table={
                    'maxHeight':'600px',
                    'overflowY': 'scroll',
                    'max_rows_in_viewport':40,
                },
                style_cell={
                        'whiteSpace': 'normal'
                },
                style_cell_conditional=[
                                {'if': {'column_id': 'Student Name'},
                                 'width': '150px'},
                                {'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'},],
                style_header={
                    'backgroundColor': 'rgb(224, 230, 255)',
                    'fontWeight': 'bold',
                    'color':'rgb(4, 57, 201)',
                },
                style_as_list_view=True,
                row_selectable='single',
                row_deletable=True,
                selected_rows=[],

            ),

            html.Div(id="output",style={'display': ''}),
        ])

        @students_db_app.expanded_callback(
            Output("output", "children"),
            [Input("students_db", "derived_virtual_selected_rows"),
             Input('url', 'pathname'),
             Input("students_db", "derived_virtual_data")])
        def edit_student(derived_virtual_selected_rows,pathname,row_data,session_state=None,**kwargs):

            form = session_state["student_data"][0]
            stream_name = session_state["student_data"][1]

            if derived_virtual_selected_rows is None:
                row_number = [0]
            else:
                row_number = derived_virtual_selected_rows
            if row_data is None:
                student_name = students_data.iloc[row_number[0]].student_name
                return student_name
            else:
                student_name = pd.DataFrame(row_data).iloc[row_number[0]].student_name
                session_state.get("student_name",student_name)


                return dcc.Location(pathname="/edit_student/{}/{}/{}".format(form,stream,student_name), id="edit_student")

        return students_db_app


def sucess():
    global timer
    if timer>0:
        return results


headers = ["Mathematics","English","Kiswahili","Physics","Chemistry","Biology","Geography","History","Business","CRE","French"]
display_student_app = DjangoDash("display_student")
display_student_app.layout = html.Div(children = [
    dash_table.DataTable(
        id="table_example",
        columns=(
            [{'name' : 'Number', 'id':'Number'}] + [{'name' : 'Exam Name', 'id':'Student Name', 'type':'text'}] +
            [{'name': sub, 'id': sub, 'type':'numeric'} for sub in headers]
        ),
        data=[dict(Model=i, **{subj: 0 for subj in headers}) for i in range(1, 10)],
        style_data={'whitespace':'normal'},
        style_table={
            'maxHeight':'600px',
            'overflowY': 'scroll',
            'max_rows_in_viewport':40,
        },
        style_cell={
                'whiteSpace': 'normal'
        },
        style_cell_conditional=[
                        {'if': {'column_id': 'Student Name'},
                         'width': '150px'},
                        {'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'},],
        style_header={
            'backgroundColor': 'rgb(224, 230, 255)',
            'fontWeight': 'bold',
            'color':'rgb(4, 57, 201)',
        },
        style_as_list_view=True,
        editable= True,

    ),
])
""""
index = derived_virtual_selected_rows[0]
global student_name
student_name = rows.iloc[index]["Student Name"]
return redirect("/edit_student/{}/{}/{}".format())"""
