# 🔍 Trendyol İndirim Yakalama Botu

Bu proje, Trendyol'daki ürünlerin fiyatlarını otomatik olarak takip eden ve fiyat düşüşlerinde kullanıcıya e-posta bildirimi gönderen bir Python uygulamasıdır.

## ✨ Özellikler

- 🕒 Belirlenen ürünlerin fiyatlarını istenilen periyotla kontrol eder
- 📧 Fiyat düşüşlerinde e-posta bildirimi gönderir
- 📦 Birden fazla ürünü takip edebilir
- 🔄 Bağlantı kopukluklarında otomatik yeniden deneme
- 💾 JSON dosyası ile kolay ürün yönetimi

## 📋 Gereksinimler

```
asyncio
playwright
```

## 🚀 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/zeysnepk/trendyol-indirim-yakala-bot.git
cd trendyol-indirim-yakala
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Playwright tarayıcısını yükleyin:
```bash
playwright install
```

4. `config/config.json` dosyasını düzenleyin:
```json
{
    "gonderen_mail_adresi" : "gonderen_mail_giriniz@gmail.com",
    "gonderen_mail_sifresi" : "mail_sifre_giriniz",
    "alici_mail_adresi" : "alici_mail_giriniz@gmail.com"
}
```

5. İsterseniz main.py dosyasında kontrol sıklığı için saniye değerini manuel ayarlayabilirsiniz:
```python
sure = 60 # Kontrol için saniye aralığı
```

Not: Gmail kullanıyorsanız, "gonderen_mail_sifresi" için uygulama şifresi oluşturmanız gerekir. [Google Hesap Güvenliği](https://myaccount.google.com/security) sayfasından uygulama şifresi oluşturabilirsiniz.

## 💻 Kullanım

1. Takip etmek istediğiniz ürünlerin URL'lerini `config/urls.txt` dosyasına ekleyin:
```
https://www.trendyol.com/marka/ornek_urun
https://www.trendyol.com/marka/ornek_urun_2
```

2. Uygulamayı başlatın:
```bash
python main.py
```

## Dosya Yapısı

```
├── config/
│   ├── config.json     # E-posta ayarları
│   └── urls.txt        # Takip edilecek ürün URL'leri
├── data/
│   └── urun_bilgileri.json  # Ürün bilgilerinin saklandığı dosya
├── src/
│   ├── scraper/
│   │   └── trendyol.py      # Trendyol scraper sınıfı
│   └── utils/
│       ├── dosya.py         # Dosya işlemleri için yardımcı sınıf
│       └── mail.py          # E-posta gönderme fonksiyonları
├── requirements.txt
└── main.py            # Ana uygulama dosyası
```

## 🔄 Nasıl Çalışır?

1. Program başlatıldığında, `urls.txt` dosyasındaki URL'ler okunur
2. Her URL için belirtilen süre aralığında (varsayılan: 60 saniye) fiyat kontrolü yapılır
3. Ürün fiyatında düşüş tespit edildiğinde:
   - Yeni fiyat bilgisi JSON dosyasına kaydedilir
   - Kullanıcıya e-posta bildirimi gönderilir
4. İnternet bağlantısı kesilirse, program otomatik olarak yeniden bağlanmayı dener

## ⚠️ Hata Durumları

- Program internet bağlantısı koptuğunda otomatik olarak yeniden deneme yapar
- Tarayıcı açılma hatalarında otomatik yeniden başlatma gerçekleştirir
- Dosya okuma/yazma hatalarında varsayılan boş değerler kullanır

## 🔐 Güvenlik Notları

- Gmail için ana şifreniz yerine uygulama şifresi kullanın


