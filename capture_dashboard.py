import time
from playwright.sync_api import sync_playwright

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 950})
        page.goto('http://localhost:8501', wait_until='networkidle')
        time.sleep(4)
        page.screenshot(path='figures/dashboard_pagina1_analisis_general.png', full_page=True)
        print('Página 1 guardada como full page')

        # Click radio button for Página 2
        labels = page.locator('div[role="radiogroup"] label')
        count = labels.count()
        print('Radio options found:', count)
        if count >= 2:
            labels.nth(1).click()
            time.sleep(4)
            page.screenshot(path='figures/dashboard_pagina2_segmentacion_kmeans.png', full_page=True)
            print('Página 2 guardada como full page')

        browser.close()

if __name__ == '__main__':
    capture()
