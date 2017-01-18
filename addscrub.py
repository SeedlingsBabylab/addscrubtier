import os
import sys
import re

original_file = ""
output_file = ""

interval_regx = re.compile("(\x15\d+_\d+)")


def add_scrub_tier():
    #Open files to use
    with open(original_file, "rU") as input:
        with open(output_file, "wb") as output:
            #Initialize variables to be used throughout the code
            begin_time = ""
            end_time = ""

            buffer = [""]*7
            scrub_buffer = []

            filling_scrubbuffer = False
            inside_personal = False

            # Loop through opened file
            for index, line in enumerate(input):
                buffer = shift_line_buffer(buffer, line)
                # Alter the formatting of the line in the file
                if "Electronic_Sound_Far Media" in line:
                    line = line.replace("\n", ", SCR\n\tScrubbed_Personal_Information\n")
                if inside_personal:
                    scrub_buffer.append(line)
                if (line.startswith("%com:") or\
                    line.startswith("%xcom:"))\
                    and "personal" in line: #Check if the line is a comment
                        filling_scrubbuffer = True #If comment line, set filling_scrubbuffer variable to true
                        scrub_buffer.append(line)

                        #Check that line is not the end of a block
                        if "begin" in line or "end" not in line:
                            begin_time = find_last_timestamp(buffer) #Set begin_time variable
                            #print "BEGIN_TIME: {}".format(begin_time)
                            scrub_buffer.append("TEMPORARY SCRUB")
                            inside_personal = True #Before the determiend "end" of the block
                        #If the line is at the end of a block
                        if "end" in line:
                            end_time = find_last_timestamp(buffer)
                            #print "END_TIME: {}".format(end_time)
                            fix_scrub_buffer(scrub_buffer, begin_time, end_time)
                            for line in scrub_buffer:
                                #Write data that was appended to scrub_buffer to the output file
                                output.write(line)
                            #Reset variables for next run through the for loop
                            inside_personal = False
                            scrub_buffer = []
                            filling_scrubbuffer = False
                #Run this else if the line is not a comment
                else:
                    if not filling_scrubbuffer:
                        output.write(line)

#Helper function used in "add_scrub_tier" function
def shift_line_buffer(buffer, newline):
    for index, line in enumerate(buffer):
        if index == 0: continue
        #Check if index is at the end of the buffer (len - 1)
        if index == len(buffer)-1:
            #Shift by placing buffer at index into buffer at index - 1
            buffer[index-1] = buffer[index]
            #Reset buffer at index to newline since reached the end of that buffer
            buffer[index] = newline
            return buffer
        #Not at the end of the buffer --> shift buffer at index to index - 1; no need to use newline here
        buffer[index-1] = buffer[index]

#Helper function used in "add_scrub_tier" function
def fix_scrub_buffer(buffer, begin_time, end_time):
    if buffer[-1] == buffer[-2]:
        #Remove item in buffer if duplicate at index -1 and -2
        del buffer[-1]

    #Convert begin_time and end_time into list types split at the "_"
    begin_split = begin_time.split("_")
    end_split = end_time.split("_")

    if buffer[1] == "TEMPORARY SCRUB":
        #Alter the formatting of the buffer at index 1 if == "TEMPORARY SCRUB"
        buffer[1] = "*SCR:\tScrub \x15{}_{}\x15\n".format(begin_split[1],
                                                  end_split[1])
    # "TEMPORARY SCRUB" should be at index 1, this deals with cases in which this does not occur
    else:
        print "Something wrong with personal info in this file:   {}\n".format(original_file)
        print "Timestamp: {}\n".format(begin_time)

#Helper function used in "add_scrub_tier" function- locates the previous timestamp
def find_last_timestamp(buffer):
    #Loop through buffer list (reversed) to find first occurrence
    for line in reversed(buffer):
        regx_result = interval_regx.search(line)
        if not regx_result:
            # interval_regx not found in line
            continue
        else:
            temp_interval_string = regx_result.group()\
                                              .replace("\025", "")
            return temp_interval_string


if __name__ == "__main__":

    original_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        add_scrub_tier()
    except Exception:
        print "\n\n{} WAS PROBLEMATIC\n\n".format(original_file)
