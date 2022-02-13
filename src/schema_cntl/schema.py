
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


def commit_schema():
    pass
