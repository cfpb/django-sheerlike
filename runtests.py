import os
import os.path
import sys

import django
from django.core.management import call_command

def run():
    this_dir = os.getcwd()
    testproj_dir = os.path.join(this_dir, "test_project")
    os.chdir(testproj_dir)
    sys.path.append(testproj_dir)
    os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
            "DJANGO_SETTINGS_MODULE", "test_project.settings")
    settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
    django.setup()
    os.chdir(os.path.join(this_dir, 'sheerlike'))
    call_command('test')
    os.chdir(this_dir)


if __name__ == '__main__':
    run()
