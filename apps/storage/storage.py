from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

StaticRootS3BotoStorage = lambda: S3BotoStorage(location=settings.STORAGE_BUCKET_PREFIX + '/static')
MediaRootS3BotoStorage  = lambda: S3BotoStorage(location=settings.STORAGE_BUCKET_PREFIX + '/media')