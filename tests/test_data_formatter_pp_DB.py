from saved_data_processing import data_formatter_DB


formatter_object_connected = data_formatter_DB.FormatterPP(
    'testUser', 'p1')


def test_get_projects_details():

    projects = [
        {
            'id': 'p1',
            'project_owners': 'tester1 <br/> tester2',
            'project_collabs': 'tester2',
            'project_members': 'tester3',
            'project_users': 'tester4',
            'project_last_access': 'las',
            'insert_user': 'tester',
            'insert_date': 'insert date',
            'project_access': 'private',
            'name': 'p1',
            'project_last_workflow': 'date'}]

    project_details = formatter_object_connected.get_projects_details(
        projects)

    assert type(project_details['user(s)']) == list
    assert type(project_details['member(s)']) == list
    assert type(project_details['Collaborator(s)']) == list
    assert type(project_details['Owner(s)']) == list
    assert type(project_details['last_accessed(s)']) == list
    assert type(project_details['insert_user(s)']) == str
    assert type(project_details['insert_date']) == str
    assert type(project_details['access']) == str
    assert type(project_details['name']) == str
    assert type(project_details['last_workflow']) == str


def test_get_subjects_details():

    subjects = [
        {
            'project': 'p1', 'ID': 'sb1', 'age': 50,
            'handedness': 'left', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb2', 'age': 10,
            'handedness': 'left', 'gender': 'F'},
        {
            'project': 'p3', 'ID': 'sb3', 'age': 20,
            'handedness': 'right', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb4', 'age': 50,
            'handedness': 'left', 'gender': 'F'},
        {
            'project': 'p3', 'ID': 'sb5', 'age': 90,
            'handedness': 'left', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb6', 'age': 74,
            'handedness': 'left', 'gender': 'F'}]

    subject_details = formatter_object_connected.get_subjects_details(
        subjects)

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict


def test_get_experiments_details():

    experiments = [
        {
            'project': 'p1', 'ID': 'exp1', 'date': '21-03-2020',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 'exp2', 'date': '19-03-2020',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 'exp3', 'date': '24-02-2020',
            'xsiType': 't3', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 'exp4', 'date': '2-03-2020',
            'xsiType': 't2', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 'exp5', 'date': '21-20-2020',
            'xsiType': 't1', 'subject_ID': 'sb3'},
        {
            'project': 'p3', 'ID': 'exp6', 'date': '11-05-2020',
            'xsiType': 't2', 'subject_ID': 'sb2'},
        {
            'project': 'p4', 'ID': 'exp7', 'date': '20-03-2020',
            'xsiType': 't1', 'subject_ID': 'sb3'}]

    experiment_details = formatter_object_connected.get_experiments_details(
        experiments)

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiment Types']) == dict


def test_get_scans_details():

    scans = [
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb1',
            'xnat:imagescandata/id': 'sc1', 'xnat:imagescandata/type': 't1',
            'project': 'p1', 'xsiType': 'tx1',
            'xnat:imagesessiondata/subject_id': 'sb3'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb2',
            'xnat:imagescandata/id': 'sc4', 'xnat:imagescandata/type': 't1',
            'project': 'p1', 'xsiType': 'tx1',
            'xnat:imagesessiondata/subject_id': 'sb1'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb1',
            'xnat:imagescandata/id': 'sc3', 'xnat:imagescandata/type': 't3',
            'project': 'p3', 'xsiType': 'tx2',
            'xnat:imagesessiondata/subject_id': 'sb2'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb2',
            'xnat:imagescandata/id': 'sc2', 'xnat:imagescandata/type': 't3',
            'project': 'p4', 'xsiType': 'tx2',
            'xnat:imagesessiondata/subject_id': 'sb1'}]

    scans_details = formatter_object_connected.get_scans_details(
        scans)

    assert type(scans_details['Number of Scans']) == int
    assert type(scans_details['Scans/Subject']) == dict
    assert type(scans_details['Scans Quality']) == dict
    assert type(scans_details['Scan Types']) == dict
    assert type(scans_details['XSI Scan Types']) == dict


def test_get_resources_details():

    resource_details = formatter_object_connected.get_resources_details()

    assert resource_details is None

    resources = [
        ['p1', 's1', 'r1', 'l1'],
        ['p1', 's2', 'r2', 'l2'],
        ['p1', 's2', 'r3', 'l3'],
        ['p1', 's3', 'r4', 'l4'],
        ['p2', 's3', 'r5', 'l5'],
        ['p2', 's3', 'r6', 'l6'],
        ['p2', 's1', 'r7', 'l7'],
        ['p1', 's1', 'r8', 'l8']]

    resource_details = formatter_object_connected.get_resources_details(
        resources)

    assert type(resource_details) == dict
    assert len(resource_details) == 1

    resources_bbrc = [[
        'p1', 's1', 'r1', {
            'version': 'v1',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-12-19'}}],
        ['p2', 's1', 'r3', {
            'version': 'v1',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-11-10'}}],
        ['p2', 's2', 'r3', {'version': 'v3'}],
        ['p2', 's2', 'r3', 0],
        ['p3', 's1', 'r6', {
            'version': 'v2',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-9-20'}}],
        ['p1', 's2', 'r8', {
            'version': 'v1',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-10-21'}}],
        ['p1', 's3', 'r9', {
            'version': 'v2',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-08-22'}}],
        ['p1', 's4', 'r10', {
            'version': 'v3',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-9-25'}}]]

    resource_details = formatter_object_connected.get_resources_details(
        resources, resources_bbrc)

    assert type(resource_details) == dict
    assert len(resource_details) == 7

    experiments = [
        {
            'project': 'p1', 'ID': 's1', 'date': '2020-3-21',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 's2', 'date': '2020-3-19',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 's3', 'date': '2020-02-24',
            'xsiType': 't3', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 's3', 'date': '2020-03-2',
            'xsiType': 't2', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 's2', 'date': '2020-02-12',
            'xsiType': 't1', 'subject_ID': 'sb3'},
        {
            'project': 'p3', 'ID': 's1', 'date': '2020-05-11',
            'xsiType': 't2', 'subject_ID': 'sb2'},
        {
            'project': 'p4', 'ID': 's2', 'date': '2020-03-20',
            'xsiType': 't1', 'subject_ID': 'sb3'}]

    diff_dates = formatter_object_connected.diff_dates(
        resources_bbrc, experiments)

    assert type(diff_dates) == dict
