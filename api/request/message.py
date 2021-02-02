from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    message = fields.Str(required=True)
    recipient = fields.Str(required=True)


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):
    __schema__ = RequestCreateMessageDtoSchema


class RequestUpdateMessageDtoSchema(Schema):
    message = fields.Str(required=True)


class RequestUpdateMessageDto(RequestDto, RequestUpdateMessageDtoSchema):
    __schema__ = RequestUpdateMessageDtoSchema
