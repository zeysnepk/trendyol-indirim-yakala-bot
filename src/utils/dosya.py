import json

class Dosya:
    def __init__(self, dosya_adi, mod='r', data_tip=list, yazilacak_veri=""):
        self.dosya_adi = dosya_adi
        self.dosya_uzantisi = dosya_adi.split('.')[1]
        self.mod = mod
        self.data_tip = data_tip
        self.data = None
        self.yazilacak_veri = yazilacak_veri
        
    def bos_veri_gonder(self):
        if self.data_tip == list:
            return []
        elif self.data_tip == dict:
            return {}
        else:
            raise ValueError("Desteklenmeyen veri tipi. Sadece list veya dict kullanılabilir.")
        
    def dosya_oku(self):
        self.dosya.seek(0)
        if not self.dosya.read():
            return self.bos_veri_gonder()
        self.dosya.seek(0)
        if self.dosya_uzantisi == "json":
            return json.load(self.dosya)
        elif self.dosya_uzantisi == "txt":
            return [line.strip() for line in self.dosya.readlines()]
        else:
            raise ValueError("Desteklenmeyen dosya uzantısı, json veya txt olmalıdır.")
        
    def dosya_yaz(self):
        self.dosya.seek(0)
        self.dosya.truncate()
        if self.dosya_uzantisi == "json":
            json.dump(self.yazilacak_veri, self.dosya, ensure_ascii=False, indent=4)
        elif self.dosya_uzantisi == "txt":
            self.dosya.writelines([line + "\n" for line in self.yazilacak_veri])
        else:
            raise ValueError("Desteklenmeyen dosya uzantısı, json veya txt olmalıdır.")
    
        
    def __enter__(self):
        try:
            self.dosya = open(self.dosya_adi, "r+", encoding="utf-8")
            
            if self.mod == 'r':
                return self.dosya_oku()
            elif self.mod == 'w':
                self.dosya_yaz()
                
        except FileNotFoundError:
            open(self.dosya_adi, 'w', encoding="utf-8").close()
            return self.bos_veri_gonder()
            
        except Exception as e:
            print(f"Dosya açılamadı: {e}")
            return self.bos_veri_gonder()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.dosya:
            self.dosya.close()