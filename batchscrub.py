import os
import sys
import subprocess

start_dir = ""

def walk_tree():
    files_processed = 0
    base = ["python", "addscrub.py"]
    with open("processed.txt", "wb") as processed:
        for root, files, dirs in os.walk()
            for file in files:
                if "newclan_merged.cha" in file or "_final.cha in file":
                    command = base + os.path.join(root, file)
                    abbrev_command = [os.path.split(element)[1] for element in command]
                    print "command: {}".format(abbrev_command)
                    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
                    pipe.communicate()  # blocks until the subprocess in complete
                    processed.write(key+":\tcommand: {}\n".format(abbrev_command))
                    files_processed_count += 1
        print "{} files processed".format(files_processed)

if __name__ == "__main__":
    start_dir = sys.argv[1]
    walk_tree()
