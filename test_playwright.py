from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe', headless=True)
    page = browser.new_page()
    html_path = os.path.abspath('informes_html/1_Practica_3_G4_22-09-26.html')
    page.goto(f'file:///{html_path}')
    page.pdf(path='test.pdf', format='Letter', print_background=True)
    browser.close()

print("PDF generado con éxito. Tamaño:", os.path.getsize('test.pdf'))
