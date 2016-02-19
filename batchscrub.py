import os
import sys
import subprocess as sp

start_dir = ""
subject = ""
visit = ""
scrubbed_root = "/Users/andrei/code/work/babylab/addscrubtier/scrubbed"

def walk_tree():
    files_processed_count = 0
    base = ["python", "addscrub.py"]
    with open("processed.txt", "wb") as processed:
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                print file
                if "newclan_merged.cha" in file or "_final.cha" in file:

                   # if file[0:3] == subject and not visit:

                    command = base + [os.path.join(root, file),
                                      os.path.join(scrubbed_root, file.replace(".cha", "_scrubbed.cha"))]

                    abbrev_command = [os.path.split(element)[1] for element in command]
                    print "command: {}".format(abbrev_command)
                    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
                    pipe.communicate()  # blocks until the subprocess in complete
                    processed.write(file[0:5]+":\tcommand: {}\n".format(abbrev_command))
                    files_processed_count += 1
        print "{} files processed".format(files_processed_count)

if __name__ == "__main__":

    start_dir = sys.argv[1]
    subject = sys.argv[2]
    visit = sys.argv[3]

    if subject == "all":
        subject = ""

    if visit == "all":
        visit = ""

    walk_tree()
