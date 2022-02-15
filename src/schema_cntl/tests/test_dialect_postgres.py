import pytest
import os
import sys


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

from dialects.postgres import DataTypes, Column, Table

@pytest.mark.parametrize('string,result',[
  ('bool', (DataTypes.BOOL, None)),
  ('text', (DataTypes.TEXT, None)),
  ('varchar(100)', (DataTypes.VARCHAR, 100)),
  ('char(50)', (DataTypes.CHAR, 50)),
  ('decimal', (DataTypes.DECIMAL, None)),
  ('int', (DataTypes.INTEGER, None)),
  ('date', (DataTypes.DATE, None))
])
def test_data_type_enumeration(string, result):
    actual = DataTypes.convert(string)
    assert all (act == exp for act, exp in zip(actual, result))

@pytest.mark.parametrize('string,enums,result',[
  ('bool', [DataTypes.VARCHAR, DataTypes.CHAR], False),
  ('varchar', [DataTypes.VARCHAR, DataTypes.CHAR], True),
  ('char', [DataTypes.VARCHAR, DataTypes.CHAR], True),
  ('decimal', [DataTypes.DECIMAL, DataTypes.INTEGER], True),
  ('int', [DataTypes.DECIMAL, DataTypes.INTEGER], True),
  ('date', [DataTypes.DECIMAL, DataTypes.INTEGER], False)
])
def test_belongs(string, enums, result):
    assert DataTypes.belongs_to_types(string, *enums) == result

@pytest.mark.parametrize('col_def,result', [
  ({
      "name": "test",
      "type": "int",
  }, "{test} int"),
  ({
      "name": "column",
      "type": "varchar(50)",
      "not_null": True
  }, "{column} varchar(50) NOT NULL"),
  ({
     "name": "key",
     "primary_key": True
  }, "{key} SERIAL PRIMARY KEY"),
  ({
    "name": "fk",
    "foreign_key_references": "foreign_table"
  }, "{fk} integer REFERENCES {fkr}")
])
def test_column_definition(col_def, result):
    assert Column.define(**col_def) == result

@pytest.mark.parametrize('name,col_defs,result',[
  ('table_name_1', [
        {
            "name": "column_name",
            "type": "varchar(100)",
        },
        {
            "name": "column_name_2",
            "type": "int",
            "not_null": True
        },
        {
            "name": "column_name_3",
            "primary_key": True,
        },
        {
            "name": "column_name_4",
            "foreign_key_references" : "foreign_table",
        },
        {
            "name": "column_name_5",
            "type": "char(25)",
        }
    ],
    ("CREATE TABLE {table_name} ({col_0} varchar(100), {col_1} int NOT NULL, {col_2} SERIAL PRIMARY KEY, {col_3} integer REFERENCES {fkr}, {col_4} char(25));", 
    ['table_name', 'col_0', 'col_1', 'col_2', 'col_3', 'col_4'],
    ['table_name_1', 'column_name', 'column_name_2', 'column_name_3', 'column_name_4', 'column_name_5'] ) 
  ),
  ('table_name_2', [
        {
            "name": "column_name",
            "primary_key": True
        },
        {
            "name": "column_name_2",
            "type": "bool"
        },
        {
            "name": "column_name_3",
            "type" : "date"
        },
    ],
    ("CREATE TABLE {table_name} ({col_0} SERIAL PRIMARY KEY, {col_1} bool, {col_2} date);",
    ['table_name', 'col_0', 'col_1', 'col_2'],
    ['table_name_2', 'column_name', 'column_name_2', 'column_name_3'])
  )
])
def test_table_creation(name, col_defs, result):
    actual_result = Table.create(name, *col_defs)
    assert actual_result[0] == result[0]
    assert all(actual_result[1][i] == res for i, res in enumerate(result[1]))
    assert all(actual_result[2][i] == res for i, res in enumerate(result[2]))