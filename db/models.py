import glob
import importlib
import os

from db.base_class import Base  # noqa
from mercury.config import settings


file_pattern = os.path.join(settings.BASE_DIR, 'apps', '**', 'models*')
file_list = glob.glob(file_pattern, recursive=True)
for file_path in file_list:
    module_path = os.path.splitext(file_path)[0].replace(
        settings.BASE_DIR, '').lstrip('/\\').replace(os.sep, '.')
    importlib.import_module(module_path)
