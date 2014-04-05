# TODO: Add tests for this module!
# Consider using:
# http://test.opendap.org/opendap/hyrax/data/nc/testfile.nc
import numpy as np

from xray.xarray import XArray
from xray.utils import FrozenOrderedDict, Frozen


class _ArrayWrapper(object):
    def __init__(self, array):
        self.array = array

    @property
    def ndim(self):
        return len(self.array.shape)

    @property
    def shape(self):
        return self.array.shape

    @property
    def size(self):
        return np.prod(self.shape)

    @property
    def dtype(self):
        t = self.array.type
        size = '' if t.size is None else str(t.size)
        return np.dtype(t.typecode + size)

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        for k in key:
            if not (isinstance(k, int)
                    or isinstance(k, slice)
                    or k is Ellipsis):
                raise IndexError('pydap only supports indexing with int, '
                                 'slice and Ellipsis objects')
        return self.array[key]


class PydapDataStore(object):
    def __init__(self, url):
        # import here so we can load this module without triggering an import
        import pydap.client
        self.ds = pydap.client.open_url(url)

    @property
    def variables(self):
        return FrozenOrderedDict((k, XArray(v.dimensions, _ArrayWrapper(v),
                                            v.attributes))
                                for k, v in self.ds.iteritems())

    @property
    def attributes(self):
        return Frozen(self.ds.attributes)
