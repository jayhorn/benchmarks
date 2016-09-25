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
import shutil

debug = True


"""
Tools
"""
JPF = "./jpf-travis/jpf-core/build/RunJPF.jar"

CBMC = "./cbmc/src/cbmc"

INFER = "infer"

CPA = "./cpachecker/scripts/cpa.sh"

JAYHORN = "../jayhorn/jayhorn/build/libs/jayhorn.jar"

#JAYHORN = "./jayhorn.jar"



########
# UTILITIES
########


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
    bench_ls = bench.split("_")
    exp = bench_ls[len(bench_ls)-1]
    expected = "UNKNOWN" if len(bench_ls)==1 else ("UNSAFE" if "false" in exp else "SAFE")
    if expected == "UNKNOWN":
        if bench.startswith("Sat"):
            expected = "SAFE"
        elif bench.startswith("Unsat"):
            expected = "UNSAFE"
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


####
# Run all benchmarks
####

def runBench(args):
    dr = args.directory
    stats = dict()
    infer_stat, jayhorn_stat = dict(), dict()
    if debug: print "Running on " + str(dr) + "  ..."
    for d in dr:
        if args.infer and args.cpa:
            infer_stat = runInfer(args, d)
            jayhorn_stat = runJayHorn(d,args)
            cpa_stat = runCpa(args, d)
            stats.update({str(d):{"infer":infer_stat,
                                  "jayhorn":jayhorn_stat,
                                  "cpa": cpa_stat
            }})
        elif args.cpa:
            cpa_stat = runCpa(args, d)
            stats.update({str(d):{"cpa":dir_stat}})
        else:
            jayhorn_stat = runJayHorn(d,args)
            stats.update({str(d):{"jayhorn":jayhorn_stat,
                                  "infer": {},
                                  "cpa": {}}})
    if stats and args.html:
         generateHtml(stats)
         

####
# Run Mine Pump with JayHorn
####

def run_jayhorn(build_dir, args):
    cmd_eldarica = ["java", "-jar", JAYHORN, "-t", "60", "-stats", "-j", build_dir, '-mem-prec', "{}".format(args.mem)]
    if args.inline:
        cmd_eldarica.extend(['-inline_size', '30', '-inline_count', '3'])

    return run_with_timeout("jayhorn-eldarica_{}_{}".format(args.mem, args.inline), cmd_eldarica, args.timeout)
    


def minePump(dr, args):
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
            print str(e)
        if cresult == 0:
            result = run_jayhorn(build_dir, args)
            st = processResult(d, bench_name, result, 'jayhorn-eldarica')
            stats.update(st) 
	else:
	    st = processResult(d, bench_name, "COMPILATION ERROR", 'jayhorn-eldarica')
            stats.update(st)
        if debug: print "---------------------"
    #pprint.pprint(stats)
    return stats

####
# Run Infer
####

def inferAnalysis(infer_out):
    stats = dict()
    for out in infer_out:
        bench_ls = out.split("_infer_out")[0]
        bench_ls = bench_ls.split("_")
        exp = bench_ls[len(bench_ls)-1]
        expected = "UNKNOWN" if len(bench_ls)==1 else ("UNSAFE" if "false" in exp else "SAFE")
        if expected == "UNKNOWN":
            if bench.startswith("Sat"):
                expected = "SAFE"
            elif bench.startswith("Unsat"):
                expected = "UNSAFE"
        bench_name = out.split("_infer_out")[0]
        result, logs = "", ""
        try:
            with open(out + os.sep + "bugs.txt", "r") as f:
                issue = f.read()
                result = "SAFE" if "No issues" in issue else "UNSAFE"
            with open(out + os.sep + "toplevel.log", "r") as f:
                for l in f.readlines():
                    logs += l + "<br>"
            stat_json = json.load(open(out + os.sep + "stats.json"))
            stat_times = stat_json['float']
            st = {"result": result, "expected":expected, "logs": logs}
        except Exception as e:
            st = {"result": "ERROR", "expected":expected, "logs": str(e)}
        stats.update({bench_name:dict(st.items() + stat_times.items())})
    return stats
        
def runInfer(args, dr):
    print "--- Running Infer --- "
    all_dir = [os.path.join(dr, name) for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
    all_build_dir = list()
    infer_out = "infer_out"
    if args.mp:
        for d in sorted(all_dir):
            if debug: print "Benchmark:\t " + str(d)
            tmp = d.split("/")
            bench = tmp[len(tmp)-1]
            build_dir = os.path.splitext(d)[0]
            bench_name = os.path.basename(d)
            out = infer_out + os.sep + (bench_name.split(".java")[0])
            all_build_dir.append(out)
            cmd = [INFER, "-o", out, "-a", "checkers", "--", "javac", d+os.sep+"Main.java", "-cp", d]
            try:
                result = run_with_timeout('infer', cmd, args.timeout)
            except Exception as e:
                print str(e)
    else:
        print all_dir
        for d in sorted(all_dir):
            if debug: print "Benchmark:\t " + str(d)
            tmp = d.split("/")
            bench = tmp[len(tmp)-1]
            java_prog = glob.glob(os.path.abspath(d) + os.sep + "*.java")
            for prog in sorted(java_prog):
	        print "Java file: " + str(prog)
                build_dir = os.path.splitext(prog)[0]+"_build"
                bench_name = os.path.basename(prog)
                infer_out = (bench_name.split(".java")[0])+"_infer_out"
                all_build_dir.append(infer_out)
                if not os.path.exists(build_dir):
                    os.mkdir(build_dir)
                cmd = [INFER, "-o", infer_out, "-a", "checkers", "--", "javac", prog, "-d", build_dir]
                try:
                    result = run_with_timeout('infer', cmd, args.timeout)
                except Exception as e:
                    print str(e)
                if debug: print "---------------------"
    stats = inferAnalysis(all_build_dir)
    pprint.pprint(stats)
    return stats

####
# Run CPA
####

def cpaAnalysis(cpa_out):
    stats = dict()
    for bench, values in cpa_out.iteritems():
        bench_ls = bench.split("_")
        exp = bench_ls[len(bench_ls)-1]
        expected = "UNKNOWN" if len(bench_ls)==1 else ("UNSAFE" if "false" in exp else "SAFE")
        if expected == "UNKNOWN":
            if bench.startswith("Sat"):
                expected = "SAFE"
            elif bench.startswith("Unsat"):
                expected = "UNSAFE"
        st = dict()
        try:
            cpa_stats = (values["logs"]).split("Report.html")[0]
            time = ""
            with open(cpa_stats+os.sep+"Statistics.txt", 'r') as f:
                for l in f.readlines():
                    if  "Total CPU time for CPAchecker" in l:
                        time = (l.split(":")[1]).rstrip()
            st = {"result": values["result"], "expected":expected, "time":time, "logs": values["logs"]}
        except Exception as e:
            st = {"result": "UNKNOWN", "expected":expected, "time":"", "logs": str(e)}
        stats.update({bench:st})
    return stats

def runCpa(args, dr):
    print "--- Running CpaChecker --- "
    all_dir = [os.path.join(dr, name)for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
    all_build_dir = list()
    raw_results = dict()
    cpa_out = "cpachecker_out"
    if not os.path.exists(cpa_out):
        os.mkdir(cpa_out)
    if args.mp:
        for d in sorted(all_dir):
            if debug: print "Benchmark:\t " + str(d)
            tmp = d.split("/")
            bench = tmp[len(tmp)-1]
            outputpath = cpa_out+os.sep+bench
            cmd = [CPA, "-valueAnalysis-java-with-RTT", "-cp", d, "-outputpath", outputpath, "Main"]
            result = ""
            try:
                result = run_with_timeout('cpa', cmd, args.timeout)
                res = ""
                if result:
                    for line in result.split("\n"):
                        if "Verification result" in line:
                            res = "UNSAFE" if "FALSE" in line else "SAFE"
                else:
                    res = "UNKNOWN"
                raw_results.update({d:{"result":res, "logs": (outputpath + os.sep + "Report.html")}})
            except Exception as e:
                raw_results.update({prog: {"result":"UNKNOWN", "logs": result}})
    else:
        for d in sorted(all_dir):
            if debug: print "Benchmark:\t " + str(d)
            tmp = d.split("/")
            bench = tmp[len(tmp)-1]
            java_prog = glob.glob(os.path.abspath(d) + os.sep + "*.java")
            for prog in sorted(java_prog):
	        print "Java file: " + str(prog)
                build_dir = os.path.splitext(prog)[0]
                build_dir = os.path.dirname(build_dir)
                bench_name = os.path.basename(prog).split(".java")[0]
                outputpath =  cpa_out+os.sep+bench_name
                cmd = [CPA, "-valueAnalysis-java-with-RTT", "-cp", build_dir, "-outputpath",outputpath, bench_name]
                result = ""
                try:
                    result = run_with_timeout('cpa', cmd, args.timeout)
                    res = ""
                    if result:
                        for line in result.split("\n"):
                            if "Verification result" in line:
                                res = "UNSAFE" if "FALSE" in line else "SAFE"
                    else:
                         res = "UNKNOWN"
                    raw_results.update({bench_name:{ "result":res, "logs":(outputpath + os.sep + "Report.html")}})
                except Exception as e:
                    raw_results.update({prog: {"result":"UNKNOWN", "logs": result}})
                
    stats = cpaAnalysis(raw_results)
    pprint.pprint(stats)
    return stats


def runJayHorn(dr, args):
    print "--- Running JayHorn --- "
    all_dir = [os.path.join(dr, name)for name in os.listdir(dr) if os.path.isdir(os.path.join(dr, name)) ]
    all_results = {}
    stats = dict()
    for d in sorted(all_dir):
        if debug: print "Benchmark:\t " + str(d)
        tmp = d.split("/")
        bench = tmp[len(tmp)-1]
        java_prog = glob.glob(os.path.abspath(d) + os.sep + "*.java")
        all_build_dir = list()
        for prog in sorted(java_prog):
	    print "Java file: " + str(prog)
            build_dir = os.path.splitext(prog)[0]+"_build"
            all_build_dir.append(build_dir)
            bench_name = os.path.basename(prog)
            if not os.path.exists(build_dir):
                os.mkdir(build_dir)
            try:
                cresult = compile(prog, build_dir)
            except Exception as e:
                print e
            if cresult == 0:
                result = run_jayhorn(build_dir, args)
                st = processResult(prog, bench_name, result, 'jayhorn-eldarica')
                stats.update(st)      
	    else:
		st = processResult(prog, bench_name, "COMPILATION ERROR", 'jayhorn-eldarica')
                stats.update(st)
        if debug: print "---------------------"     
    return stats

head="""
          <div id="%s" class="tab-pane active">
            <table class="table">
 <tr class = "info">
<td><b>Benchmark</b></td>
      <td><b>Result</b></td>
      <td><b>Expected</b></td>
    <td><b>Soot2Cfg (Time)</b></td>
<td><b>CheckSat (Time)</b></td>
<td><b>Hornify (Time)</b></td>
    </tr>
"""

infer_head="""
          <div id="%s" class="tab-pane">
            <table class="table">
 <tr class = "info">
<td><b>Benchmark</b></td>
      <td><b>Result</b></td>
      <td><b>Expected</b></td>
    <td><b>Analysis (Time)</b></td>
<td><b> Capture (Time)</b></td>
<td><b> Reporting (Time)</b></td>
    </tr>
"""

cpa_head="""
          <div id="%s" class="tab-pane">
            <table class="table">
 <tr class = "info">
<td><b>Benchmark</a></td>
      <td><b>Result</b></td>
      <td><b>Expected</b></td>
    <td><b>Analysis (Time)</b></td>
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

template_cpa="""

 <tr data-toggle="collapse" data-target="#%s" class="accordion-toggle %s">
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

template_hidden_cpa = """
<tr class = %s>
    <td  class="hiddenRow"><div class="accordian-body collapse" id="%s"> <a href=%s>CPAChecker Report</a> </div> </td>
</tr>
"""

foot_table = """
</table>
</div>
"""

def jayHornHtml(stats):
    row = ""
    id = 0
    color = "active"
    for bench, values in sorted(stats.items()):
        id_s = "jayhorn"+str(id)
        try:
            if values["expected"] == "UNKNOWN":
                color = "active"
            else:
                color = "danger" if values["result"] != values["expected"] else "success"
            row += template2 % (id_s, color, bench, values["result"],\
                                values["expected"], str(values["soot2cfg"]),\
                                str(values["time"]), str(values["toHorn"])) + "\n"
            row += template_hidden % (color, id_s, values["logs"]) + "\n"
        except Exception as e:
            print "Exception: " + str(e)
            row += template2 % ("active", id_s, bench, " ", " ", " ", " ", " ") + "\n"
            row += template_hidden % (color, id_s, values["logs"]) + "\n"
        id +=1
    jayhorn_head = head % "jayhorn"
    table = jayhorn_head + row
    return table

def inferHtml(stats):
    row = ""
    id = 0
    color = "active"
    for bench, values in sorted(stats.items()):
        id_s = "infer"+str(id)
        try:
            if values["expected"] == "UNKNOWN":
                color = "active"
            else:
                color = "danger" if values["result"] != values["expected"] else "success"
            row += template2 % (id_s, color, bench, values["result"],\
                                values["expected"], str(values["analysis_time"]),\
                                str(values["capture_time"]), str(values["reporting_time"])) + "\n"
            row += template_hidden % (color, id_s, values["logs"]) + "\n"
        except Exception as e:
            print "Exception: " + str(e)
            row += template2 % ("active", id_s, bench, " ", " ", " ", " ", " ") + "\n"
            row += template_hidden % (color, id_s, values["logs"]) + "\n"
        id +=1
    head_in = infer_head % "infer"
    table = head_in + row
    return table

def cpaHtml(stats):
    row = ""
    id = 0
    color = "active"
    for bench, values in sorted(stats.items()):
        id_s = "cpa"+str(id)
        try:
            if values["expected"] == "UNKNOWN":
                color = "active"
            else:
                color = "danger" if values["result"] != values["expected"] else "success"
            row += template_cpa % (id_s, color, bench, values["result"],\
                                values["expected"], str(values["time"])) + "\n"
            row += template_hidden_cpa % (color, id_s, values["logs"]) + "\n"
        except Exception as e:
            print "Exception: " + str(e)
            row += template_cpa % ("active", id_s, bench, " ", " ", " ") + "\n"
            row += template_hidden % (color, id_s, values["logs"]) + "\n"
        id +=1
    head_in = cpa_head % "cpa"
    table = head_in + row
    return table

def generateHtml(stats):
    row = ""
    id = 0
    color = "active"
    jayhorn_table, infer_table, cpa_table = "", "", ""
    for d, v in stats.iteritems():
        try:
            jayhorn_table += jayHornHtml(v['jayhorn'])
        except Exception as e:
            print str(e)
            
        try:
            infer_table += inferHtml(v['infer'])
        except Exception as e:
            print str(e)
            
        try:
            cpa_table += cpaHtml(v['cpa'])
        except Exception as e:
            print str(e)

    jayhorn_table = jayhorn_table + foot_table
    infer_table = infer_table + foot_table
    cpa_table = cpa_table + foot_table
    header, footer = "", "" 
    with open("view_results/up.html") as h, open ("view_results/low.html") as l:
        header = h.read()
        footer = l.read()
    out = "view_results/results.html" 
    with  open(out, 'w') as f:
        f.write(header)
        f.write(jayhorn_table)
        f.write(infer_table)
        f.write(cpa_table)
        f.write(footer)

def generateMinePumpHtml(stats):
    row = ""
    id = 0
    color = "active"
    jayhorn_table, infer_table, cpa_table = "", "", ""
    
    try:
        jayhorn_table += jayHornHtml(stats['jayhorn'])
    except Exception as e:
        print str(e)
            
    try:
        infer_table += inferHtml(stats['infer'])
    except Exception as e:
        print str(e)    
    try:
        cpa_table += cpaHtml(stats['cpa'])
    except Exception as e:
        print str(e)

    jayhorn_table = jayhorn_table + foot_table
    infer_table = infer_table + foot_table
    cpa_table = cpa_table + foot_table
    header, footer = "", "" 
    with open("view_results/up.html") as h, open ("view_results/low.html") as l:
        header = h.read()
        footer = l.read()
    out = "view_results/minepump.html" 
    with  open(out, 'w') as f:
        f.write(header)
        f.write(jayhorn_table)
        f.write(infer_table)
        f.write(cpa_table)
        f.write(footer)
    try:
        shutil.move("cpachecker_out", "view_results")
    except Exception as e:
        print str(e)
        
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
    parser.add_argument('-infer', '--infer', required=False, dest="infer", action="store_true")
    parser.add_argument('-cpa', '--cpa', required=False, dest="cpa", action="store_true")
    parser.add_argument ('--timeout', help='Timeout',
                    type=float, default=60.0, dest="timeout")

    parser.add_argument('-mem', '--mem', required=False, dest="mem", help='Mem prec for JayHorn',
                    type=int, default=3)
    parser.add_argument('-inline', '--inline', required=False, dest="inline", action="store_true")


    args = parser.parse_args()
    try:
        if args.mp:
            if args.cpa:
                jayhorn_stats = minePump(args.directory[0], args)
                cpa_stats = runCpa(args, args.directory[0])
                infer_stats = runInfer(args, args.directory[0])
                generateMinePumpHtml({"cpa":cpa_stats,
                                      "jayhorn":jayhorn_stats,
                                      "infer":infer_stats})
            else:
                stats = minePump(args.directory[0], args)
                generateMinePumpHtml({"cpa":{},
                                      "jayhorn":stats,
                                      "infer":{}})
        else:
            runBench(args)
        #main (args)
    except Exception as e:
        print str(e)

