import json
import os
import sys
from argparse import ArgumentParser

APP_DIR= os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(APP_DIR)
sys.path.append(SRC_DIR)

from schema_cntl.schema import commit_schema
from schema_cntl.util.logger import getLogger

log = getLogger('schema_cntl.main')

def parse_cli_args(args):
    parser = ArgumentParser()
    parser.add_argument('action', nargs='*', help = "Actions: commit, generate")
    parser.add_argument('-str', '--start', help="Starting strand of the revision history")
    parser.add_argument('-end', '--end', help="Ending strand of the revision history")
    return parser.parse_args(args)


def commit(file):
    if os.path.exists(os.path.join(os.getcwd(), file)):
        with open(os.path.join(os.getcwd(), file), 'r') as infile:
            schema = json.loads(infile)
        return commit_schema(schema)
    log.warning("No schema found at %s", os.path.join(os.getcwd(), file))
    
        
def do_program(args):
    args = parse_cli_args(args)

    if args.action[0] == 'commit':
        commit(args.action[1])


def entrypoint():
    """Entrypoint for build package
    """
    do_program(sys.argv[1:])


if __name__ == "__main__":
    do_program(sys.argv[1:])
