import os
from datetime import date

class Kullanici:
    def __init__(self, tip, kullanici_adi, parola, kimlik):
        self.tip = tip             
        self.kullanici_adi = kullanici_adi
        self.parola = parola
        self.kimlik = kimlik       
class Basvuru:
    def __init__(self, ogrenci_no, basvuru_tarihi, basvuru_durumu, yurt_id):
        self.ogrenci_no = ogrenci_no
        self.basvuru_tarihi = basvuru_tarihi
        self.basvuru_durumu = basvuru_durumu  
        self.yurt_id = yurt_id

    def __str__(self):
        return f"{self.ogrenci_no} - {self.basvuru_tarihi} - {self.basvuru_durumu} - {self.yurt_id}"

class Yurt:
    def __init__(self, yurt_id, yurt_adi, toplam_kontenjan, dolu_kontenjan):
        self.yurt_id = yurt_id
        self.yurt_adi = yurt_adi
        self.toplam_kontenjan = toplam_kontenjan
        self.dolu_kontenjan = dolu_kontenjan

class DosyaIslemleri:
    def __init__(self, kullanicilar_dosyasi="kullanicilar.txt", basvurular_dosyasi="basvurular.txt", yurtlar_dosyasi="yurtlar.txt"):
        self.kullanicilar_dosyasi = kullanicilar_dosyasi
        self.basvurular_dosyasi = basvurular_dosyasi
        self.yurtlar_dosyasi = yurtlar_dosyasi

    def kullanicilari_oku(self):
        kullanicilar = []
        if not os.path.exists(self.kullanicilar_dosyasi):
            return kullanicilar
        with open(self.kullanicilar_dosyasi, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(";")
                if len(parts) == 4:
                    k = Kullanici(parts[0], parts[1], parts[2], parts[3])
                    kullanicilar.append(k)
        return kullanicilar

    def basvurulari_oku(self):
        basvurular = []
        if not os.path.exists(self.basvurular_dosyasi):
            return basvurular
        with open(self.basvurular_dosyasi, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(";")
                if len(parts) == 4:
                    b = Basvuru(parts[0], parts[1], parts[2], parts[3])
                    basvurular.append(b)
        return basvurular

    def basvurulari_yaz(self, basvurular):
        with open(self.basvurular_dosyasi, "w", encoding="utf-8") as f:
            for b in basvurular:
                f.write(f"{b.ogrenci_no};{b.basvuru_tarihi};{b.basvuru_durumu};{b.yurt_id}\n")

    def yurtlari_oku(self):
        yurtlar = []
        if not os.path.exists(self.yurtlar_dosyasi):
            return yurtlar
        with open(self.yurtlar_dosyasi, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(";")
                if len(parts) == 4:
                    yurt_id = parts[0]
                    yurt_adi = parts[1]
                    toplam = int(parts[2])
                    dolu = int(parts[3])
                    y = Yurt(yurt_id, yurt_adi, toplam, dolu)
                    yurtlar.append(y)
        return yurtlar

    def yurtlari_yaz(self, yurtlar):
        with open(self.yurtlar_dosyasi, "w", encoding="utf-8") as f:
            for y in yurtlar:
                f.write(f"{y.yurt_id};{y.yurt_adi};{y.toplam_kontenjan};{y.dolu_kontenjan}\n")

    def yurt_kontenjani_artir(self, yurt_id):
        yurtlar = self.yurtlari_oku()
        for y in yurtlar:
            if y.yurt_id == yurt_id:
                y.dolu_kontenjan += 1
                break
        self.yurtlari_yaz(yurtlar)

    def yurt_kontenjani_guncelle(self, yurt_id, yeni_toplam, yeni_dolu):
        yurtlar = self.yurtlari_oku()
        bulundu = False
        for y in yurtlar:
            if y.yurt_id == yurt_id:
                y.toplam_kontenjan = yeni_toplam
                y.dolu_kontenjan = yeni_dolu
                bulundu = True
                break
        if bulundu:
            self.yurtlari_yaz(yurtlar)
            return True
        return False

class GirisIslemleri:
    def __init__(self, dosya_islemleri):
        self.dosya_islemleri = dosya_islemleri

    def kullanici_dogrula(self, kullanici_adi, parola):
        kullanicilar = self.dosya_islemleri.kullanicilari_oku()
        for k in kullanicilar:
            if k.kullanici_adi == kullanici_adi and k.parola == parola:
                return k
        return None

class PersonelIslemleri:
    def __init__(self, dosya_islemleri):
        self.dosya_islemleri = dosya_islemleri

    def basvurulari_listele(self):
        basvurular = self.dosya_islemleri.basvurulari_oku()
        bekleyenler = [b for b in basvurular if b.basvuru_durumu == "beklemede"]
        if not bekleyenler:
            print("Beklemede başvuru yok.")
        else:
            for b in bekleyenler:
                print(b)

    def basvuru_onayla(self, ogrenci_no):
        basvurular = self.dosya_islemleri.basvurulari_oku()
        for basvuru in basvurular:
            if basvuru.ogrenci_no == ogrenci_no and basvuru.basvuru_durumu == "beklemede":
                basvuru.basvuru_durumu = "onaylandı"
                self.dosya_islemleri.yurt_kontenjani_artir(basvuru.yurt_id)
                self.dosya_islemleri.basvurulari_yaz(basvurular)
                print(f"{ogrenci_no} nolu başvuru onaylandı.")
                return
        print("Onaylanacak uygun başvuru bulunamadı.")

    def basvuru_reddet(self, ogrenci_no):
        basvurular = self.dosya_islemleri.basvurulari_oku()
        for basvuru in basvurular:
            if basvuru.ogrenci_no == ogrenci_no and basvuru.basvuru_durumu == "beklemede":
                basvuru.basvuru_durumu = "reddedildi"
                self.dosya_islemleri.basvurulari_yaz(basvurular)
                print(f"{ogrenci_no} nolu başvuru reddedildi.")
                return
        print("Reddedilecek uygun başvuru bulunamadı.")

    def yurtlari_goster(self):
        yurtlar = self.dosya_islemleri.yurtlari_oku()
        if not yurtlar:
            print("Yurt bilgisi bulunamadı.")
        else:
            for y in yurtlar:
                print(f"Yurt ID: {y.yurt_id}, Adı: {y.yurt_adi}, Toplam: {y.toplam_kontenjan}, Dolu: {y.dolu_kontenjan}")

    def yurt_kontenjani_guncelle(self):
        yurt_id = input("Güncellenecek Yurt ID: ")
        try:
            yeni_toplam = int(input("Yeni Toplam Kontenjan: "))
            yeni_dolu = int(input("Yeni Dolu Kontenjan: "))
        except ValueError:
            print("Lütfen sayı giriniz.")
            return

        if yeni_dolu > yeni_toplam:
            print("Dolu kontenjan, toplam kontenjandan fazla olamaz.")
            return

        basarili = self.dosya_islemleri.yurt_kontenjani_guncelle(yurt_id, yeni_toplam, yeni_dolu)
        if basarili:
            print(f"{yurt_id} yurdunun kontenjanı güncellendi.")
        else:
            print(f"{yurt_id} ID'li yurt bulunamadı.")

class OgrenciIslemleri:
    def __init__(self, dosya_islemleri, ogrenci_no):
        self.dosya_islemleri = dosya_islemleri
        self.ogrenci_no = ogrenci_no

    def basvuru_yap(self, yurt_id):
        basvurular = self.dosya_islemleri.basvurulari_oku()
        today = date.today().isoformat()
        yeni_basvuru = Basvuru(self.ogrenci_no, today, "beklemede", yurt_id)
        basvurular.append(yeni_basvuru)
        self.dosya_islemleri.basvurulari_yaz(basvurular)
        print("Başvuru yapıldı.")

    def basvuru_durumunu_goruntule(self):
        basvurular = self.dosya_islemleri.basvurulari_oku()
        ogrenci_basvurular = [b for b in basvurular if b.ogrenci_no == self.ogrenci_no]
        if not ogrenci_basvurular:
            print("Herhangi bir başvurunuz yok.")
        else:
            for b in ogrenci_basvurular:
                print(f"Yurt: {b.yurt_id}, Durum: {b.basvuru_durumu}")

if __name__ == "__main__":
    dosya = DosyaIslemleri()
    giris = GirisIslemleri(dosya)

    
    kullanici_adi = input("Kullanıcı adı: ")
    parola = input("Parola: ")

    k = giris.kullanici_dogrula(kullanici_adi, parola)
    if k is None:
        print("Giriş başarısız. Bilgilerinizi kontrol edin.")
    else:
        print(f"Hoşgeldiniz {k.kullanici_adi}, Tip: {k.tip}")
        if k.tip == "öğrenci":
            
            ogrenci_islem = OgrenciIslemleri(dosya, k.kimlik)
            while True:
                print("\n[1] Başvuru Yap\n[2] Başvuru Durumunu Gör\n[3] Çıkış")
                secim = input("Seçiminiz: ")
                if secim == "1":
                    yurt_id = input("Yurt ID giriniz: ")
                    ogrenci_islem.basvuru_yap(yurt_id)
                elif secim == "2":
                    ogrenci_islem.basvuru_durumunu_goruntule()
                elif secim == "3":
                    print("Çıkış yapılıyor...")
                    break
                else:
                    print("Geçersiz seçim.")

        elif k.tip == "personel":
            
            pers = PersonelIslemleri(dosya)
            while True:
                print("\n[1] Başvuruları Listele\n[2] Başvuru Onayla\n[3] Başvuru Reddet\n[4] Yurt Kontenjanlarını Göster\n[5] Yurt Kontenjanını Güncelle\n[6] Çıkış")
                secim = input("Seçiminiz: ")
                if secim == "1":
                    pers.basvurulari_listele()
                elif secim == "2":
                    ogr_no = input("Onaylanacak öğrenci no: ")
                    pers.basvuru_onayla(ogr_no)
                elif secim == "3":
                    ogr_no = input("Reddedilecek öğrenci no: ")
                    pers.basvuru_reddet(ogr_no)
                elif secim == "4":
                    pers.yurtlari_goster()
                elif secim == "5":
                    pers.yurt_kontenjani_guncelle()
                elif secim == "6":
                    print("Çıkış yapılıyor...")
                    break
                else:
                    print("Geçersiz seçim.")
