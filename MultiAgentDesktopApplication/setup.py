# setup.py
from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(
    console=['main.py'],  # 将 main.py 作为入口点
    options={
        'py2exe': {
            'packages': ['public', 'CaseStudy', 'OneSpecieClass', 'TwoSpeciesClass', 'matplotlib', 'PySide6'],  # 指定需要包含的包
            'includes': ['matplotlib.backends.backend_qt5agg', 'matplotlib.backends.backend_qtagg', 'matplotlib.backends.backend_qt'],
            'excludes': ['Tkinter'],  # 排除不需要的包
        }
    },
)

# $env:MPLBACKEND="Qt5Agg"
# nuitka --follow-imports --standalone --enable-plugin=pyside6 main.py
