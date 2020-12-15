import os
import sys
import subprocess as sp

start_dir = ""
subject = ""
visit = ""

#scrubbed_root = "/Users/andrei/code/work/babylab/addscrubtier/scrubbed"
scrubbed_root = "/Users/andrei/code/work/babylab/addscrubtier/scrubbed12"


def walk_tree():
    #Initialize variables "files_processed_count" and "base"
    files_processed_count = 0
    base = ["python", "addscrub.py"]
    #Open file for writing in binary mode (wb)
    with open("processed.txt", "wb") as processed:
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                print file
                #if "newclan_merged.cha" in file or "_final.cha" in file:
                #Call helper function to see if the subject in question has already been visited
                if check_subject_visit(file):
                    command = base + [os.path.join(root, file),
                                      os.path.join(scrubbed_root, file.replace(".cha", "_scrubbed.cha"))]

                    abbrev_command = [os.path.split(element)[1] for element in command]
                    print "command: {}".format(abbrev_command)
                    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
                    pipe.communicate()  # blocks until the subprocess in complete
                    #Write to file processed
                    processed.write(file[0:5]+":\tcommand: {}\n".format(abbrev_command))
                    #Increment variable files_processed_count to keep track of number of fiels processed
                    files_processed_count += 1
        #Print the count
        print "{} files processed".format(files_processed_count)

#Helper function called in "walk_tree" function - returns boolean
def check_subject_visit(file):

    #Conditions that would indicate a subject has already been visited; therefore returns "True"
    if subject == "all" and visit == "all":
        return True
    if subject == "all" and visit == file[3:5]:
        return True
    if subject == file[0:2] and visit == "all":
        return True
    if subject == file[0:2] and visit == file[3:5]:
        return True

    #Returns "False" only if none of the above conditions are met
    return False

if __name__ == "__main__":

    start_dir = sys.argv[1]
    subject = sys.argv[2]
    visit = sys.argv[3]

    walk_tree()
