# -*- coding: utf-8 -*-
"""
Created on Tue May 18 09:46:36 2021

@author: HowardYsmaelLChua
"""

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go
import psycopg2
import numpy as np
import pandas as pd
import dash_table
import calendar
from dash.exceptions import PreventUpdate
from flask import request


def querydatafromdatabase(sql, values,dbcolumns):
    db = psycopg2.connect(
        user="zqvziszzrkkqut",
        password="a3c11acd5681142f297cab2e0da37e5ba273f15a90b8ea4485fbcfb7c2774dfa",
        host="ec2-34-232-191-133.compute-1.amazonaws.com",
        port=5432,
        database="dd6pb7ecn5jjlm")
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dbcolumns)
    db.close()
    return rows

def modifydatabase(sqlcommand, values):
    db = psycopg2.connect(
        user="zqvziszzrkkqut",
        password="a3c11acd5681142f297cab2e0da37e5ba273f15a90b8ea4485fbcfb7c2774dfa",
        host="ec2-34-232-191-133.compute-1.amazonaws.com",
        port=5432,
        database="dd6pb7ecn5jjlm")
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()

# load login table
sql = "SELECT * FROM login"
df = querydatafromdatabase(sql,[],["id","name","password"])
columns=[{"name": i, "id": i} for i in df.columns]
data=df.to_dict("rows")
name = df.name.unique().tolist()
pair = df[['name','password']]
username_password = pair.values.tolist()

VALID_USERNAME_PASSWORD_PAIRS = username_password

app = dash.Dash(__name__)
server = app.server

app.title = "e-Quipped Maintenance Application"

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# load login table
sql = "SELECT * FROM login"
df = querydatafromdatabase(sql,[],["id","name","password"])
columns=[{"name": i, "id": i} for i in df.columns]
data=df.to_dict("rows")
name = df.name.unique().tolist()

# load notification table
sql0 = "SELECT * FROM notification"
df0 = querydatafromdatabase(sql0,[],["id","name","date","priority","equi","users"])
columns0=[{"name": i, "id": i} for i in df0.columns]
data0=df0.to_dict("rows")
id0 = df0.id.unique().tolist()
name0 = df0.name.unique().tolist()

# load order table
sql1 = "SELECT * FROM orders"
df1 = querydatafromdatabase(sql1,[],["id","name","type","date","hours",
                                     "damage","equi","emp","notif"])
columns1=[{"name": i, "id": i} for i in df1.columns]
data1=df1.to_dict("rows")
name1 = df1.name.unique().tolist()
years = df1["date"].astype('datetime64[ns]').dt.year
years_list = np.unique(years.values.tolist())

# load user table
sql2 = "SELECT * FROM users"
df2 = querydatafromdatabase(sql2,[],["id","name","date","dept","type","login"])
columns2=[{"name": i, "id": i} for i in df2.columns]
data2=df2.to_dict("rows")
name2 = df2.name.unique().tolist()

# load equipment table
sql3 = "SELECT * FROM equipment"
df3 = querydatafromdatabase(sql3,[],["id","name","brand","model",
                                              "date","cost","loc"])
columns3=[{"name": i, "id": i} for i in df3.columns]
data3=df3.to_dict("rows")
name3 = df3.name.unique().tolist()

# load damage table
sql4 = "SELECT * FROM damage"
df4 = querydatafromdatabase(sql4,[],["id","name"])
columns4=[{"name": i, "id": i} for i in df4.columns]
data4= df4.to_dict("rows")
name4 = df4.name.unique().tolist()

# load location table
sql5 = "SELECT * FROM location"
df5 = querydatafromdatabase(sql5,[],["id","name"])
columns5=[{"name": i, "id": i} for i in df5.columns]
data5= df5.to_dict("rows")
name5 = df5.name.unique().tolist()


image_filename = 'equipped-logo.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename2 = 'equipped-icon.jpg' # replace with your own image
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
                
    html.Div(' ',
        style={'backgroundColor':'rgb(0,123,255)','height':20,'borderRadius':5}),
        
    html.Div([
        html.H2('Please select the Tab of the data you wish to manage on the left.',
                            style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir',}),      
        html.H3("Here is a brief guide of how to use each tab:",style={'color':'rgb(0,123,255)',
                                   'font-family':'minion'}),
        html.H4("Transactional Data:"),
        html.Div([
            html.P("> Notification: usually created by the operator; this is created to inform maintenance of a malfunction in the machine.",style={
                                   'font-family':'minion'}),
            html.P("> Orders: usually created by technicians; this is to record details of the maintenance work.",style={
                                   'font-family':'minion'}),
        ],style={'margin-left':25}
                 ),
        
        html.H4("Master Data:"),
        html.Div([
            html.P("> Users: manage employee records like name and location assignment",style={
                                   'font-family':'minion'}),
            html.P("> Equipment: manage specifications of machines or tools",style={
                                   'font-family':'minion'}),
            html.P("> Damage: add/edit/delete types of damage",style={
                                   'font-family':'minion'}),
            html.P("> Location: add/edit/delete names of locations in the plant",style={
                                   'font-family':'minion'}),
        ],style={'margin-left':25}
                 ),
        
        html.H4("Reports:"),
        html.Div([
            html.P("> Report 1: Equipment Repair Report by Damage and Order types",style={
                                   'font-family':'minion'}),
            html.P("> Report 2: Time Sheet Report of Employees per Month",style={
                                   'font-family':'minion'}),
            ],style={'margin-left':25}
            ),
        
        ])
    ])


registration_page = html.Div([
    html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
    
    html.Div([
                html.H1('User Access Management',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Username:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Password:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Button(
                            id='login-submit-button',
                            n_clicks=0,
                            children='Refresh',
                            style={'fontSize':14,
                                   'color':'rgb(255,255,255)',
                                   'backgroundColor':'rgb(0,123,255)',
                                   'borderRadius':5,
                                   'height':38,'display':'none'},
                            ),
                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='login-name',value='User ID', type='text',
                              style={'width':120}),
                    html.Br(),html.Br(),
                    dcc.Input(id='login-password',value='Password', type='password',
                              style={'width':120}),
                    html.Div([
                        
                            html.Br(),html.Br(),
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='login-mode',
                            value=[]),
                          
                        dcc.ConfirmDialog(
                            id='login-confirm'),
                          
                      html.Br(),
                      html.Button(
                        id='login-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='login-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                ], style={'display':'inline-block', 'margin-left':25}),
                    html.Br(),html.Br(),
                    dcc.Link('Navigate to "Main Menu"', href='/'),
                    html.Br(),html.Br(),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
                    ],
        style={'display':'inline-block','float':'left'}),

    html.Div([
        html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
        dcc.Dropdown(
                        id='login-dropdown',
                        options=[{'label':n, 'value':n} for n in name],
                        style={},
                    ),
        html.Br(),
        dash_table.DataTable(
        id='logintable',
        row_selectable='single',
        columns=columns,
        data=data,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='loginsubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50}),
    
    
    
])   

notification_page = html.Div([
        dcc.ConfirmDialog(id='notif-confirm'),
        html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
        
        html.Div([
            html.H1('Maintenance Notifications',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Name:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Priority:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('Date:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Equipment:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Requestor:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Button(
                        id='notif-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38,'display':'none'},
                        ),

                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='notif-name', type='text',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(id='notif-priority',value='Low',
                                 options=[{'label':'Very High', 'value':'Very High'},
                                          {'label':'High', 'value':'High'},
                                          {'label':'Medium', 'value':'Medium'},
                                          {'label':'Low', 'value':'Low'}],
                              style={'width':200}),
                    html.Br(),
                    dcc.Input(id='notif-date', type='date',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(
                        id='notif-equi',
                        options=[{'label':n, 'value':n} for n in name3],
                        style={'width':200},
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='notif-user',
                        options=[{'label':n, 'value':n} for n in name2],
                        style={'width':200},
                    ),
                    html.Br(),html.Br(),
                    html.Div([
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='notif-mode',
                            value=[]),
                      html.Br(),
                      html.Button(
                        id='notif-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='notif-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                            
                ], style={'display':'inline-block', 'margin-left':25}),
                
                html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
    
    ], style={'float':'left','display':'inline-block'}),
        

    html.Div([
        html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
        dcc.Dropdown(
                        id='notif-dropdown',
                        options=[{'label':n, 'value':n} for n in name0],
                        style={},
                    ),
        html.Br(),
        dash_table.DataTable(
        id='notiftable',
        row_selectable='single',
        columns=columns0,
        data=data0,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='notifsubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50}),

])

order_page = html.Div([
    dcc.ConfirmDialog(id='order-confirm'),
        html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
        
        html.Div([
            html.H1('Maintenance Orders',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Name:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Type:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('Date:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Work in Hours:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Damage:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('Equipment:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('User:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('Notification:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Button(
                        id='order-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38,'display':'none'},
                        ),

                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='order-name', type='text',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(id='order-type',value='Corrective',
                                 options=[{'label':'Corrective', 'value':'Corrective'},
                                          {'label':'Breakdown', 'value':'Breakdown'},
                                          {'label':'Preventive', 'value':'Preventive'}],
                              style={'width':200}),
                    html.Br(),
                    dcc.Input(id='order-date', type='date',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Input(id='order-hours',value=0, type='number',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(
                        id='order-damage',
                        options=[{'label':n, 'value':n} for n in name4],
                        style={'width':200},
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='order-equi',
                        options=[{'label':n, 'value':n} for n in name3],
                        style={'width':200},
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='order-emp',
                        options=[{'label':n, 'value':n} for n in name2],
                        style={'width':200},
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='order-notif',
                        options=[{'label':n, 'value':m} for n,m in zip(name0,id0)],
                        style={'width':200},
                    ),

                    html.Br(),
                    html.Div([
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='order-mode',
                            value=[]),
                      html.Br(),
                      html.Button(
                        id='order-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='order-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                            
                ], style={'display':'inline-block', 'margin-left':25}),

    html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
    
    ], style={'float':'left','display':'inline-block'}),

    html.Div([
        html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
        dcc.Dropdown(
                        id='order-dropdown',
                        options=[{'label':n, 'value':n} for n in name1],
                        style={},
                    ),
        html.Br(),
        dash_table.DataTable(
        id='ordertable',
        row_selectable='single',
        columns=columns1,
        data=data1,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='ordersubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50,'width':'42%'}),

])

user_page = html.Div([
    dcc.ConfirmDialog(id='user-confirm'),
        html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
        
         html.Div([
             html.H1('Users',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Name:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Date:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Location:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('Type:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Username:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Button(
                        id='user-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38,'display':'none'},
                        ),
                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='user-name', type='text',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Input(id='user-date',value='Date', type='date',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(id='user-dept',
                              options=[{'label':n, 'value':n} for n in name5],
                              style={'width':200}),
                    html.Br(),
                    dcc.Dropdown(id='user-type',
                                 options=[{'label':'Admin', 'value':'Admin'},
                                          {'label':'Operator', 'value':'Operator'},
                                          {'label':'Technician', 'value':'Technician'}],
                              style={'width':200}),
                    html.Br(),
                    dcc.Dropdown(
                        id='user-login',
                        options=[{'label':n, 'value':n} for n in name],
                        style={'width':200},
                    ),
                    html.Br(),html.Br(),
                    html.Div([
                    html.Div([
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='user-mode',
                            value=[]),
                      html.Br(),
                      html.Button(
                        id='user-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='user-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                            
                ]),

                    ], style={'display':'inline-block', 'margin-left':25}),
                html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),    

], style={'float':'left','display':'inline-block'}),
         
             html.Div([
                 html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
                 dcc.Dropdown(
                        id='user-dropdown',
                        options=[{'label':n, 'value':n} for n in name2],
                        style={},
                    ),
                 html.Br(),
        dash_table.DataTable(
        id='usertable',
        row_selectable='single',
        columns=columns2,
        data=data2,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='usersubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50}),
         
        ])

user_page2 = html.Div([
    dcc.ConfirmDialog(id='user-confirm'),
        html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
        
         html.Div([
             html.H1('Users',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Name:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Date:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Location:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Label('Type:',
                      style={'font-weight':'bold','font-size':18}),
                    
                    html.Label('Username:',
                      style={'font-weight':'bold','font-size':18,'display':'none'}),
                    html.Br(),html.Br(),html.Br(),
                    html.Button(
                        id='user-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38,'display':'none'},
                        ),
                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='user-name', type='text',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Input(id='user-date',value='Date', type='date',
                              style={'width':200}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(id='user-dept',
                              options=[{'label':n, 'value':n} for n in name5],
                              style={'width':200}),
                    html.Br(),
                    dcc.Dropdown(id='user-type',
                                 options=[{'label':'Admin', 'value':'Admin'},
                                          {'label':'Operator', 'value':'Operator'},
                                          {'label':'Technician', 'value':'Technician'}],
                              style={'width':200}),
                    
                    dcc.Dropdown(
                        id='user-login',
                        options=[{'label':n, 'value':n} for n in name],
                        style={'width':200,'display':'none'},
                    ),
                    html.Br(),html.Br(),
                    html.Div([
                    html.Div([
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='user-mode',
                            value=[]),
                      html.Br(),
                      html.Button(
                        id='user-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='user-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                            
                ]),

                    ], style={'display':'inline-block', 'margin-left':25}),
                html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),    

], style={'float':'left','display':'inline-block'}),
         
             html.Div([
                 html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
                 dcc.Dropdown(
                        id='user-dropdown',
                        options=[{'label':n, 'value':n} for n in name2],
                        style={},
                    ),
                 html.Br(),
        dash_table.DataTable(
        id='usertable',
        row_selectable='single',
        columns=columns2,
        data=data2,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='usersubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50}),
         
        ])

equipment_page = html.Div([
        dcc.ConfirmDialog(id='equi-confirm'),
        html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
        
        html.Div([
            html.H1('Equipment',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Name:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Brand:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Model:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Date Acquired:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Acquisition Cost:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Location Installed:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),html.Br(),
                    html.Button(
                        id='equi-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38, 'display':'none'},
                        ),
                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='equi-name', type='text',
                              style={'width':175}),
                    html.Br(),html.Br(),
                    dcc.Input(id='equi-brand', type='text',
                              style={'width':175}),
                    html.Br(),html.Br(),
                    dcc.Input(id='equi-model', type='text',
                              style={'width':175}),
                    html.Br(),html.Br(),
                    dcc.Input(id='equi-date', type='date',
                              style={'width':175}),
                    html.Br(),html.Br(),
                    dcc.Input(id='equi-cost', type='text',
                              style={'width':175}),
                    html.Br(),html.Br(),
                    dcc.Dropdown(
                        id='equi-loc',
                        options=[{'label':n, 'value':n} for n in name5],
                        style={'width':200},
                    ),
                    html.Br(),html.Br(),
                    
                    html.Div([
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='equi-mode',
                            value=[]),

                      html.Br(),
                      html.Button(
                        id='equi-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='equi-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                    
                      
                    ],style={'float':'left','display': 'inline-block', 
                             'margin-left':25}),
            
            html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
            
            ], style={'float':'left','display':'inline-block'}),

    html.Div([
        html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
        dcc.Dropdown(
                        id='equi-dropdown',
                        clearable=False,
                        options=[{'label':n, 'value':n} for n in name3],
                        style={},
                    ),

        html.Br(),
        
        html.Div([dash_table.DataTable(
        id='equitable',
        row_selectable='single',
        columns=columns3,
        data=data3,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='equisubmitmode',
                  style={'display':'none'})
        ]
            )
        
        
        ], style={'display':'inline-block','margin-left':50}),

])
                             
damage_page = html.Div([
    dcc.ConfirmDialog(id='damage-confirm'),
    html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
    
    html.Div([
                html.H1('Damage',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Br(),
                html.Button(
                        id='damage-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38,'display':'none'},
                        ),
                html.Div([
                    html.Label('Damage Text:',
                      style={'font-weight':'bold','font-size':18})
                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='damage-name', type='text',
                              style={'width':200}),
                    
                    html.Div([html.Br(),
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='damage-mode',
                            value=[]),
                      html.Br(),
                      html.Button(
                        id='damage-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='damage-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                ], style={'display':'inline-block', 'margin-left':25}),
                    html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
                    
                    ],
        style={'display':'inline-block','float':'left'}),

    html.Div([
        html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
        dcc.Dropdown(
                        id='damage-dropdown',
                        options=[{'label':n, 'value':n} for n in name4],
                        style={},
                    ),
        html.Br(),
        dash_table.DataTable(
        id='damagetable',
        row_selectable='single',
        columns=columns4,
        data=data4,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='damagesubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50}),
    
])                     

location_page = html.Div([
    dcc.ConfirmDialog(id='loc-confirm'),
    html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
    
    html.Div([
                html.H1('Location',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Br(),
                html.Button(
                        id='loc-submit-button',
                        n_clicks=0,
                        children='Refresh',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38,'display':'none'},
                        ),
                html.Div([
                    html.Label('Location Text:',
                      style={'font-weight':'bold','font-size':18})
                    ],style={'display':'inline-block','float':'left'}),
                         
                
                html.Div([
                    dcc.Input(id='loc-name', type='text',
                              style={'width':200}),
                    
                    html.Div([html.Br(),
                        
                          dcc.Checklist(
                            options=[
                                {'label': 'Edit Mode', 'value': 1},
                            ],
                            id='loc-mode',
                            value=[]),
                      html.Br(),
                      html.Button(
                        id='loc-save-button',
                        n_clicks=0,
                        children='Save Settings',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38}),
                      html.Br(),
                      html.Button(
                        id='loc-delete-button',
                        n_clicks=0,
                        children='Delete this Entry',
                        style={'fontSize':14,
                       'color':'rgb(255,255,255)',
                       'backgroundColor':'rgb(0,123,255)',
                       'borderRadius':5,
                       'height':38})],
                             ),
                ], style={'display':'inline-block', 'margin-left':25}),
                    html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
                    
                    ],
        style={'display':'inline-block','float':'left'}),

    html.Div([
        html.H3('Search:',
                style={'color':'rgb(0,123,255)','font-family':'avenir'}),
        dcc.Dropdown(
                        id='loc-dropdown',
                        options=[{'label':n, 'value':n} for n in name5],
                        style={},
                    ),
        html.Br(),
        dash_table.DataTable(
        id='loctable',
        row_selectable='single',
        columns=columns5,
        data=data5,
        style_cell={'font-family':'minion'}
        ),
        dcc.Input(id='locsubmitmode',
                  style={'display':'none'})
        ], style={'display':'inline-block','margin-left':50}),
    
])        

report1_page = html.Div([
    html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
    
    html.Div([
                html.H1('Equipment Report',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.H3('Filter by:',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('Equipment:',
                      style={'font-weight':'bold','font-size':18})
                    ],
                    style={'display':'inline-block','float':'left'}),
                
                html.Div([
                    dcc.Dropdown(
                        id='report1-equi',
                        options=[{'label':n, 'value':n} for n in name3],
                        style={'width':200},
                        value = name3[0]
                    ),
                    html.Br(),
                    html.Button(
                        id='report1-submit-button',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38, 'width':120},
                        ),
                    ],
                    style={'display':'inline-block','margin-left':50}),
                
                

                    html.Br(),
                    html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
                    
                    ]
        ,style={'display':'inline-block','float':'left'}),
    
    html.Div([
        html.Div([
            html.H2('By Order Type',
            style={'color':'rgb(0,123,255)','textAlign':'center'}),
            dcc.Graph(id = 'pie-chart-type')],
                 style={'display':'inline-block','width':'28%'}),
        
        html.Div([
            html.H2('By Damage Type',
            style={'color':'rgb(0,123,255)','textAlign':'center'}),
            dcc.Graph(id = 'pie-chart-damage')],
                 style={'display':'inline-block','width':'42%'}),
        
              ],
             style={'display':'block'})
    
    ])   
  
report2_page = html.Div([
    html.Div(' ', style={'backgroundColor':'rgb(0,123,255)','height':42}),
    
    html.Div([
                html.H1('Time Sheet Report',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.H3('Filter by:',
                style={'color':'rgb(0,123,255)',
                               'font-family':'avenir'}),
                html.Div([
                    html.Label('User:',
                      style={'font-weight':'bold','font-size':18}),
                    html.Br(),html.Br(),
                    html.Label('Year:',
                      style={'font-weight':'bold','font-size':18})
                    ],
                    style={'display':'inline-block','float':'left'}),
                
                html.Div([
                    dcc.Dropdown(
                        id='report2-user',
                        options=[{'label':n, 'value':n} for n in name2],
                        style={'width':200},
                        value = name2[0]
                    ),
                    html.Br(),
                    dcc.Dropdown(
                    id='report2-year',
                        options=[{'label':n, 'value':n} for n in years_list],
                        style={'width':200},
                        value = years_list[1]
                    ),
                    html.Br(),
                    html.Button(
                        id='report2-submit-button',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':14,
                               'color':'rgb(255,255,255)',
                               'backgroundColor':'rgb(0,123,255)',
                               'borderRadius':5,
                               'height':38, 'width':120},
                        ),
                    ],
                    style={'display':'inline-block','margin-left':50}),
                
                

                    html.Br(),
                    html.Br(),html.Br(),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                     style={'height':125}),
                    
                    ]
        ,style={'display':'inline-block','float':'left'}),
    
    html.Div([
        html.Div([
            html.H2('Time Series of Work Hours',
            style={'color':'rgb(0,123,255)','textAlign':'center'}),
            html.H3('Sorted by Calendar Month',
            style={'color':'rgb(0,123,255)','textAlign':'center'}),
            dcc.Graph(id = 'bar-chart-user')],
                 style={'display':'inline-block','width':'55%'}),
        
              ],
             style={'display':'block'})
    
    ])
     

# index layout
app.layout = url_bar_and_content_div

layout2 = html.Div([
    
                html.Div([
                    html.Button(
                        id='reg-button',
                        n_clicks=0,
                        children='Manage User Access',
                        style={'fontSize':18,
                               'color':'rgb(0,123,255)',
                               'backgroundColor':'rgb(255,255,255)',
                               'borderRadius':5,
                               'height':42,'width':200,
                               'font-family':'minion', 'display':'inline-block','float':'right'}),
                    
                     dcc.ConfirmDialog(id='reg-confirm'),

                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                     style={'height':100,'display':'inline-block'}),
                
                    html.Div([html.H1('WELCOME',
                            style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir'}),
                    
                    html.H2('to e-Quipped Maintenance Manager',
                            style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir'}),    
                    ],style={'display':'inline-block','margin-left':50}),
                            
                        ],
                        style={}),

    html.Div([
        dcc.Tabs(id='tabs', value='home', children=[
        dcc.Tab(label='Home', value='home',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Notification', value='notif',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Orders', value='orders',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(id='users-tab',label='Users', value='users',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Equipment', value='equi',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Damage', value='damage',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Location', value='loc',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Report 1', value='report1',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18}),
        dcc.Tab(label='Report 2', value='report2',style={'color':'rgb(0,123,255)',
                                   'font-family':'avenir','fontSize':18})
        ]),
        

    ], style={}),
    html.Div(id='tabs-content', style={}),

])


# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    registration_page,
    layout2
])


# Index callbacks
@app.callback(
    Output('page-content', 'children'),
              
    [Input('url', 'pathname'),]
     )
def display_page(pathname):
    if pathname == "/register":
        return registration_page
    else:
        return layout2
    
# main menu callbacks
@app.callback(
    [Output('url','pathname'),
    Output('reg-confirm','displayed'),
    Output('reg-confirm','message')],
    [
     Input('reg-button','n_clicks'),
     ]
    )
def menu_output(reg_button):   
       if reg_button:
           username = request.authorization['username']
           # load user table
           sql2 = "SELECT type,login FROM users"
           df2 = querydatafromdatabase(sql2,[],["type","login"])
           login2 = df2[df2['type']=="Admin"].login.unique().tolist()
           if username in login2:
               return ['/register',False, None]
           else:
               return ['/',True, "Sorry, only 'Admin' users are allowed access. Please contact your system administrator for details."]
       else:
           return ['/',False,None]
       
# Tab callbacks
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'home':
        return layout_index
    elif tab == 'notif':
        return notification_page
    elif tab == 'orders':
        return order_page
    elif tab == 'users':
        username = request.authorization['username']
        # load user table
        sql2 = "SELECT type,login FROM users"
        df2 = querydatafromdatabase(sql2,[],["type","login"])
        login2 = df2[df2['type']=="Admin"].login.unique().tolist()
        if username in login2:
            return user_page
        else:
            return user_page2
    elif tab == 'equi':
        return equipment_page
    elif tab == 'damage':
        return damage_page
    elif tab == 'loc':
        return location_page
    elif tab == 'report1':
        return report1_page
    elif tab == 'report2':
        return report2_page

# login registration callbacks
@app.callback(
    [
     Output('logintable', 'data'),
     Output('logintable', 'columns'),
     Output('loginsubmitmode','value'),
     Output('login-dropdown','options')
     ],
    [Input('login-submit-button', 'n_clicks'),
     Input('login-save-button', 'n_clicks'),
     Input('login-delete-button','n_clicks'),
     Input('login-mode', 'value'),
     ],
    [
     State('login-name', 'value'),
     State('login-password', 'value'),
     State('logintable','selected_rows'),     
     State('logintable', 'data'),
     State('login-dropdown','value')
     ])
def login_output(login_submit_button,login_save_button,login_delete_button,login_mode,
           login_name, login_password, selected_rows,data,login_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="login-submit-button":
           sql = "SELECT * FROM login"
           df = querydatafromdatabase(sql,[],["id","name","password"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="login-save-button":
           # Add Mode
           if 1 not in login_mode:
               sql2 = "SELECT name as name FROM login"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if login_name in name2: 
                   return [data,columns,0,options]
                   return print("There is already an entry with the same name.")
               else:
                   sql = "SELECT max(id) as id FROM login"
                   df = querydatafromdatabase(sql,[],["id"])
                   input_id = int(df['id'][0])+1
                   sqlinsert = "INSERT INTO login(id,name,password) VALUES(%s, %s, %s)"
                   modifydatabase(sqlinsert, [input_id,login_name,login_password])
                   sql = "SELECT * FROM login"
                   df = querydatafromdatabase(sql,[],["id","name","password"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM login"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if login_name in name2:
                   if login_name == login_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE login SET name=%s,password=%s WHERE id=%s"
                       modifydatabase(sqlinsert, [login_name,login_password,input_id])
                       sql = "SELECT * FROM login"
                       df = querydatafromdatabase(sql,[],["id","name","password"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM login"
                       df = querydatafromdatabase(sql,[],["id","name","password"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE login SET name=%s,password=%s, WHERE id=%s"
                   modifydatabase(sqlinsert, [login_name,login_password,input_id])
                   sql = "SELECT * FROM login"
                   df = querydatafromdatabase(sql,[],["id","name","password"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="login-delete-button":
           if 1 not in login_mode:
               sql = "SELECT * FROM login"
               df = querydatafromdatabase(sql,[],["id","name","password"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM login WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM login"
               df = querydatafromdatabase(sql,[],["id","name","password"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="login-mode":
           sql = "SELECT * FROM login"
           df = querydatafromdatabase(sql,[],["id","name","password"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
   else:
      sql = "SELECT * FROM login"
      df = querydatafromdatabase(sql,[],["id","name","password"])
      columns=[{"name": i, "id": i} for i in df.columns]
      data=df.to_dict("rows")
      name = df.name.unique().tolist()
      options=[{'label':n, 'value':n} for n in name]
      return [data,columns,2,options]


@app.callback(
    [
     Output('login-name', 'value'),
     Output('login-password', 'value'),
     ],
    [
     Input('loginsubmitmode', 'value'),
     Input('logintable','selected_rows')
     ],
    [
     State('login-name', 'value'),
     State('login-password', 'value'),
     State('logintable', 'data'),
     ])
def login_clear(loginsubmitmode, selected_rows,login_name, login_password, data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="loginsubmitmode" :
          if loginsubmitmode==0:
              return ["",""]
          elif loginsubmitmode==1:
              return [login_name,login_password]
          elif loginsubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM login WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],["id","name","password"])              
                          
                  return [df['name'][0],df['password'][0]]    
              else:
                  return ["",""]
       elif eventid =="logintable":
           if selected_rows:
                sql = "SELECT * FROM login WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],["id","name","password"])              
        
                return [df['name'][0],df['password'][0]]          
           else:
                return ["",""]      
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('logintable', 'selected_rows'),
    [Input('login-dropdown', 'value') ])
def login_choose_row(login_dropdown):
    sql = "SELECT * FROM login"
    df = querydatafromdatabase(sql,[],["id","name","password"])
    row_id = df[df["name"]==login_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('login-dropdown', 'value'),
    Input('logintable', 'selected_rows'))
def login_choose_row2(selected_rows):
    sql = "SELECT * FROM login"
    df = querydatafromdatabase(sql,[],["id","name","password"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('login-confirm','displayed'),
     Output('login-confirm','message')],
    [Input('login-submit-button', 'n_clicks'),
     Input('login-save-button', 'n_clicks'),
     Input('login-delete-button','n_clicks'),
     Input('login-mode', 'value'),
     ],
    State('login-name', 'value'),
    State('login-dropdown','value'))
def login_output_warning(login_submit_button,login_save_button,login_delete_button,login_mode,
                   login_name,login_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="login-submit-button":
           return [False,None]
       elif eventid =="login-save-button":
           # Add Mode
           if 1 not in login_mode:
               sql2 = "SELECT name as name FROM login"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if login_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM login"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if login_name in name2:  
                   if login_name == login_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="login-delete-button":
           if 1 not in login_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="login-mode":
           return [False,None]

   else:
      raise PreventUpdate

# notification callbacks
@app.callback(
    [
     Output('notiftable', 'data'),
     Output('notiftable', 'columns'),
     Output('notifsubmitmode','value'),
     Output('notif-dropdown','options')
     ],
    [Input('notif-submit-button', 'n_clicks'),
     Input('notif-save-button', 'n_clicks'),
     Input('notif-delete-button','n_clicks'),
     Input('notif-mode', 'value'),
     ],
    [
     State('notif-name', 'value'),
     State('notif-date', 'value'),
     State('notif-priority', 'value'),
     State('notif-equi', 'value'),
     State('notif-user','value'),
     State('notiftable','selected_rows'),     
     State('notiftable', 'data'),
     State('notif-dropdown','value')
     ])
def notif_output(notif_submit_button,notif_save_button,notif_delete_button,
           notif_mode,notif_name, notif_date, notif_priority,
           notif_equi,notif_user,selected_rows,data,notif_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="notif-submit-button":
           sql = "SELECT * FROM notification"
           df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="notif-save-button":
           # Add Mode
           if 1 not in notif_mode:
               sql2 = "SELECT name as name FROM notification"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if notif_name in name2: 
                   return [data,columns,0,options]
                   return print("There is already an entry with the same name.")
               else:
                   sql = "SELECT max(id) as id FROM notification"
                   df = querydatafromdatabase(sql,[],["id"])
                   input_id = int(df['id'][0])+1
                   sqlinsert = "INSERT INTO notification(id,name,date,priority,equi) VALUES(%s, %s, %s, %s, %s)"
                   modifydatabase(sqlinsert, [input_id,notif_name, notif_date, notif_priority,notif_equi,notif_user])
                   sql = "SELECT * FROM notification"
                   df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM notification"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if notif_name in name2:
                   if notif_name == notif_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE notification SET name=%s,date=%s,priority=%s,equi=%s,users=%s WHERE id=%s"
                       modifydatabase(sqlinsert, [notif_name,notif_date,notif_priority,notif_equi,notif_user,input_id])
                       sql = "SELECT * FROM notification"
                       df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM notification"
                       df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE notification SET name=%s,date=%s,priority=%s,equi=%s,users=%s WHERE id=%s"
                   modifydatabase(sqlinsert, [notif_name,notif_date,notif_priority,notif_equi,notif_user,input_id])
                   sql = "SELECT * FROM notification"
                   df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="notif-delete-button":
           if 1 not in notif_mode:
               sql = "SELECT * FROM notification"
               df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM notification WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM notification"
               df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="notif-mode":
           sql = "SELECT * FROM notification"
           df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]

   else:
      sql = "SELECT * FROM notification"
      df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
      columns=[{"name": i, "id": i} for i in df.columns]
      data=df.to_dict("rows")
      name = df.name.unique().tolist()
      options=[{'label':n, 'value':n} for n in name]
      return [data,columns,2,options]


@app.callback(
    [
     Output('notif-name', 'value'),
     Output('notif-date', 'value'),
     Output('notif-priority', 'value'),
     Output('notif-equi', 'value'),
     Output('notif-user', 'value'),
     ],
    [
     Input('notifsubmitmode', 'value'),
     Input('notiftable','selected_rows')
     ],
    [
     State('notif-name', 'value'),
     State('notif-date', 'value'),
     State('notif-priority', 'value'),
     State('notif-equi', 'value'),
     State('notif-user', 'value'),
     State('notiftable', 'data'),
     ])
def notif_clear(notifsubmitmode, selected_rows,notif_name, notif_date,
          notif_priority,notif_equi,notif_user,data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="notifsubmitmode" :
          if notifsubmitmode==0:
              return ["","","","",""]
          elif notifsubmitmode==1:
              return [notif_name, notif_date,notif_priority,notif_equi,notif_user]
          elif notifsubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM notification WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                             ["id","name","date","priority","equi","users"])              
                          
                  return [df['name'][0],df['date'][0],df['priority'][0],df['equi'][0],df['users'][0]]    
              else:
                  return ["","","","",""]
       elif eventid =="notiftable":
           if selected_rows:
                sql = "SELECT * FROM notification WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                           ["id","name","date","priority","equi","users"])              
        
                return [df['name'][0],df['date'][0],df['priority'][0],df['equi'][0],df['users'][0]]         
           else:
                return ["","","","",""]     
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('notiftable', 'selected_rows'),
    [Input('notif-dropdown', 'value') ])
def notif_choose_row(notif_dropdown):
    sql = "SELECT * FROM notification"
    df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
    row_id = df[df["name"]==notif_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('notif-dropdown', 'value'),
    Input('notiftable', 'selected_rows'))
def notif_choose_row2(selected_rows):
    sql = "SELECT * FROM notification"
    df = querydatafromdatabase(sql,[],["id","name","date","priority","equi","users"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('notif-confirm','displayed'),
     Output('notif-confirm','message')],
    [Input('notif-submit-button', 'n_clicks'),
     Input('notif-save-button', 'n_clicks'),
     Input('notif-delete-button','n_clicks'),
     Input('notif-mode', 'value'),
     ],
    State('notif-name', 'value'),
    State('notif-dropdown','value'))
def notif_output_warning(notif_submit_button,notif_save_button,notif_delete_button,notif_mode,
                   notif_name,notif_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="notif-submit-button":
           return [False,None]
       elif eventid =="notif-save-button":
           # Add Mode
           if 1 not in notif_mode:
               sql2 = "SELECT name as name FROM notification"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if notif_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM notification"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if notif_name in name2:  
                   if notif_name == notif_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="notif-delete-button":
           if 1 not in notif_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="notif-mode":
           return [False,None]

   else:
      raise PreventUpdate

# order callbacks
@app.callback(
    [
     Output('ordertable', 'data'),
     Output('ordertable', 'columns'),
     Output('ordersubmitmode','value'),
     Output('order-dropdown','options')
     ],
    [Input('order-submit-button', 'n_clicks'),
     Input('order-save-button', 'n_clicks'),
     Input('order-delete-button','n_clicks'),
     Input('order-mode', 'value'),
     ],
    [
     State('order-name', 'value'),
     State('order-type', 'value'),
     State('order-date', 'value'),
     State('order-hours', 'value'),
     State('order-damage', 'value'),
     State('order-equi', 'value'),
     State('order-emp', 'value'),
     State('order-notif', 'value'),
     State('ordertable','selected_rows'),     
     State('ordertable', 'data'),
     State('order-dropdown','value')
     ])
def order_output(order_submit_button,order_save_button,order_delete_button,
           order_mode,order_name, order_type, order_date, order_hours,
           order_damage,order_equi,order_emp,order_notif,
           selected_rows,data,order_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="order-submit-button":
           sql = "SELECT * FROM orders"
           df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="order-save-button":
           # Add Mode
           if 1 not in order_mode:
               # load user table
               sql2 = "SELECT name as name FROM users"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if order_name in name2: 
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                       sql = "SELECT max(id) as id FROM orders"
                       df = querydatafromdatabase(sql,[],["id"])
                       input_id = int(df['id'][0])+1
                       sqlinsert = "INSERT INTO orders(id,name,type,date,hours,damage,equi,emp,notif) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                       modifydatabase(sqlinsert, [input_id,order_name, order_type, order_date,order_hours,order_damage,order_equi,order_emp,order_notif])
                       sql = "SELECT * FROM orders"
                       df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                                  "damage","equi","emp","notif"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]     
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM orders"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if order_name in name2:
                   if order_name == order_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE orders SET name=%s,type=%s,date=%s,hours=%s,damage=%s,equi=%s,emp=%s,notif=%s WHERE id=%s"
                       modifydatabase(sqlinsert, [order_name, order_type, order_date,order_hours,order_damage,order_equi,order_emp,order_notif,input_id])
                       sql = "SELECT * FROM orders"
                       df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM orders"
                       df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE orders SET name=%s,type=%s,date=%s,hours=%s,damage=%s,equi=%s,emp=%s,notif=%s WHERE id=%s"
                   modifydatabase(sqlinsert, [order_name, order_type, order_date,order_hours,order_damage,order_equi,order_emp,order_notif,input_id])
                   sql = "SELECT * FROM orders"
                   df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="order-delete-button":
           if 1 not in order_mode:
               sql = "SELECT * FROM orders"
               df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM orders WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM orders"
               df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="order-mode":
           sql = "SELECT * FROM orders"
           df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]

   else:
           sql = "SELECT * FROM orders"
           df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]


@app.callback(
    [
     Output('order-name', 'value'),
     Output('order-type', 'value'),
     Output('order-date', 'value'),
     Output('order-hours', 'value'),
     Output('order-damage', 'value'),
     Output('order-equi', 'value'),
     Output('order-emp', 'value'),
     Output('order-notif', 'value'),
     ],
    [
     Input('ordersubmitmode', 'value'),
     Input('ordertable','selected_rows')
     ],
    [
     State('order-name', 'value'),
     State('order-type', 'value'),
     State('order-date', 'value'),
     State('order-hours', 'value'),
     State('order-damage', 'value'),
     State('order-equi', 'value'),
     State('order-emp', 'value'),
     State('order-notif', 'value'),
     State('ordertable', 'data'),
     ])
def order_clear(ordersubmitmode, selected_rows,order_name, order_type, order_date, order_hours,
           order_damage,order_equi,order_emp,order_notif,data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="ordersubmitmode" :
          if ordersubmitmode==0:
              return ["","","","","","","",""]
          elif ordersubmitmode==1:
              return [order_name, order_type, order_date, order_hours,
                      order_damage,order_equi,order_emp,order_notif]
          elif ordersubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM orders WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                             ["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])              
                          
                  return [df['name'][0],df['type'][0],df['date'][0],df['hours'][0],
                          df['damage'][0],df['equi'][0],df['emp'][0],df['notif'][0]]    
              else:
                  return ["","","","","","","",""]
       elif eventid =="ordertable":
           if selected_rows:
                sql = "SELECT * FROM orders WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                           ["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])              
        
                return [df['name'][0],df['type'][0],df['date'][0],df['hours'][0],
                          df['damage'][0],df['equi'][0],df['emp'][0],df['notif'][0]]         
           else:
                return ["","","","","","","",""]     
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('ordertable', 'selected_rows'),
    [Input('order-dropdown', 'value') ])
def order_choose_row(order_dropdown):
    sql = "SELECT * FROM orders"
    df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
    row_id = df[df["name"]==order_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('order-dropdown', 'value'),
    Input('ordertable', 'selected_rows'))
def order_choose_row2(selected_rows):
    sql = "SELECT * FROM orders"
    df = querydatafromdatabase(sql,[],["id","name","type","date","hours",
                                              "damage","equi","emp","notif"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('order-confirm','displayed'),
     Output('order-confirm','message')],
    [Input('order-submit-button', 'n_clicks'),
     Input('order-save-button', 'n_clicks'),
     Input('order-delete-button','n_clicks'),
     Input('order-mode', 'value'),
     ],
    State('order-name', 'value'),
    State('order-dropdown','value'))
def order_output_warining(order_submit_button,order_save_button,order_delete_button,order_mode,
                   order_name,order_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="order-submit-button":
           return [False,None]
       elif eventid =="order-save-button":
           # Add Mode
           if 1 not in order_mode:
               sql2 = "SELECT name as name FROM orders"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if order_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM orders"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if order_name in name2:  
                   if order_name == order_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="order-delete-button":
           if 1 not in order_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="order-mode":
           return [False,None]

   else:
      raise PreventUpdate

# user callbacks
@app.callback(
    [
     Output('usertable', 'data'),
     Output('usertable', 'columns'),
     Output('usersubmitmode','value'),
     Output('user-dropdown','options')
     ],
    [Input('user-submit-button', 'n_clicks'),
     Input('user-save-button', 'n_clicks'),
     Input('user-delete-button','n_clicks'),
     Input('user-mode', 'value'),
     ],
    [
     State('user-name', 'value'),
     State('user-date', 'value'),
     State('user-dept', 'value'),
     State('user-type', 'value'),
     State('user-login', 'value'),
     State('usertable','selected_rows'),     
     State('usertable', 'data'),
     State('user-dropdown','value')
     ])
def user_output(user_submit_button,user_save_button,user_delete_button,
           user_mode,user_name, user_date, user_dept, user_type, user_login,
           selected_rows,data,user_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="user-submit-button":
           sql = "SELECT * FROM users"
           df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="user-save-button":
           # Add Mode
           if 1 not in user_mode:
               sql2 = "SELECT name as name FROM users"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if user_name in name2: 
                   return [data,columns,0,options]
                   return print("There is already an entry with the same name.")
               else:
                   sql = "SELECT max(id) as id FROM users"
                   df = querydatafromdatabase(sql,[],["id"])
                   input_id = int(df['id'][0])+1
                   sqlinsert = "INSERT INTO users(id,name,date,dept,type,login) VALUES(%s, %s, %s, %s, %s, %s)"
                   modifydatabase(sqlinsert, [input_id,user_name, user_date,user_dept,user_type,user_login])
                   sql = "SELECT * FROM users"
                   df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM users"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if user_name in name2:
                   if user_name == user_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE users SET name=%s,date=%s,dept=%s,type=%s,login=%s WHERE id=%s"
                       modifydatabase(sqlinsert, [user_name, user_date,user_dept,user_type,user_login,input_id])
                       sql = "SELECT * FROM users"
                       df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM users"
                       df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE users SET name=%s,date=%s,dept=%s,type=%s,login=%s WHERE id=%s"
                   modifydatabase(sqlinsert, [user_name, user_date,user_dept,user_type,user_login,input_id])
                   sql = "SELECT * FROM users"
                   df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="user-delete-button":
           if 1 not in user_mode:
               sql = "SELECT * FROM users"
               df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM users WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM users"
               df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="user-mode":
           sql = "SELECT * FROM users"
           df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]

   else:
           sql = "SELECT * FROM users"
           df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]


@app.callback(
    [
     Output('user-name', 'value'),
     Output('user-date', 'value'),
     Output('user-dept', 'value'),
     Output('user-type', 'value'),
     Output('user-login', 'value'),
     ],
    [
     Input('usersubmitmode', 'value'),
     Input('usertable','selected_rows')
     ],
    [
     State('user-name', 'value'),
     State('user-date', 'value'),
     State('user-dept', 'value'),
     State('user-type', 'value'),
     State('user-login', 'value'),
     State('usertable', 'data'),
     ])
def user_clear(usersubmitmode, selected_rows,
               user_name, user_date, user_dept, user_type, user_login,data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="usersubmitmode" :
          if usersubmitmode==0:
              return ["","","","",""]
          elif usersubmitmode==1:
              return [user_name, user_date, user_dept, user_type, user_login]
          elif usersubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM users WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                             ["id","name","date","dept","type","login"])       
                          
                  return [df['name'][0],df['date'][0],df['dept'][0],
                          df['type'][0],df['login'][0]]    
              else:
                  return ["","","","",""]
       elif eventid =="usertable":
           if selected_rows:
                sql = "SELECT * FROM users WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                           ["id","name","date","dept","type","login"])     
        
                return [df['name'][0],df['date'][0],df['dept'][0],
                          df['type'][0],df['login'][0]]           
           else:
                return ["","","","",""]     
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('usertable', 'selected_rows'),
    [Input('user-dropdown', 'value') ])
def user_choose_row(user_dropdown):
    sql = "SELECT * FROM users"
    df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
    row_id = df[df["name"]==user_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('user-dropdown', 'value'),
    Input('usertable', 'selected_rows'))
def user_choose_row2(selected_rows):
    sql = "SELECT * FROM users"
    df = querydatafromdatabase(sql,[],["id","name","date","dept","type","login"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('user-confirm','displayed'),
     Output('user-confirm','message')],
    [Input('user-submit-button', 'n_clicks'),
     Input('user-save-button', 'n_clicks'),
     Input('user-delete-button','n_clicks'),
     Input('user-mode', 'value'),
     ],
    State('user-name', 'value'),
    State('user-dropdown','value'))
def user_output_warining(user_submit_button,user_save_button,user_delete_button,user_mode,
                   user_name,user_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="user-submit-button":
           return [False,None]
       elif eventid =="user-save-button":
           # Add Mode
           if 1 not in user_mode:
               sql2 = "SELECT name as name FROM users"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if user_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM users"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if user_name in name2:  
                   if user_name == user_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="user-delete-button":
           if 1 not in user_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="user-mode":
           return [False,None]

   else:
      raise PreventUpdate

# equipment callbacks
@app.callback(
    [
     Output('equitable', 'data'),
     Output('equitable', 'columns'),
     Output('equisubmitmode','value'),
     Output('equi-dropdown','options')
     ],
    [Input('equi-submit-button', 'n_clicks'),
     Input('equi-save-button', 'n_clicks'),
     Input('equi-delete-button','n_clicks'),
     Input('equi-mode', 'value'),
     ],
    [
     State('equi-name', 'value'),
     State('equi-brand', 'value'),
     State('equi-model', 'value'),
     State('equi-date', 'value'),
     State('equi-cost', 'value'),
     State('equi-loc', 'value'),
     State('equitable','selected_rows'),     
     State('equitable', 'data'),
     State('equi-dropdown','value')
     ])
def equi_output(equi_submit_button,equi_save_button,equi_delete_button,
           equi_mode,equi_name, equi_brand, equi_model, equi_date, equi_cost,equi_loc,
           selected_rows,data,equi_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="equi-submit-button":
           sql = "SELECT * FROM equipment"
           df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="equi-save-button":
           # Add Mode
           if 1 not in equi_mode:
               sql2 = "SELECT name as name FROM equipment"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if equi_name in name2: 
                   return [data,columns,0,options]
                   return print("There is already an entry with the same name.")
               else:
                   sql = "SELECT max(id) as id FROM equipment"
                   df = querydatafromdatabase(sql,[],["id"])
                   input_id = int(df['id'][0])+1
                   sqlinsert = "INSERT INTO equipment(id,name,brand,model,date,cost,loc) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                   modifydatabase(sqlinsert, [input_id,equi_name, equi_brand,equi_model,equi_date,equi_cost,equi_loc])
                   sql = "SELECT * FROM equipment"
                   df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM equipment"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if equi_name in name2:
                   if equi_name == equi_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE equipment SET name=%s,brand=%s,model=%s,date=%s,cost=%,loc=%ss WHERE id=%s"
                       modifydatabase(sqlinsert, [equi_name, equi_brand,equi_model,equi_date,equi_cost,equi_loc,input_id])
                       sql = "SELECT * FROM equipment"
                       df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM equipment"
                       df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE equipment SET name=%s,brand=%s,model=%s,date=%s,cost=%,loc=%ss WHERE id=%s"
                   modifydatabase(sqlinsert, [equi_name, equi_brand,equi_model,equi_date,equi_cost,equi_loc,input_id])
                   sql = "SELECT * FROM equipement"
                   df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="equi-delete-button":
           if 1 not in equi_mode:
               sql = "SELECT * FROM equipment"
               df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM equipment WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM equipment"
               df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="equi-mode":
           sql = "SELECT * FROM equipment"
           df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]

   else:
           sql = "SELECT * FROM equipment"
           df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]


@app.callback(
    [
     Output('equi-name', 'value'),
     Output('equi-brand', 'value'),
     Output('equi-model', 'value'),
     Output('equi-date', 'value'),
     Output('equi-cost', 'value'),
     Output('equi-loc', 'value'),
     ],
    [
     Input('equisubmitmode', 'value'),
     Input('equitable','selected_rows')
     ],
    [
     State('equi-name', 'value'),
     State('equi-brand', 'value'),
     State('equi-model', 'value'),
     State('equi-date', 'value'),
     State('equi-cost', 'value'),
     State('equi-loc', 'value'),
     State('equitable', 'data'),
     ])
def equi_clear(equisubmitmode, selected_rows,
               equi_name,equi_brand,equi_model,equi_date,equi_cost,equi_loc,data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="equisubmitmode" :
          if equisubmitmode==0:
              return ["","","","","",""]
          elif equisubmitmode==1:
              return [equi_name,equi_brand,equi_model,equi_date,equi_cost,equi_loc]
          elif equisubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM equipment WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                             ["id","name","brand","model",
                                              "date","cost","loc"])              
                          
                  return [df['name'][0],df['brand'][0],df['model'][0],
                          df['date'][0],df['cost'][0],df['loc'][0]]    
              else:
                  return ["","","","","",""]
       elif eventid =="equitable":
           if selected_rows:
                sql = "SELECT * FROM equipment WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],
                                           ["id","name","brand","model",
                                              "date","cost","loc"])              
        
                return [df['name'][0],df['brand'][0],df['model'][0],
                          df['date'][0],df['cost'][0],df['loc'][0]]          
           else:
                return ["","","","","",""]   
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('equitable', 'selected_rows'),
    [Input('equi-dropdown', 'value') ])
def equi_choose_row(equi_dropdown):
    sql = "SELECT * FROM equipment"
    df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
    row_id = df[df["name"]==equi_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('equi-dropdown', 'value'),
    Input('equitable', 'selected_rows'))
def equi_choose_row2(selected_rows):
    sql = "SELECT * FROM equipment"
    df = querydatafromdatabase(sql,[],["id","name","brand","model",
                                              "date","cost","loc"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('equi-confirm','displayed'),
     Output('equi-confirm','message')],
    [Input('equi-submit-button', 'n_clicks'),
     Input('equi-save-button', 'n_clicks'),
     Input('equi-delete-button','n_clicks'),
     Input('equi-mode', 'value'),
     ],
    State('equi-name', 'value'),
    State('equi-dropdown','value'))
def equi_output_warining(equi_submit_button,equi_save_button,equi_delete_button,equi_mode,
                   equi_name,equi_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="equi-submit-button":
           return [False,None]
       elif eventid =="equi-save-button":
           # Add Mode
           if 1 not in equi_mode:
               sql2 = "SELECT name as name FROM equipment"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if equi_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM equipment"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if equi_name in name2:  
                   if equi_name == equi_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="equi-delete-button":
           if 1 not in equi_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="equi-mode":
           return [False,None]

   else:
      raise PreventUpdate

# damage callbacks
@app.callback(
    [
     Output('damagetable', 'data'),
     Output('damagetable', 'columns'),
     Output('damagesubmitmode','value'),
     Output('damage-dropdown','options')
     ],
    [Input('damage-submit-button', 'n_clicks'),
     Input('damage-save-button', 'n_clicks'),
     Input('damage-delete-button','n_clicks'),
     Input('damage-mode', 'value'),
     ],
    [
     State('damage-name', 'value'),
     State('damagetable','selected_rows'),     
     State('damagetable', 'data'),
     State('damage-dropdown','value')
     ])
def damage_output(damage_submit_button,damage_save_button,damage_delete_button,damage_mode,
           damage_name, selected_rows,data,damage_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="damage-submit-button":
           sql = "SELECT * FROM damage"
           df = querydatafromdatabase(sql,[],["id","name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="damage-save-button":
           # Add Mode
           if 1 not in damage_mode:
               sql2 = "SELECT name as name FROM damage"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if damage_name in name2: 
                   return [data,columns,0,options]
                   return print("There is already an entry with the same name.")
               else:
                   sql = "SELECT max(id) as id FROM damage"
                   df = querydatafromdatabase(sql,[],["id"])
                   input_id = int(df['id'][0])+1
                   sqlinsert = "INSERT INTO damage(id,name) VALUES(%s, %s)"
                   modifydatabase(sqlinsert, [input_id,damage_name])
                   sql = "SELECT * FROM damage"
                   df = querydatafromdatabase(sql,[],["id","name"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM damage"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if damage_name in name2:
                   if damage_name == damage_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE damage SET name=%s WHERE id=%s"
                       modifydatabase(sqlinsert, [damage_name,input_id])
                       sql = "SELECT * FROM damage"
                       df = querydatafromdatabase(sql,[],["id","name"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM damage"
                       df = querydatafromdatabase(sql,[],["id","name"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE damage SET name=%s WHERE id=%s"
                   modifydatabase(sqlinsert, [damage_name,input_id])
                   sql = "SELECT * FROM damage"
                   df = querydatafromdatabase(sql,[],["id","name"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="damage-delete-button":
           if 1 not in damage_mode:
               sql = "SELECT * FROM damage"
               df = querydatafromdatabase(sql,[],["id","name"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM damage WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM damage"
               df = querydatafromdatabase(sql,[],["id","name"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="damage-mode":
           sql = "SELECT * FROM damage"
           df = querydatafromdatabase(sql,[],["id","name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]

   else:
           sql = "SELECT * FROM damage"
           df = querydatafromdatabase(sql,[],["id","name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]


@app.callback(
    [
     Output('damage-name', 'value'),
     ],
    [
     Input('damagesubmitmode', 'value'),
     Input('damagetable','selected_rows')
     ],
    [
     State('damage-name', 'value'),
     State('damagetable', 'data'),
     ])
def damage_clear(damagesubmitmode, selected_rows,damage_name, data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="damagesubmitmode" :
          if damagesubmitmode==0:
              return [""]
          elif damagesubmitmode==1:
              return [damage_name]
          elif damagesubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM damage WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],["id","name"])              
                          
                  return [df['name'][0]]    
              else:
                  return [""]
       elif eventid =="damagetable":
           if selected_rows:
                sql = "SELECT * FROM damage WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],["id","name"])              
        
                return [df['name'][0]]          
           else:
                return [""]      
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('damagetable', 'selected_rows'),
    [Input('damage-dropdown', 'value') ])
def damage_choose_row(damage_dropdown):
    sql = "SELECT * FROM damage"
    df = querydatafromdatabase(sql,[],["id","name"])
    row_id = df[df["name"]==damage_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('damage-dropdown', 'value'),
    Input('damagetable', 'selected_rows'))
def damage_choose_row2(selected_rows):
    sql = "SELECT * FROM damage"
    df = querydatafromdatabase(sql,[],["id","name"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('damage-confirm','displayed'),
     Output('damage-confirm','message')],
    [Input('damage-submit-button', 'n_clicks'),
     Input('damage-save-button', 'n_clicks'),
     Input('damage-delete-button','n_clicks'),
     Input('damage-mode', 'value'),
     ],
    State('damage-name', 'value'),
    State('damage-dropdown','value'))
def damage_output_warning(damage_submit_button,damage_save_button,damage_delete_button,damage_mode,
                   damage_name,damage_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="damage-submit-button":
           return [False,None]
       elif eventid =="damage-save-button":
           # Add Mode
           if 1 not in damage_mode:
               sql2 = "SELECT name as name FROM damage"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if damage_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM damage"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if damage_name in name2:  
                   if damage_name == damage_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="damage-delete-button":
           if 1 not in damage_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="damage-mode":
           return [False,None]

   else:
      raise PreventUpdate

# location callbacks
@app.callback(
    [
     Output('loctable', 'data'),
     Output('loctable', 'columns'),
     Output('locsubmitmode','value'),
     Output('loc-dropdown','options')
     ],
    [Input('loc-submit-button', 'n_clicks'),
     Input('loc-save-button', 'n_clicks'),
     Input('loc-delete-button','n_clicks'),
     Input('loc-mode', 'value'),
     ],
    [
     State('loc-name', 'value'),
     State('loctable','selected_rows'),     
     State('loctable', 'data'),
     State('loc-dropdown','value')
     ])
def loc_output(loc_submit_button,loc_save_button,loc_delete_button,loc_mode,
           loc_name, selected_rows,data,loc_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="loc-submit-button":
           sql = "SELECT * FROM location"
           df = querydatafromdatabase(sql,[],["id","name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]
       elif eventid =="loc-save-button":
           # Add Mode
           if 1 not in loc_mode:
               sql2 = "SELECT name as name FROM location"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if loc_name in name2: 
                   return [data,columns,0,options]
                   return print("There is already an entry with the same name.")
               else:
                   sql = "SELECT max(id) as id FROM location"
                   df = querydatafromdatabase(sql,[],["id"])
                   input_id = int(df['id'][0])+1
                   sqlinsert = "INSERT INTO location(id,name) VALUES(%s, %s)"
                   modifydatabase(sqlinsert, [input_id,loc_name])
                   sql = "SELECT * FROM location"
                   df = querydatafromdatabase(sql,[],["id","name"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM location"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if loc_name in name2:
                   if loc_name == loc_dropdown:
                       input_id=data[selected_rows[0]]['id']
                       sqlinsert = "UPDATE location SET name=%s WHERE id=%s"
                       modifydatabase(sqlinsert, [loc_name,input_id])
                       sql = "SELECT * FROM location"
                       df = querydatafromdatabase(sql,[],["id","name"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                   else:
                       sql = "SELECT * FROM location"
                       df = querydatafromdatabase(sql,[],["id","name"])
                       columns=[{"name": i, "id": i} for i in df.columns]
                       data=df.to_dict("rows")
                       name = df.name.unique().tolist()
                       options=[{'label':n, 'value':n} for n in name]
                       return [data,columns,0,options]
                       return print("There is already an entry with the same name.")
               else:
                   input_id=data[selected_rows[0]]['id']
                   sqlinsert = "UPDATE location SET name=%s WHERE id=%s"
                   modifydatabase(sqlinsert, [loc_name,input_id])
                   sql = "SELECT * FROM location"
                   df = querydatafromdatabase(sql,[],["id","name"])
                   columns=[{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")
                   name = df.name.unique().tolist()
                   options=[{'label':n, 'value':n} for n in name]
                   return [data,columns,0,options]
       elif eventid =="loc-delete-button":
           if 1 not in loc_mode:
               sql = "SELECT * FROM location"
               df = querydatafromdatabase(sql,[],["id","name"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]
               return print("Please enable 'Edit Mode' in order to delete.")
           else:
               input_id=data[selected_rows[0]]['id']
               sqldelete = "DELETE FROM location WHERE id=%s"
               modifydatabase(sqldelete, [input_id])
               sql = "SELECT * FROM location"
               df = querydatafromdatabase(sql,[],["id","name"])
               columns=[{"name": i, "id": i} for i in df.columns]
               data=df.to_dict("rows")
               name = df.name.unique().tolist()
               options=[{'label':n, 'value':n} for n in name]
               return [data,columns,0,options]        
       elif eventid =="loc-mode":
           sql = "SELECT * FROM location"
           df = querydatafromdatabase(sql,[],["id","name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]

   else:
           sql = "SELECT * FROM location"
           df = querydatafromdatabase(sql,[],["id","name"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           name = df.name.unique().tolist()
           options=[{'label':n, 'value':n} for n in name]
           return [data,columns,2,options]


@app.callback(
    [
     Output('loc-name', 'value'),
     ],
    [
     Input('locsubmitmode', 'value'),
     Input('loctable','selected_rows')
     ],
    [
     State('loc-name', 'value'),
     State('loctable', 'data'),
     ])
def loc_clear(locsubmitmode, selected_rows,loc_name, data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="locsubmitmode" :
          if locsubmitmode==0:
              return [""]
          elif locsubmitmode==1:
              return [loc_name]
          elif locsubmitmode==2:
              if selected_rows:
                  
                  sql = "SELECT * FROM location WHERE id =%s"
                  df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],["id","name"])              
                          
                  return [df['name'][0]]    
              else:
                  return [""]
       elif eventid =="loctable":
           if selected_rows:
                sql = "SELECT * FROM location WHERE id =%s"
                df = querydatafromdatabase(sql,[data[selected_rows[0]]['id']],["id","name"])              
        
                return [df['name'][0]]          
           else:
                return [""]      
   else:
      raise PreventUpdate()
      
@app.callback(
    Output('loctable', 'selected_rows'),
    [Input('loc-dropdown', 'value') ])
def loc_choose_row(loc_dropdown):
    sql = "SELECT * FROM location"
    df = querydatafromdatabase(sql,[],["id","name"])
    row_id = df[df["name"]==loc_dropdown]['name'].index
    return list(row_id)

@app.callback(
    Output('loc-dropdown', 'value'),
    Input('loctable', 'selected_rows'))
def loc_choose_row2(selected_rows):
    sql = "SELECT * FROM location"
    df = querydatafromdatabase(sql,[],["id","name"])
    chosen_row = df["name"][selected_rows[0]]
    return chosen_row

@app.callback(
    [Output('loc-confirm','displayed'),
     Output('loc-confirm','message')],
    [Input('loc-submit-button', 'n_clicks'),
     Input('loc-save-button', 'n_clicks'),
     Input('loc-delete-button','n_clicks'),
     Input('loc-mode', 'value'),
     ],
    State('loc-name', 'value'),
    State('loc-dropdown','value'))
def loc_output_warning(loc_submit_button,loc_save_button,loc_delete_button,loc_mode,
                   loc_name,loc_dropdown):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="loc-submit-button":
           return [False,None]
       elif eventid =="loc-save-button":
           # Add Mode
           if 1 not in loc_mode:
               sql2 = "SELECT name as name FROM location"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if loc_name in name2:
                   return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
           # Edit Mode
           else:
               sql2 = "SELECT name as name FROM location"
               df2 = querydatafromdatabase(sql2,[],["name"])
               name2 = list(df2['name'])
               if loc_name in name2:  
                   if loc_name == loc_dropdown:
                       return [False, None]
                   else:
                       return [True,"There is already an entry with the same name.\nPlease choose a different scenario name."]
               else:  
                   return [False,None]
       elif eventid =="loc-delete-button":
           if 1 not in loc_mode:     
               return [True,"Please enable 'Edit Mode' in order to delete."]
           else:    
               return [False,None]        
       elif eventid =="loc-mode":
           return [False,None]

   else:
      raise PreventUpdate
      
@app.callback(
    Output("pie-chart-type", "figure"), 
    Input('report1-submit-button', 'n_clicks'),
    State('report1-equi','value'))
def generate_chart(n_clicks,report1_equi):
    
    sql1 = "SELECT type,equi FROM orders"
    df1 = querydatafromdatabase(sql1,[],["type","equi"])
    df1_equi = df1[df1["equi"] == report1_equi]
    df1_type = df1_equi['type']
    
    vcount = df1_type.value_counts()
    vcount_list = vcount.tolist()
    
    labels = ['Corrective','Preventive','Breakdown']
    values = vcount_list
    colors = ['rgb(134,169,189)','rgb(242,217,187)','rgb(44,82,103)']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                marker=dict(colors=colors,
                                line=dict(color='#000000', width=2)),hole=0.3,
                                showlegend=False)])
    fig.update_traces(textposition='outside', textinfo='value+label'),
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))   
    return fig

@app.callback(
    Output("pie-chart-damage", "figure"), 
    [Input('report1-submit-button', 'n_clicks')],
    State('report1-equi','value'))
def generate_chart2(n_clicks, report1_equi):
    
    # load damage table
    sql4 = "SELECT name FROM damage"
    df4 = querydatafromdatabase(sql4,[],["name"])
    ls4 = df4.name.unique().tolist()
    
    sql1 = "SELECT damage,equi FROM orders"
    df1 = querydatafromdatabase(sql1,[],["damage","equi"])
    df1_equi = df1[df1["equi"] == report1_equi]
    ls1 = df1_equi.damage.tolist()
    
    ls41 = ls4 + ls1
    df41 = pd.DataFrame(ls41, columns = ['damage'])
    
    vcount = df41.value_counts()
    vcount_list = vcount.tolist()
    
    labels = ls4
    values = vcount_list
    colors = []
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                marker=dict(colors=colors,
                                line=dict(color='#000000', width=2)),hole=0.3,
                                showlegend=False)])
    fig.update_traces(textposition='outside', textinfo='value+label'),
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))   
    return fig

@app.callback(
    Output("bar-chart-user", "figure"), 
    [Input('report2-submit-button', 'n_clicks')],
    [State('report2-user', 'value'),
     State('report2-year','value')])
def generate_chart3(n_clicks,report2_user,report2_year):
    
    sql1 = "SELECT emp,hours,date FROM orders"
    df1 = querydatafromdatabase(sql1,[],["emp","hours","date"])
    df1_user = df1[df1["emp"] == report2_user]
    df1_user["date"] = df1_user["date"].astype('datetime64[ns]')
    df1_date = df1_user[["hours","date"]]
    
    df1_date['month'] = df1_date['date'].dt.month
    df1_date['year'] = df1_date['date'].dt.year
    df1_date = df1_date[df1_date['year']==report2_year]
    df_hours_month = df1_date[['hours','month']]
    sum_months = df_hours_month.groupby('month').sum()
    
    months = df1_date['month'].unique().tolist()
    months.sort()
    for m in months:
        month_name = calendar.month_abbr[m]
        months = [month_name if x == m else x for x in months]
    hours = sum_months['hours'].tolist()
    data = [go.Bar(
       x = months,
       y = hours
    )]
    fig = go.Figure(data=data) 
    fig.update_layout(
    xaxis_title="Months",
    yaxis_title="Work Hours")
    return fig
      
if __name__ == '__main__':
    app.run_server(debug=False)