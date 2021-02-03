import datetime

from marshmallow import fields


class DatetimeField(fields.DateTime):
    def _serialize(self, value, attr, obj, **kwargs):
        return super()._serialize(value, attr, obj, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        # self.datetime_to_iso(obj["update_at"])
        return super()._deserialize(value, attr, data, **kwargs)

    @staticmethod
    def datetime_to_iso(dt):
        if isinstance(dt, datetime.datetime):
            return dt.isoformat()
        return dt
