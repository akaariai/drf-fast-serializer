from datetime import date, datetime, timedelta
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'benchmark.settings')
from django import setup
setup()
from rest_framework import renderers
from rest_framework import serializers
import fast_serializer
from drf_ujson.renderers import UJSONRenderer
from django.db.transaction import atomic

# Set up test data
from tester.models import MySimpleModel as MyModel
with atomic():
    MyModel.objects.all().delete()
    print("Generating data")
    for i in range(0, 10000):
        MyModel.create(i)
# The serializers

class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel

print("Test plain serializer:")
samples = []
for i in range(0, 10):
    start = datetime.now()
    data = renderers.JSONRenderer().render(MySerializer(MyModel.objects.all(), many=True).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))

print("Test obj_to_representation:")

class ToReprSerializer(fast_serializer.Mixin, serializers.ModelSerializer):
    to_representation = fast_serializer.obj_to_representation

    class Meta:
        model = MyModel

samples = []
for i in range(0, 10):
    start = datetime.now()
    data = renderers.JSONRenderer().render(ToReprSerializer(MyModel.objects.all(), many=True).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))
print("Test ordered=False:")

class OrderedSerializer(fast_serializer.Mixin, serializers.ModelSerializer):
    class Meta:
        model = MyModel

samples = []
for i in range(0, 10):
    start = datetime.now()
    data = renderers.JSONRenderer().render(
        serializers.ListSerializer(MyModel.objects.all(),
                                   child=OrderedSerializer(ordered=False)).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))

print("Test both:")
samples = []
for i in range(0, 10):
    start = datetime.now()
    data = renderers.JSONRenderer().render(
        serializers.ListSerializer(MyModel.objects.all(),
                                   child=ToReprSerializer(ordered=False)).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))

print("Test both + ujson:")
samples = []
for i in range(0, 10):
    start = datetime.now()
    data = UJSONRenderer().render(
        serializers.ListSerializer(MyModel.objects.all(),
                                   child=ToReprSerializer(ordered=False)).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))

class ToDictSerializer(fast_serializer.Mixin, serializers.ModelSerializer):
    to_representation = fast_serializer.dict_to_representation

    class Meta:
        model = MyModel

print("Test both + ujson + dict:")
samples = []
for i in range(0, 10):
    start = datetime.now()
    data = UJSONRenderer().render(
        serializers.ListSerializer(MyModel.objects.values(),
                                   child=ToDictSerializer(ordered=False)).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))

print("Test plain serializer + pre-fetch data:")
samples = []
objs = list(MyModel.objects.all())
for i in range(0, 10):
    start = datetime.now()
    data = renderers.JSONRenderer().render(MySerializer(objs, many=True).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))

print("Test both + ujson + pre-fetched data:")
samples = []
objs = list(MyModel.objects.all())
for i in range(0, 10):
    start = datetime.now()
    data = UJSONRenderer().render(
        serializers.ListSerializer(objs,
                                   child=ToReprSerializer(ordered=False)).data)
    samples.append(datetime.now() - start)
print("Avg: %s" % (sum(samples, timedelta()) / 10))
