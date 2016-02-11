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
            buffer = [None, None, None, None, None]

            for line in input:
                shift_line_buffer(buffer, line)
                if (line.startswith("%com:") or line.startswith("%xcom:"))\
                    and "personal" in line:
                        print line
                else:
                    output.write(line)

def shift_line_buffer(buffer, newline):
    for index, line in enumerate(buffer):
        if index == 0: continue
        if index == len(buffer):
            buffer[index] = newline
            return buffer
        buffer[index-1] = buffer[index]

def find_last_timestamp(buffer):
    for line in reversed(buffer):
        interval_regx_result = interval_regx.search(line)
        if not interval_regx_result:
            continue
        else:
            temp_interval_string = interval_regx_result.group()\
                                                       .replace("\025", "")
            return temp_interval_string


if __name__ == "__main__":

    original_file = sys.argv[1]
    output_file = sys.argv[2]

    add_scrub_tier()


