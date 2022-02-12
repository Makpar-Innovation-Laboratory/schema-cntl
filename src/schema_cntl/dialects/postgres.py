from enum import Enum
from psycopg2 import sql

class DataTypes(Enum):
  BOOL="bool"
  VARCHAR="varchar"
  DOUBLE="float8"
  INTEGER="int"
  DECIMAL="decimal"
  DATE="date"

class Column:
  
  @staticmethod
  def column_definition(name, data_type, limit=None, foreign_key_references=None, primary_key=False, not_null=False):
    if primary_key:
        return "{} SERIAL PRIMARY KEY".format(name)

    if foreign_key_references is not None:
        return "{} integer REFERENCES {}".format(name, foreign_key_references)

    col_def = "{} {}".format(name, data_type.value)

    if limit is not None:
        col_def = "{}({})".format(col_def, limit)

    if not_null:
        col_def = "{} NOT NULL".format(col_def)

    return col_def

