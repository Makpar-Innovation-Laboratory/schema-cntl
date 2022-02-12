import pytest
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

from dialects.postgres import DataTypes, Column

@pytest.mark.parametrize('name,data_type,limit,fk,pk,nnull,result', [
  ('test', DataTypes.INTEGER, None, None, False, False, 'test int'),
  ('column', DataTypes.VARCHAR, 50, None, False, True, 'column varchar(50) NOT NULL'),
  ('key', None, None, None, True, False, 'key SERIAL PRIMARY KEY'),
  ('fk', None, None, 'foreign_table', False, False, 'fk integer REFERENCES foreign_table' )
])
def test_column_definition(name, data_type, limit, fk, pk, nnull, result):
    test_result = Column.column_definition(name,data_type, limit, fk, pk, nnull)
    assert test_result == result
