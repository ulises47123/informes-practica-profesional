import os
import base64
import glob

base_dir = r"C:\Users\Usuario\Music\proyectos\informes-practica-profesional"
out_dir = os.path.join(base_dir, "informes_html")
os.makedirs(out_dir, exist_ok=True)

# Load signature & institutional logo
with open(os.path.join(base_dir, "firma.png"), "rb") as f:
    firma_b64 = base64.b64encode(f.read()).decode("utf-8")

with open(os.path.join(base_dir, "image1.png"), "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

txt_files = sorted(glob.glob(os.path.join(base_dir, "[1-8]_Practica_*.txt")))

for txt_path in txt_files:
    fname = os.path.basename(txt_path)
    html_name = fname.replace(".txt", ".html")
    
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

    html_out = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe Diario de Práctica - {fecha_val}</title>
  <style>
    @page {{
      size: letter;
      margin: 1in 1.25in;
    }}
    body {{
      background-color: #f2f2f2;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 30px 0;
      color: #000000;
    }}
    .document-page {{
      background-color: #ffffff;
      width: 8.5in;
      min-height: 11in;
      margin: 0 auto;
      padding: 1in 1.25in;
      box-sizing: border-box;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
      font-size: 12pt;
      line-height: 1.5;
    }}
    /* Header layout matching docx header1.xml */
    .docx-header {{
      margin-bottom: 24pt;
    }}
    .docx-header-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 8pt;
    }}
    .docx-header-table td {{
      vertical-align: middle;
      border: none;
      padding: 0;
    }}
    .header-logo-cell {{
      width: 65px;
      text-align: left;
    }}
    .header-logo-cell img {{
      height: 68px;
      display: block;
    }}
    .header-text-cell {{
      text-align: center;
      font-size: 8pt;
      line-height: 1.25;
      padding-left: 10px;
    }}
    .header-text-cell .inst-title {{
      font-weight: bold;
    }}
    .header-right-label {{
      text-align: right;
      font-size: 9pt;
      font-weight: bold;
      margin-top: 4pt;
      letter-spacing: 0.3px;
    }}
    
    /* Body typography exactly as Word template */
    h1.doc-title {{
      font-size: 14pt;
      font-weight: bold;
      color: #000000;
      margin: 6pt 0;
      line-height: 1.5;
    }}
    h2.section-heading {{
      font-size: 13pt;
      font-weight: bold;
      color: #000000;
      margin: 6pt 0 2pt 0;
      line-height: 1.5;
    }}
    .lead-meta {{
      margin: 6pt 0;
      line-height: 1.5;
    }}
    .prompt-text {{
      font-size: 12pt;
      color: #000000;
      margin: 2pt 0 4pt 0;
      line-height: 1.5;
    }}
    .answer-text {{
      font-size: 12pt;
      color: #000000;
      margin: 4pt 0 10pt 0;
      line-height: 1.5;
      white-space: pre-line;
      text-align: justify;
    }}
    .signature-container {{
      margin-top: 10pt;
    }}
    .signature-container img {{
      height: 70px;
      display: block;
      margin-top: 6pt;
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
    <!-- Encabezado idéntico al documento Word original -->
    <div class="docx-header">
      <table class="docx-header-table">
        <tr>
          <td class="header-logo-cell">
            <img src="data:image/png;base64,{logo_b64}" alt="Escudo IES N°5">
          </td>
          <td class="header-text-cell">
            <div>Tecnicatura Superior en Soporte de Infraestructura de</div>
            <div>Tecnología de la Información</div>
            <div class="inst-title">INSTITUTO DE EDUCACION SUPERIOR N° 5</div>
            <div class="inst-title">“JOSE EUGENIO TELLO”</div>
          </td>
        </tr>
      </table>
      <div class="header-right-label">PRÁCTICAS PROFESIONALIZANTES III</div>
    </div>

    <h1 class="doc-title">Informe Diario de Práctica</h1>
    <div class="lead-meta">
      Tecnicatura en Soporte de Infraestructura en Tecnologías de la Información<br>
      Institución: I.E.S.N° 5<br>
      Curso: 3° Año
    </div>

    <div class="lead-meta">
      Grupo N°/Nombre: Grupo 4<br>
      Integrantes: Cabezas, Ulises Julian<br>
      Fecha: {fecha_val}
    </div>

    <h2 class="section-heading">1. Actividad realizada</h2>
    <div class="prompt-text">Describir brevemente las tareas desarrolladas en la jornada.</div>
    <div class="answer-text">{sec1}</div>

    <h2 class="section-heading">2. Problema(s) encontrado(s)</h2>
    <div class="prompt-text">Enumerar los problemas detectados en los equipos o conexiones.</div>
    <div class="answer-text">{sec2}</div>

    <h2 class="section-heading">3. Procedimiento / Solución aplicada</h2>
    <div class="prompt-text">Detallar los pasos realizados para solucionar el problema.</div>
    <div class="answer-text">{sec3}</div>

    <h2 class="section-heading">4. Evidencia fotográfica</h2>
    <div class="prompt-text">Insertar aquí 2 o 3 fotos de la práctica con breve descripción debajo de cada una.</div>
    <div class="answer-text">{sec4}</div>

    <h2 class="section-heading">5. Reflexión del grupo</h2>
    <div class="prompt-text">¿Qué aprendimos hoy?<br>¿Qué dificultades tuvimos y cómo las resolvimos?<br>¿Qué mejoraríamos para la próxima jornada?</div>
    <div class="answer-text">{sec5}</div>

    <h2 class="section-heading">6. Responsable del informe</h2>
    <div class="prompt-text">Nombre y firma: Cabezas, Ulises Julian</div>
    <div class="signature-container">
      <img src="data:image/png;base64,{firma_b64}" alt="Firma">
    </div>
  </div>

</body>
</html>
"""
    dest_path = os.path.join(out_dir, html_name)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Re-generated HTML:", html_name)

print("All HTML files updated to match Word document design exactly.")
