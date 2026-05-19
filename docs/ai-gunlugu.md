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