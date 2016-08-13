import argparse
import textwrap
import json
import csv
import os
import glob
import subprocess
import stats

def processFile(bench, result, tool):
    stats = {"tool": tool, "ans":"", "time":"", "mem":"", "inst":""}
    if result is None:
        stats.update({"ans":"ERR"})
        return {bench:stats}, stats
    if tool == "JPF":
        for r in result.splitlines():
            if 'no errors detected' in r:
                #stat('Result-JPF', 'SAFE')
                stats.update({"ans":"SAFE"})
            if 'elapsed time' in r:
                t = r.split()
                time = t[len(t)-1]
                stats.update({"time":str(time)})
            if 'max memory' in r:
                t = r.split()
                mem = t[len(t)-1]
                stats.update({"mem":str(mem)})
            if 'instructions' in r:
                t = r.split()
                ins = t[len(t)-1]
                stats.update({"inst":str(ins)})
            if 'java.lang.AssertionError' in r:
                #stat('Result-JPF', 'CEX')
                stats.update({"ans":"CEX"})
    elif tool == "Z3" or tool == "ELD":
        if "checker says true" in result:
            #if tool == "Z3": stat('Result-Z3', 'SAFE')
            #if tool == "ELD": stat('Result-ELDARICA', 'SAFE')
            stats.update({"ans":"SAFE"})
        if "checker says false" in result:
            #if tool == "Z3": stat('Result-Z3', 'CEX')
            #if tool == "ELD": stat('Result-ELDARICA', 'CEX')
            stats.update({"ans":"CEX"})
    return {bench:stats}, stats


config = """ target=Main
 classpath=${jpf-core}/../../benchmarks/MinePump/spec1-5/%s
"""

"""
Tools
"""
JPF = "./jpf-travis/jpf-core/build/RunJPF.jar"

CBMC = "./cbmc/src/cbmc"

JAYHORN = "./jayhorn/jayhorn/build/libs/jayhorn.jar"


def runCommand(command):
    try:
        #with stats.timer(tool):
        p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result, _ = p.communicate()
        #stats.stop(tool)
        return result
    except Exception as e:
        print str(e)
        return None


class BenchStats(object):
    def __init__(self, tools, bench):
        self.tools = tools
        self.t_n = tool_name
        result = 'Result-'+str(tool_name)
        self.stat(result, 'UNKNOWN')
        self.stat('BENCHMARK', str(bench))
        return

    def run(self):
        result = self.runJar()
        self.processFile(result)
        stats.brunch_print()


    def runJar(self):
        try:
            tt = 'TIME-'+str(self.t_n)
            with stats.timer(tt):
                p = subprocess.Popen(self.t_e, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result, _ = p.communicate()
                return result

        except Exception as e:
            print str(e)
            return None

    def stat (self, key, val): stats.put (key, val)

    def processFile(self, result):
        if self.t_n == "JPF":
            for r in result.splitlines():
                if 'no errors detected' in r:
                    self.stat('Result-JPF', 'SAFE')
                if 'java.lang.AssertionError' in r:
                    self.stat('Result-JPF', 'CEX')
        elif self.t_n == "Z3" or self.t_n == "ELDARICA":
            if "checker says true" in result:
                if self.t_n == "Z3": self.stat('Result-Z3', 'SAFE')
                if self.t_n == "ELDARICA": self.stat('Result-ELDARICA', 'SAFE')
            if "checker says false" in result:
                if self.t_n == "Z3": self.stat('Result-Z3', 'CEX')
                if self.t_n == "ELDARICA": self.stat('Result-ELDARICA', 'CEX')



def runBench(args):
    dr = args.directory
    viz_html = ""
    all_dir = [os.path.join(dr, name)for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
    all_results = {}
    for d in all_dir:
        print "Benchmark:\t " + str(d)
        tmp = d.split("/")
        bench = tmp[len(tmp)-1]
        jpf = glob.glob(os.path.abspath(d) + os.sep + "*.jpf")
        cmd_z3 = ['java', "-jar", JAYHORN, "-solver", "z3",  "-t", "20", "-j", d]
        cmd_eldarica = ['java', "-jar", JAYHORN, "-t", "20", "-j", d]
        print "---------------------"




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Bench Analysis Utils',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                   Bench Analysis Utils
            --------------------------------
            '''))
    #parser.add_argument ('file', metavar='BENCHMARK', help='Benchmark file')
    parser.add_argument ('directory', metavar='DIR', help='Benchmark dirs')
    #parser.add_argument('-fc', '--fc', required=False, dest="fc", action="store_true")
    #parser.add_argument('-err', '--err', required=False, dest="err", action="store_true")

    args = parser.parse_args()
    try:
        runBench(args)
    except Exception as e:
        print str(e)
