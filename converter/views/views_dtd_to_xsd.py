# views_dtd_to_xsd.py
import re
from xml.dom import minidom
from django.shortcuts import render

def parse_dtd_elements(dtd_content):
    """Parse les déclarations ELEMENT de la DTD"""
    elements = {}
    element_pattern = r'<!ELEMENT\s+(\w+)\s*\(([^>]*)\)>'
    for match in re.finditer(element_pattern, dtd_content, re.DOTALL):
        elem_name = match.group(1)
        children_str = match.group(2).strip()
        # Diviser par virgule ou pipe pour gérer | et ,
        children = [c.strip() for c in re.split(r'[|,]', children_str)]
        elements[elem_name] = children
    return elements

def parse_dtd_attributes(dtd_content):
    """Parse les déclarations ATTLIST de la DTD"""
    attributes = {}
    attlist_pattern = r'<!ATTLIST\s+(\w+)\s+(.*?)>'
    for match in re.finditer(attlist_pattern, dtd_content, re.DOTALL):
        elem_name = match.group(1)
        attr_content = match.group(2)
        attr_pattern = r'(\w+)\s+(\w+)\s+(#REQUIRED|#IMPLIED|#FIXED|"[^"]*"|\w+)'
        attrs = []
        for attr_match in re.finditer(attr_pattern, attr_content):
            attrs.append({
                'name': attr_match.group(1),
                'type': attr_match.group(2),
                'use': attr_match.group(3)
            })
        if elem_name not in attributes:
            attributes[elem_name] = []
        attributes[elem_name].extend(attrs)
    return attributes

def get_xsd_type(dtd_type):
    """Mappe les types DTD aux types XSD"""
    mapping = {
        'CDATA':'xs:string','ID':'xs:ID','IDREF':'xs:IDREF','IDREFS':'xs:IDREFS',
        'ENTITY':'xs:ENTITY','ENTITIES':'xs:ENTITIES','NMTOKEN':'xs:NMTOKEN',
        'NMTOKENS':'xs:NMTOKENS','NOTATION':'xs:NOTATION'
    }
    return mapping.get(dtd_type, 'xs:string')

def build_xsd(dtd_content):
    """Convertit une DTD complète en XSD"""
    elements = parse_dtd_elements(dtd_content)
    attributes = parse_dtd_attributes(dtd_content)

    xsd = '<?xml version="1.0" encoding="UTF-8"?>\n<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n'

    for elem_name, children in elements.items():
        # Vérifier si l'élément contient du texte (#PCDATA)
        if '#PCDATA' in children and len(children) == 1:
            # Élément texte simple
            if elem_name in attributes:
                xsd += f'  <xs:element name="{elem_name}">\n    <xs:complexType>\n      <xs:simpleContent>\n        <xs:extension base="xs:string">\n'
                for attr in attributes[elem_name]:
                    use = 'required' if attr['use'] == '#REQUIRED' else 'optional'
                    xsd_type = get_xsd_type(attr['type'])
                    xsd += f'          <xs:attribute name="{attr["name"]}" type="{xsd_type}" use="{use}"/>\n'
                xsd += '        </xs:extension>\n      </xs:simpleContent>\n    </xs:complexType>\n  </xs:element>\n'
            else:
                xsd += f'  <xs:element name="{elem_name}" type="xs:string"/>\n'
        else:
            # Élément complexe avec enfants
            xsd += f'  <xs:element name="{elem_name}">\n    <xs:complexType>\n      <xs:sequence>\n'
            for child in children:
                min_occurs = "1"
                max_occurs = "1"
                child_name = child

                # Gérer les multiplicateurs
                if child.endswith('+'):
                    child_name = child[:-1].strip()
                    min_occurs = "1"
                    max_occurs = "unbounded"
                elif child.endswith('*'):
                    child_name = child[:-1].strip()
                    min_occurs = "0"
                    max_occurs = "unbounded"
                elif child.endswith('?'):
                    child_name = child[:-1].strip()
                    min_occurs = "0"
                    max_occurs = "1"

                if child_name != "#PCDATA":
                    xsd += f'        <xs:element name="{child_name}" type="xs:string" minOccurs="{min_occurs}" maxOccurs="{max_occurs}"/>\n'

            xsd += '      </xs:sequence>\n'

            # Ajouter les attributs si présents
            if elem_name in attributes:
                for attr in attributes[elem_name]:
                    use = 'required' if attr['use'] == '#REQUIRED' else 'optional'
                    xsd_type = get_xsd_type(attr['type'])
                    xsd += f'      <xs:attribute name="{attr["name"]}" type="{xsd_type}" use="{use}"/>\n'

            xsd += '    </xs:complexType>\n  </xs:element>\n'

    xsd += '</xs:schema>'

    # Formatter proprement le XML
    try:
        dom = minidom.parseString(xsd)
        return dom.toprettyxml(indent="  ")
    except:
        return xsd

def convert_dtd_to_schema(request):
    """Vue Django pour convertir DTD -> XSD"""
    context = {'xsd_result': None, 'error': None, 'fileDTD': ''}

    if request.method == "POST":
        dtd_content = request.POST.get('fileDTD', '').strip()
        context['fileDTD'] = dtd_content

        if not dtd_content:
            context['error'] = "Veuillez fournir une DTD"
        else:
            try:
                context['xsd_result'] = build_xsd(dtd_content)
            except Exception as e:
                context['error'] = f"Erreur de conversion: {str(e)}"

    return render(request, 'converter/convert_dtd_to_schema.html', context)
