# Import flask dependencies
from flask import Blueprint, render_template, session, request,\
    redirect, url_for
from realtime_data_processing import graph_generator_pp, graph_generator

# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

graph_data_stats = []  # Contains graph Data loaded globally for get request
project_lists = []  # Contains project list globally for get request
username = ''  # For saving username globally
password = ''  # For saving password globally
server = ''  # For saving server url globally
ssl = ''  # For saving username globally


# Set the route and accepted methods
@dashboards.route('/stats/', methods=['POST', 'GET'])
def stats():

    if request.method == "POST":

        global username, server, password, ssl
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        server = user_details['server']
        ssl = False if user_details.get('ssl') is None else True
        global graph_data_stats
        global project_lists
        global db
        plotting_object = graph_generator.GraphGenerator(username,
                                                         password,
                                                         server,
                                                         ssl)
        graph_data_stats = plotting_object.graph_generator()
        project_lists = plotting_object.project_list_generator()

        # Disconnecting the api session
        del plotting_object

        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login'))
        else:
            project_list = project_lists[0]
            project_list_ow_co_me = project_lists[1]
            graph_data = graph_data_stats[0]
            stats_data = graph_data_stats[1]
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server,
                                   db=False)
    else:
        # If user reloads page without logging out then should again show data

        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login'))
        else:
            project_list = project_lists[0]
            project_list_ow_co_me = project_lists[1]
            graph_data = graph_data_stats[0]
            stats_data = graph_data_stats[1]
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server,
                                   db=False)


# this route give the details of the project
@dashboards.route('project/<id>', methods=['GET'])
def project(id):

    global username, password, server, ssl

    data_array = graph_generator_pp.GraphGenerator(
        username, password, server, ssl, id
    ).graph_generator()

    graph_data = data_array[0]
    stats_data = data_array[1]
    members = data_array[2]['member(s)']
    users = data_array[2]['user(s)']
    collaborators = data_array[2]['Collaborator(s)']
    owners = data_array[2]['Owner(s)']
    last_accessed = data_array[2]['last_accessed(s)']
    insert_users = data_array[2]['insert_user(s)']
    insert_date = data_array[2]['insert_date']
    access = data_array[2]['access']
    name = data_array[2]['name']
    last_workflow = data_array[2]['last_workflow']

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graph_data,
        stats_data=stats_data,
        username=username.capitalize(),
        server=server,
        db=False,
        members=members,
        users=users,
        collaborators=collaborators,
        owners=owners,
        last_accessed=last_accessed,
        insert_date=insert_date,
        insert_users=insert_users,
        access=access,
        name=name,
        last_workflow=last_workflow,
        id=id)


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():

    global graph_data_stats, username, password, ssl
    global server
    graph_data_stats = []
    username = ''
    password = ''
    server = ''
    ssl = ''

    if 'username' in session:
        del session['username']
    if 'error' in session:
        session['error'] = -1

    return redirect(url_for('auth.login'))
