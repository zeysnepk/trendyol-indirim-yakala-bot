import json
import requests
from bs4 import BeautifulSoup
import time
import random

class Trendyol:
    def __init__(self, data=None):
        self.data = data or {}
        
        # CSS Selectors ve class isimleri
        self.urun_ad_selector = "h1.pr-new-br span"
        self.urun_fiyat_selector = "span.prc-dsc"
        self.son_gun_fiyat_selector = "div.featured-price-info"
        
        # HTTP headers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "tr-TR,tr;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://www.trendyol.com/",
            "Connection": "keep-alive"
        }

    def urun_sayfa_ac(self, url):
        try:
            # Random gecikme ile bot davranışını gizle
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers, timeout=100)
            
            # Yanıt varsa
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Hata: Sayfa açılamadı. Durum kodu: {response.status_code}")
                return None
        except Exception as e:
            print(f"Sayfa açılamadı: {e}")
            return None
            
    def urun_bilgileri_gonder(self, soup):
        try:
            if not soup:
                return None, None, None
                
            urun_ad_element = soup.select(self.urun_ad_selector)
            if len(urun_ad_element) > 1: 
                urun_ad = urun_ad_element[-1].text.strip()
            else:
                urun_ad = urun_ad_element[0].text.strip()
            urun_ad = urun_ad if urun_ad_element else "Ürün adı bulunamadı"
            
            urun_fiyat_element = soup.select_one(self.urun_fiyat_selector)
            if urun_fiyat_element:
                urun_fiyat_text = urun_fiyat_element.text.strip()
                urun_fiyat = float(urun_fiyat_text.replace('TL', '').replace('.', '').replace(',', '.').strip())
            else:
                urun_fiyat = None
            
            # Eğer son 30 günün en düşük fiyatı gibi bilgilendirme varsa
            son_gun_fiyat_element = soup.select_one(self.son_gun_fiyat_selector)
            son_gun_fiyat = son_gun_fiyat_element.text.strip() if son_gun_fiyat_element else ""
            
            return urun_ad, urun_fiyat, son_gun_fiyat
        except Exception as e:
            print(f"Ürün bilgileri alınamadı: {e}")
            return None, None, None


def main():
    try:
        with open("urun_bilgileri.json", "r", encoding='utf-8') as json_file:
            content = json_file.read().strip() 
            if not content:  
                data = {}
            else:
                data = json.loads(content) 
    except (json.JSONDecodeError, FileNotFoundError):
        data = {}
    
    trendyol = Trendyol(data)
    
    try:
        with open("urls.txt", "r") as f:
            urls = [line.strip() for line in f.readlines()]
        
        for url in urls:
            soup = trendyol.urun_sayfa_ac(url)
            urun_ad, urun_fiyat, son_gun_fiyat = trendyol.urun_bilgileri_gonder(soup)
            print(f"{urun_ad}\n{urun_fiyat}\n{son_gun_fiyat}\n")
            # Random bekleme
            time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Hata: {str(e)}")

if __name__ == "__main__":
    main()
