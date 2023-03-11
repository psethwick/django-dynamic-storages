# Generated by Django 3.1.2 on 2020-10-24 18:05

import uuid

import cryptography.fernet
import django.db.models.deletion
from django.db import migrations, models

import dynamic_storages.fields.dynamic_storage
import dynamic_storages.fields.encrypted_content
import dynamic_storages.fields.encrypted_json
import dynamic_storages.tests.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TestStorageTarget",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, help_text="UUID identifying this objects", primary_key=True, serialize=False)),
                ("name", models.CharField(db_index=True, help_text="Name of this object", max_length=150)),
                ("description", models.TextField(blank=True, help_text="Description of this object", null=True)),
                ("last_checked", models.DateTimeField(blank=True, editable=False, help_text="Timestamp identifying when this storage provider was last checked", null=True)),
                (
                    "last_status",
                    models.CharField(
                        choices=[["v", "Valid"], ["e", "Error"], ["u", "Unknown"]],
                        default="u",
                        editable=False,
                        help_text="Flag indiciating what the last status check result was",
                        max_length=1,
                    ),
                ),
                ("status_detail", models.TextField(blank=True, editable=False, help_text="Status details from last status check", null=True)),
                (
                    "provider",
                    models.CharField(
                        choices=[
                            ("libcloud", "Apache LibCloud"),
                            ("azure", "Azure Blob Storage"),
                            ("dropbox", "Dropbox"),
                            ("ftp", "FTP"),
                            ("gcloud", "Google Cloud Storage"),
                            ("s3boto3", "S3/Boto3"),
                            ("do", "Digital Ocean (boto3)"),
                            ("sftp", "SFTP"),
                            ("default", None),
                        ],
                        default="gcloud",
                        help_text="Specific storage provider this target utilizes - generally an object storage solution of some sort",
                        max_length=8,
                    ),
                ),
                (
                    "config",
                    dynamic_storages.fields.encrypted_json.EncryptedJSONField(
                        blank=True, default=dict, help_text="Key/value pairs to pass to the storage provider when initializing the storage backend", null=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, help_text="Timestamp indicating when this object was created")),
                ("modified", models.DateTimeField(auto_now=True, db_index=True, help_text="Timestamp indicating when this object was last updated")),
            ],
            options={
                "verbose_name": "Storage Target",
                "verbose_name_plural": "Storage Targets",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TestImageStorageModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", dynamic_storages.fields.dynamic_storage.DynamicStorageImageField(upload_to=dynamic_storages.tests.models.upload_to)),
                ("storage_target", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tests.teststoragetarget")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TestFileStorageModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", dynamic_storages.fields.dynamic_storage.DynamicStorageFileField(upload_to=dynamic_storages.tests.models.upload_to)),
                ("storage_target", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tests.teststoragetarget")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TestEncryptedImageFieldModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.BinaryField(default=cryptography.fernet.Fernet.generate_key, help_text="Generated Fernet key", max_length=60)),
                ("image", dynamic_storages.fields.encrypted_content.EncryptedImageField(upload_to=dynamic_storages.tests.models.upload_to)),
                ("storage_target", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tests.teststoragetarget")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TestEncryptedFileFieldModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.BinaryField(default=cryptography.fernet.Fernet.generate_key, help_text="Generated Fernet key", max_length=60)),
                (
                    "file",
                    dynamic_storages.fields.encrypted_content.EncryptedFileField(
                        fernet=dynamic_storages.tests.models.get_fernet, upload_to=dynamic_storages.tests.models.upload_to
                    ),
                ),
                ("storage_target", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tests.teststoragetarget")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
