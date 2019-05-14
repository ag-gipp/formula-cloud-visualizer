import requests
import os
from xml.dom import minidom
from lxml import etree

url = "http://localhost:10044/svg"

def mathml2latex_yarosh(equation):
    """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich """
    xslt_file = "../mathconverter/xsl_yarosh/mmltex.xsl"
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return str(newdom)

class Expression:
    def __init__(self, count, depth, mml):
        self.count = count
        self.depth = depth

        math = "<math xmlns:m=\"http://www.w3.org/1998/Math/MathML\">" + mml + "</math>"
        # payload = {'q': math, 'type': 'mml'}
        # res = requests.post(url, data=payload)
        self.tex = mathml2latex_yarosh(math)
        if self.tex:
            self.tex = "$" + self.tex + "$"
        else:
            self.tex = " "

    def getCount(self):
        return self.count

    def getDepth(self):
        return self.depth

    def getTEX(self):
        return self.tex


def parse_document(path):
    expressions = list()
    print("Parse xml stats...")
    doc = minidom.parse(path)
    print("Finished parsing stats...")

    max = 50
    counter = 0
    elements = doc.getElementsByTagName("element")
    for element in elements:
        if counter > max:
            break

        counter += 1
        children = element.childNodes[1].toxml()
        count = int(element.getAttribute("count"))
        depth = int(element.getAttribute("max-depth"))
        expr = Expression(count, depth, children)

        if len(expressions) < depth:
            expressions.append(list())

        expressions[depth-1].append(expr)

    return expressions
