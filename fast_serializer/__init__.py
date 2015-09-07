from collections import OrderedDict
from rest_framework.fields import empty
from django.utils.functional import cached_property


class Mixin(object):
    ordered = False

    def __init__(self, *args, **kwargs):
        self.ordered = kwargs.pop('ordered', self.ordered)
        super(Mixin, self).__init__(*args, **kwargs)

    def obj_to_representation(self, obj):
        data = [(f, getattr(obj, f.field_name)) for
                f in self.repr_fields]
        if self.ordered:
            return OrderedDict(
                [(f.field_name, f.to_representation(val) if val else None)
                 for f, val in data])
        else:
            return dict(
                [(f.field_name, f.to_representation(val) if val else None)
                 for f, val in data])

    def dict_to_representation(self, d):
        data = [(f, d.get(f.field_name, None)) for
                f in self.repr_fields]
        if self.ordered:
            return OrderedDict(
                [(f.field_name, f.to_representation(val) if val else None)
                 for f, val in data])
        else:
            return dict(
                [(f.field_name, f.to_representation(val) if val else None)
                 for f, val in data])

    @cached_property
    def repr_fields(self):
        return [field for field in self.fields.values()
                if (not field.read_only) or (field.default is not empty)]


obj_to_representation = Mixin.obj_to_representation
dict_to_representation = Mixin.dict_to_representation
