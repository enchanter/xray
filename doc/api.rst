.. currentmodule:: xray

API reference
=============

Dataset
-------

Creating a dataset
~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: generated/

   Dataset
   open_dataset
   Dataset.concat

Attributes and underlying data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   Dataset.variables
   Dataset.virtual_variables
   Dataset.coordinates
   Dataset.noncoordinates
   Dataset.dimensions
   Dataset.attributes

Dataset contents
~~~~~~~~~~~~~~~~

Datasets implement the mapping interface with keys given by variable names
and values given by ``DatasetArray`` objects focused on each variable name.

.. autosummary::
   :toctree: generated/

   Dataset.__getitem__
   Dataset.__setitem__
   Dataset.__delitem__
   Dataset.merge
   Dataset.copy

Selecting
~~~~~~~~~

.. autosummary::
   :toctree: generated/

   Dataset.indexed_by
   Dataset.labeled_by
   Dataset.reindex
   Dataset.reindex_like
   Dataset.rename
   Dataset.replace
   Dataset.select
   Dataset.unselect
   Dataset.squeeze
   Dataset.groupby

IO / Conversion
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   Dataset.dump
   Dataset.dumps
   Dataset.dump_to_store
   Dataset.to_dataframe
   Dataset.from_dataframe


DatasetArray
------------

.. autosummary::
   :toctree: generated/

   DatasetArray

Selecting
~~~~~~~~~

.. autosummary::
   :toctree: generated/

   DatasetArray.loc
   DatasetArray.indexed_by
   DatasetArray.labeled_by
   DatasetArray.reindex
   DatasetArray.reindex_like
   DatasetArray.rename
   DatasetArray.select
   DatasetArray.unselect
   DatasetArray.squeeze

Group operations
~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   DatasetArray.groupby
   DatasetArray.concat

Manipulating data
~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   DatasetArray.transpose
   DatasetArray.T
   DatasetArray.reduce
   DatasetArray.all
   DatasetArray.any
   DatasetArray.argmax
   DatasetArray.argmin
   DatasetArray.cumprod
   DatasetArray.cumsum
   DatasetArray.max
   DatasetArray.min
   DatasetArray.mean
   DatasetArray.prod
   DatasetArray.ptp
   DatasetArray.std
   DatasetArray.sum
   DatasetArray.var

IO / Conversion
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   DatasetArray.to_dataframe
   DatasetArray.to_series
   DatasetArray.copy
   DatasetArray.from_series


XArray
------

`XArray` objects provide a low-level interface for manipulating the contents
of `Dataset` objects. Essentially, they are `DatasetArray`s without coordinate
labels.

.. autosummary::
   :toctree: generated/

   XArray

Top-level functions
-------------------

.. autosummary::
   :toctree: generated/

   as_xarray
   broadcast_xarrays
   xarray_equal
   align
   encode_cf_datetime
   decode_cf_datetime
