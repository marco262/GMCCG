#### EDIT THESE CONFIG OPTIONS ####
# Prints code to console when done parsing
PRINT_CODE = True
# Copies the parsed code to the clipboard
COPY_TO_CLIPBOARD = True
# Will convert any commented out code to "think lit(*)" so it shows up in MUSH output
PARSE_COMMENTS = False
# Will include all blank lines in the source as "think %b"
INCLUDE_BLANK_LINES = False
##################################


import os
from glob import glob

# Try to import the clipboard module
if COPY_TO_CLIPBOARD:
    try:
        import clipboard
    except ImportError:
        clipboard = None
else:
    clipboard = None

def parse_comment(line):
    line = line.rstrip('\n')
    return "think lit(//{})\n".format(line)

def parse_file(filename):
    out_str = ""
    skip = False
    with open(filename) as f:
        for line in f:
            # Open each line of the file separately, as determined by
            # the placement of 
            if line.startswith('/*'):
                # Start of a comment block. Skip all following lines
                # until the comment block ends
                skip = True
            elif line.startswith('*/'):
                # End of a comment block
                skip = False
            elif skip:
                # We're in the middle of a comment block. Skip this line.
                if PARSE_COMMENTS:
                    out_str += parse_comment(line)
            elif line.startswith('//'):
                # Comment skip
                if PARSE_COMMENTS:
                    out_str += parse_comment(line[2:])
            elif line == '\n':
                # Skip empty lines, for brevity
                if INCLUDE_BLANK_LINES:
                    out_str += "think %b\n"
            elif (not line.startswith('@') and
                  not line.startswith('&') and
                  not line.startswith('think')):
                # All MUSH code lines will start with @, & or think.
                # If they don't, they're continuation lines, and should
                # be appended to the previous line, after stripping all
                # leading tabs.
                out_str = out_str.rstrip('\n') + line.lstrip('\t')
            else:
                out_str += line
    line_count = out_str.count('\n')
    out_str = "think Entering {} lines...\n{}".format(line_count, out_str)
    out_str += "think Finished entry."
    if PRINT_CODE:
        print(out_str)

    # Copy the resulting string to the clipboard
    # If the clipboard module couldn't be imported, skip this step
    if clipboard:
        if os.name == 'nt':
            # If the OS type we're running on is Windows, replace all new-lines
            # with carriage return/new line. This helps with copy/pasting to
            # some Windows-based MUSH clients
            clipboard.copy(out_str.replace('\n', '\r\n'))
        else:
            # If OS type is not Windows, just add to clipboard.
            clipboard.copy(out_str)
    return out_str


# The list of directories to search for text files in
# If you don't want to run through a directory
directories = [
##    '1 - Data Dictionary',
##    '2 - Support Functions',
##    '3 - Stat Setter',
##    '4 - XP and Costs',
##    '5 - Health System',
##    '6 - Roller',
##    '7 - Sheet',
##    '8 - Chargen',
    '9 - Critical Sub-Systems',
#    'A - Bonus Sub-Systems',
]


# Go through all the listed directories, and parse each file 1-by-1
# The parsed code will be automatically printed to the console and added to your clipboard
# (depending on your config options)
# The script will pause after each file. Click Enter to continue.

# parse_file('2 - Support Functions/2a - Setup and Data.txt')
for d in directories:
    for filename in glob(os.path.join(d, "*.txt")):
        out_str = parse_file(filename)
        print("\n\n{} has been copied to the clipboard ({} lines).\n"
              "Hit Enter to parse the next file...".format(filename, out_str.count('\n') - 1))
        input()
        print("\n\n\n")
print("Done!")
