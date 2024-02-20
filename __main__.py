import file_dialog
import vdf_to_json
import argparse
import os

parser = argparse.ArgumentParser(description="Simple App to export and import Closed Caption txt files to export them to json\nFor Easier implementation with Crowdsourcing Translation websites")
parser.add_argument("-o", "--output",
                    metavar='OUTPUT_PATH',
                    type=str,
                    action='store',
                    help="Set Output of converted file")
parser.add_argument("-i", "--input",
                    metavar='INPUT_PATH',
                    type=str,
                    help="Set input file")

args = parser.parse_args()

if args.input is not None:
    # Input is provided, perform conversion based on the input
    input_extension = os.path.splitext(args.input)[1].lower()

    if input_extension == ".json":
        if args.output is not None:
            vdf_to_json.json_to_vdf_file(args.input, Override_file_Output=args.output)
            print(f"Converted JSON file to .txt at {args.output}")
        else:
            vdf_to_json.json_to_vdf_file(args.input)
            print(f"Converted JSON file to .txt at {os.path.splitext(args.input)[0] + '.txt'}")
    elif input_extension in [".txt", ".vdf"]:
        if args.output is not None:
            vdf_to_json.cc_txt_to_json_dump(args.input, args.output)
            print(f"Converted VDF file to .json at {args.output}")
        else:
            vdf_to_json.cc_txt_to_json_dump(args.input)
            print(f"Converted VDF file to .json at {os.path.splitext(args.input)[0] + '.json'}")
    else:
        print("Input file needs to have one of the extensions: \".json\", \".txt\", \".vdf\"")
else:
    # No input provided, start the GUI
    file_dialog.GUI().start_gui()
