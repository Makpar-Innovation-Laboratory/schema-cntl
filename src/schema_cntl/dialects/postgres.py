from enum import Enum
from psycopg2 import sql


class DataTypes(Enum):
    BOOL = "bool"
    TEXT = "text"
    CHAR = "char"
    VARCHAR = "varchar"
    DOUBLE = "float8"
    INTEGER = "int"
    DECIMAL = "decimal"
    DATE = "date"

    @staticmethod
    def limited():
        return [DataTypes.CHAR, DataTypes.VARCHAR]

    @staticmethod
    def convert(string=None):
        if string is None:
            return None, None

        limit = None
        if any(datatype.value in string for datatype in DataTypes.limited()) \
                and '(' in string:
            split = string.replace(')', '').split('(')
            string, limit = split[0], int(split[-1])

        for member in DataTypes.__members__.values():
            if member.value == string:
                return member, limit
        return None, None

    @staticmethod
    def belongs_to_types(string, *enums):
        types = [member.value for member in DataTypes.__members__.values()
                 if member in enums]
        for data_type in types:
            if string == data_type:
                return True
        return False


class Column:
    RENAME = "RENAME COLUMN {old_name} TO {new_name}"
    ADD_CONST = "ADD CONSTRAINT {constraint_name} FOREIGN KEY {fk_name} REFERENCES {primary_table} ({fk_name})"

    @staticmethod
    def define(**col_def):
        """Create a column definition clause in **PostgreSQL**. Column names will be parameterized to prevent injection, i.e. the `name` passed into this method is not the name of the column, but the name of the column parameter in the clause that is passed into the query cursor.

        :param kwargs: Keyword arguments. The input format should make the `schema.json` input format.
        :return: Column definition clause for `CREATE TABLE` **PostgreSQL** statement.
        :rtype: str
        """
        if col_def.get('primary_key', None) is not None:
            return "{%s} SERIAL PRIMARY KEY" % (col_def['name'])

        if col_def.get('foreign_key_references', None) is not None:
            return "{%s} integer REFERENCES {fkr}" % (col_def['name'])

        # data type is not parameterized in string, so it is converted into an enum before formatting
        # so user input can never directly touched the query string
        enumerated_type, limit = DataTypes.convert(col_def['type'])
        if enumerated_type is None:
            raise ValueError(
                "No data type specified for column %s" % (col_def['name']))
        definition = "{%s} %s" % (col_def['name'], enumerated_type.value)
        if limit is not None:
            definition += "(%s)" % (limit)

        if col_def.get('not_null', None) is not None:
            definition += " NOT NULL"

        return definition

    @staticmethod
    def add(**col_def):
        """`ADD COLUMN` subclause in **PostgreSQL**, for use in `ALTER TABLE` clauses. Column names will be parameterized to prevent injection, i.e. the `name` passed into this method is not the name of the column, but the name of the column parameter in the clause that is passed into the query cursor.

        :param kwargs: Keyword arguments. The input format should make the `schema.json` input format.
        :return: Column definition clause for `ADD COLUMN` **PostgreSQL** statement.
        :rtype: str
        """
        # data type is not parameterized in string, so it is converted into an enum before formatting
        # so user input can never directly touched the query string
        enumerated_type, limit = DataTypes.convert(col_def['type'])
        if enumerated_type is None:
            raise ValueError(
                "No data type specified for column %s" % (col_def['name']))

        add_column = "ADD COLUMN {%s} %s" % (
            col_def['name'], enumerated_type.value)

        if limit is not None:
            definition += "(%s)" % (limit)

        if col_def.get('not_null', None):
            add_column += " NOT NULL"

        if col_def.get('foreign_key_references', None) is not None:
            add_column += "CONSTRAINT fk REFERENCES {fkr}"

        return add_column

    @staticmethod
    def add_constraint(**col_def):
        pass

    @staticmethod
    def drop_constraint(**col_def):
        pass

    @staticmethod
    def drop(**col_def):
        return "DROP COLUMN {%s}" % col_def['name']


class Table:

    @staticmethod
    def create(table_name, *col_defs):
        """Generate a `CREATE TABLE` PostgreSQL  statement. Table and column names will be parameterized in query to prevent injection, i.e. `table_name` and `col_def[]['name']` are not the names of the table and columns, but the names of the column and column parameters in the statement.

        :param table_name: name of table
        :type table_name: string
        :param `*args`: column objects from `schema.tables[]` structure, with `name` replaced by a parameterized key.
        :return: `CREATE TABLE` statement, parameter names, parameter values
        :rtype: tuple
        """
        create_table = "CREATE TABLE {table_name} ("

        parameters = [table_name]
        parameter_names = ['table_name']
        for i, col_def in enumerate(col_defs):
            # parameterize column_name
            param_name = 'col_' + str(i)
            parameters.append(col_def['name'])
            parameter_names.append(param_name)
            col_def['name'] = param_name

            col_statement = Column.define(**col_def)

            create_table += col_statement

            if col_defs.index(col_def) != len(col_defs) - 1:
                create_table += ", "

        create_table += ");"
        return create_table, parameter_names, parameters

    @staticmethod
    def alter(table_name, **col_formulae):
        statement = ""
        parameters = [table_name]
        parameter_names = ['table_name']
        accumulated = 0

        for verb, cols in col_formulae.items():
            alter_table = None

            for i, formula in enumerate(cols):
                param_name = 'col_' + str(i + accumulated)
                parameters.append(formula['name'])
                parameter_names.append(param_name)
                formula['name'] = param_name

                if verb == 'ALTERED':
                    pass
                elif verb == 'ADDED':
                    if alter_table is None:
                        alter_table = "ALTER TABLE {table_name} "
                    else:
                        alter_table += ", "
                    alter_table += Column.add(**formula)
                elif verb == 'REMOVED':
                    if alter_table is None:
                        alter_table = "ALTER TABLE {table_name} "
                    alter_table += Column.drop(**formula)

            if len(cols) > 0:
                accumulated = len(cols)

            if alter_table is not None:
                statement += alter_table + "; "

        return statement, parameter_names, parameters
