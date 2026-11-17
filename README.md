# Generador de informes diarios de práctica profesional

Scripts en Python que toman informes escritos en texto plano (con la estructura de `plantilla.txt`) y generan el **Informe Diario de Práctica** con el formato institucional en Word (`.docx`) y en HTML listo para imprimir o pasar a PDF.

## Archivos

- `plantilla.txt`: estructura de cada informe (grupo, integrantes, fecha y las 6 secciones).
- `Informe_Diario_Practica.docx`: plantilla Word vacía que usa `generar_docx.py` (con su logo `image1.png`).
- `generar_docx.py`: genera un `.docx` por informe en `informes_docx/`.
- `generar_html.py`: genera HTML con diseño propio en `informes_html/`.
- `generar_html_word_exact.py`: genera HTML que imita la plantilla de Word.
- `test_playwright.py`: prueba de conversión de un HTML a PDF con Playwright.

## Uso

1. Escribí cada jornada en un archivo `N_Practica_<curso>_<grupo>_<dd-mm-aa>.txt` (N de 1 a 8) siguiendo `plantilla.txt`.
2. Poné tu firma escaneada como `firma.png` en la carpeta (no se incluye en el repo).
3. Ajustá en los scripts la ruta `base_dir`, el grupo y el nombre del responsable.
4. Ejecutá:

```bash
pip install python-docx playwright
python generar_docx.py
python generar_html.py
```

> Los informes reales, la firma y los datos del grupo están excluidos con `.gitignore`.
