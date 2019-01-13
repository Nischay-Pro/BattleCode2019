import argparse
import os
import subprocess
try:
    from termcolor import cprint
except:
    None
import time
import sys
import os
import shutil

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", const=str, nargs="?")
    parser.add_argument("-l", "--less", const=str, nargs="?")
    travis = False
    if os.path.isfile("input.txt"):
        print("Travis Mode")
        travis = True
        lessmoded = True
        fileman = open("input.txt", "r") 
        dataman = fileman.read()
        print(dataman)
        frk = dataman.split("\n")
        frk = frk[0]
        frk = frk.split(" ")
        for itm in frk:
            dirman = os.path.split(itm)[0]
            if "bc19-scaffold/bots" in dirman:
                redpath = dirman
                bluepath = redpath
                break
    else:
        print("Non Travis Mode")
        args = parser.parse_args()
        redpath = str(args.test)
        less = int(args.less)
        bluepath = redpath
        lessmoded = False
        clearScreen()
        if less == 1:
            lessmoded = True
        else:
            lessmoded = False
            cprint("Starting up", "red")

    stats = {
        "turn":"Preparing...",
        "bot": os.path.basename(os.path.normpath(redpath)),
        "args": "Waiting",
        "seed":{
            1:"Checking..."
        }
    }
    checktime = time.time()
    shutil.rmtree("seed_logs",ignore_errors=True,onerror=None)
    os.makedirs("seed_logs")
    for seed in range(1,1001):
        if not lessmoded:
            stats["turn"] = "Preparing..."
        pretty_print(stats, seed, lessmode=lessmoded)
        process = subprocess.Popen(["bc19run", "-b", bluepath, "-r", redpath, "-d", "false", "-s", str(seed)], stdout=subprocess.PIPE)
        # lprint("Testing on Seed %s" % seed, lessmoded)
        if not lessmoded:
            stats["args"] = " ".join(process.args)
        verbose = []
        counter = 10
        for line in iter(process.stdout.readline, b''):
            data = line.decode(sys.stdout.encoding)
            data = data.encode('utf-8').decode('utf-8')
            data = str(data)
            if "Script Helper Turn" in data:
                currtime = time.time()
                if currtime - checktime > 2:
                    data2 = data.split("\n")[0]
                    data2 = data.split("@")
                    if not lessmoded:
                        stats["turn"] = data2[1].strip()
                    pretty_print(stats, seed, lessmode=lessmoded)
                    checktime = time.time()
            verbose.append(data)
            if counter < 10:
                counter -= 1
                if counter <= 0:
                    if not lessmoded:
                        stats["seed"][seed] = "Failed"
                    with open('seed_logs/seed_%s.txt' % seed, mode='wt', encoding='utf-8') as myfile:
                        myfile.write('\n'.join(verbose))
                    process.terminate()
                    break
            if "vm.js" in data:
                if not lessmoded:
                    stats["seed"][seed] = "Failed"
                lprint("Seed %s Failed. Script Error" % seed, lessmoded, travis)
                counter -= 1
            if "Robot is frozen due" in data:
                if not lessmoded:
                    stats["seed"][seed] = "Time Failed"
            if "blue won" in data:
                if not lessmoded:
                    if stats["seed"][seed] == "Time Failed":
                        stats["seed"][seed] = "Passed (Time Failed)"
                lprint("Seed %s Passed" % seed, lessmoded, travis)
                pretty_print(stats, seed, lessmode=lessmoded)
                process.terminate()
                break
            if "red won" in data:
                if not lessmoded:
                    if stats["seed"][seed] == "Time Failed":
                        stats["seed"][seed] = "Passed (Time Failed)"
                lprint("Seed %s Passed" % seed, lessmoded, travis)
                pretty_print(stats, seed, lessmode=lessmoded)
                process.terminate()
                break
            if "failed to initialize" in data:
                if not lessmoded:    
                    stats["seed"][seed] = data.strip()
                pretty_print(stats, seed, lessmode=lessmoded)
                lprint("Seed %s Failed. Initialization Error" % seed, lessmoded, travis)
    pretty_print(stats, 1000, done=True, lessmode=lessmoded)
    lprint("Done", lessmoded, travis)


def lprint(whattoprint, lessmode, travis):
    if lessmode:
        print(whattoprint)
        with open('log.txt', mode='a+', encoding='utf-8') as myfile:
            myfile.write('\n%s' % whattoprint)


def pretty_print(stats, seed, done=False, lessmode=False):
    if lessmode == False:
        try:
            clearScreen()
            cprint("******************************", "magenta")
            if done == False:
                cprint("Running Seed Testing!", "red", attrs=['bold'])
            else:
                cprint("Seed Testing Finished!", "red", attrs=['bold'])
            cprint("Bot: %s" % stats["bot"], "green")
            cprint("Argument: %s" % stats["args"], "green")
            cprint("Seed: %s / %s" % (seed, 1000), "white")
            cprint("Turn Status:")
            turn = stats["turn"]
            if turn != "Preparing...":
                cprint("\t Turn\t: %s / 999" % (turn), "white")
            else:
                cprint("\t Turn\t: %s" % (turn))
            cprint("Seed Status:", "cyan")
            for itm in stats["seed"].keys():
                status = stats["seed"][itm]
                color = "red"
                if "Passed" in status:
                    color = "blue"
                if "Time Failed" in status:
                    color = "yellow"
                if "Checking..." in status:
                    color = "blue"
                if "failed to initialize" in status:
                    color = "red"
                cprint("\t Seed %s\t: %s" % (itm, status), color)
            cprint("******************************", "magenta")
        except KeyError:
            print(stats)

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    

if __name__ == "__main__":
    main()