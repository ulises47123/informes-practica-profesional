import os
import glob
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

base_dir = r"C:\Users\Usuario\Music\proyectos\informes-practica-profesional"
template_docx = os.path.join(base_dir, "Informe_Diario_Practica.docx")
firma_path = os.path.join(base_dir, "firma.png")
out_dir = os.path.join(base_dir, "informes_docx")
os.makedirs(out_dir, exist_ok=True)

txt_files = sorted(glob.glob(os.path.join(base_dir, "[1-8]_Practica_*.txt")))

for txt_path in txt_files:
    fname = os.path.basename(txt_path)
    out_docx_name = fname.replace(".txt", ".docx")
    out_docx_path = os.path.join(out_dir, out_docx_name)
    
    with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        
    lines = [l.strip() for l in content.splitlines()]
    
    fecha_val = ""
    for l in lines:
        if l.startswith("Fecha:"):
            fecha_val = l.replace("Fecha:", "").strip()
            break
            
    def extract_section(text, sec_title, next_title):
        p1 = text.find(sec_title)
        if p1 == -1: return ""
        p1 += len(sec_title)
        if next_title:
            p2 = text.find(next_title, p1)
            raw = text[p1:p2] if p2 != -1 else text[p1:]
        else:
            raw = text[p1:]
        lines_sec = [x.strip() for x in raw.strip().splitlines() if x.strip()]
        if lines_sec and any(k in lines_sec[0] for k in ["Describir", "Enumerar", "Detallar", "Insertar", "Nombre y"]):
            lines_sec = lines_sec[1:]
        return "\n".join(lines_sec)

    sec1 = extract_section(content, "1. Actividad realizada", "2. Problema(s) encontrado(s)")
    sec2 = extract_section(content, "2. Problema(s) encontrado(s)", "3. Procedimiento / Solución aplicada")
    sec3 = extract_section(content, "3. Procedimiento / Solución aplicada", "4. Evidencia fotográfica")
    sec4 = extract_section(content, "4. Evidencia fotográfica", "5. Reflexión del grupo")
    sec5 = extract_section(content, "5. Reflexión del grupo", "6. Responsable del informe")
    
    # Load template fresh
    doc = docx.Document(template_docx)
    
    # Update Metadata paragraphs
    # P2: \nGrupo N°/Nombre: _______
    doc.paragraphs[2].text = "\nGrupo N°/Nombre: Grupo 4"
    for r in doc.paragraphs[2].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P3: Integrantes: _________________________________________
    doc.paragraphs[3].text = "Integrantes: Cabezas, Ulises Julian"
    for r in doc.paragraphs[3].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P4: Fecha: ___ / ___ / 2026\n
    doc.paragraphs[4].text = f"Fecha: {fecha_val}\n"
    for r in doc.paragraphs[4].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P6: prompt 1 -> add answer below in P7
    # P7 currently has '\n'
    doc.paragraphs[7].text = sec1 + "\n"
    for r in doc.paragraphs[7].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P9: prompt 2 -> add answer in P10
    doc.paragraphs[10].text = sec2 + "\n"
    for r in doc.paragraphs[10].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P12: prompt 3 -> add answer in P13
    doc.paragraphs[13].text = sec3 + "\n"
    for r in doc.paragraphs[13].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P15: prompt 4 -> add answer in P16
    doc.paragraphs[16].text = sec4 + "\n"
    for r in doc.paragraphs[16].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P18: reflection questions -> add answers in P19
    doc.paragraphs[19].text = sec5 + "\n"
    for r in doc.paragraphs[19].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # P21: Nombre y firma: _____________________________
    doc.paragraphs[21].text = "Nombre y firma: Cabezas, Ulises Julian"
    for r in doc.paragraphs[21].runs:
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # In P22, insert signature picture
    p22 = doc.paragraphs[22]
    p22.text = ""
    run_img = p22.add_run()
    run_img.add_picture(firma_path, width=Inches(1.8))
    
    doc.save(out_docx_path)
    print("Generated DOCX:", out_docx_name)

print("All DOCX files generated successfully.")
