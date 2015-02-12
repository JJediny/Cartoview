VERSION = (0, 9, 11 , 'final' , 0) #major.minor.build.release (PEP standard)

def get_version(*args, **kwargs): #same as django
    # Don't litter django/__init__.py with all the get_version stuff.
    # Only import if it's actually called.
    from django.utils.version import get_version
    return get_version(version = VERSION)
