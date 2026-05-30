# Penaltı Oyunu AI Günlüğü

Bu dosya, projede yapılan geliştirmelerin yapay zeka ile nasıl ilerlediğini takip etmek için kullanılacaktır.

## Başlangıç: Proje İskeleti Kurulumu
- Application Factory pattern kullanılarak Flask 3.x yapısı oluşturuldu.
- Blueprintler tanımlandı (main, auth).
- Gereksinimler (requirements.txt) belirlendi.

Sanal ortamı aktif ederken PowerShell Execution Policy (Yetki) hatası aldım. Terminalde `Set-ExecutionPolicy Unrestricted -Scope Process` komutunu çalıştırarak yetki sorununu çözdüm.

---

## Oturum 1 - 11 Mayıs 2026
### Hedef
Application Factory pattern kullanılarak Flask 3.x iskeletinin oluşturulması, Blueprintlerin (main, auth) tanımlanması ve veritabanı bağlantısının kurulması.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *Bağlam: internek programclıgı dersim için Pen12 adında bir penaltı oyunu yapıyorum. Hedef: Application Factory yapısına uygun, 'main' ve 'auth' blueprintlerini içeren boş bir Flask proje iskeleti oluşturmak ve SQLAlchemy/Flask-Migrate entegrasyonunu sağlamak.*

### Ajanın Önerdiği Plan
Ajan, kodları tek bir `app.py` dosyasına yığmak yerine, kurumsal projelerde kullanılan modüler "Application Factory" (`create_app`) yapısını kurmayı önerdi. Bu sayede projenin ileride büyümesi durumunda yönetilmesi çok daha kolay olacaktı. Planı onayladım.

### Üretilen Kodda Düzelttiklerim
Sanal ortamı aktif ederken PowerShell Execution Policy (Yetki) hatası aldım. Terminalde `Set-ExecutionPolicy Unrestricted -Scope Process` komutunu manuel olarak çalıştırarak işletim sistemi seviyesindeki yetki sorununu çözdüm.

### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Veritabanı modelleri için planı onayladıktan sonra terminalde `flask db init` komutunu çalıştırdığımda `Error: No such command 'db'.` hatası ile karşılaştım.
- **Çözüm:** Hatanın nedenini araştırdığımızda, ilk iskelet kurulumunda oluşturduğumuz `app/__init__.py` ve `config.py` dosyalarının henüz boş olduğunu, dolayısıyla `Flask-SQLAlchemy` ve `Flask-Migrate` eklentilerinin ana uygulamaya (`create_app` içine) bağlanmadığını tespit ettim. Proje kılavuzundaki "Hata mesajıyla yardım" stratejisini kullanarak ajana hatayı ve hedefimi belirten bir prompt verdim. Ajan, `config.py` içine veritabanı yolunu (`SQLALCHEMY_DATABASE_URI`) ekledi ve `app/__init__.py` dosyasını güncelleyerek eklentileri (`db.init_app(app)`) uygulamaya dahil etti. Modellerin içeri aktarılmasını da sağladıktan sonra migrasyon komutları (`init`, `migrate`, `upgrade`) sorunsuz bir şekilde çalıştı.

### Bu Oturumdan Öğrendiğim
Büyük çaplı web projelerinde dosya hiyerarşisinin (Application Factory) önemini ve ORM (SQLAlchemy) araçlarının Flask uygulamasına nasıl entegre (init_app) edildiğini öğrendim. Ayrıca PowerShell yetkilendirme kısıtlamalarına müdahale etmeyi tecrübe ettim.

---

## Oturum 2 - 13 Mayıs 2026
### Hedef
Kullanıcıların oyuna girebilmesi için güvenli Kayıt (Register) ve Giriş (Login) sistemlerini (Auth Blueprint) kodlamak ve şifreleme mantığını kurmak.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *Bağlam: Pen12 oyunu iskeletimiz hazır. Hedef: Flask-Login ve Werkzeug kullanarak kullanıcı kayıt ve giriş sistemini oluştur. Şifreler veritabanına düz metin olarak kaydedilmemeli.*

### Ajanın Önerdiği Plan
Ajan, güvenlik zafiyeti (CWE-256) oluşturmamak için kullanıcı şifrelerini `Werkzeug.security` modülündeki `generate_password_hash` fonksiyonu ile pbkdf2:sha256 algoritmasını kullanarak şifrelemeyi planladı. Oturum (session) yönetimi için ise cookie tabanlı `Flask-Login` kütüphanesini projeye dahil etti. Güvenlik standartlarına uygun olduğu için planı onayladım.

### Üretilen Kodda Düzelttiklerim
Sistem sorunsuz çalıştı, manuel kod müdahalesine gerek kalmadı. Sadece test için sahte kullanıcılar oluşturdum.

### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Kayıt formunu test ederken bilgileri gönderdiğimde `500 Internal Server Error` aldım. Terminal loglarını incelediğimde `No module named 'email_validator'` hatasını tespit ettim.
- **Çözüm:** Form doğrulama aracı olan Flask-WTF'in e-posta formatını kontrol etmek için bu arka plan paketine ihtiyaç duyduğunu anladım. Terminalden `pip install email-validator` komutuyla paketi kurup `requirements.txt` dosyasını güncelleyerek sorunu başarıyla çözdüm.

### Bu Oturumdan Öğrendiğim
Kullanıcı parolalarının veritabanında kesinlikle düz metin (plain text) olarak saklanmaması gerektiğini, kriptografik hash fonksiyonlarının ve tuzlama (salting) işlemlerinin veri ihlallerine karşı nasıl koruma sağladığını pratik olarak gördüm.

---

## Oturum 3 - 15 Mayıs 2026
### Hedef
Temel arayüz şablonlarının (base.html) oluşturulması, Navbar (Gezinme Çubuğu) entegrasyonu ve oturum durumuna göre menülerin dinamikleşmesi.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *Bağlam: Kayıt ve giriş sistemimiz çalışıyor. Hedef: Tüm sayfalarda kullanılacak bir base.html (Ana şablon) oluştur. Navbar ekle ve Jinja2 kullanarak kullanıcı giriş yapmışsa menüde adını ve 'Çıkış Yap' butonunu göster, giriş yapmamışsa 'Kayıt Ol' ve 'Giriş Yap' görünsün.*

### Ajanın Önerdiği Plan
Ajan, tekrar eden HTML kodlarını engellemek için Jinja2 template motorunun `{% block content %}` kalıtım (inheritance) yapısını kullandı. Navbar için de Bootstrap 5 kütüphanesini projeye CDN üzerinden dahil etti.

### Üretilen Kodda Düzelttiklerim
Başlangıçta ajanın eklediği Navbar açık renkli (light) bir temadaydı. Penaltı oyununun ilerideki karanlık stadyum temasına uygun olması için Bootstrap class'larını `navbar-dark bg-dark` olarak manuel olarak güncelledim.

### Karşılaştığım Hatalar ve Çözümler
Ciddi bir hata ile karşılaşmadım. Ancak Flask rotalarını (endpoint) yazarken `url_for` kullanımında blueprint isimlerini dahil etmeyi (`url_for('auth.login')` gibi) unuttuğum bir an oldu. Ajanın uyarılarıyla bu rotalama sorununu çözdüm.

### Bu Oturumdan Öğrendiğim
Jinja2 ile HTML dosyaları içerisinde if/else gibi programlama mantıklarını nasıl çalıştıracağımı (`{% if current_user.is_authenticated %}`) ve şablon kalıtımı sayesinde spagetti kod yazmaktan nasıl kurtulacağımı öğrendim.

---

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

---

## Oturum 5 - 19 Mayıs 2026
### Hedef
Kullanıcı istatistiklerini (Profil) ve rekabet ortamını (Liderlik Tablosu) oluşturacak veritabanı sorgularını ve arayüzleri yazmak.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *[Buraya liderlik tablosu ve profil için verdiğimiz promptu yapıştır]*

### Ajanın Önerdiği Plan
Ajanın planında en çok dikkatimi çeken nokta veritabanı optimizasyonuydu. Kullanıcıların oyunlarını ve şutlarını çekerken oluşabilecek N+1 sorgu problemini engellemek için SQLAlchemy'nin `joinedload` özelliğini kullandı. Bu sayede veriler tek seferde çekilerek uygulamanın performansı artırıldı. Ayrıca sıfıra bölünme hatası (ZeroDivisionError) ihtimaline karşı hesaplamaları backend'de güvene aldı.
*[Buraya ajanın routes.py için `joinedload` önerdiği kısmın ekran görüntüsünü "docs/img/oturum-5-joinedload.png" olarak ekle]*

### Üretilen Kodda Düzelttiklerim
Ajanın yazdığı sorgular ve Bootstrap şablonları sorunsuz çalıştığı için ekstra bir düzeltme yapmadım.

### Karşılaştığım Hatalar ve Çözümler
Sorun yaşamadım, veriler anlık olarak doğru yansıdı.

### Bu Oturumdan Öğrendiğim
Veritabanı ilişkilerinde (One-to-Many vb.) tabloları birleştirirken performans sorunları yaşamamak için `joinedload` gibi eager loading (istek anında yükleme) yöntemlerinin ne kadar kritik olduğunu öğrendim. Ayrıca karmaşık verileri Bootstrap "Card" ve "Table" bileşenleriyle kullanıcıya sunmanın arayüzü nasıl profesyonelleştirdiğini gördüm.

---

## Oturum 6 - 21 Mayıs 2026
### Hedef
Kullanıcı giriş sayfasına "Şifremi Unuttum" özelliği eklemek ve güvenli bir e-posta sıfırlama sistemi (Şifre yenileme linki gönderimi) kurmak.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *Bağlam: Pen12 oyununun kullanıcı giriş (login) sayfasına "Şifremi Unuttum" (Forgot Password) özelliği eklemek istiyoruz. Hedef: Kullanıcının e-posta adresine güvenli bir şifre sıfırlama bağlantısı gönderen, e-posta tabanlı bir şifre sıfırlama sistemi kurmak. Adımlar: UI Güncellemesi, Yeni Şablonlar, Formlar, Güvenli Token (Backend), Rotalar ve E-posta Gönderimi. smtplib kullanarak uygula.*

### Ajanın Önerdiği Plan
Ajan, projeye `Flask-Mail` gibi ekstra harici bağımlılıklar yüklemek yerine Python'un standart kütüphanesi olan `smtplib` kullanmayı önerdi. Bununla birlikte şifre sıfırlama linklerinin güvenliğini sağlamak için `itsdangerous` modülü ile süreli (30 dakika geçerli) ve şifreli token mimarisi planladı. Siber güvenlik açısından projenin hafif kalmasını sağlarken güvenlik standartlarını en üstte tuttuğu için bu planı doğrudan onayladım.

### Üretilen Kodda Düzelttiklerim
Ajanın oluşturduğu `.env` dosyasına kendi kişisel Gmail şifrem yerine, Google güvenlik ayarlarından projeye özel oluşturduğum 16 haneli "Uygulama Şifresini" (App Password) manuel olarak girdim.

### Karşılaştığım Hatalar ve Çözümler
Uygulama kodsal olarak hatasız çalıştı ancak mail gönderebilmesi için Flask sunucusunun `.env` dosyasını yeniden okuması gerekiyordu. Ajanın yönlendirmesiyle terminalden `Ctrl+C` yapıp `flask run --debug` ile sunucuyu yeniden başlatarak mail gönderimini sorunsuz hale getirdim.

### Bu Oturumdan Öğrendiğim
Parola sıfırlama sistemlerinde düz linkler yerine `itsdangerous` ile süreli/kriptografik token oluşturmanın (Secure Coding) ne kadar kritik olduğunu öğrendim. Ayrıca üçüncü parti yazılımların Gmail gibi servislere güvenli erişimi için ana şifre yerine "Uygulama Şifreleri" (App Passwords) kullanma mantığını kavradım.

---

## Oturum 7 - 30 Mayıs 2026
### Hedef
Mevcut yavan oyun arayüzünü profesyonel bir 3D stadyum atmosferine dönüştürmek, ekrandaki beyaz boşlukları kapatmak ve karakter (kaleci/şutör) animasyonlarını eklemek.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.5 Flash / Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *Bağlam: Pen12 oyununun backend mantığı çalışıyor ancak görsel tasarım profesyonel seviyeye çıkarılmalı. Hedef: Beyaz alanları yok etmek, neon yeşil (#deff9a) vurgulu karanlık bir stadyum tasarımı kurmak ve karakter özelleştirme eklemek. Saf siyah zemin, stadyum ışıkları, taraftar emojileri ve Scoreboard'u dijital yayın panosu gibi tasarla.*
2. *Düzeltme: Kaleci şut kurtarırken kalenin dışına taşıyor. Kaleci animasyonunun sınırlarını düzelt. translateX değerlerini sınırla, kaleci beyaz direklerin dışına çıkmasın.*

### Ajanın Önerdiği Plan
Ajan, dışarıdan `.jpg/.png` resimleri yükleyip sistemi yormak yerine, karanlık modern bir tema (Theme_4) eşliğinde tamamen CSS gradientleri ve CSS gölgeleri ile stadyum derinliği oluşturmayı önerdi. Ayrıca skoru anında sıfırlamak için frontend'e AJAX tabanlı bir "Yeni Maç" butonu, backend'e ise `/reset_game` rotası eklemeyi planladı.

### Üretilen Kodda Düzelttiklerim
Verdiğim ilk prompt sonucunda CSS sınırları (boundaries) tam çizilmediği için kaleci şut atıldığında ekranın dışına uçuyordu. İkinci bir düzeltme promptu girerek kalecinin atlama (`dive`) animasyonunun sadece kale direkleri arasında kalmasını sağladım.

### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Ajan yoğun CSS kodlarını yazarken "Yapay Zeka Modeli Kullanım Kotası" (AI Credit) dolduğu için işlem yarıda kesildi ve arayüz hatalı/yarım bir görünümde kaldı.
- **Çözüm:** Yeni kotaları beklemek yerine, projenin en son sorunsuz çalışan haline dönmek için `Git` altyapısını kullandım. Terminalde `git restore .` komutunu çalıştırarak o anki bozuk kodları sildim ve projeyi anında stabil haline geri getirdim.

### Bu Oturumdan Öğrendiğim
Görsel tasarımlarda CSS ile 3D perspektif (`transform`, `perspective`) katmayı ve animasyonlarda eksenel sınırlandırmaların (boundary constraints) önemini tecrübe ettim. En büyük kazanımım ise, işler tamamen ters gittiğinde `Git` versiyon kontrol sisteminin hayat kurtaran `git restore .` komutunun gücünü uygulamalı olarak görmek oldu.

---

## Oturum 8 - 30 Mayıs 2026
### Hedef
Kılavuzun 7. maddesinde yer alan zorunlu "Hata Yönetimi Sayfaları" gereksinimini karşılamak; uygulamaya özel 404 (Sayfa Bulunamadı) ve 500 (Sunucu Hatası) hata yakalayıcıları ile tematik arayüzler entegre etmek.

### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager View

### Verdiğim Promptlar
1. *Bağlam: Pen12 oyununda proje gereksinimlerini karşılamak için özel hata sayfaları (Custom Error Pages) oluşturmamız gerekiyor. Sistemde "Theme_4" karanlık stadyum/neon yeşil konsepti hakim. Hedef: Flask blueprint yapısına uygun olarak 404 (Not Found) ve 500 (Internal Server Error) hata yakalayıcılarını (error handlers) ve bu hatalar için özel şablonları oluşturmak.*

### Ajanın Önerdiği Plan
Ajan, hata yakalayıcı fonksiyonları doğrudan ana uygulama nesnesi yerine `auth` veya `main` blueprint'i üzerinden `@main.app_errorhandler` dekoratörüyle kaydetmeyi önerdi. Şablon tarafında ise kod tekrarını önlemek için mevcut `base.html` yapısını genişleterek (inheritance), stadyum konseptine uygun ("Top Taca Çıktı" ve "VAR İncelemesi") tasarımlar hazırlamayı planladı. Mimari bütünlüğü koruduğu için planı onayladım.

### Üretilen Kodda Düzelttiklerim
Ajanın hata yakalama fonksiyonlarında döndürdüğü HTTP durum kodlarını (404 ve 500) kontrol ettim, backend rotalarında herhangi bir sözdizimi hatası olmadığı için koda manuel müdahale gerekmedi.

### Karşılaştığım Hatalar ve Çözümler
Uygulama planlandığı gibi tek seferde çalıştı. Tarayıcı üzerinden `http://127.0.0.1:5000/olmayansayfa` adresine giderek 404 mekanizmasının kararlılığını test ettim ve özel tasarımın sorunsuz yüklendiğini doğruladım.

### Bu Oturumdan Öğrendiğim
Kullanıcı deneyimi ve uygulama güvenliği açısından ham Flask/Python hata sayfalarını (raw stack traces) son kullanıcıya göstermemenin önemini öğrendim. `app_errorhandler` yapısı sayesinde global istisnaların (global exceptions) nasıl merkezi olarak yönetileceğini ve projenin genel temasıyla uyumlu hata sayfaları tasarlamayı tecrübe ettim.