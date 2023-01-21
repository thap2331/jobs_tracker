import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--run_mode", help="run mode")
args = parser.parse_args()

if args.run_mode == "test":
    os.environ["runmode"] = "dev"
else:
    os.environ["runmode"] = "prod"

print(os.environ.get("runmode"))
