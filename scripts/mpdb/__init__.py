# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-04 20:39:27'

"""

"""
import os
import sys
DIR = os.path.dirname(__file__)

try:
    import Qt
except ImportError:
    sys.path.append(os.path.join(DIR,"_vendor"))
    import Qt

import utils
reload(utils)
import scriptEditor
# reload(scriptEditor)
import codeEditor
reload(codeEditor)
import panel
reload(panel)
import toolbar
reload(toolbar)
import MPDB
reload(MPDB)


from MPDB import MPDB
from MPDB import install
from MPDB import set_trace
from scriptEditor import scriptEditorEventFilter
from scriptEditor import scriptEditorExecuteAll
from scriptEditor import scriptEditorExecute
from scriptEditor import reporterSetText

from toolbar import Debugger_UI
from panel import Debugger_Panel
from codeEditor import CodeEditor

quitting = False
f_globals = globals()
f_locals = locals()