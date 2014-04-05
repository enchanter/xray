from cStringIO import StringIO
import numpy as np
import warnings

from xray.backends.common import AbstractDataStore
from xray.conventions import (is_valid_nc3_name, coerce_nc3_dtype,
                              encode_cf_variable)
from xray.xarray import XArray
from xray.utils import Frozen, FrozenOrderedDict


class ScipyDataStore(AbstractDataStore):
    """
    Stores data using the scipy.io.netcdf package.
    This store has the advantage of being able to
    be initialized with a StringIO object, allow for
    serialization.
    """
    def __init__(self, filename_or_obj, mode='r', mmap=None, version=1):
        # import here so we can load this module without triggering an import
        import scipy
        if mode != 'r' and scipy.__version__ < (0, 13):
            warnings.warn('scipy %s detected; '
                          'the minimal recommended version is 0.13. '
                          'NetCDF3 files may not write correctly!'
                          % scipy.__version__, ImportWarning)

        import scipy.io
        # if filename is a NetCDF3 bytestring we store it in a StringIO
        if (isinstance(filename_or_obj, basestring)
            and filename_or_obj.startswith('CDF')):
            # TODO: this check has the unfortunate side-effect that
            # paths to files cannot start with 'CDF'.
            filename_or_obj = StringIO(filename_or_obj)
        self.ds = scipy.io.netcdf.netcdf_file(
            filename_or_obj, mode=mode, mmap=mmap, version=version)

    @property
    def variables(self):
        return FrozenOrderedDict((k, XArray(v.dimensions, v.data,
                                            v._attributes))
                                 for k, v in self.ds.variables.iteritems())

    @property
    def attributes(self):
        return Frozen(self.ds._attributes)

    @property
    def dimensions(self):
        return Frozen(self.ds.dimensions)

    def set_dimension(self, name, length):
        if name in self.dimensions:
            raise ValueError('%s does not support modifying dimensions'
                             % type(self).__name__)
        self.ds.createDimension(name, length)

    def _validate_attr_key(self, key):
        if not is_valid_nc3_name(key):
            raise ValueError("Not a valid attribute name")

    def _cast_attr_value(self, value):
        if isinstance(value, basestring):
            value = unicode(value)
        else:
            value = coerce_nc3_dtype(np.atleast_1d(value))
            if value.ndim > 1:
                raise ValueError("netCDF attributes must be 1-dimensional")
        return value

    def set_attribute(self, key, value):
        self._validate_attr_key(key)
        setattr(self.ds, key, self._cast_attr_value(value))

    def set_variable(self, name, variable):
        variable = encode_cf_variable(variable)
        data = coerce_nc3_dtype(variable.data)
        self.set_necessary_dimensions(variable)
        self.ds.createVariable(name, data.dtype, variable.dimensions)
        scipy_var = self.ds.variables[name]
        if data.ndim == 0:
            scipy_var.assignValue(data)
        else:
            scipy_var[:] = data[:]
        for k, v in variable.attributes.iteritems():
            self._validate_attr_key(k)
            setattr(scipy_var, k, self._cast_attr_value(v))

    def del_attribute(self, key):
        delattr(self.ds, key)

    def sync(self):
        self.ds.flush()
