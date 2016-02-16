# -*- coding: utf-8 -*-
import json

from django.conf import settings
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:  # Django < 1.9 pragma: no cover
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .managers import FieldHistoryManager


@python_2_unicode_compatible
class FieldHistory(models.Model):
    object_id = models.TextField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    object = GenericForeignKey()
    field_name = models.CharField(max_length=500)
    serialized_data = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True,
                                        db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    objects = FieldHistoryManager()

    @property
    def field_value(self):
        data = json.loads(self.serialized_data)
        return data[self.field_name]

    def __str__(self):
        return '{} field history for {}'.format(self.field_name, self.object)

    class Meta:
        app_label = 'field_history'