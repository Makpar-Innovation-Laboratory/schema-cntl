
# 1. get first_revision
#     a. create table statement
#
# 1. get revisions
#     previous_revision = first_revision
#
#     for revision in revisions:
#       
#       a. find keys in revision not in previous_revision
#           i. alter table statement for keys
#
#       b. find keys with values different from prevision
#           i. alter column statements for key, values
#
#       c. previous_revision = revision

from innoldb.qldb import Document

from schema_cntl import settings

def commit(schema):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, snapshot=schema)
    schema_doc.save()
    return schema_doc

def revision_history(id, start = 0, no = 1):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True)
    if start + no > len(schema_doc.strands):
        raise KeyError("Too many strands specified")
    return schema_doc.strands[start:start+no]

def revisions(id):
    return len(Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True).strands)

def differences(id, strand_start_index, strand_end_index):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True)

    if strand_start_index > len(schema_doc.strands) - 1 or \
      strand_end_index > len(schema_doc.strands):
        raise ValueError("Specified indices exceed number of strands")

    start_strand = schema_doc.strands[strand_start_index]
    start_columns = start_strand.schema.tables[0]['columns']
    start_names = [ col['name'] for col in start_columns ]

    end_strand = schema_doc.strands[strand_end_index]
    end_columns = end_strand.schema.tables[0]['columns']
    end_names = [ col['name'] for col in end_columns ]
    
    # will include new columns, but also altered columns
    relative_diff = [ col for col in end_columns if col not in start_columns]

    relative_altered = [ col for col in relative_diff if col['name'] in start_names]

    relative_new = [ col for col in relative_diff if col not in relative_altered ]

    print(relative_diff)
    print(relative_altered)
    print(relative_new)
