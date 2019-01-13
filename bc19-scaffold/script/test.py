import argparse
import os
import subprocess
from multiprocessing import Pool, Process, Value, Manager
try:
    from termcolor import cprint
except:
    None
import time
import sys
import os

def main():
    manager = Manager()
    stats = manager.dict()
    stats["bluew"] = 0
    stats["redw"] = 0
    stats["count"] = 0
    stats["current"] = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--red", const=str, nargs="?")
    parser.add_argument("-b", "--blue", nargs="?")
    parser.add_argument("-c", "--count", nargs="?")
    parser.add_argument("-s", "--store", nargs="?")
    args = parser.parse_args()
    redpath = str(args.red)
    bluepath = str(args.blue)
    count = int(args.count)

    stats["count"] = count
    storereplay = True

    if int(args.store) == 0:
        storereplay = False
    else:
        storereplay = True

    totalrunning = 0

    morerun = 0
    MAX_PROCESS = 10

    clearScreen()
    cprint("Starting up", "red")
    while True:
        if morerun < count:
            print("Alloting Processes")
            pool = Pool(processes=MAX_PROCESS)
            temp = count - morerun
            if temp > MAX_PROCESS:
                shouldrun = MAX_PROCESS
            else:
                shouldrun = temp
            for i in range(shouldrun):
                totalrunning += 1
                morerun += 1
                pool.apply_async(runSimulation, args=(bluepath, redpath, stats, morerun, storereplay))
            pool.close()
            pool.join()
            totalrunning = 0
        else:
            break
    pretty_print(stats, done=True)

    
def pretty_print(stats, done=False):
    clearScreen()
    cprint("******************************", "magenta")
    if done == False:
        cprint("Running Simulation!", "red", attrs=['bold'])
    else:
        cprint("Simulation Finished!", "red", attrs=['bold'])
    cprint("Simulation: %s / %s" % (stats["current"], stats["count"]), "white")
    cprint("Turn Status:")
    for itm in stats.keys():
        if itm != "bluew" and itm != "redw" and itm != "count" and itm != "current":
            turn = stats[itm]
            if turn != "Preparing...":
                cprint("\t Turn\t: %s / 999" % (turn), "white")
            else:
                cprint("\t Turn\t: %s" % (turn))
    cprint("Current Streak:", "cyan")
    cprint("\t Red Wins\t: %s" % (stats["redw"]), "red")
    cprint("\t Blue Wins\t: %s" % (stats["bluew"]), "blue")
    cprint("******************************", "magenta")

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def runSimulation(bluepath, redpath, stats, intal, storereplay):
    stats["current"] += 1
    stats[intal] = "Preparing..."
    # clearScreen()
    pretty_print(stats)
    checktime = 0
    if storereplay:
        process = subprocess.Popen(["bc19run", "-b", bluepath, "-r", redpath, "-d", "false", "--re", "replay%s.bc19" % intal], stdout=subprocess.PIPE)  
    else:
        process = subprocess.Popen(["bc19run", "-b", bluepath, "-r", redpath, "-d", "false"], stdout=subprocess.PIPE)  
    for line in iter(process.stdout.readline, b''):  # replace '' with b'' for Python 3
        data = line.decode(sys.stdout.encoding)
        if "Script Helper Turn" in data:
            currtime = time.time()
            if currtime - checktime > 2:
                data = data.split("\n")[0]
                data = data.split("@")
                stats[intal] = data[1]
                pretty_print(stats)
                checktime = time.time()
        if "Game over, blue won " in data:
            stats["bluew"] += 1
        elif "Game over, red won " in data:
            stats["redw"] += 1
    del stats[intal]
    

if __name__ == "__main__":
    main()