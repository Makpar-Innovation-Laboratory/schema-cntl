import pytest
import os
import sys


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

from main import parse_cli_args


@pytest.mark.parametrize('args,exp_props,exp_values',[
  (['commit', 'src/schema.json'], ['action'], [['commit', 'src/schema.json']]),
  (['history', 'schema.json','--start' ,'0', '--end', '1'], ['action', 'start', 'end'], [['history', 'schema.json'], '0', '1']),
  (['diff', 'schema.json', '0', '2', [['diff', 'schema.json', '0', '1']]])
])
def test_cli_arg_parsing(args,exp_props,exp_values):
    parsed_args = parse_cli_args(args)
    print(parsed_args)
    assert all( getattr(parsed_args, exp_prop) == exp_value 
                  for exp_prop, exp_value in zip(exp_props, exp_values) )