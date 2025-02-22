import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.utils.dosya import Dosya

config_dosya_adi = "config/config.json"

with Dosya(config_dosya_adi) as config:
    config_data = config
    
gonderen = config_data["gonderen_mail_adresi"]
sifre = config_data["gonderen_mail_sifresi"]
alan = config_data["alici_mail_adresi"]

def mail_gonder(ad, fiyat, onceki_fiyat, url):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  
        server.login(gonderen, sifre)
        
        # Mail içeriği
        msg = MIMEMultipart()
        msg["From"] = gonderen
        msg["To"] = alan
        msg["Subject"] = f"{ad} adlı ürünün fiyatı düştü!!!!"
        msg.attach(MIMEText(f"Ürün: {ad}\nEski Fiyat: {onceki_fiyat} TL\nYeni Fiyat: {fiyat} TL\nLink: {url}", "plain"))
        
        server.sendmail(gonderen, alan, msg.as_string())
        server.quit()
        print("Mail başarıyla gönderildi!")
    except Exception as e:
        print(f"Hata, mail gönderilemedi: {str(e)}")