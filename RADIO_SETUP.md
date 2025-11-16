# Hafif Ayaklar Radyo Özelliği - Kurulum Rehberi

## Genel Bakış

Hafif Ayaklar radyosu, DJ'lerin canlı yayın yapabildiği ve kullanıcıların bu yayınları dinleyebildiği bir özelliktir. **Agora.io** altyapısı kullanılarak browser-based (tarayıcı tabanlı) olarak çalışır - **hiçbir yazılım kurulumuna gerek yoktur**.

### Özellikler

✅ Browser-based canlı yayın (DJ'ler için yazılım kurulumu gerekmez)
✅ Mikrofon desteği (DJ konuşabilir + PC'den müzik çalabilir)
✅ Sınırsız DJ sayısı (admin tarafından yetkilendirilir)
✅ Tamamen esnek program zamanlaması
✅ Çakışma kontrolü (aynı anda 2 program olamaz)
✅ Gerçek zamanlı dinleyici sayısı
✅ Admin panel entegrasyonu

---

## 1. Agora.io Hesabı Oluşturma

### Adım 1: Hesap Aç
1. [https://console.agora.io/](https://console.agora.io/) adresine gidin
2. **Sign Up** butonuna tıklayın
3. Email ile kayıt olun veya Google/GitHub ile giriş yapın

### Adım 2: Yeni Proje Oluştur
1. Dashboard'a giriş yaptıktan sonra **"Project Management"** sekmesine gidin
2. **"Create"** butonuna tıklayın
3. Proje bilgilerini doldurun:
   - **Project Name**: `Hafif Ayaklar Radio` (veya istediğiniz isim)
   - **Use Case**: `Social` veya `Live Broadcasting` seçin
   - **Authentication mechanism**: **Secured mode: APP ID + Token** SEÇİN (önemli!)

4. **"Submit"** tıklayın

### Adım 3: App ID ve App Certificate Alın
1. Oluşturduğunuz projeye tıklayın
2. **App ID** otomatik görünecektir - kopyalayın
3. **App Certificate** için:
   - Yanındaki **"Generate"** veya **"Enable"** butonuna tıklayın
   - Onaylayın
   - Oluşan **App Certificate**'i kopyalayın

⚠️ **ÖNEMLİ:** App Certificate'i güvenli bir yere kaydedin, bir daha gösterilmeyecek!

---

## 2. Environment Variables Ayarlama

### Development (Geliştirme) Ortamı

`.env` dosyanızı açın (yoksa `.env.example`'dan kopyalayın):

```bash
cp .env.example .env
nano .env
```

Aşağıdaki satırları ekleyin/düzenleyin:

```env
# Agora.io Configuration
AGORA_APP_ID=your_app_id_here
AGORA_APP_CERTIFICATE=your_app_certificate_here
```

**Örnekle:**
```env
AGORA_APP_ID=a1b2c3d4e5f6g7h8i9j0
AGORA_APP_CERTIFICATE=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

### Production (Canlı) Ortamı

Production ortamında environment variables'ı sunucu üzerinde ayarlamalısınız:

**PythonAnywhere:**
1. Web tab → Environment variables bölümüne gidin
2. Ekleyin:
   ```
   AGORA_APP_ID = your_app_id
   AGORA_APP_CERTIFICATE = your_certificate
   ```

**VPS/Dedicated Server:**
```bash
# .env dosyasında veya systemd service dosyasında
Environment="AGORA_APP_ID=your_app_id"
Environment="AGORA_APP_CERTIFICATE=your_certificate"
```

---

## 3. Python Paketlerini Kurma

Agora token generation için gerekli paketi kurun:

```bash
pip install agora-token
```

Tüm gereksinimleri güncellemek için:

```bash
pip freeze > requirements.txt
```

---

## 4. Database Migration

Radyo modelleri için migration çalıştırın:

```bash
python manage.py migrate
```

Bu komut şu modelleri oluşturacak:
- `RadioProgram` - Radyo programları
- `UserProfile.is_dj` - DJ yetkilendirmesi

---

## 5. DJ Yetkilendirme

### Admin Panel Üzerinden

1. Django admin'e giriş yapın: `http://yourdomain.com/admin/`
2. **Core → User profiles** bölümüne gidin
3. DJ yapmak istediğiniz kullanıcının profilini açın
4. **"DJ Yetkisi"** (is_dj) checkbox'ını işaretleyin
5. **Save** tıklayın

### Python Shell Üzerinden

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from core.models import UserProfile

# Kullanıcıyı DJ yap
user = User.objects.get(username='dj_username')
profile = user.userprofile
profile.is_dj = True
profile.save()

print(f"{user.username} artık DJ!")
```

---

## 6. İlk Programı Oluşturma

### DJ Kullanıcı Olarak:

1. Siteye giriş yapın
2. Navbar'daki **Müteferrik** (şemsiye ikonu) menüsüne tıklayın
3. **Radyo** seçin
4. **DJ Paneli** butonuna tıklayın
5. **Yeni Program** butonuna tıklayın
6. Program bilgilerini doldurun:
   - Başlık
   - Açıklama
   - Başlangıç zamanı
   - Bitiş zamanı
7. **Programı Oluştur** tıklayın

### Admin Panel Üzerinden:

1. Admin'e giriş yapın
2. **Core → Radio programs** bölümüne gidin
3. **Add radio program** tıklayın
4. Formu doldurun ve kaydedin

---

## 7. Canlı Yayın Yapma (DJ)

### Yayın Başlatma:

1. **DJ Paneli**'ne gidin
2. Program zamanı geldiğinde **"Yayını Başlat"** butonu aktif olur
3. Butona tıklayın
4. Tarayıcı mikrofon izni isteyecek - **"İzin Ver"** tıklayın
5. Yayın başlar!

### Yayın Sırasında:

- Mikrofonunuz otomatik açık olacak - konuşabilirsiniz
- PC'nizden müzik çalarken tarayıcıda DJ panelinde kalabilirsiniz
- Müzik tarayıcınızdan duyulur (örn: YouTube, Spotify)
- Dinleyici sayısı gerçek zamanlı güncellenir

### Yayını Bitirme:

1. **"Yayını Bitir"** butonuna tıklayın
2. Onaylayın
3. Yayın sonlanır ve program tamamlandı olarak işaretlenir

---

## 8. Canlı Yayın Dinleme (Kullanıcılar)

1. **Radyo** sayfasına gidin (Müteferrik menüsünden)
2. Canlı yayınlar listede **CANLI** badge'i ile görünür
3. **"Dinle"** butonuna tıklayın
4. Program sayfasında **"Dinlemeye Başla"** butonuna tıklayın
5. Ses seviyesini ayarlayın
6. Yayını dinleyin!

---

## 9. Sorun Giderme

### "Agora.io yapılandırması eksik" Hatası

**Sebep:** Environment variables ayarlanmamış.

**Çözüm:**
1. `.env` dosyasını kontrol edin
2. `AGORA_APP_ID` ve `AGORA_APP_CERTIFICATE` doğru girilmiş mi?
3. Sunucuyu yeniden başlatın:
   ```bash
   # Development
   python manage.py runserver

   # Production (Gunicorn)
   sudo systemctl restart hafifayaklar
   ```

### "Agora token paketi kurulu değil" Hatası

**Çözüm:**
```bash
pip install agora-token
```

### Mikrofon İzni Verilmiyor

**Çözüm:**
1. Tarayıcınızın site ayarlarına gidin
2. Mikrofon iznini manuel olarak verin
3. Sayfayı yenileyin

### Ses Duyulmuyor

**DJ için:**
- Mikrofonunuzun doğru seçildiğinden emin olun (tarayıcı ayarları)
- Mikrofon izni verilmiş mi kontrol edin

**Dinleyici için:**
- Ses seviyesi 0'da mı kontrol edin
- **"Dinlemeye Başla"** butonuna tıkladınız mı?
- Tarayıcı ses ayarlarını kontrol edin

### Program Çakışması

**Hata:** "Bu saatlerde başka bir program var"

**Çözüm:**
- Başka bir programla çakışmayacak saat seçin
- Admin panelden mevcut programları kontrol edin

---

## 10. Agora.io Ücretsiz Limitler

Agora.io ücretsiz tier'da şu limitler vardır:

- ✅ **10,000 dakika/ay** ücretsiz
- ✅ Sınırsız kanal sayısı
- ✅ Sınırsız kullanıcı

**Hesaplama örneği:**
- Günde 2 saat yayın = 60 saat/ay = 3,600 dakika/ay → **ÜCRETSİZ**
- Günde 5 saat yayın = 150 saat/ay = 9,000 dakika/ay → **ÜCRETSİZ**

10,000 dakikayı aşarsanız ücretlendirme başlar:
- ~$0.99 / 1000 dakika (bölgeye göre değişir)

---

## 11. Güvenlik Notları

✅ **App Certificate GİZLİ tutulmalıdır** - asla public repo'lara commit etmeyin
✅ Token'lar server-side oluşturulur (client'a App Certificate açılmaz)
✅ Her token süresi sınırlıdır (DJ: 6 saat, Dinleyici: 3 saat)
✅ `.env` dosyası `.gitignore`'da olmalı

---

## 12. Destek ve Dokümantasyon

- **Agora.io Docs:** https://docs.agora.io/
- **Python SDK:** https://github.com/AgoraIO-Community/agora-token-service-python
- **Hafif Ayaklar Issues:** [GitHub Issues](https://github.com/yourusername/hafif_ayaklar/issues)

---

## Özet Checklist

- [ ] Agora.io hesabı oluşturuldu
- [ ] App ID ve App Certificate alındı
- [ ] `.env` dosyasına eklendi
- [ ] `pip install agora-token` çalıştırıldı
- [ ] `python manage.py migrate` çalıştırıldı
- [ ] En az 1 kullanıcı DJ yapıldı
- [ ] İlk program oluşturuldu
- [ ] Test yayını yapıldı
- [ ] Dinleyici olarak test edildi

✅ Kurulum tamamlandı! Artık radyo özelliğini kullanabilirsiniz.

---

**Sorularınız için:** GitHub Issues veya proje ekibiyle iletişime geçin.
