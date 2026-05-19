# Penaltı Oyunu AI Günlüğü

Bu dosya, projede yapılan geliştirmelerin yapay zeka ile nasıl ilerlediğini takip etmek için kullanılacaktır.

## Başlangıç: Proje İskeleti Kurulumu
- Application Factory pattern kullanılarak Flask 3.x yapısı oluşturuldu.
- Blueprintler tanımlandı (main, auth).
- Gereksinimler (requirements.txt) belirlendi.


Sanal ortamı aktif ederken PowerShell Execution Policy (Yetki) hatası aldım. Terminalde Set-ExecutionPolicy Unrestricted -Scope Process komutunu çalıştırarak yetki sorununu çözdüm.

### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Veritabanı modelleri için planı onayladıktan sonra terminalde `flask db init` komutunu çalıştırdığımda `Error: No such command 'db'.` hatası ile karşılaştım.
- **Çözüm:** Hatanın nedenini araştırdığımızda, ilk iskelet kurulumunda oluşturduğumuz `app/__init__.py` ve `config.py` dosyalarının henüz boş olduğunu, dolayısıyla `Flask-SQLAlchemy` ve `Flask-Migrate` eklentilerinin ana uygulamaya (`create_app` içine) bağlanmadığını tespit ettim. Proje kılavuzundaki "Hata mesajıyla yardım" stratejisini kullanarak ajana hatayı ve hedefimi belirten bir prompt verdim. Ajan, `config.py` içine veritabanı yolunu (`SQLALCHEMY_DATABASE_URI`) ekledi ve `app/__init__.py` dosyasını güncelleyerek eklentileri (`db.init_app(app)`) uygulamaya dahil etti. Modellerin içeri aktarılmasını da sağladıktan sonra migrasyon komutları (`init`, `migrate`, `upgrade`) sorunsuz bir şekilde çalıştı.
- **Hata:** Kayıt formunu gönderirken `500 Internal Server Error` aldım. Terminal loglarını incelediğimde `No module named 'email_validator'` hatasını tespit ettim.
- **Çözüm:** Terminalden `pip install email-validator` komutuyla paketi kurup `requirements.txt` dosyasını güncelleyerek sorunu başarıyla çözdüm.

## Oturum 4 - 17 Mayıs 2026
### Hedef
Pen12'nin temel oyun mekaniğini (12 bölgeli kale arayüzü ve backend olasılık hesaplamaları) oluşturmak.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *[Buraya verdiğimiz oyun mekaniği promptunu yapıştır]*

### Ajanın Önerdiği Plan
Ajanın planını incelediğimde, şut atma işlemini klasik bir form POST işlemi yerine **AJAX (Fetch API)** kullanarak yapmayı önerdiğini gördüm. Bu, her şutta sayfanın yenilenmesini engelleyerek modern ve akıcı bir oyun deneyimi sunacağı için bu inisiyatifi çok başarılı buldum ve planı olduğu gibi onayladım. Ayrıca UTC bazlı günlük oyun (`Game`) kontrolü veritabanı yığılmasını önlemek için çok mantıklıydı.
*[Buraya ajanın AJAX kullanmayı önerdiği 'Important' kısmının ekran görüntüsünü "docs/img/oturum-4-ajax-onerisi.png" olarak ekle]*

### Üretilen Kodda Düzelttiklerim
Ajanın ürettiği şablon ve rotalar sorunsuz çalıştı, manuel bir müdahaleye gerek kalmadı.

### Karşılaştığım Hatalar ve Çözümler
Uygulama planlandığı gibi tek seferde hatasız çalıştı.

### Bu Oturumdan Öğrendiğim
Backend (Python/Flask) ile Frontend (JavaScript) arasında asenkron veri iletişiminin (AJAX) nasıl kurulduğunu ve sayfa yenilenmeden dinamik olarak DOM manipülasyonu yapmanın kullanıcı deneyimini (UX) ne kadar artırdığını uygulamalı olarak öğrendim.