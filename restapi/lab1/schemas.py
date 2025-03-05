from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
import uuid


class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=Length(min=1))
    author = fields.Str(required=True, validate=Length(min=1))

    def make_object(self, data, **kwargs):
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        return data

    @validates("title")
    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Title is required and cannot be empty.")

    @validates("author")
    def validate_author(self, value):
        if not value.strip():
            raise ValidationError("Author is required and cannot be empty.")
