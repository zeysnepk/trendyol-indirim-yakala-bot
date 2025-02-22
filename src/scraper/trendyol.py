import json
import asyncio
from playwright.async_api import async_playwright

class Trendyol():
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None

        # Trendyol api için CSS Selector lar
        #product-detail-app > div > div.flex-container > div > div:nth-child(2) > div:nth-child(2) > div > div.product-detail-wrapper > div.pr-in-w > div > div > div:nth-child(1) > h1 > span:nth-child(2)
        self.urun_ad = "#product-detail-app > div > div.flex-container > div > div:nth-child(2) > div:nth-child(2) > div > div.product-detail-wrapper > div.pr-in-w > div > div > div:nth-child(1) > h1 > span"
                            #product-detail-app > div > div.flex-container > div > div:nth-child(2) > div:nth-child(2) > div > div.product-detail-wrapper > div.pr-in-w > div > div > div.product-price-container > div > div > div > div.featured-prices > span.prc-dsc
                            #product-detail-app > div > div.flex-container > div > div:nth-child(2) > div:nth-child(2) > div > div.product-detail-wrapper > div.pr-in-w > div > div > div.product-price-container > div > div > div > div.featured-prices > span.prc-org
                            #product-detail-app > div > div.flex-container > div > div:nth-child(2) > div:nth-child(2) > div > div.product-detail-wrapper > div.pr-in-w > div > div > div.product-price-container > div > div > span
        self.urun_fiyat = 'span[class="prc-dsc"]'

    # Tarayıcıyı açar(Chrome)
    async def browser_ac(self):
        try:
            if self.browser is None:
                self.playwright = await async_playwright().start()
                self.browser = await self.playwright.chromium.launch(headless=True)
                return True
        except Exception as e:
            print(f"Chrome açılamadı: {e}")
            return False
            
    # Ürünün bulunduğu sayfayı açar
    async def urun_sayfa_ac(self, url):
        try:
            if self.browser is None:
                print(1)
                await self.browser_ac()
            self.page = await self.browser.new_page()
            await self.page.goto(url, wait_until="networkidle", timeout=10000) 
        except Exception as e:
            print(f"Sayfa açılamadı: {e}")
            
    # Ürün ad ve fiyatını alıp gönderir
    async def urun_bilgileri_gonder(self):
        try:
            await self.page.wait_for_load_state("networkidle")
            urun_ad_list = await self.page.locator(self.urun_ad).all_inner_texts()
            # Doğru kullanım:
            urun_fiyat = await self.page.locator(self.urun_fiyat).nth(0).inner_text()
            if len(urun_ad_list) > 1:
                urun_ad = urun_ad_list[-1]
            else:
                urun_ad = urun_ad_list[0]
                
            urun_fiyat = float(urun_fiyat.replace('TL', '').replace('.', '').replace(',', '.').strip())
            return urun_ad, urun_fiyat
        except Exception as e:
            print("Ürün None", e)
            return None, None
            
    # Ürün bilgileri alındıktan sonra ürün sayfasını kapatır
    async def urun_sayfa_kapa(self):
        try:
            if self.page:
                await self.page.close()
                self.page = None
        except Exception as e:
            print(f"Sayfa kapatılamadı: {e}")
            
    # Tüm işlemler bittikten sonra tarayıcıyı kapatır
    async def browser_kapa(self):
        if self.browser:
            try:
                await self.browser.close()
                await self.playwright.stop()
                self.browser = None
                self.page = None 
                return True
            except Exception as e:
                print(f"Tarayıcı kapatılamadı: {e}")
                return False
            
# Kullanım örneği:
async def main(data):
    try:
        trendyol = Trendyol(data)
        with open("urls.txt", "r") as f:
            urls = [line.strip() for line in f.readlines()]
        for url in urls:
            await trendyol.urun_fiyat_kontrol(url)
    except Exception as e:
        print(f"Hata: {str(e)}")
    finally: 
        await trendyol.browser_kapa()

if __name__ == "__main__":
    # JSON dosyasından ürün bilgileri alınır
    try:
        with open("urun_bilgileri.json", "r", encoding='utf-8') as json_file:
            content = json_file.read().strip() 
            if not content:  
                data = {}
            else:
                data = json.loads(content) 
    except json.JSONDecodeError:
        data = {}
    asyncio.run(main(data))