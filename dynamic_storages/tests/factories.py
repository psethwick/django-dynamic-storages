import logging

import factory
import factory.django
import factory.fuzzy
from django.core.files.base import ContentFile
from faker import Faker

from .abstract import AbstractStorageTargetFactory
from .models import (
    TestFileStorageModel,
    TestImageStorageModel,
    TestStorageTarget,
)

log = logging.getLogger(__name__)

fake = Faker()


class TestStorageTargetFactory(AbstractStorageTargetFactory):
    class Meta:
        model = TestStorageTarget


def gen_file():
    return ContentFile(fake.binary(), name=fake.file_name())


class TestFileStorageModelFactory(factory.django.DjangoModelFactory):
    storage_target = factory.SubFactory(TestStorageTargetFactory)
    file = factory.django.FileField(from_func=gen_file)

    class Meta:
        model = TestFileStorageModel


class TestImageStorageModelFactory(factory.django.DjangoModelFactory):
    storage_target = factory.SubFactory(TestStorageTargetFactory)
    image = factory.django.ImageField()

    class Meta:
        model = TestImageStorageModel
