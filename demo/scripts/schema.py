import os
from pprint import pprint

DEMO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(DEMO_DIR, 'schemas')
VERSIONS= ['v1.0.0', 'v1.0.1', 'v1.0.2']

if __name__=="__main__":

    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    os.environ['LEDGER'] = 'schema'

    # NOTE: Import needs to come after environment variable has been set! The library will scan the environment
    #       on import and set the ledger. 
    from innoldb.qldb import Query

    results = Query('version_control').get_all()
    for result in results:
        pprint(vars(result))