"""
Модуль с Marshmallow схемами используемый для сериализация данных в дата_классы
"""
from marshmallow import EXCLUDE, Schema, fields, post_load
from marshmallow_meta import meta

from app.core.data_classes import LinkA


@meta(unknown=EXCLUDE)
class LinkASchema(Schema):
    """
    Используется для сериализация данных полученных от BeautifulSoup
    в дата_класс Alink
    """

    href = fields.Str()
    title = fields.Str(load_default="title")

    @post_load
    def make_object(self: "LinkASchema", any_data: dict, **_: dict) -> LinkA:
        """
        При вызове LinkASchema().load(data) будет
        возвращен одноименный дата класс LinkA
        :param data:
        :param _:
        :return:
        """
        return LinkA(**any_data)
