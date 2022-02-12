from enum import Enum
from psycopg2 import sql

class DataTypes(Enum):
  BOOL="bool"
  TEXT="text"
  CHAR="char"
  VARCHAR="varchar"
  DOUBLE="float8"
  INTEGER="int"
  DECIMAL="decimal"
  DATE="date"

  @staticmethod
  def convert(string):
      for member in DataTypes.__members__.values():
          if string == member.value:
              return member
      return None

  @staticmethod
  def belongs_to_types(string, *enums):
      types = [ member.value for member in DataTypes.__members__.values() if member in enums ]
      try:
          for data_type in types:
              if string == data_type:
                  return True
          return False
      except ValueError:
          return False

class Column:
  
  @staticmethod
  def define(name, data_type, limit=None, foreign_key_references=None, primary_key=False, not_null=False):
    if primary_key:
        return "{%s} SERIAL PRIMARY KEY"%(name)

    if foreign_key_references is not None:
        return "{%s} integer REFERENCES {%s}"%(name, foreign_key_references)

    col_def = "{%s} %s"%(name, data_type.value)

    if limit is not None and data_type in [DataTypes.CHAR, DataTypes.VARCHAR]:
        col_def += "(%s)"%(limit)

    if not_null:
        col_def += " NOT NULL"

    return col_def

class Table:

  @staticmethod
  def create(table_name, **col_defs):
      create_table = "CREATE TABLE {%s}("%(table_name)
      for col_def in col_defs:
          col_statement = Column.define(
              name = col_def['name'], 
              data_type = DataTypes.convert(col_def['type']), 
              limit = col_def.get('limit', None), 
              primary_key = col_def.get('primary_key', False),
              foreign_key_references = col_def.get('foreign_key_references', None),
              not_null = col_def.get('not_null', False)
          )

          create_table += col_statement

          if col_defs.index(col_def) != len(col_def) - 1:
              create_table += ","

      create_table + ");"
      return create_table


