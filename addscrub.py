import os
import sys
import re

original_file = ""
output_file = ""

interval_regx = re.compile("(\x15\d+_\d+)")


def add_scrub_tier():
    with open(original_file, "rU") as input:
        with open(output_file, "wb") as output:
            begin_time = ""
            end_time = ""

            buffer = [""]*7
            scrub_buffer = []

            filling_scrubbuffer = False
            inside_personal = False

            for index, line in enumerate(input):
                buffer = shift_line_buffer(buffer, line)
                if "Electronic_Sound_Far Media" in line:
                    line = line.replace("\n", ", SCR\n\tScrubbed_Personal_Information\n")
                if inside_personal:
                    scrub_buffer.append(line)
                if (line.startswith("%com:") or\
                    line.startswith("%xcom:"))\
                    and "personal" in line:
                        filling_scrubbuffer = True
                        scrub_buffer.append(line)

                        if "begin" in line or "end" not in line:
                            begin_time = find_last_timestamp(buffer)
                            #print "BEGIN_TIME: {}".format(begin_time)
                            scrub_buffer.append("TEMPORARY SCRUB")
                            inside_personal = True
                        if "end" in line:
                            end_time = find_last_timestamp(buffer)
                            #print "END_TIME: {}".format(end_time)
                            fix_scrub_buffer(scrub_buffer, begin_time, end_time)
                            for line in scrub_buffer:
                                output.write(line)
                            inside_personal = False
                            scrub_buffer = []
                            filling_scrubbuffer = False
                else:
                    if not filling_scrubbuffer:
                        output.write(line)

def shift_line_buffer(buffer, newline):
    for index, line in enumerate(buffer):
        if index == 0: continue
        if index == len(buffer)-1:
            buffer[index-1] = buffer[index]
            buffer[index] = newline
            return buffer
        buffer[index-1] = buffer[index]

def fix_scrub_buffer(buffer, begin_time, end_time):
    if buffer[-1] == buffer[-2]:
        del buffer[-1]

    begin_split = begin_time.split("_")
    end_split = end_time.split("_")

    if buffer[1] == "TEMPORARY SCRUB":
        buffer[1] = "*SCR:\tScrub \x15{}_{}\x15\n".format(begin_split[1],
                                                  end_split[1])
    else:
        print "Something wrong with personal info in this file:   {}\n".format(original_file)
        print "Timestamp: {}\n".format(begin_time)

def find_last_timestamp(buffer):
    for line in reversed(buffer):
        regx_result = interval_regx.search(line)
        if not regx_result:
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
