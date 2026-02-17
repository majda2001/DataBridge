# views_validate_xsd.py
from io import StringIO
from django.shortcuts import render
from lxml import etree

def validate_with_xmlschema(request):
    """Valide un fichier XML avec un XMLSchema"""
    context = {'validation_result': None, 'is_valid': None, 'error': None, 'fileXML': '', 'fileXMLSchema': ''}

    if request.method == "POST":
        xml_content = request.POST.get('fileXML', '').strip()
        schema_content = request.POST.get('fileXMLSchema', '').strip()
        context['fileXML'] = xml_content
        context['fileXMLSchema'] = schema_content

        if not xml_content or not schema_content:
            context['error'] = "Veuillez fournir un fichier XML et un XMLSchema"
        else:
            try:
                schema_doc = etree.parse(StringIO(schema_content))
                xmlschema = etree.XMLSchema(schema_doc)
                doc = etree.parse(StringIO(xml_content))
                is_valid = xmlschema.validate(doc)

                context['is_valid'] = is_valid
                context['validation_result'] = "Fichier XML valide ✓" if is_valid else "Fichier XML invalide ✗"
                if not is_valid:
                    context['error'] = xmlschema.error_log.last_error
            except etree.XMLSyntaxError as e:
                context['error'] = f"Erreur de syntaxe XML: {str(e)}"
            except etree.XMLSchemaParseError as e:
                context['error'] = f"Erreur dans le XMLSchema: {str(e)}"
            except Exception as e:
                context['error'] = f"Erreur: {str(e)}"

    return render(request, 'converter/validate_xmlschema.html', context)
