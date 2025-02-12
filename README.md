# Log Backup Firebase

Bu script, Ubuntu sunucunuzdaki log dosyalarını otomatik olarak yedekleyip Firebase Storage'a yükler.

## Özellikler

- Log dosyalarını günlük olarak tar.gz formatında arşivler
- Arşivi Firebase Storage'a yükler
- Yükleme başarılı olduktan sonra yerel arşiv dosyasını temizler
- Cron ile otomatik çalışma desteği
- Hata durumlarında bilgilendirme

## Gereksinimler

- Python 3.6 veya üzeri
- Firebase projesi ve Firebase Admin SDK
- Firebase Storage bucket'ı
- Ubuntu Server

## Kurulum Adımları

1. Gerekli Python paketlerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Firebase Console'dan yeni bir proje oluşturun (veya mevcut projenizi kullanın):
   - https://console.firebase.google.com adresine gidin
   - Yeni proje oluşturun veya mevcut projenizi seçin
   - "Project Settings" > "Service accounts" bölümüne gidin
   - "Generate New Private Key" butonuna tıklayın
   - İndirilen JSON dosyasını güvenli bir yere kaydedin

3. `.env` dosyası oluşturun:
   ```bash
   FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase-credentials.json
   FIREBASE_BUCKET_NAME=your-project-id.appspot.com
   LOG_DIRECTORY=/var/log  # veya başka bir log dizini
   ```

4. Scripti test edin:
   ```bash
   python backup_logs.py
   ```

## Cron Job Kurulumu

1. Crontab'ı düzenleyin:
   ```bash
   crontab -e
   ```

2. Her gün saat 19:00'da çalışacak şekilde ayarlayın:
   ```bash
   0 19 * * * cd /path/to/script/directory && /usr/bin/python3 backup_logs.py >> /var/log/backup_logs.log 2>&1
   ```

## Güvenlik Önerileri

- Firebase credentials dosyasını güvenli bir yerde saklayın ve yetkilendirmesini sınırlayın
- `.env` dosyasına sadece root kullanıcısının erişimi olduğundan emin olun
- Düzenli olarak Firebase Storage'daki yedekleri kontrol edin
- Eski yedekleri temizlemek için bir retention policy oluşturun

## Hata Ayıklama

Script çalışmazsa şu adımları kontrol edin:

1. Python versiyonunun uyumlu olduğundan emin olun:
   ```bash
   python3 --version
   ```

2. Gerekli paketlerin yüklü olduğunu kontrol edin:
   ```bash
   pip list | grep firebase-admin
   pip list | grep python-dotenv
   ```

3. `.env` dosyasındaki yolların ve değerlerin doğru olduğunu kontrol edin

4. Log dosyasını kontrol edin:
   ```bash
   tail -f /var/log/backup_logs.log
   ```

## Log Yapısı

Firebase Storage'da loglar şu yapıda saklanır:
```
logs_backup/
  └── YYYY-MM-DD/
      └── logs_backup_YYYYMMDD_HHMMSS.tar.gz
```

## İletişim

Herhangi bir sorun veya öneriniz için issue açabilirsiniz. 