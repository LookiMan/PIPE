from flask import url_for
from marshmallow import fields

from . import ma
from .models import File


class FileSchema(ma.SQLAlchemyAutoSchema):

    def __init__(self, is_files_owner=None, **kwargs):
        super().__init__(**kwargs)
        self.is_files_owner = is_files_owner

    class Meta:
        model = File
        fields = ('id', 'name', 'action')

    action = fields.Method('get_action')

    def get_action(self, obj):
        return url_for(
            'remove_controller' if self.is_files_owner else 'download_controller',
            file_id=obj.id
        )
