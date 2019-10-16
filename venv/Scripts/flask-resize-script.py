#!c:\users\zver\desktop\nomer-3-b-main\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Flask-Resize','console_scripts','flask-resize'
__requires__ = 'Flask-Resize'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Flask-Resize', 'console_scripts', 'flask-resize')()
    )
