# 🤓 digiCFO - Finansal Analiz Platformu

Modern, modüler ve kullanıcı dostu bir finansal analiz ve raporlama platformu.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Modüller](#modüller)
- [Geliştirme](#geliştirme)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## ✨ Özellikler

### 📊 Finansal Analiz
- **Gelir Tablosu Analizi**: Detaylı gelir ve gider analizi
- **Bilanço Analizi**: Aktif ve pasif kalemlerinin analizi
- **Nakit Akış Analizi**: İşletme, yatırım ve finansman faaliyetleri
- **Finansal Rasyolar**: Kapsamlı finansal oran hesaplamaları
- **Büyük Veri Motoru**: Tüm finansal verilerin tek havuzda toplanması

### 🏢 Sektör Analizi
- BIST firmaları ile karşılaştırma
- Sektör ortalamaları
- Piyasa değeri ve çarpan analizi (F/K, FD/FAVÖK, FD/Satışlar, PD/DD)

### 📈 Raporlama
- Excel export (çoklu sayfa desteği)
- PDF rapor oluşturma
- HTML raporlar
- Sankey diyagramları ile görselleştirme

### 🔒 Güvenlik
- Kullanıcı kimlik doğrulama
- Güvenli şifre yönetimi
- Session state yönetimi

### 📥 Veri Girişi
- Excel dosyası desteği
- CSV dosyası desteği
- PDF dosyası okuma
- Mapping wizard ile esnek veri eşleştirme

### 🎯 TMS/UFRS Uyumluluk
- Türkiye Muhasebe Standartları (TMS) kontrolü
- Uluslararası Finansal Raporlama Standartları (UFRS/IFRS) kontrolü
- Otomatik uyumluluk raporu

## 🚀 Kurulum

### 🌐 Streamlit Cloud (Önerilen - Ücretsiz)

**Canlı Demo:** [Streamlit Cloud'da Çalıştır](https://streamlit.io/cloud)

1. **Streamlit Cloud'a gidin:** https://streamlit.io/cloud
2. **GitHub hesabınızla giriş yapın**
3. **"New app" → Repository:** `ErmanDincel/Erman1`
4. **Main file:** `app1.py`
5. **Deploy!**

**Environment Variables (Streamlit Cloud Secrets):**
```toml
SUPABASE_DB_URL = "postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres"
DB_ENABLED = "true"
OPENAI_API_KEY = "[YOUR_API_KEY]"
```

### 💻 Lokal Kurulum

#### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

#### Adımlar

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/ErmanDincel/Erman1.git
cd Erman1
```

2. **Gerekli kütüphaneleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Yapılandırma dosyasını oluşturun:**

`config.py` dosyasını oluşturun veya `.streamlit/secrets.toml` dosyasını yapılandırın:

```python
# config.py
DEMO_USERNAME = "your_username"
DEMO_PASSWORD = "your_password"
```

veya

```toml
# .streamlit/secrets.toml
DEMO_USERNAME = "your_username"
DEMO_PASSWORD = "your_password"
```

4. **Uygulamayı çalıştırın:**
```bash
streamlit run app1.py
```

Tarayıcınızda `http://localhost:8501` adresinden erişebilirsiniz.

## 📖 Kullanım

### 1. Giriş Yapma
- Kullanıcı adı ve şifrenizi girin
- Demo hesabı için sistem yöneticinize başvurun

### 2. Veri Yükleme
- Sol menüden veya ana ekrandan dosya yükleme bölümüne gidin
- Excel, CSV veya PDF dosyanızı seçin
- Mapping wizard ile verilerinizi eşleştirin (opsiyonel)

### 3. Firma Bilgileri
- Firma adı, sektör ve diğer bilgileri girin
- BIST firması seçebilir veya manuel giriş yapabilirsiniz

### 4. Analiz
- Ana menüden istediğiniz sekme/sekmelere gidin:
  - **Ham Veri**: Yüklenen ham verileri görüntüleyin
  - **Sektör**: Sektör karşılaştırmaları
  - **Veri Kontrol**: Veri doğrulama ve düzeltme
  - **Gelir Tablosu**: Gelir tablosu analizi
  - **Bilanço**: Bilanço analizi
  - **Nakit Akış**: Nakit akış analizi
  - **Büyük Veri**: Tüm verilerin birleştirilmiş görünümü
  - **Rasyo/Oran Kontrol**: Finansal oran analizi
  - **Rapor**: PDF ve Excel rapor oluşturma
  - **Veri Onayı**: Veri onaylama ekranı

### 5. Rapor İndirme
- Rapor sekmesinden Excel, PDF veya HTML formatında rapor indirin

## 📁 Proje Yapısı

```
digiCFO_Projesi/
├── app1.py                      # Ana uygulama dosyası
├── config.py                    # Güvenlik yapılandırması
├── auth.py                      # Kimlik doğrulama modülü
├── utils.py                     # Yardımcı fonksiyonlar
├── data_loader.py               # Veri yükleme modülü
├── financial_analyzer.py        # Finansal analiz modülü
├── mapping.py                   # Veri eşleştirme modülü
├── mapping_wizard.py            # Mapping wizard UI
├── excel_reader.py              # Gelişmiş Excel okuma
├── tms_ufrs_compliance.py       # TMS/UFRS uyumluluk
├── translation.py               # Finansal tablo çevirileri
├── converters.py                # Finansal tablo converter'ları
├── buyuk_veri_engine.py         # Büyük veri motoru
├── session_manager.py           # Session state yönetimi
├── module_loader.py             # Modül yükleme yardımcıları
├── views/                       # UI modülleri
│   ├── __init__.py
│   ├── dashboard.py             # Ana dashboard
│   ├── upload_view.py           # Dosya yükleme
│   ├── company_info.py          # Firma bilgileri
│   ├── gelir_tablosu.py         # Gelir tablosu görünümü
│   ├── bilanco.py               # Bilanço görünümü
│   ├── nakit_akis.py            # Nakit akış görünümü
│   ├── buyuk_veri.py            # Büyük veri görünümü
│   ├── rasyo_oran.py            # Rasyo/oran görünümü
│   ├── reports.py               # Raporlama görünümü
│   ├── veri_onay.py             # Veri onay görünümü
│   ├── ham_veri.py              # Ham veri görünümü
│   ├── sektor.py                # Sektör görünümü
│   └── ileri_analiz.py          # İleri analiz görünümü
└── BistTumSektorHissesort.xlsx  # BIST sektör verileri
```

## 🔧 Modüller

### Ana Modüller

#### `app1.py`
Ana uygulama dosyası. Streamlit sayfa yapılandırması, yönlendirme mantığı ve modül entegrasyonunu içerir.

#### `auth.py`
Kullanıcı kimlik doğrulama ve yetkilendirme işlemlerini yönetir.

#### `utils.py`
Yardımcı fonksiyonlar:
- Veri formatlama ve temizleme
- Excel, PDF, HTML export
- Türkçe karakter düzeltme
- Sayı formatlama

#### `data_loader.py`
Dış veri kaynaklarından veri çekme:
- BIST verileri (Yahoo Finance)
- TCMB döviz kurları
- TÜİK TÜFE verileri
- Sektör verileri

#### `financial_analyzer.py`
Finansal analiz ve hesaplamalar:
- Rasyo hesaplamaları (ticari ve banka için ayrı)
- Finansal oran analizi
- Cache'li hesaplama fonksiyonları

#### `mapping.py`
Veri standardizasyonu ve eşleştirme fonksiyonları.

#### `converters.py`
Finansal tablo dönüştürücüleri:
- Gelir Tablosu Converter
- Bilanço Converter
- Nakit Akış Tablosu şemaları

#### `translation.py`
Finansal tablo çeviri fonksiyonları (TFRS uyumlu Türkçe çeviri).

#### `buyuk_veri_engine.py`
Büyük veri motoru: Tüm finansal verileri birleştirir ve istatistikler hesaplar.

#### `session_manager.py`
Merkezi session state yönetimi için yardımcı fonksiyonlar.

#### `module_loader.py`
Güvenli modül yükleme ve fallback mekanizmaları.

### View Modülleri

View modülleri Streamlit UI bileşenlerini içerir. Her modül belirli bir ekran/sekme için sorumludur.

## 🛠️ Geliştirme

### Modül Ekleme

1. Yeni modülü uygun dizine ekleyin
2. `app1.py`'de import edin
3. Fallback mekanizması ekleyin (opsiyonel)
4. View modülü ise `views/__init__.py`'ye ekleyin

### Test Etme

```bash
# Syntax kontrolü
python -m py_compile app1.py

# Modül import testi
python test_all_modules.py

# Streamlit test
streamlit run app1.py
```

### Kod Stili

- **Docstring**: Google style veya NumPy style
- **Type Hints**: Mümkün olduğunca ekleyin
- **Error Handling**: Try-except blokları ile güvenli hata yönetimi
- **Fallback**: Modül import hatalarında graceful degradation

## 📝 Dokümantasyon

Detaylı API dokümantasyonu için modül dosyalarının başındaki docstring'lere bakın.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje özel bir projedir. Tüm hakları saklıdır.

## 👥 Geliştiriciler

digiCFO Team

## 📧 İletişim

Sorularınız için sistem yöneticinize başvurun.

---

**Versiyon**: 2.0  
**Son Güncelleme**: 18 Aralık 2025

