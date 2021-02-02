from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchUserDtoSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()


class RequestPatchUserDto(RequestDto, RequestPatchUserDtoSchema):
    fields: list
    __schema__ = RequestPatchUserDtoSchema

    def __init__(self, *args, **kwargs):
        self.fields = []
        super(RequestPatchUserDto, self).__init__(*args, **kwargs)

    def set(self, key, value):
        self.fields.append(key)
        super(RequestPatchUserDto, self).set(key, value)


class RequestCreateUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)


class RequestCreateUserDto(RequestDto, RequestCreateUserDtoSchema):
    __schema__ = RequestCreateUserDtoSchema
