from src.scraper.trendyol import Trendyol
from src.utils.dosya import Dosya
import src.utils.mail as mail
import asyncio
import socket

# İstenilen ürünlerin url lerinin bulunduğu dosya
urls_dosya_adi = "config/urls.txt"

# Ürün bilgileri kaydedilecek json dosya
bilgiler_dosya_adi = "data/urun_bilgileri.json"

urunler = []

def dosya_oku(dosya_adi):
    with Dosya(dosya_adi) as icerik:
        return icerik
    
def dosya_yaz(dosya_adi, veri):
    with Dosya(dosya_adi, 'w', yazilacak_veri=veri) as icerik:
        pass
    
def silinmis_linkleri_cikar(urls, urun_bilgileri):
    mevcut_urunler = [urun for urun in urun_bilgileri if urun["url"] in urls]
    dosya_yaz(bilgiler_dosya_adi, mevcut_urunler)
    return mevcut_urunler
        
    
# Dosya Class ı ile dosyaları oku
urun_bilgileri = dosya_oku(bilgiler_dosya_adi)
urls = dosya_oku(urls_dosya_adi)

# Tekrar eden url leri temizle
urls_listesi = list(set(urls)) 
dosya_yaz(urls_dosya_adi, urls_listesi)

urun_bilgileri = silinmis_linkleri_cikar(urls_listesi, urun_bilgileri)
sure = 60 # Kontrol için saniye aralığı

async def urunler_kontrol(url, trendyol):
    try:
        await trendyol.urun_sayfa_ac(url)
        ad, fiyat = await trendyol.urun_bilgileri_gonder()
        print(ad, fiyat)
        await trendyol.urun_sayfa_kapa()
        urun = next((urun for urun in urun_bilgileri if urun["url"] == url), None)
        if urun:
            if fiyat < urun["fiyat"]:
                mail.mail_gonder(ad, fiyat, urun["fiyat"], url)
                print(f"[Fiyat Güncellendi] {ad} | Yeni: {fiyat} | Eski: {urun['fiyat']}\n")
                urun["fiyat"] = fiyat # Yeni fiyatı güncelle
                return True
            else:
                print(f"[Fiyat Aynı] {ad} | Fiyat: {fiyat}\n")
        else:
            print(f"[Urun Bulunamadı] {url}\n")
            data = {"urun_ad": ad, "fiyat": fiyat, "url": url}  
            urun_bilgileri.append(data)  
            return True
        return False
    except Exception as e:
        print(f"Ürün Kontrolde Hata: {str(e)}")
        return False


# İnternet kontrolü yapar
async def internet_kontrol():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        print("İnternet bağlantısı yok")
        return False

# Ana fonksiyon
async def main():
    try:
        while True:
            # Chrome aç
            trendyol = Trendyol()
            await trendyol.browser_ac()
            if not await internet_kontrol():
                print("Bağlantı yok, tekrar deneyecek...")
                await asyncio.sleep(60)
                continue
            for url in urls_listesi:
                if await urunler_kontrol(url, trendyol):
                    dosya_yaz(bilgiler_dosya_adi, urun_bilgileri)
            await asyncio.sleep(sure)          
    except Exception as e:
        print(f"Hata: {str(e)}")
        print("Tekrar başlatılıyor...")
        await asyncio.sleep(10) 
        await main()
    finally: 
        await trendyol.browser_kapa()

asyncio.run(main())


