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
    file_path = os.path.join(os.getcwd(), file)

    if os.path.exists(file_path):
        with open(file_path, 'r') as infile:
            schema = json.load(infile)

        doc = commit_schema(schema)

        if schema.get('id', None) is None or schema.get('meta_id', None) is None:
            schema['id'], schema['meta_id'] = doc.id, doc.meta_id

        with open(file_path, 'w') as outfile:
            json.dump(schema, outfile)

        log.info("Schema commited to DOCUMENT(meta_id=%s)", doc.meta_id)

    else:
        log.warning("No schema found at %s", file_path)
    
        
def do_program(args):
    args = parse_cli_args(args)

    if args.action[0] == 'commit':
        if len(args.action) > 1:
            commit(args.action[1])
        else:
            log.warning("No file path inputted with commit action")

def entrypoint():
    """Entrypoint for build package
    """
    do_program(sys.argv[1:])


if __name__ == "__main__":
    do_program(sys.argv[1:])
