import argparse
import textwrap
import json
import csv
import os
import glob
import subprocess
import stats
import pprint
import threading
from multiprocessing import Process, Pool
import multiprocessing

debug = True


"""
Tools
"""
JPF = "./jpf-travis/jpf-core/build/RunJPF.jar"

CBMC = "./cbmc/src/cbmc"

JAYHORN = "./jayhorn/jayhorn/build/libs/jayhorn.jar"

#JAYHORN = "./jayhorn.jar"


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



def compile(prog, build_dir):
    if debug: print "Compiling ... " + prog
    d = build_dir + os.sep + ".." + os.sep
    cmd = ['rm', '-rf', build_dir+os.sep+'*']
    print " ".join(x for x in cmd)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cmd = ['javac', '-d', build_dir, '-sourcepath', d,  prog]
    p.communicate()
    print " ".join(x for x in cmd)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result, _ = p.communicate()
    rc = p.returncode
    return rc


def run_with_timeout(tool, command, timeout):
    import time
    import subprocess
    if debug: print "Running .. " + " ".join(x for x in command)
    p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while timeout > 0:
        if p.poll() is not None:
            result, _ = p.communicate()
            return result
        time.sleep(0.1)
        timeout -= 0.1
    else:
        try:
            p.kill()
        except OSError as e:
            if e.errno != 3:
                raise
    return None

def processResult(d, bench, result, tool):
    if debug: print result
    #opt = " ".join(x for x in options)
    
    bench_ls = bench.split("_")
    exp = bench_ls[len(bench_ls)-1]
    expected = "UNKNOWN" if len(bench_ls)==1 else ("UNSAFE" if "false" in exp else "SAFE")
    stats = {"tool": tool, "result":"", "expected":expected,
             "time":"", "mem":"",
             "soot2cfg":"", "toHorn":"", "logs": ""}
    if result is None:
        stats.update({"result":"TIMEOUT", "logs": "Timeout"})
        b = os.path.relpath(os.path.dirname(d))
        bench = str(b)+"/"+bench
        return {bench:stats}
    logs = ""
    if "COMPILATION ERROR" in result:
        logs += "Compilation error<br>"
        stats.update({"result": "COMPILATION ERROR"})
    else:
        for r in result.splitlines():
            if "BRUNCH_STAT" not in r:
                logs += r +"<br>"
            if 'jayhorn' in tool:
                if "BRUNCH_STAT" in r:
                    goodLine = r.split()
                    if 'Result' in goodLine:
                        stats.update({"result": goodLine[2]})
                    elif 'CheckSatTime' in goodLine :
                        stats.update({"time": "".join(x for x in goodLine[2:])})
                    elif 'SootToCFG' in goodLine :
                        stats.update({"soot2cfg": "".join(x for x in goodLine[2:])})
                    elif 'ToHorn' in goodLine :
                        stats.update({"toHorn": "".join(x for x in goodLine[2:])})
    b = os.path.relpath(os.path.dirname(d))
    bench = str(b)+"/"+bench
    stats.update({"logs":logs})
    return {bench:stats} 

def runBench(args):
    dr = args.directory
    stats = dict()
    for d in dr:
        dir_stat = runDir(d)
        stats.update({str(d):dir_stat})
    if stats and args.html:
         generateHtml(stats)

def getOption(java_file):
    first_line = ""
    with open(java_file, 'r') as f:
        first_line = f.readline()
    if "JayHorn-Option" in first_line:
        first_line = (first_line.split(":")[1]).rstrip()
        return first_line
    else:
        return ""


def minePump(dr):
    all_dir = [os.path.join(dr, name)for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
    all_results = {}
    stats = dict()
    for d in sorted(all_dir):
        if debug: print "Benchmark:\t " + str(d)
        tmp = d.split("/")
        bench = tmp[len(tmp)-1]
        build_dir = d+os.sep+"build"
        if not os.path.exists(build_dir):
                os.mkdir(build_dir)
        java_file = d + os.sep + "Main.java"
        bench_name = os.path.basename(d)
        try:
            cresult = compile(java_file, build_dir)
        except Exception as e:
            print e
        #bench_option = getOption(java_file)
        #jayhorn_option = ['-rta'] if 'rta' in bench_option else []
        if cresult == 0:
            cmd_eldarica = ["java", "-jar", JAYHORN, "-t", "30", "-stats", "-j", build_dir] 
            result = run_with_timeout('jayhorn-eldarica', cmd_eldarica, args.timeout)
            st = processResult(d, bench_name, result, 'jayhorn-eldarica')
            stats.update(st) 
	else:
	    st = processResult(d, bench_name, "COMPILATION ERROR", 'jayhorn-eldarica')
            stats.update(st)
        if debug: print "---------------------"
    pprint.pprint(stats)
    return stats
        

def runDir(dr):
    all_dir = [os.path.join(dr, name)for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
    all_results = {}
    stats = dict()
    for d in sorted(all_dir):
        if debug: print "Benchmark:\t " + str(d)
        tmp = d.split("/")
        bench = tmp[len(tmp)-1]
        #cls = glob.glob(os.path.abspath(d) + os.sep + "*.class")
        java_prog = glob.glob(os.path.abspath(d) + os.sep + "*.java")
        all_build_dir = list()
        for prog in sorted(java_prog):
	    print "Java file: " + str(prog)
            build_dir = os.path.splitext(prog)[0]+"_build"
            all_build_dir.append(build_dir)
            #java_file = java_prog[0]
            bench_name = os.path.basename(prog)
            if not os.path.exists(build_dir):
                os.mkdir(build_dir)
            try:
                cresult = compile(prog, build_dir)
            except Exception as e:
                print e
            #bench_option = getOption(java_file)
            #jayhorn_option = ['-rta'] if 'rta' in bench_option else []
            if cresult == 0:
                cmd_z3 = ['java', "-jar", JAYHORN, "-solver", "z3",  "-t", "20", "-stats", "-j", d]
                cmd_eldarica = ["java", "-jar", JAYHORN, "-t", "20", "-stats", "-j", build_dir] 
                result = run_with_timeout('jayhorn-eldarica', cmd_eldarica, args.timeout)
                st = processResult(prog, bench_name, result, 'jayhorn-eldarica')
                stats.update(st)      
	    else:
		st = processResult(prog, bench_name, "COMPILATION ERROR", 'jayhorn-eldarica')
                stats.update(st)
        if debug: print "---------------------"
    pprint.pprint(stats)
    return stats

head="""
 <tr class = "info">
<td><b>Benchmark</a></td>
      <td><b>Result</a></td>
      <td><b>Expected</a></td>
    <td><b>Soot2Cfg (Time)</b></td>
<td><b>CheckSat (Time)</b></td>
<td><b>Hornify (Time)</b></td>
    </tr>
"""

template="""
 <tr class = "%s">
      <td>%s</td>
<td>%s</td>
 <td>%s</td>
    <td>%s</td>
<td>%s</td>
<td>%s</td>
    </tr>
"""

template2="""
 <tr data-toggle="collapse" data-target="#%s" class="accordion-toggle %s">
      <td>%s</td>
<td>%s</td>
 <td>%s</td>
    <td>%s</td>
<td>%s</td>
<td>%s</td>
    </tr>
"""
template_hidden = """
<tr class = %s>
    <td  class="hiddenRow"><div class="accordian-body collapse" id="%s"> %s </div> </td>
</tr>
"""
 
def generateHtml(stats):
    row = ""
    id = 0
    color = "active"
    for bench_dir, bench_stats in stats.iteritems():
        for bench, values in sorted(bench_stats.items()):
            try:
                if values["expected"] == "UNKNOWN":
                    color = "active"
                else:
                    color = "danger" if values["result"] != values["expected"] else "success"
                row += template2 % (str(id), color, bench, values["result"], values["expected"], str(values["soot2cfg"]), str(values["time"]), str(values["toHorn"])) + "\n"
                row += template_hidden % (color, str(id), values["logs"]) + "\n"
                id +=1
            except Exception as e:
                print "Exception: " + str(e)
                row += template2 % ("active", str(id), bench, " ", " ", " ", " ", " ") + "\n"
                row += template_hidden % (color, str(id), values["logs"]) + "\n"
            
    table = head + row
    header, footer = "", "" 
    with open("view_results/up.html") as h, open ("view_results/low.html") as l:
        header = h.read()
        footer = l.read()
    with  open("view_results/results.html", 'w') as f:
        f.write(header)
        f.write(table)
        f.write(footer)

        
def generateHtmlMinePump(stats):
    row = ""
    id = 0
    color = "active"
    for bench, values in stats.iteritems():
        try:
            color = "danger" if values["result"] != values["expected"] else "success"
            row += template2 % (str(id), color, bench, values["result"], values["expected"],
                                str(values["soot2cfg"]), str(values["time"]), str(values["toHorn"])) + "\n"
            row += template_hidden % (color, str(id), values["logs"]) + "\n"
            id +=1
        except Exception as e:
            print "Excpetion" + str(e)
            row += template2 % ("active", str(id), bench, " ", " ", " ", " ", " ") + "\n"
            row += template_hidden % (color, str(id), values["logs"]) + "\n"
            
    table = head + row
    header, footer = "", "" 
    with open("view_results/up.html") as h, open ("view_results/low.html") as l:
        header = h.read()
        footer = l.read()
    with  open("view_results/minepump.html", 'w') as f:
        f.write(header)
        f.write(table)
        f.write(footer)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='JAYHORN Bench Analysis Utils',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                   JAYHORN Bench Analysis Utils
            --------------------------------
            '''))
    #parser.add_argument ('file', metavar='BENCHMARK', help='Benchmark file')
    parser.add_argument ('directory',  help='Benchmark dirs', nargs='*')
    parser.add_argument('-html', '--html', required=False, dest="html", action="store_true")
    parser.add_argument('-mp', '--mp', required=False, dest="mp", action="store_true")
    parser.add_argument ('--timeout', help='Timeout',
                    type=float, default=20.0, dest="timeout")

    args = parser.parse_args()
    stats = None
    try:
        if args.mp:
            stats = minePump(args.directory[0])
            generateHtmlMinePump(stats)
        else:
            runBench(args)
        #main (args)
    except Exception as e:
        print str(e)

