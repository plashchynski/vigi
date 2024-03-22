# This file is used to create a cache object for the application
# and then import it in the main application file (vigi/__init__.py)
# as well as in the blueprint files (vigi/routes/*.py)

from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
