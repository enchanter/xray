from collections import OrderedDict
import warnings

import numpy as np

from common import AbstractDataStore
from xray.xarray import XArray
from xray.conventions import encode_cf_variable
from xray.utils import FrozenOrderedDict


class NetCDF4DataStore(AbstractDataStore):

    def __init__(self, filename, mode='r', clobber=True, diskless=False,
                 persist=False, format='NETCDF4'):
        # import here so we can load this module without triggering an import
        import netCDF4 as nc4
        if nc4.__version__ < (1, 0, 6):
            warnings.warn('python-netCDF4 %s detected; '
                          'the minimal recommended version is 1.0.6.'
                          % nc4.__version__, ImportWarning)

        self.ds = nc4.Dataset(filename, mode=mode, clobber=clobber,
                              diskless=diskless, persist=persist,
                              format=format)

    @property
    def variables(self):
        def convert_variable(var):
            var.set_auto_maskandscale(False)
            dimensions = var.dimensions
            data = var
            if var.ndim == 0:
                # work around for netCDF4-python's broken handling of 0-d
                # arrays (slicing them always returns a 1-dimensional array):
                # https://github.com/Unidata/netcdf4-python/pull/220
                data = np.asscalar(var[...])
            attributes = OrderedDict((k, var.getncattr(k))
                                     for k in var.ncattrs())
            # netCDF4 specific encoding; save _FillValue for later
            encoding = {}
            filters = var.filters()
            if filters is not None:
                encoding.update(filters)
            chunking = var.chunking()
            if chunking is not None:
                if chunking == 'contiguous':
                    encoding['contiguous'] = True
                    encoding['chunksizes'] = None
                else:
                    encoding['contiguous'] = False
                    encoding['chunksizes'] = tuple(chunking)
            # TODO: figure out how to round-trip "endian-ness" without raising
            # warnings from netCDF4
            # encoding['endian'] = var.endian()
            encoding['least_significant_digit'] = \
                attributes.pop('least_significant_digit', None)
            return XArray(dimensions, data, attributes, encoding,
                          indexing_mode='orthogonal')
        return FrozenOrderedDict((k, convert_variable(v))
                                 for k, v in self.ds.variables.iteritems())

    @property
    def attributes(self):
        return FrozenOrderedDict((k, self.ds.getncattr(k))
                                 for k in self.ds.ncattrs())

    @property
    def dimensions(self):
        return FrozenOrderedDict((k, len(v))
                                 for k, v in self.ds.dimensions.iteritems())

    def set_dimension(self, name, length):
        self.ds.createDimension(name, size=length)

    def set_attribute(self, key, value):
        self.ds.setncatts({key: value})

    def set_variable(self, name, variable):
        variable = encode_cf_variable(variable)
        self.set_necessary_dimensions(variable)
        fill_value = variable.attributes.pop('_FillValue', None)
        encoding = variable.encoding
        self.ds.createVariable(
            varname=name,
            datatype=variable.dtype,
            dimensions=variable.dimensions,
            zlib=encoding.get('zlib', False),
            complevel=encoding.get('complevel', 4),
            shuffle=encoding.get('shuffle', True),
            fletcher32=encoding.get('fletcher32', False),
            contiguous=encoding.get('contiguous', False),
            chunksizes=encoding.get('chunksizes'),
            endian=encoding.get('endian', 'native'),
            least_significant_digit=encoding.get('least_significant_digit'),
            fill_value=fill_value)
        nc4_var = self.ds.variables[name]
        nc4_var.set_auto_maskandscale(False)
        if variable.data.ndim == 0:
            nc4_var[:] = variable.data
        else:
            nc4_var[:] = variable.data[:]
        nc4_var.setncatts(variable.attributes)

    def del_attribute(self, key):
        self.ds.delncattr(key)

    def sync(self):
        self.ds.sync()
