from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseGetEmployeeDtoSchema(Schema):
    eid = fields.Int(required=True, allow_none=False)


class ResponseGetEmployee(ResponseDto, ResponseGetEmployeeDtoSchema):
    __schema__ = ResponseGetEmployeeDtoSchema