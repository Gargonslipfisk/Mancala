"""
Implementation of singleton enforcement for classes


Implemented as a metaclass. Taken from
   http://code.activestate.com/recipes/102187-singleton-as-a-metaclass/

"""

import sys
import threading

if sys.version_info[0] == 3:
    basestring = str


# ---------------------------------------------------------------------

class SingletonMetaclass( type ):
    """
    Metaclass to tranform any class into a singleton. The singleton is enforced
    across all objects constructed with the same parameters (a constructor
    called with different parameters instantiates another singleton).

    To add it to a class:
      * in Python 2 use the \c __metaclass__ class attribute::
           __metaclass__ = SingletonMetaclass
      * in Python 3, use the ``metaclass`` named parameter to the class::
           class Name( object, metaclass = SingletonMetaclass )

    To clear the singleton state for all classes (and hence make any later
    call to constructors create a new instance), call the class method
    clear_instances()
    """

    # A lock to ensure thread safety (two threads trying to instantiate the
    # same singleton)
    # We need to use a reentrant lock since a singleton class might instantiate
    # another singleton class in its constructor
    lock = threading.RLock()

    # List of created instances
    instances = {}

    @staticmethod
    def clear_instances( classname=None ):
        """
          :param classname: (str or class) specific class to clear

        Clear all created instances (resetting all instantiated
        singletons: later constructor calls will create new objects).
        If passed a class name or a class object, it will clear only the
        singleton object(s) instantiated for that class.

        It's a class method, so call as SingletonMetaclass.clear_instances()
        """
        #print( "CLEAR:", classname )
        with SingletonMetaclass.lock:
            if classname is None:
                SingletonMetaclass.instances = {}
            else:
                if isinstance(classname,basestring) and not classname.startswith('<class'):
                    prefix = "<class '%s'>" % classname
                else:
                    prefix = str(classname)
                for k in list(SingletonMetaclass.instances):
                    if k.startswith(prefix):
                        del SingletonMetaclass.instances[k]


    def __init__(cls,name,bases,dic):
        """Metaclass initializer"""
        super(SingletonMetaclass,cls).__init__(name,bases,dic)


    def __call__(cls,*args,**kw):
        """
        Metaclass interception of the object construction
        """
        # Create a key by joining the class name with the calling args
        key = str(cls) + str(args) + str(kw)
        #import logging; l = logging.getLogger('__file__')

        # Thread-protected code
        with SingletonMetaclass.lock:
            # Search for the key in the already instantiated singletons
            # If not there, instantiate the class
            #l.info( key )
            if key not in SingletonMetaclass.instances:
                #l.info( "new instance" )
                SingletonMetaclass.instances[key] = super(SingletonMetaclass,cls).__call__(*args,**kw)
            return SingletonMetaclass.instances[key]


