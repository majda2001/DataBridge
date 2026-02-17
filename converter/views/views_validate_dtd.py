# views_validate_dtd.py
from io import StringIO
from django.shortcuts import render
from lxml import etree

def validate_with_dtd(request):
    """Valide un fichier XML avec une DTD"""
    context = {'validation_result': None, 'is_valid': None, 'error': None, 'fileXML': '', 'fileDTD': ''}

    if request.method == "POST":
        xml_content = request.POST.get('fileXML', '').strip()
        dtd_content = request.POST.get('fileDTD', '').strip()
        context['fileXML'] = xml_content
        context['fileDTD'] = dtd_content

        if not xml_content or not dtd_content:
            context['error'] = "Veuillez fournir un fichier XML et une DTD"
        else:
            try:
                dtd = etree.DTD(StringIO(dtd_content))
                root = etree.XML(xml_content.encode('utf-8'))
                is_valid = dtd.validate(root)

                context['is_valid'] = is_valid
                context['validation_result'] = "Fichier XML valide ✓" if is_valid else "Fichier XML invalide ✗"
                if not is_valid:
                    context['error'] = dtd.error_log.last_error
            except etree.XMLSyntaxError as e:
                context['error'] = f"Erreur de syntaxe XML: {str(e)}"
            except etree.DTDParseError as e:
                context['error'] = f"Erreur dans la DTD: {str(e)}"
            except Exception as e:
                context['error'] = f"Erreur: {str(e)}"

    return render(request, 'converter/validate_dtd.html', context)
