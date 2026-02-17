# views_xml_to_json.py
import json
import xmltodict
from django.shortcuts import render

def convert_xml_to_json(request):
    """Convertit un fichier XML en JSON"""
    context = {'json_result': None, 'error': None, 'fileXML': ''}

    if request.method == "POST":
        xml_content = request.POST.get('fileXML', '').strip()
        context['fileXML'] = xml_content

        if not xml_content:
            context['error'] = "Veuillez fournir un fichier XML"
        else:
            try:
                json_obj = xmltodict.parse(xml_content)
                context['json_result'] = json.dumps(json_obj, indent=2, ensure_ascii=False)
            except Exception as e:
                context['error'] = f"Erreur de conversion: {str(e)}"

    return render(request, 'converter/convert_xml_to_json.html', context)
