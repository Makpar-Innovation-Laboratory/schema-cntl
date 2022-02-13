import json
import os
import sys
from argparse import ArgumentParser
from pprint import pprint

APP_DIR= os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(APP_DIR)
sys.path.append(SRC_DIR)

from schema_cntl import settings, schema
from schema_cntl.schema import commit_schema, generate_revision_history, generate_differences
from schema_cntl.util.logger import getLogger

log = getLogger('schema_cntl.main')

def parse_cli_args(args):
    parser = ArgumentParser()
    parser.add_argument('action', nargs='*', help = "Actions: commit, history, diff")
    parser.add_argument('-str', '--start', help="Starting strand of the revision history", default=0, type=int)
    parser.add_argument('-no', '--number', help="Ending strand of the revision history", default=1, type=int)
    return parser.parse_args(args)

def print_revision_line(index, start = 0):
    if settings.LOG_LEVEL in ['INFO', 'DEBUG']:
        index += start
        print('---------------------------------------------- REVISION ', index)

def load_schema(file):
    file_path = os.path.join(os.getcwd(), file)

    if os.path.exists(file_path):
        with open(file_path, 'r') as infile:
            schema = json.load(infile)

        return schema

    log.warning("No schema found at %s", file_path)
    return None

def save_schema(file, schema):
    file_path = os.path.join(os.getcwd(), file)

    with open(file_path, 'w') as outfile:
        json.dump(schema, outfile)

def commit(file):
    schema = load_schema(file)

    if schema is not None:
        doc = commit_schema(schema)

        if schema.get('id', None) is None or schema.get('meta_id', None) is None:
            schema['id'], schema['meta_id'] = doc.id, doc.meta_id

        save_schema(file, schema)

        log.info("Schema commited to DOCUMENT(meta_id=%s)", doc.meta_id)

def history(file, start, no):
    schema = load_schema(file)

    if schema is not None:

        if schema.get('id', None) is None:
            log.warning('Schema has no id, please commit before generating history')
            return

        items = generate_revision_history(id=schema['id'], start=start, no=no)

        for i, item in enumerate(items):
            print_revision_line(i, start)
            pprint(item.schema.to_json())
        

def diff(file, start, end):
    schema = load_schema(file)

    if schema is not None:

        if schema.get('id', None) is None:
            log.warning('Schema has no id, please commit before generating revision diff')
            return

        generate_differences(id=schema['id'], strand_start_index=start, strand_end_index=end)
        


def do_program(args):
    args = parse_cli_args(args)

    if args.action[0] == 'commit':
        if len(args.action) > 1:
            commit(args.action[1])
        else:
            log.warning("Command is of the form `commit <path-to-schema.json>`")
            return
    
    if args.action[0] == 'history':
        history(args.action[1], args.start, args.number)
        return

    if args.action[0] == 'diff':
        if len(args.action[1:]) == 3:
            diff(file=args.action[1], start=int(args.action[2]), end=int(args.action[3]))
            pass
        else:
            log.warning("Command is of the form `diff <revision 1> <revision 2>`")
            return 

def entrypoint():
    """Entrypoint for build package
    """
    do_program(sys.argv[1:])


if __name__ == "__main__":
    do_program(sys.argv[1:])
