# Log Backup GitHub

Bu script, Ubuntu sunucunuzdaki log dosyalarını otomatik olarak yedekleyip GitHub repository'nize yükler.

## Özellikler

- Log dosyalarını günlük olarak tar.gz formatında arşivler
- Arşivi GitHub repository'nize yükler
- Yükleme başarılı olduktan sonra yerel arşiv dosyasını temizler
- Cron ile otomatik çalışma desteği
- Hata durumlarında bilgilendirme

## Gereksinimler

- Python 3.6 veya üzeri
- GitHub hesabı
- Private GitHub repository
- GitHub Personal Access Token
- Ubuntu Server

## Kurulum Adımları

1. Gerekli Python paketlerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. GitHub'da yeni bir private repository oluşturun

3. GitHub Personal Access Token oluşturun:
   - GitHub.com'da profil ayarlarınıza gidin
   - "Developer settings" > "Personal access tokens" > "Tokens (classic)" bölümüne gidin
   - "Generate new token" butonuna tıklayın
   - Token'a "repo" yetkisi verin
   - Oluşturulan token'ı güvenli bir yere kaydedin

4. `.env` dosyası oluşturun:
   ```bash
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_REPO=your_repository_name
   LOG_DIRECTORY=/var/log  # veya başka bir log dizini
   ```

5. Scripti test edin:
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

- GitHub Personal Access Token'ınızı güvenli bir yerde saklayın
- Repository'nin private olduğundan emin olun
- `.env` dosyasına sadece root kullanıcısının erişimi olduğundan emin olun
- Düzenli olarak GitHub'daki yedekleri kontrol edin
- Repository boyutunu kontrol edin ve gerekirse eski yedekleri temizleyin

## Hata Ayıklama

Script çalışmazsa şu adımları kontrol edin:

1. Python versiyonunun uyumlu olduğundan emin olun:
   ```bash
   python3 --version
   ```

2. Gerekli paketlerin yüklü olduğunu kontrol edin:
   ```bash
   pip list | grep PyGithub
   pip list | grep python-dotenv
   ```

3. `.env` dosyasındaki değerlerin doğru olduğunu kontrol edin

4. Log dosyasını kontrol edin:
   ```bash
   tail -f /var/log/backup_logs.log
   ```

## Log Yapısı

GitHub repository'nizde loglar şu yapıda saklanır:
```
logs_backup/
  └── YYYY-MM-DD/
      └── logs_backup_YYYYMMDD_HHMMSS.tar.gz
```

## İletişim

Herhangi bir sorun veya öneriniz için issue açabilirsiniz. 