from django.urls import path
from .views import (
    index,
    validate_with_dtd,
    validate_with_xmlschema,
    convert_xml_to_json,
    convert_dtd_to_schema
)

app_name = 'converter'

urlpatterns = [
    path('', index, name='index'),
    path('validate-dtd/', validate_with_dtd, name='validate_dtd'),
    path('validate-xmlschema/', validate_with_xmlschema, name='validate_xmlschema'),
    path('convert-xml-to-json/', convert_xml_to_json, name='convert_xml_to_json'),
    path('convert-dtd-to-schema/', convert_dtd_to_schema, name='convert_dtd_to_schema'),
]
