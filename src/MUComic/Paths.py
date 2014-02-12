import appdirs
import os.path

datapath = appdirs.user_data_dir('MUComicLoad', 'OpenSomething.Org')
configfile = os.path.join(appdirs.user_data_dir('MUComicLoad', 'OpenSomething.Org'), 'mucomicload.conf')
dbfile = os.path.join(appdirs.user_data_dir('MUComicLoad','OpenSomething.Org'),'mucomicload.db')
coverfolder = os.path.join(appdirs.user_data_dir('MUComicLoad', 'OpenSomething.Org'), 'covers')
