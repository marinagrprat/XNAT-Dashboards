import pyxnat
import pyxnat.core.errors as pyxnat_errors
import socket
import json
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")


class Fetcher:

    SELECTOR = None

    # Initializing the central interface object in the constructor
    def __init__(self, name, password, server, ssl):

        SELECTOR = pyxnat.Interface(
            server=server,
            user=name,
            password=password,
            verify=(not ssl))
        self.SELECTOR = SELECTOR

    # Disconnect with the instance
    def __del__(self):
        print("Disconnected")
        self.SELECTOR.disconnect()

    def get_projects_details(self):

        try:
            projects = self.SELECTOR.select('xnat:projectData').all().data

        except pyxnat_errors.DatabaseError as dbe:
            if str(dbe).find('500') != -1:
                # 500 represent error in url or uri
                return 500
            elif str(dbe).find('401') != -1:
                # 401 represent error in login details
                return 401
        except socket.error as se:
            if str(se).find('SSL') != -1:
                # If verification enable and host unable to verify
                return 191912
            else:
                # Wrong URL Connection can't be established
                return 1

        return projects

    def get_subjects_details(self):

        try:
            subjects = self.SELECTOR.get(
                '/data/subjects',
                params={'columns': 'ID,project,handedness,'
                        'age,gender'})
            subjects_data = subjects.json()['ResultSet']['Result']

        except json.JSONDecodeError:
            if str(subjects).find('500') != -1:
                # 500 represent error in url or uri
                return 500
            elif str(subjects).find('401') != -1:
                # 401 represent error in login details
                return 401
        except socket.error as se:
            if str(se).find('SSL') != -1:
                # If verification enable and host unable to verify
                return 191912
            else:
                # Wrong URL Connection can't be established
                return 1

        return subjects_data

    def get_experiments_details(self):

        '''
        Using array method to get the experiment information present on XNAT.

        This will add a get_experiment_details key in stats dictionary
        which will have details of number of experiments, experiment per
        project, type of experiment, experiment per subjects.
        '''
        try:
            experiments = self.SELECTOR.array.experiments(
                experiment_type='',
                columns=['subject_ID']).data
        except pyxnat_errors.DatabaseError as dbe:
            if str(dbe).find('500') != -1:
                # 500 represent error in url or uri
                return 500
            elif str(dbe).find('401') != -1:
                # 401 represent error in login details
                return 401
        except socket.error as se:
            if str(se).find('SSL') != -1:
                # If verification enable and host unable to verify
                return 191912
            else:
                # Wrong URL Connection can't be established
                return 1

        return experiments

    def get_scans_details(self):

        '''
        Using array method to get the scans information present on XNAT.

        This will add a get_scans_details key in stats dictionary
        which will have details of number of scans, scans per subject,
        scans per project, scans per experimetn, type of experiment,
        scan quality (usable or unusable), xsi type of scan.
        '''
        try:
            scans = self.SELECTOR.array.scans(
                columns=['xnat:imageScanData/quality',
                         'xnat:imageScanData/type']).data

        except pyxnat_errors.DatabaseError as dbe:
            if str(dbe).find('500') != -1:
                # 500 represent error in url or uri
                return 500
            elif str(dbe).find('401') != -1:
                # 401 represent error in login details
                return 401
        except socket.error as se:
            if str(se).find('SSL') != -1:
                # If verification enable and host unable to verify
                return 191912
            else:
                # Wrong URL Connection can't be established
                return 1

        return scans

    def fetch_all(self):

        all_data = {}

        all_data['projects'] = self.get_projects_details()
        if type(all_data['projects']) == int:
            return all_data['projects']
        all_data['subjects'] = self.get_subjects_details()
        all_data['experiments'] = self.get_experiments_details()
        all_data['scans'] = self.get_scans_details()

        return all_data


class FetcherLong:

    SELECTOR = None
    fetcher = None

    # Initializing the central interface object in the constructor
    def __init__(self, name, password, server, ssl):

        SELECTOR = pyxnat.Interface(
            server=server,
            user=name,
            password=password,
            verify=(not ssl))
        self.SELECTOR = SELECTOR
        self.fetcher = Fetcher(name, password, server, ssl)

    def get_resources(self):

        experiments = self.fetcher.get_experiments_details()

        resources = []

        for exp in tqdm(experiments):
            res = self.SELECTOR.select.experiments(exp['ID']).resources()
            res_Arr = []

            for r in res:
                res_Arr.append(r)

            if res_Arr == []:
                resources.append(
                    [exp['project'], exp['ID'], 'No Data', 'No Data'])
            else:
                for r in res_Arr:
                    resources.append(
                        [exp['project'], exp['ID'], r.id(), r.label()])

        return resources

    def get_experiment_resources(self):

        resource_bbrc_validator = []
        experiments = self.fetcher.get_experiments_details()

        for exp in tqdm(experiments):

            BBRC_VALIDATOR = self.SELECTOR.select.experiment(
                exp['ID']).resource('BBRC_VALIDATOR')
            exists = 'Exists' if BBRC_VALIDATOR.exists() else 'No Exists'

            if exists:
                try:
                    resource_bbrc_validator.append([
                        exp['project'],
                        exp['ID'],
                        exists,
                        self.tests_resource(
                            BBRC_VALIDATOR, 'ArchivingValidator')])
                except IndexError:
                    resource_bbrc_validator.append(
                        [exp['project'], exp['ID'], True, 0])
            else:
                resource_bbrc_validator.append([
                    exp['project'], exp['ID'], False, 0])

        return resource_bbrc_validator

    def tests_resource(self, res, name, key=None):

        j = [e for e in list(res.files('{}*.json'.format(name)))][0]
        j = json.loads(res._intf.get(j._uri).text)
        if key is None:
            return j
        else:
            return j[key]