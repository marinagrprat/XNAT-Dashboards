from dashboards.data_cleaning import data_formatter as df
from dashboards.data_cleaning import data_filter as dt_filter
from dashboards.data_cleaning import graph_generator as gg
from dashboards.bbrc import data_formatter as df_bbrc
from dashboards.bbrc import data_filter as dt_filter_bbrc
import os.path as op
import dashboards
import pyxnat
from dashboards import pickle as pk
import pickle

pickle_path = op.join(op.dirname(__file__), 'test_save.pickle')
fp = op.join(op.dirname(dashboards.__file__), '..', '.xnat.cfg')
x = pyxnat.Interface(config=fp)


def test_001_pickle_save():  # should be run first

    pk.save(x, pickle_path)
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    assert isinstance(data, dict)
    assert data['server'] == "https://devxnat.barcelonabeta.org"
    assert data['verify'] == 1
    assert isinstance(data['info'], dict)
    assert isinstance(data['resources'], list)
    assert isinstance(data['extra_resources'], list)


def test_002_get_projects_details():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    projects = data['info']['projects']
    project_details = df.Formatter().get_projects_details(projects)

    assert isinstance(project_details['Number of Projects'], int)
    assert isinstance(project_details['Projects Visibility'], dict)

    assert project_details['Number of Projects'] != 0
    assert len(project_details['Projects Visibility']) != 0


def test_003_get_projects_details_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    projects = data['info']['projects']
    project = data['info']['projects'][0]
    project_id = project['id']
    project_details = df.FormatterPP(project_id).get_projects_details(projects)

    assert isinstance(project_details['Owner(s)'], list)
    assert isinstance(project_details['Collaborator(s)'], list)
    assert isinstance(project_details['member(s)'], list)
    assert isinstance(project_details['user(s)'], list)
    assert isinstance(project_details['last_accessed(s)'], list)
    assert isinstance(project_details['insert_user(s)'], str)
    assert isinstance(project_details['insert_date'], str)
    assert isinstance(project_details['access'], str)
    assert isinstance(project_details['name'], str)
    assert isinstance(project_details['last_workflow'], str)


def test_004_get_projects_details_specific():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    projects = data['info']['projects']
    project_details_specific = df.Formatter().get_projects_details_specific(projects)

    assert isinstance(project_details_specific, dict)
    assert len(project_details_specific) != 0


def test_005_get_subjects_details():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    subjects = data['info']['subjects']
    subject_details = df.Formatter().get_subjects_details(subjects)

    assert isinstance(subject_details['Number of Subjects'], int)
    assert isinstance(subject_details['Subjects/Project'], dict)

    assert subject_details['Number of Subjects'] != 0
    assert len(subject_details['Subjects/Project']) != 0


def test_006_get_subjects_details_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    subjects = data['info']['subjects']
    project = data['info']['projects'][0]
    project_id = project['id']
    subject_details = df.FormatterPP(project_id).get_subjects_details(subjects)

    assert isinstance(subject_details['Number of Subjects'], int)
    assert subject_details['Number of Subjects'] != 0


def test_007_get_experiments_details():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    experiments = data['info']['experiments']
    experiments_details = df.Formatter().get_experiments_details(experiments)

    assert isinstance(experiments_details['Number of Experiments'], int)
    assert isinstance(experiments_details['Experiments/Project'], dict)
    assert isinstance(experiments_details['Experiment Types'], dict)

    assert experiments_details['Number of Experiments'] != 0
    assert len(experiments_details['Experiments/Project']) != 0
    assert len(experiments_details['Experiment Types']) != 0


def test_008_get_experiments_details_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    experiments = data['info']['experiments']
    project = data['info']['projects'][0]
    project_id = project['id']
    experiments_details = df.FormatterPP(project_id).get_experiments_details(experiments)

    assert isinstance(experiments_details['Number of Experiments'], int)
    assert isinstance(experiments_details['Experiment Types'], dict)

    assert experiments_details['Number of Experiments'] != 0
    assert len(experiments_details['Experiment Types']) != 0


def test_009_get_scans_details():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    scans = data['info']['scans']
    scans_details = df.Formatter().get_scans_details(scans)

    assert isinstance(scans_details['Number of Scans'], int)
    assert isinstance(scans_details['Scans/Project'], dict)
    assert isinstance(scans_details['Scans Quality'], dict)
    assert isinstance(scans_details['Scan Types'], dict)

    assert scans_details['Number of Scans'] != 0
    assert len(scans_details['Scans/Project']) != 0
    assert len(scans_details['Scans Quality']) != 0
    assert len(scans_details['Scan Types']) != 0


def test_010_get_scans_details_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    scans = data['info']['scans']
    project = data['info']['projects'][0]
    project_id = project['id']
    scans_details = df.FormatterPP(project_id).get_scans_details(scans)

    assert isinstance(scans_details['Number of Scans'], int)
    assert isinstance(scans_details['Scans Quality'], dict)
    assert isinstance(scans_details['Scan Types'], dict)

    assert scans_details['Number of Scans'] != 0
    assert len(scans_details['Scans Quality']) != 0
    assert len(scans_details['Scan Types']) != 0


def test_011_get_resources_details():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources = data['resources']
    resource_details = df.Formatter().get_resources_details(resources)

    assert isinstance(resource_details, dict)
    assert len(resource_details) != 0


def test_012_get_resources_details_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources = data['resources']
    project = data['info']['projects'][0]
    project_id = project['id']
    resource_details = df.FormatterPP(project_id).get_resources_details(resources)

    assert isinstance(resource_details, dict)
    assert len(resource_details) != 0


def test_013_get_bbrc_resource_details():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources_bbrc = data['extra_resources']
    resource_bbrc_details = df_bbrc.Formatter().get_resource_details(resources_bbrc)

    assert isinstance(resource_bbrc_details, dict)
    assert len(resource_bbrc_details) != 0


def test_014_diff_dates():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources_bbrc = data['extra_resources']
    experiments = data['info']['experiments']
    project = data['info']['projects'][0]
    project_id = project['id']
    dict_diff_dates = df_bbrc.Formatter().diff_dates(resources_bbrc, experiments, project_id)

    assert isinstance(dict_diff_dates, dict)
    assert len(dict_diff_dates) != 0


def test_015_generate_test_grid_bbrc():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources_bbrc = data['extra_resources']
    project = data['info']['projects'][0]
    project_id = project['id']
    test_grid = df_bbrc.Formatter().generate_test_grid_bbrc(resources_bbrc, project_id)

    assert isinstance(test_grid, list)
    assert len(test_grid) != 0


def test_016_get_project_list():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    info = data['info']
    resources = data['resources']
    filtered = dt_filter.DataFilter(
        'testUser', info, 'admin', [], resources)
    projects = filtered.get_project_list()

    assert isinstance(projects, dict)
    assert isinstance(projects['project_list'], list)


def test_017_filter_projects():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    info = data['info']
    resources = data['resources']
    filtered = dt_filter.DataFilter(
        'testUser', info, 'admin', [], resources)
    filtered.filter_projects(info, resources)


def test_018_reorder_graphs():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    info = data['info']
    resources = data['resources']
    filtered = dt_filter.DataFilter(
        'testUser', info, 'admin', [], resources)
    ordered_graphs = filtered.reorder_graphs()

    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_019_reorder_graphs_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    info = data['info']
    resources = data['resources']
    project = data['info']['projects'][0]
    project_id = project['id']
    role = 'admin'
    filtered = dt_filter.DataFilterPP(
        'testUser', info, project_id, role, {role: [project_id]}, resources)
    ordered_graphs = filtered.reorder_graphs_pp()

    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_020_filter_projects_bbrc():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources_bbrc = data['extra_resources']
    filtered = dt_filter_bbrc.DataFilter(
        'admin', [], resources_bbrc)
    filtered.filter_projects(resources_bbrc)


def test_021_reorder_graphs_bbrc():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources_bbrc = data['extra_resources']
    filtered = dt_filter_bbrc.DataFilter(
        'admin', [], resources_bbrc)
    ordered_graphs = filtered.reorder_graphs()

    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_022_reorder_graphs_bbrc_PP():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    experiments = data['info']['experiments']
    resources_bbrc = data['extra_resources']
    project = data['info']['projects'][0]
    project_id = project['id']
    role = 'admin'
    filtered = dt_filter_bbrc.DataFilterPP(experiments, project_id,
                                           role, {role: [project_id]}, resources_bbrc)
    ordered_graphs = filtered.reorder_graphs_pp()

    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_023_get_overview():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    project = data['info']['projects'][0]
    project_id = project['id']
    role = 'admin'
    graph_object = gg.GraphGenerator(
        ['testUser'], role, data, {role: [project_id]})

    graph_list = graph_object.get_overview()

    assert isinstance(graph_list, list)
    assert len(graph_list) != 0


def test_024_get_project_view():
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    project = data['info']['projects'][0]
    project_id = project['id']
    role = 'admin'
    graph_object = gg.GraphGeneratorPP(
        ['testUser'], project_id, role, data, {role: [project_id]})

    graph_list = graph_object.get_project_view()

    assert isinstance(graph_list, list)
    assert len(graph_list) != 0