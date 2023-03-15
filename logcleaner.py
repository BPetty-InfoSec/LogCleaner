# An app that will format text files using RegEx from a format file.
# Each format will be a .json file consisting of an array of objects.
# Each object requires an "action" and a "pattern" attribute
# Actions (currently) consist of replace and delete
# The Replace action requires a "replace" attribute as well, which will
#   be used to replace the pattern on search.
# The files will exist in the "formats" subdirectory.
# Command-line arguments will be:
#   - the name of the format to be used
#   - the name of the file to be formatted
#   - (optionally) a "formats" argument that will display a list of available formats and a short description

import os, re, json
import argparse

parser = argparse.ArgumentParser(description='Read command line arguments')
parser.add_argument('logFormat', help="""The name of the format to be applied to the log file.
                    These format files are located in the "formats" subdirectory""")
parser.add_argument('logFile', help="The log file to read")
parser.add_argument('-o', '--outputFile',
                    help="Name of file to store results of formatting.")
args = parser.parse_args()

if os.name == 'nt':
    osSep = "\\" 
else:
    osSep = "/"

def main(appPath):
    if args.outputFile:
        outputFile = args.outputFile
    else:
        outputFile = CreateGenericLogfile()
    with open(outputFile, 'w') as outputLog:
        try:
            with open(args.logFile, 'rt') as readLog:
                editedLog = readLog.read()
                formats = GetFormats(appPath + osSep + "formats" + osSep + args.logFormat + '.json')
                for item in formats:
                    if item["action"]:
                        match item["action"].lower():
                            case "delete":
                                if item["pattern"]:
                                    editedLog = re.sub(item["pattern"],"",editedLog)
                                else:
                                    print("You must have a pattern for each format")
                                    break
                            case "replace":
                                if item["replace"]:
                                    editedLog = re.sub(item["pattern"],item["replace"],editedLog)
                                else:
                                    print("You must have a replace item for any replace pattern")
                                    break
                            case _:
                                break
                    else:
                        print("Every format line must have an action")
                formatString = "Formatting log file [" + args.logFile + \
                    "] with format-file [" + args.logFormat + \
                    "] and saving to [" + outputFile + "]"
                print(formatString)
                outputLog.write(editedLog)
        except:
            print("The log file [" + args.logFile + "] cannot be opened. Check that it exists and is readable.")
            os._exit(os.EX_OSFILE)


def CreateGenericLogfile(iterDex=0):
    if iterDex == 0:
        iterToken = ""
    else:
        iterToken = str(iterDex)
    outputLogName = "parsedLog" + iterToken + ".log"
    if os.path.isfile(outputLogName):
        outputLogName = CreateGenericLogfile(iterDex+1)
    else:
        with open(outputLogName, 'x') as createLog:
            pass
    return outputLogName


def GetFormats(formatPath):
    try:
        with open(formatPath, 'r') as formatFile:
            return json.load(formatFile)
    except:
        print("The format file [" + formatPath + "] cannot be opened. Check that it exists and is readable.")
        os._exit(os.EX_)


if __name__ == '__main__':
    appPath = os.path.dirname(__file__)
    main(appPath)
