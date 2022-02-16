from innoldb.qldb import Document

from schema_cntl import settings
from schema_cntl.dialects.postgres import Table
from schema_cntl.util.logger import getLogger

log = getLogger('schema_cntl.schema')


def commit(schema):
    schema_doc = Document(table=settings.TABLE,
                          ledger=settings.LEDGER, snapshot=schema)
    schema_doc.save()
    return schema_doc


def revision_history(id, start=0, no=1):
    schema_doc = Document(table=settings.TABLE,
                          ledger=settings.LEDGER, id=id, stranded=True)

    if start + no > len(schema_doc.strands):
        raise KeyError("Too many strands specified")

    return schema_doc.strands[start:start+no]


def revisions(id):
    return len(Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True).strands)


def revision_schema(id, strand_no):
    schema_doc = Document(table=settings.TABLE,
                          ledger=settings.LEDGER, id=id, stranded=True)

    if strand_no > len(schema_doc.strands) - 1:
        raise KeyError("Too many strands specified")

    revision_doc = schema_doc.strands[strand_no]

    create_tables = []
    for table in revision_doc.schema.tables:
        pieces = Table.create(table['name'], *table['columns'])
        create_tables.append(pieces)

    return create_tables


def differences(id, strand_start_index, strand_end_index):
    schema_doc = Document(table=settings.TABLE,
                          ledger=settings.LEDGER, id=id, stranded=True)

    if strand_start_index > len(schema_doc.strands) - 1 or \
            strand_end_index > len(schema_doc.strands):
        raise ValueError("Specified indices exceed number of strands")

    log.debug('Computing schema differences in revision #%s relative to #%s...',
              strand_end_index, strand_start_index)

    # TODO: compute difference in tables themselves, i.e. addition, subtractions

    alter_tables = []

    start_strand = schema_doc.strands[strand_start_index]
    end_strand = schema_doc.strands[strand_end_index]

    end_table_names = [tb['name'] for tb in end_strand.schema.tables]

    for table in start_strand.schema.tables:
        if table['name'] in end_table_names:

            start_columns = start_strand.schema.tables[0]['columns']
            start_names = [col['name'] for col in start_columns]

            end_columns = end_strand.schema.tables[0]['columns']
            end_names = [col['name'] for col in end_columns]

            # NOTE: columns in end but not in start, by strict property
            # equality, i.e. a column with the same name but different
            # data type will get caught in this generator expression.
            diff_rel_to_start = [
                col for col in end_columns if col not in start_columns]
            # therefore, find columns whose names are in diff, but whose
            # properties are different
            altered_rel_to_start = [
                col for col in diff_rel_to_start if col['name'] in start_names]
            # columns whose names are in diff and not in start at all
            new_rel_to_start = [
                col for col in diff_rel_to_start if col not in altered_rel_to_start]

            # columns not in diff, but in start
            removed_rel_to_start = [
                col for col in start_columns if col['name'] not in end_names]

            formulae = {
                'ALTERED': altered_rel_to_start,
                'ADDED': new_rel_to_start,
                'REMOVED': removed_rel_to_start
            }

            log.debug('Schema Formula: %s', formulae)

            alter_tables.append(Table.alter(settings.TABLE, **formulae))

    return alter_tables
