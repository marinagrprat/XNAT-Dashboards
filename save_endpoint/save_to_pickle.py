import sys
import pickle
from os.path import dirname, abspath
from datetime import datetime
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_interface import data_fetcher


class SaveToPk:

    role = ''
    coll_users_data = None
    coll_users = None
    fetcher_long = None
    fetcher = None

    def __init__(self, username, password, server, ssl, role):

        self.role = role
        self.fetcher = data_fetcher.Fetcher(username, password, server, ssl)
        self.fetcher_long = data_fetcher.FetcherLong(
            username, password, server, ssl)

    def __save_to_db(self, info):

        try:
            date_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            with open(
                'pickles/users_data/' + self.role + '.pickle',
                    'wb') as handle:

                pickle.dump(
                    {'role': self.role,
                     'time_date': date_time,
                     'info': info},
                    handle,
                    protocol=pickle.HIGHEST_PROTOCOL)

            print("Saved")
        except Exception:
            print(Exception.with_traceback())
            return 1000

    def save_data(self):

        info = self.fetcher.fetch_all()

        if type(info) != int:
            self.__save_to_db(info)
            return 0
        else:
            return info

    def save_resources(self):

        resources = self.fetcher_long.get_resources()

        with open(
                'pickles/resources/' + self.role + '.pickle',
                'wb') as handle:

            pickle.dump({
                'role': self.role,
                'resources': resources},
                handle, protocol=pickle.HIGHEST_PROTOCOL)

        exp_resources = self.fetcher_long.get_experiment_resources()

        with open(
                'pickles/resources/' + self.role + 'bbrc.pickle',
                'wb') as handle:

            pickle.dump({
                'role': self.role,
                'resources': exp_resources},
                handle, protocol=pickle.HIGHEST_PROTOCOL)
