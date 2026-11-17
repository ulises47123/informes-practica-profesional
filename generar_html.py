import os
import base64
import glob

base_dir = r"C:\Users\Usuario\Music\proyectos\informes-practica-profesional"
out_dir = os.path.join(base_dir, "informes_html")
os.makedirs(out_dir, exist_ok=True)

# Load signature
firma_path = os.path.join(base_dir, "firma.png")
with open(firma_path, "rb") as f:
    firma_b64 = base64.b64encode(f.read()).decode("utf-8")

# Parse each txt file
txt_files = sorted(glob.glob(os.path.join(base_dir, "[1-8]_Practica_*.txt")))

for txt_path in txt_files:
    fname = os.path.basename(txt_path)
    html_name = fname.replace(".txt", ".html")
    
    with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    # Extract fields
    lines = [l.strip() for l in content.splitlines()]
    
    fecha = ""
    for l in lines:
        if l.startswith("Fecha:"):
            fecha = l.replace("Fecha:", "").strip()
            break
            
    # Parse numbered sections
    def extract_section(text, sec_title, next_title):
        p1 = text.find(sec_title)
        if p1 == -1: return ""
        p1 += len(sec_title)
        if next_title:
            p2 = text.find(next_title, p1)
            raw = text[p1:p2] if p2 != -1 else text[p1:]
        else:
            raw = text[p1:]
        # Remove prompt line (first non-empty line usually)
        lines_sec = [x.strip() for x in raw.strip().splitlines() if x.strip()]
        if lines_sec and ("Describir" in lines_sec[0] or "Enumerar" in lines_sec[0] or "Detallar" in lines_sec[0] or "Insertar" in lines_sec[0] or "Nombre y" in lines_sec[0]):
            lines_sec = lines_sec[1:]
        return "\n".join(lines_sec)

    sec1 = extract_section(content, "1. Actividad realizada", "2. Problema(s) encontrado(s)")
    sec2 = extract_section(content, "2. Problema(s) encontrado(s)", "3. Procedimiento / Solución aplicada")
    sec3 = extract_section(content, "3. Procedimiento / Solución aplicada", "4. Evidencia fotográfica")
    sec4 = extract_section(content, "4. Evidencia fotográfica", "5. Reflexión del grupo")
    sec5 = extract_section(content, "5. Reflexión del grupo", "6. Responsable del informe")
    
    # Process reflection items
    ref_ap = ""
    ref_dif = ""
    ref_mej = ""
    if sec5:
        p_ap = sec5.find("¿Qué aprendimos hoy?")
        p_dif = sec5.find("¿Qué dificultades tuvimos y cómo las resolvimos?")
        p_mej = sec5.find("¿Qué mejoraríamos para la próxima jornada?")
        
        if p_ap != -1 and p_dif != -1:
            ref_ap = sec5[p_ap + len("¿Qué aprendimos hoy?"):p_dif].strip()
        if p_dif != -1 and p_mej != -1:
            ref_dif = sec5[p_dif + len("¿Qué dificultades tuvimos y cómo las resolvimos?"):p_mej].strip()
        if p_mej != -1:
            ref_mej = sec5[p_mej + len("¿Qué mejoraríamos para la próxima jornada?"):].strip()

    # Process evidence photos
    ev_cards = ""
    for line in sec4.splitlines():
        line = line.strip()
        if not line: continue
        tag = ""
        desc = line
        if line.startswith("[Foto"):
            idx_close = line.find("]:")
            if idx_close != -1:
                tag = line[:idx_close+1].strip("[]")
                desc = line[idx_close+2:].strip()
        ev_cards += f'''
        <div class="evidence-card">
          <div class="evidence-tag">{tag}</div>
          <div class="evidence-desc">{desc}</div>
        </div>'''

    html_out = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe Diario de Práctica - {fecha}</title>
  <style>
    @page {{
      size: A4;
      margin: 20mm;
    }}
    body {{
      background-color: #f0f2f5;
      font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 30px 0;
      color: #1a1a1a;
      line-height: 1.45;
    }}
    .document-page {{
      background-color: #ffffff;
      width: 210mm;
      min-height: 297mm;
      margin: 0 auto;
      padding: 22mm 24mm;
      box-sizing: border-box;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
      border: 1px solid #dcdcdc;
    }}
    .header-box {{
      text-align: center;
      border-bottom: 2px solid #2b4c7e;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }}
    .header-box h1 {{
      font-size: 18pt;
      margin: 0 0 5px 0;
      color: #1d3557;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .header-box h2 {{
      font-size: 11pt;
      margin: 3px 0;
      font-weight: 600;
      color: #333333;
    }}
    .header-box .institution-info {{
      font-size: 9.5pt;
      color: #555555;
      margin-top: 4px;
    }}
    .meta-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 18px;
      font-size: 10pt;
    }}
    .meta-table td {{
      padding: 6px 10px;
      border: 1px solid #c9d6df;
    }}
    .meta-table .label {{
      font-weight: bold;
      background-color: #f4f7f9;
      width: 25%;
      color: #1d3557;
    }}
    .meta-table .val {{
      width: 75%;
    }}
    .section-title {{
      font-size: 10.5pt;
      font-weight: bold;
      color: #1d3557;
      border-left: 4px solid #2b4c7e;
      padding-left: 8px;
      margin-top: 14px;
      margin-bottom: 3px;
      text-transform: uppercase;
    }}
    .section-prompt {{
      font-size: 8.5pt;
      color: #6c757d;
      font-style: italic;
      margin-bottom: 6px;
      padding-left: 12px;
    }}
    .section-content {{
      font-size: 10pt;
      text-align: justify;
      margin-bottom: 12px;
      padding-left: 12px;
      color: #222222;
    }}
    .reflection-item {{
      margin-bottom: 6px;
      padding-left: 12px;
    }}
    .reflection-q {{
      font-weight: bold;
      color: #2b4c7e;
      font-size: 9.5pt;
    }}
    .reflection-a {{
      font-size: 10pt;
      color: #222222;
      text-align: justify;
      margin-top: 2px;
    }}
    .evidence-box {{
      display: flex;
      gap: 16px;
      margin-top: 8px;
      margin-bottom: 12px;
      padding-left: 12px;
    }}
    .evidence-card {{
      flex: 1;
      border: 1px dashed #90a4ae;
      background-color: #fafbfc;
      border-radius: 4px;
      padding: 12px;
      text-align: center;
      min-height: 80px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }}
    .evidence-tag {{
      font-size: 9pt;
      font-weight: bold;
      color: #2b4c7e;
      margin-bottom: 4px;
    }}
    .evidence-desc {{
      font-size: 8.5pt;
      color: #455a64;
    }}
    .signature-area {{
      margin-top: 28px;
      display: flex;
      justify-content: flex-end;
      page-break-inside: avoid;
    }}
    .signature-box {{
      width: 250px;
      text-align: center;
      border-top: 1px solid #1a1a1a;
      padding-top: 6px;
    }}
    .signature-img {{
      max-height: 60px;
      max-width: 180px;
      display: block;
      margin: 0 auto 4px auto;
    }}
    .signature-name {{
      font-size: 9.5pt;
      font-weight: bold;
      color: #1a1a1a;
    }}
    .signature-role {{
      font-size: 8pt;
      color: #555555;
    }}
    @media print {{
      body {{
        background: none;
        padding: 0;
      }}
      .document-page {{
        box-shadow: none;
        border: none;
        margin: 0;
        width: 100%;
        min-height: auto;
        padding: 0;
      }}
    }}
  </style>
</head>
<body>

  <div class="document-page">
    <div class="header-box">
      <h1>Informe Diario de Práctica</h1>
      <h2>Tecnicatura en Soporte de Infraestructura en Tecnologías de la Información</h2>
      <div class="institution-info">
        Institución: <strong>I.E.S. N° 5 "José Eugenio Tello"</strong> &nbsp;|&nbsp; Curso: <strong>3° Año</strong>
      </div>
    </div>

    <table class="meta-table">
      <tr>
        <td class="label">Grupo N° / Nombre:</td>
        <td class="val">Grupo 4</td>
      </tr>
      <tr>
        <td class="label">Integrantes:</td>
        <td class="val">Cabezas, Ulises Julian</td>
      </tr>
      <tr>
        <td class="label">Fecha:</td>
        <td class="val">{fecha}</td>
      </tr>
    </table>

    <div class="section-title">1. Actividad realizada</div>
    <div class="section-prompt">Describir brevemente las tareas desarrolladas en la jornada.</div>
    <div class="section-content">
      {sec1}
    </div>

    <div class="section-title">2. Problema(s) encontrado(s)</div>
    <div class="section-prompt">Enumerar los problemas detectados en los equipos o conexiones.</div>
    <div class="section-content">
      {sec2}
    </div>

    <div class="section-title">3. Procedimiento / Solución aplicada</div>
    <div class="section-prompt">Detallar los pasos realizados para solucionar el problema.</div>
    <div class="section-content">
      {sec3}
    </div>

    <div class="section-title">4. Evidencia fotográfica</div>
    <div class="section-prompt">Insertar aquí 2 o 3 fotos de la práctica con breve descripción debajo de cada una.</div>
    <div class="evidence-box">
      {ev_cards}
    </div>

    <div class="section-title">5. Reflexión del grupo</div>
    <div class="reflection-item">
      <div class="reflection-q">¿Qué aprendimos hoy?</div>
      <div class="reflection-a">{ref_ap}</div>
    </div>
    <div class="reflection-item">
      <div class="reflection-q">¿Qué dificultades tuvimos y cómo las resolvimos?</div>
      <div class="reflection-a">{ref_dif}</div>
    </div>
    <div class="reflection-item">
      <div class="reflection-q">¿Qué mejoraríamos para la próxima jornada?</div>
      <div class="reflection-a">{ref_mej}</div>
    </div>

    <div class="section-title">6. Responsable del informe</div>
    <div class="signature-area">
      <div class="signature-box">
        <img class="signature-img" src="data:image/png;base64,{firma_b64}" alt="Firma">
        <div class="signature-name">Cabezas, Ulises Julian</div>
        <div class="signature-role">Estudiante practicante - Grupo 4</div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    dest_path = os.path.join(out_dir, html_name)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Generated:", html_name)

print("All HTML files created successfully.")
