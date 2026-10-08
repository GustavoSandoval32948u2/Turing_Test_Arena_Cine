"""Genera el diagrama editable y las tablas desde las mismas delta del codigo."""
import csv
from pathlib import Path
import xml.etree.ElementTree as ET
from afd.clasificador import ClasificadorAFD


def exportar():
    carpeta = Path(__file__).parent / 'documentacion_lexica'
    carpeta.mkdir(exist_ok=True)
    banco = ClasificadorAFD().automatas
    mxfile = ET.Element('mxfile', host='app.diagrams.net')
    with (carpeta / 'transiciones_afd.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['AFD', 'Token', 'Frase', 'Origen', 'Simbolo', 'Destino', 'Aceptacion'])
        for afd in banco:
            pagina = ET.SubElement(mxfile, 'diagram', id=afd.nombre, name=f'{afd.nombre} {afd.token} {afd.frase}')
            modelo = ET.SubElement(pagina, 'mxGraphModel', page='1', pageWidth='1600', pageHeight='900')
            root = ET.SubElement(modelo, 'root')
            ET.SubElement(root, 'mxCell', id='0')
            ET.SubElement(root, 'mxCell', id='1', parent='0')
            def nodo(id, texto, x, y, w, h, estilo):
                cell = ET.SubElement(root, 'mxCell', id=id, value=texto, vertex='1', parent='1', style=estilo)
                ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})
            nodo('titulo', f'{afd.nombre} | {afd.token} | {afd.frase}\nInicio q0; final q{afd.final} absorbente. OTRO = cualquier simbolo fuera del alfabeto de esta frase.\nSe consume toda la entrada. Orden de seleccion: paginas A000 en adelante; gana el primer AFD que acepta.\nNormalizacion: minusculas/sin tildes; ¿ ? ¡ ! son simbolos separados. Sin palabras: DESCONOCIDO.', 20, 10, 1500, 120, 'text;whiteSpace=wrap;html=0;fontSize=17;align=left;')
            for q in range(afd.final+1):
                nodo(f'q{q}', f'q{q}', 80+q*180, 210, 70, 70,
                     'shape=doubleEllipse;html=0;' if q == afd.final else 'ellipse;html=0;')
            nodo('inicio', '', 25, 235, 8, 8, 'ellipse;fillColor=#000000;')
            edge = ET.SubElement(root, 'mxCell', id='start', edge='1', parent='1', source='inicio', target='q0', style='endArrow=classic;')
            ET.SubElement(edge, 'mxGeometry', relative='1', **{'as':'geometry'})
            grupos = {}
            filas = []
            for (q,s), dest in afd.delta.items():
                writer.writerow([afd.nombre, afd.token, afd.frase, f'q{q}', s, f'q{dest}', dest==afd.final])
                grupos.setdefault((q,dest), []).append(s)
                filas.append(f'q{q} | {s} | q{dest}')
            for i, ((q,dest), simbolos) in enumerate(grupos.items()):
                edge = ET.SubElement(root, 'mxCell', id=f'e{i}', value=', '.join(simbolos), edge='1', parent='1', source=f'q{q}', target=f'q{dest}', style='curved=1;endArrow=classic;html=0;fontSize=12;')
                geo=ET.SubElement(edge, 'mxGeometry', relative='1', **{'as':'geometry'})
                if q != dest and dest != q+1:
                    arr=ET.SubElement(geo,'Array', **{'as':'points'})
                    ET.SubElement(arr,'mxPoint',x=str(115+(q+dest)*90),y=str(320+q*25))
            # Tabla junto al diagrama: permite leer todas las transiciones sin cruces.
            for col, start in enumerate(range(0,len(filas),18)):
                nodo(f'tabla{col}', 'Origen | simbolo | destino\n'+'\n'.join(filas[start:start+18]), 30+col*310, 500, 300, 370, 'text;html=0;align=left;verticalAlign=top;fontFamily=monospace;fontSize=12;')
    ET.indent(mxfile)
    ET.ElementTree(mxfile).write(carpeta/'AFD_Lexico_Cine.drawio', encoding='utf-8', xml_declaration=True)
    with (carpeta/'catalogo_y_prioridad.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer=csv.writer(f); writer.writerow(['Orden','AFD','Token','Frase','Estado final'])
        for i,a in enumerate(banco): writer.writerow([i,a.nombre,a.token,a.frase,f'q{a.final}'])
    print(f'Exportados {len(banco)} AFD con sus tablas y diagrama editable.')

if __name__ == '__main__':
    exportar()
