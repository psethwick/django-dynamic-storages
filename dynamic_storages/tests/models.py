import hashlib
import logging
from uuid import uuid4

from django.core.files.storage import default_storage
from django.db import models

from dynamic_storages.fields.dynamic_storage import (
    DynamicStorageFileField,
    DynamicStorageImageField,
)
from dynamic_storages.models import AbstractStorageTarget

log = logging.getLogger(__name__)


class TestStorageTarget(AbstractStorageTarget):
    class Meta(AbstractStorageTarget.Meta):
        abstract = False


class TestBase(models.Model):
    storage_target = models.ForeignKey(
        "TestStorageTarget", null=True, on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


def get_storage(instance):
    if instance and getattr(instance, "storage_target", None):
        return instance.storage_target.storage_backend
    return default_storage


def upload_to(instance, filename):
    prefix = hashlib.md5(str(uuid4()).encode("utf-8")).hexdigest()
    return "{}/{}".format(prefix, filename)


class TestFileStorageModel(TestBase):
    file = DynamicStorageFileField(
        storage_instance_callable=get_storage, upload_to=upload_to
    )

    class Meta:
        abstract = False


class TestImageStorageModel(TestBase):
    image = DynamicStorageImageField(
        storage_instance_callable=get_storage, upload_to=upload_to
    )

    class Meta:
        abstract = False
