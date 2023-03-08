"""
Ported to Python 3.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.utils import PY2
if PY2:
    from future.builtins import filter, map, zip, ascii, chr, hex, input, next, oct, open, pow, round, super, bytes, dict, list, object, range, str, max, min  # noqa: F401

from foolscap.api import Violation, RemoteException
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure
from typing import Any

# Type rref: RemoteReference from foolscap.referenceable
# but since we are dynamically adding a class variable
# it kind of defeats the purpose of static typing so leave as 'Any'
def add_version_to_remote_reference(rref: Any, default: Any) -> Deferred[Any]:
    """I try to add a .version attribute to the given RemoteReference. I call
    the remote get_version() method to learn its version. I'll add the
    default value if the remote side doesn't appear to have a get_version()
    method."""
    d: Deferred[Any] = rref.callRemote("get_version")
    def _got_version(version: Any) -> Any:
        rref.version = version
        return rref
    def _no_get_version(f: Failure) -> Any:
        f.trap(Violation, RemoteException)
        rref.version = default
        return rref
    d.addCallbacks(_got_version, _no_get_version)
    return d
