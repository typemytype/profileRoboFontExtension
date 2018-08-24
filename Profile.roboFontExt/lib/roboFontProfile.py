import AppKit
import cProfile
import os
import tempfile

from mojo.compile import executeCommand
from mojo.UI import HelpWindow


python = os.path.join(AppKit.NSBundle.mainBundle().bundlePath(), "Contents", "MacOS", "python")


def ShowProfile(func, *args, **kwargs):
    """
    +------------------------------+
    |        function name         |
    | total time % ( self time % ) |
    |         total calls          |
    +------------------------------+

                total time %
                  calls
    parent --------------------> children
    """
    statsPath = tempfile.mkstemp(suffix=".stats")[1]
    dotPath = tempfile.mkstemp(suffix=".dot")[1]
    svgPath = tempfile.mkstemp(suffix=".svg")[1]

    pro = cProfile.Profile()
    pro.runcall(func, *args, **kwargs)
    pro.print_stats(sort=1)
    pro.dump_stats(statsPath)

    gprof2dot = os.path.join(os.path.dirname(__file__), "gprof2dot.py")

    cmds = [python, gprof2dot, "-o", dotPath, "--node-thres", "0", "--edge-thres", "1", "-f", "pstats", statsPath]
    stdout, stderr = executeCommand(cmds, shell=True)

    cmds = ["dot", dotPath, "-Tsvg", "-o", svgPath]
    stdout, stderr = executeCommand(cmds, shell=True)

    f = open(svgPath, "r", encoding="utf-8")
    data = f.read()
    f.close()

    HelpWindow(htmlString=data, title="Profiling: %s" % func.__name__)

    os.remove(statsPath)
    os.remove(dotPath)
    os.remove(svgPath)
