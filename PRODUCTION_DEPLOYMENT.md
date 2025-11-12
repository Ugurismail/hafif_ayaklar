# Production Deployment Checklist

Bu dokümanda Hafif Ayaklar projesini production ortamına deploy etmeden önce yapılması gerekenler listelenmiştir.

## ✅ Tamamlanan Güvenlik İyileştirmeleri

### 1. CSRF Koruması (CRITICAL)
- ✅ `@csrf_exempt` decorator'ı kaldırıldı (iat_result view)
- ✅ CSRF token production ayarları eklendi
- ✅ CSRF_TRUSTED_ORIGINS environment variable ile konfigüre edilebilir hale getirildi

### 2. Environment Variables (.env dosyası)
- ✅ `.env.example` dosyası oluşturuldu
- ✅ SECRET_KEY environment variable'dan okunuyor
- ✅ DEBUG modu environment variable ile kontrol ediliyor
- ✅ ALLOWED_HOSTS environment variable ile konfigüre edilebilir

### 3. Logging Sistemi
- ✅ Kapsamlı logging konfigürasyonu eklendi
- ✅ Rotating file handlers (10MB max, 5 backup)
- ✅ Ayrı error log dosyası
- ✅ Log level environment variable ile ayarlanabilir

### 4. Admin URL Güvenliği
- ✅ Admin URL path environment variable ile değiştirilebilir
- ✅ Default: `/admin/` → Production'da farklı bir path kullanılmalı (örn: `/secret-admin-panel/`)

### 5. Media File Validation
- ✅ Image file validator oluşturuldu
- ✅ File size kontrolü (max 5MB)
- ✅ File extension kontrolü
- ✅ Image dimension kontrolü (max 4000x4000)
- ✅ Maximum upload size settings'e eklendi

### 6. Production Security Settings
- ✅ SSL/HTTPS ayarları DEBUG=False olduğunda otomatik aktif
- ✅ CSRF_COOKIE_SECURE
- ✅ SESSION_COOKIE_SECURE
- ✅ SECURE_SSL_REDIRECT
- ✅ HSTS Headers
- ✅ X-Frame-Options
- ✅ Content-Type nosniff
- ✅ XSS Filter

## 🔧 Production'a Geçmeden Önce Yapılması Gerekenler

### 1. Environment Variables Ayarları

Production sunucusunda bir `.env` dosyası oluşturun (`.env.example` dosyasını baz alarak):

```bash
# 1. Yeni bir SECRET_KEY oluştur
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# 2. .env dosyası oluştur
cp .env.example .env

# 3. .env dosyasını düzenle
nano .env
```

**Kritik ayarlar:**
```env
DJANGO_SECRET_KEY=<yukarıda_oluşturduğunuz_key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ADMIN_URL_PATH=secret-admin-9x8y7z  # Farklı bir path seçin
LOG_LEVEL=WARNING
```

### 2. Database Konfigürasyonu

**PostgreSQL Kurulumu (Önerilen):**
```bash
# PostgreSQL veritabanı oluştur
createdb hafif_ayaklar

# .env dosyasına ekle
DATABASE_URL=postgresql://username:password@localhost:5432/hafif_ayaklar
```

**Migrationları çalıştır:**
```bash
python manage.py migrate
```

### 3. Static Files

```bash
# Static dosyaları topla
python manage.py collectstatic --noinput
```

### 4. Superuser Oluştur

```bash
python manage.py createsuperuser
```

### 5. Paket Güncellemeleri

**Kritik:** Eski paket versiyonlarını güncelleyin:

```bash
# requirements.txt'i güncelle
pip install --upgrade Django  # 4.2.2 → 5.2.8+
pip install --upgrade Pillow  # 10.3.0 → latest
pip install --upgrade python-dotenv  # .env desteği için

# Güncel requirements.txt oluştur
pip freeze > requirements.txt
```

### 6. Logs Dizini İzinleri

```bash
# Logs dizininin yazma izinleri olduğundan emin ol
chmod 755 logs/
```

### 7. Rate Limiting (Opsiyonel ama Önerilen)

Django ratelimit veya django-axes yükleyin:

```bash
pip install django-ratelimit
```

settings.py'ye ekleyin:
```python
MIDDLEWARE = [
    # ... diğer middleware'ler
    'django_ratelimit.middleware.RatelimitMiddleware',
]
```

### 8. Cache Konfigürasyonu (Opsiyonel)

**Redis kurulumu (Önerilen):**
```bash
pip install redis django-redis
```

settings.py'ye ekle:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 9. Email Konfigürasyonu

`.env` dosyasına email ayarlarını ekleyin:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 10. HTTPS Sertifikası

**Let's Encrypt ile ücretsiz SSL:**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 🚀 Deployment Komutları

### PythonAnywhere Deployment

1. **Dosyaları yükle:**
```bash
git clone https://github.com/yourusername/hafif_ayaklar.git
cd hafif_ayaklar
```

2. **Virtual environment:**
```bash
mkvirtualenv --python=/usr/bin/python3.11 hafif_ayaklar
pip install -r requirements.txt
```

3. **.env dosyası oluştur:**
```bash
cp .env.example .env
nano .env  # Ayarları düzenle
```

4. **Database ve static files:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

5. **Web app configuration:**
- Source code: `/home/yourusername/hafif_ayaklar`
- Working directory: `/home/yourusername/hafif_ayaklar`
- WSGI file: Edit to use your project's wsgi.py
- Static files: `/static/` → `/home/yourusername/hafif_ayaklar/staticfiles/`
- Media files: `/media/` → `/home/yourusername/hafif_ayaklar/media/`

### VPS/Dedicated Server Deployment (Nginx + Gunicorn)

1. **Gunicorn kurulumu:**
```bash
pip install gunicorn
```

2. **Gunicorn test:**
```bash
gunicorn hafifayaklar.wsgi:application --bind 0.0.0.0:8000
```

3. **Systemd service oluştur:**
```bash
sudo nano /etc/systemd/system/hafifayaklar.service
```

```ini
[Unit]
Description=Hafif Ayaklar Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/hafif_ayaklar
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:/path/to/hafif_ayaklar.sock hafifayaklar.wsgi:application

[Install]
WantedBy=multi-user.target
```

4. **Nginx konfigürasyonu:**
```bash
sudo nano /etc/nginx/sites-available/hafifayaklar
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /path/to/hafif_ayaklar/staticfiles/;
    }

    location /media/ {
        alias /path/to/hafif_ayaklar/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/hafif_ayaklar.sock;
    }
}
```

5. **Servisleri başlat:**
```bash
sudo systemctl start hafifayaklar
sudo systemctl enable hafifayaklar
sudo systemctl restart nginx
```

## 🔍 Production Checklist

- [ ] `.env` dosyası oluşturuldu ve tüm değerler ayarlandı
- [ ] `DEBUG=False` ayarlandı
- [ ] Yeni `SECRET_KEY` oluşturuldu
- [ ] `ALLOWED_HOSTS` doğru domain'lerle dolduruldu
- [ ] `CSRF_TRUSTED_ORIGINS` HTTPS URL'leriyle dolduruldu
- [ ] Admin URL path değiştirildi
- [ ] PostgreSQL veritabanı kuruldu ve migrate edildi
- [ ] Static files toplandı (`collectstatic`)
- [ ] Media files dizini oluşturuldu ve izinleri ayarlandı
- [ ] Logs dizini oluşturuldu ve yazılabilir
- [ ] HTTPS/SSL sertifikası kuruldu
- [ ] Django ve diğer paketler güncellendi
- [ ] Superuser oluşturuldu
- [ ] Email ayarları yapıldı (password reset için)
- [ ] Backup sistemi kuruldu
- [ ] Monitoring/logging servisi kuruldu (Sentry, Rollbar, vb.)

## 🛡️ Güvenlik Test

Production'a geçtikten sonra:

1. **Django Security Check:**
```bash
python manage.py check --deploy
```

2. **OWASP ZAP veya Burp Suite ile güvenlik testi**

3. **SSL Test:**
https://www.ssllabs.com/ssltest/

4. **Headers Check:**
https://securityheaders.com/

## 📊 Monitoring

**Önerilen araçlar:**
- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **Uptime Robot** - Uptime monitoring
- **Google Analytics** - User analytics

## 🔄 Backup Stratejisi

**Düzenli backup alın:**
```bash
# Database backup
pg_dump hafif_ayaklar > backup_$(date +%Y%m%d).sql

# Media files backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

## 📞 Sorun Giderme

**Hata loglarını kontrol et:**
```bash
# Django logs
tail -f logs/django_errors.log

# Gunicorn logs (systemd)
sudo journalctl -u hafifayaklar -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

## ⚠️ Önemli Notlar

1. **ASLA** production'da `DEBUG=True` kullanmayın
2. **ASLA** default SECRET_KEY kullanmayın
3. **HER ZAMAN** HTTPS kullanın
4. **HER ZAMAN** düzenli backup alın
5. **HER ZAMAN** güncel paket versiyonları kullanın
6. **HER ZAMAN** rate limiting kullanın
7. **HER ZAMAN** error monitoring aktif olsun

---

Sorularınız için: [GitHub Issues](https://github.com/yourusername/hafif_ayaklar/issues)
