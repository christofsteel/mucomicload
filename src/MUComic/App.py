from appdirs import AppDirs
import os

app = AppDirs('MUComicLoad', 'OpenSomething.Org')
if not os.path.isdir(app.user_data_dir):
	os.makedirs(app.user_data_dir)
if not os.path.isdir(os.path.join(app.user_data_dir,'covers')):
	os.makedirs(os.path.join(app.user_data_dir, 'covers'))
