Fast serializer implementation for Django request framework
===========================================================

This package implements a `FastSerializerMixin` for Django request framework.

This project requires usage of the upcoming 3.0 or later version of DRF.
Compared to normal serializer this package gives around 2x speedup, and
DRF 3.0 itself is around 3x faster than DRF 2.4. See below for benchmark
results.

The mixin has a couple of fast implementations for to_representation() method,
one for dict based data, and another for object based data. The limitations
for these methods are:

  - Only getattr() based access for object based data, and only dict.get()
    access for dictionary based data.
  - No support for callables (properties on objects do work).
  - No support for nested, dot separated attributes.
  - No support for serializer transform_ methods.

In addition the `Mixin` class allows one to use non-sorted
dictionaries. In practice this means the fields of the serializers will be
serialized in random order.

Usage:

    import fast_serializer
    from rest_framework import serializers

    class MySerializer(fast_serializer.Mixin, serializers.Serializer):
        a_field = serializers.IntegerField()

        to_representation = fast_serializer.obj_to_representation

    class MyObj(object):
        def __init__(self, val):
            self.a_field = val

    objs = [MyObj(i) for i in range(0, 1000)]
    data = str(MySerializer(objs, many=True).data)

    # If your data is dictionary based, change to_representation line to:
         to_represesntation = fast_serializer.dict_to_representation

    objs = [{'a_field': i} for i in range(0, 1000)]
    data = str(MySerializer(objs, many=True).data)

Non ordered output can be achieved by setting class variable `ordered` to
`False`, or by passing `ordered=False` kwarg to `__init__`. Due to reasons
how `many=True` is implemented, passing `ordered` kwarg must be done with
`serializers.ListSerializer(objs=data, child=MySerializer(ordered=False))`
instead of using `MySerializer(data, many=True, ordered=False)`. Note that
the `Mixin` class must be placed before `serializers.Serializer` in the
class definition.

Benchmarks
==========

The benchmark is simple: fetch 1000 objects from database and serialize them
to JSON. The test is repeated 10 times, and average is reported. The
benchmark project can be found from benchmark directory.

Results for a model with 2x of char, integer, boolean, date and datetime fields each,
plus pk field:

  - Plain DRF 3.0: 0.21s
  - Obj based access: 0.16s
  - Setting `ordered=False`: 0.18s
  - Both obj based access and `ordered=False`: 0.14s
  - Both + UltraJSON renderer (https://github.com/gizmag/drf-ujson-renderer): 0.11s
  - Both + UltraJSON + .values(): 0.11s
  - Plain DRF, pre-fetched data: 0.13s
  - Both + UltraJSON + pre-fetched data: 0.029s

We see that the serializer with UltraJSON renderer is 4x faster than DRF 3.0.
When data access is taken in account, the speed gain is more modest, around 2x.

Results for a model with 2x of char field (plus pk field), 10000 objects:

  - Plain DRF 3.0: 0.48s
  - Obj based access: 0.30s
  - Setting `ordered=False`: 0.36s
  - Both obj based access and `ordered=False`: 0.21s
  - Both + UltraJSON renderer: 0.15s
  - Both + UltraJSON + .values(): 0.094s
  - Plain DRF, pre-fetched data: 0.39s
  - Both + UltraJSON + pre-fetched data: 0.066s

For this test case faster serializer + renderer gives 3x speedup, and for
prefetched data the speedup is 6x.

Running the benchmarks is simple. Create a virtualenv, `pip install -r requirements.txt`,
run `python manage.py migrate`, run `python benchmark.py`.
