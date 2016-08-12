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

JPF = "./jpf-travis/jpf-core/build/RunJPF.jar"

#JPF = "./jpf/RunJPF.jar"

JAYHORN = "./jayhorn/jayhorn/build/libs/jayhorn.jar"


def runJar(jar):
    try:
        #with stats.timer(tool):
        p = subprocess.Popen(jar, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        #stat('BENCHMARK', str(d))
        tmp = d.split("/")
        bench = tmp[len(tmp)-1]
        jpf = glob.glob(os.path.abspath(d) + os.sep + "*.jpf")
        cmd_z3 = ['java', "-jar", JAYHORN, "-solver", "z3",  "-t", "20", "-j", d]
        cmd_eldarica = ['java', "-jar", JAYHORN, "-t", "20", "-j", d]
        #z3_result = runJar(cmd_z3)
        #z3_ans, z3_stats = processFile(bench, z3_result, "Z3")
        #eldarica_result = runJar(cmd_eldarica)
        #eldarica_ans, eldarica_stats = processFile(bench, eldarica_result, "ELD")
        if len(jpf) == 1:
            # file = fileinput.FileInput(jpf[0], inplace=True, backup='.bak')
            # for line in file:
            #     print line.replace("/Users/teme/Documents/GitHub/jayhorn/jayhorn/build/resources/test/", "${jpf-core}/../../benchmarks/")
            # file.close()
            cmd_jpf = ['java', "-jar", JPF, "+shell.port=4242", jpf[0]]
            jpf_result = runJar(cmd_jpf)
            jpf_ans, jpf_stats = processFile(bench, jpf_result, "JPF")
            print "JPF RESULT:\t" + str(jpf_stats)
        else:
            print "JPF RESULT:\t" + "NO JPF CONFIG"
        #print "JAYHORN (ELDARICA) RESULT:\t" + str(eldarica_stats)
        #print "JAYHORN (Z3) RESULT:\t" + str(z3_stats)
        #stats.brunch_print()

        print "---------------------"


# def runBench(args):
#     dr = args.directory
#     all_dir = [os.path.join(dr, name)for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
#     all_results = {}
#     for d in all_dir:
#         tmp = d.split("/")
#         bench = tmp[len(tmp)-1]
#         jpf = glob.glob(os.path.abspath(d) + os.sep + "*.jpf")
#         cmd_z3 = ['java', "-jar", JAYHORN, "-solver", "z3",  "-t", "20", "-j", d]
#         cmd_eldarica = ['java', "-jar", JAYHORN, "-t", "20", "-j", d]
#         cmd_jpf = ['java', "-jar", JPF, "+shell.port=4242", jpf[0]] if len(jpf) == 1 else []
#         tools = {"Z3", cmd_z3, "ELDARICA", cmd_eldarica, "JPF", cmd_jpf}
#         runner = BenchStats(tools, d)
#         runner.run()




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
