import json
import os
import sys
from argparse import ArgumentParser
from pprint import pprint

APP_DIR= os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(APP_DIR)
sys.path.append(SRC_DIR)

from schema_cntl import settings
from schema_cntl.schema import commit, revision_history, differences, revision_schema
from schema_cntl.util.logger import getLogger

log = getLogger('schema_cntl.main')

def parse_cli_args(args):
    parser = ArgumentParser()
    parser.add_argument('action', nargs='*', help = "Actions: commit, history, diff, schema")
    parser.add_argument('-l', '--limit', help="Number of records in the revision history", default=1, type=int)
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

def commit_schema(file):
    schema = load_schema(file)

    if schema is not None:
        doc = commit(schema)

        if schema.get('id', None) is None or schema.get('meta_id', None) is None:
            schema['id'], schema['meta_id'] = doc.id, doc.meta_id

        save_schema(file, schema)

        log.info("Schema commited to DOCUMENT(meta_id=%s)", doc.meta_id)

def generate_history(file, no):
    schema = load_schema(file)

    if schema is not None:

        if schema.get('id', None) is None:
            log.warning('Schema has no id, please commit before generating history')
            return

        items = revision_history(id=schema['id'], start=0, no=no)

        for i, item in enumerate(items):
            print_revision_line(i, 0)
            pprint(item.schema.to_json())
        

def generate_diff(file, start, end):
    schema = load_schema(file)

    if schema is not None:

        if schema.get('id', None) is None:
            log.warning('Schema has no id, please commit before generating revision diff')
            return

        differences(id=schema['id'], strand_start_index=start, strand_end_index=end)
        

def generate_schema_revision(file, revision):
    schema = load_schema(file)

    if schema is not None:

        if schema.get('id', None) is None:
            log.warning('Schema has no id, please commit before generating schema')
            return

        revision_schema(id=schema['id'], strand_no=revision)

def do_program(args):
    args = parse_cli_args(args)

    command_form = None 

    if args.action[0] == 'commit':
        if len(args.action[1:]) == 1:
            commit_schema(args.action[1])
            return
        command_form = "`commit <path-to-schema>`"
    
    if args.action[0] == 'history':
        if len(args.action[1:]) == 1:
            generate_history(args.action[1], args.number)
            return
        command_form = "`history <path-to-schema> --limit <limit>`"
        

    if args.action[0] == 'diff':
        if len(args.action[1:]) == 3:
            generate_diff(file=args.action[1], start=int(args.action[2]), end=int(args.action[3]))
            return
        command_form = "`diff <path-to-schema> <revision 1> <revision 2>`"

    if args.action[0] == 'schema':
        if len(args.action[1:]) == 2:
            generate_schema_revision(file=args.action[1], revision=int(args.action[2]))
            return
        command_form = "`schema <path-to-schema> <revision>`"

    if command_form is not None:
        log.warning("Command is of the form : %s", command_form)
        return

    log.warning("Input not understood.")
    return

def entrypoint():
    """Entrypoint for build package
    """
    do_program(sys.argv[1:])


if __name__ == "__main__":
    do_program(sys.argv[1:])
