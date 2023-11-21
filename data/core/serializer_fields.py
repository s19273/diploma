import base64
from datetime import datetime

import six
from data.core.utils import get_formatted_date
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.Field):
    def to_internal_value(self, data):

        if isinstance(data, six.string_types):
            try:
                imgstr = data.split(';base64,')[1]
                data = imgstr.encode()
                decoded_string = base64.b64decode(data)

            except TypeError:
                self.fail('invalid_image')

            datetime_now = datetime.now()
            time_string = get_formatted_date(datetime_now)
            file_name = str(time_string) + '.jpg'
            data = ContentFile(decoded_string, name=file_name)

        return data

    def to_representation(self, value):
        if value:
            return value.name
        return None
