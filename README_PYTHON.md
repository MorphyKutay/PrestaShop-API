# PrestaShop Python Tkinter Yönetim Paneli

Modern ve kullanıcı dostu Python Tkinter uygulaması ile PrestaShop ürün ve sipariş yönetimi.

## 📋 Özellikler

### 🛍️ Ürün Yönetimi
- ✅ Ürün listeleme (sayfalama desteği)
- ✅ Ürün arama
- ✅ Ürün detaylarını görüntüleme
- ✅ Yeni ürün ekleme
- ✅ Ürün düzenleme
- ✅ Ürün silme
- ✅ Stok görüntüleme

### 📦 Sipariş Yönetimi
- ✅ Sipariş listeleme
- ✅ Sipariş detaylarını görüntüleme
- ✅ Müşteri bilgilerini görüntüleme
- ✅ Teslimat adresi görüntüleme
- ✅ Sipariş ürünlerini görüntüleme
- ✅ Sipariş durumu güncelleme
- ✅ Sipariş silme

### 🎨 Kullanıcı Arayüzü
- ✅ Modern ve temiz tasarım
- ✅ Kolay kullanım
- ✅ Sağ tık menüleri
- ✅ Çift tıklama ile detay görüntüleme
- ✅ Renkli durum göstergeleri
- ✅ Responsive tasarım

## 🚀 Kurulum

### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Yapılandırma

`config.env` dosyasını düzenleyin:

```env
API_URL=http://localhost/prestashop/api/api.php
API_KEY=your_secret_api_key_here
```

**Önemli:** 
- `API_URL`: PHP API'nizin tam URL'i
- `API_KEY`: `config.php` dosyasındaki API anahtarı ile aynı olmalı

### 3. Uygulamayı Çalıştırın

```bash
python app.py
```

## 📖 Kullanım

### Ana Ekran

Uygulama açıldığında otomatik olarak API bağlantısı test edilir. Bağlantı başarılıysa sol menüden işlemleri yapabilirsiniz.

### Ürün Yönetimi

#### Ürünleri Listeleme
1. Sol menüden "📦 Ürünler" seçin
2. Tüm ürünler tabloda görüntülenir
3. Sayfalama otomatik olarak yapılır

#### Ürün Arama
1. Üst kısımdaki arama kutusuna ürün adı yazın
2. "Ara" butonuna tıklayın

#### Yeni Ürün Ekleme
1. "➕ Yeni Ürün" butonuna tıklayın
2. Formu doldurun:
   - Ürün Adı (zorunlu)
   - Fiyat (zorunlu)
   - Referans
   - EAN13
   - Stok Miktarı
   - Kısa Açıklama
   - Durum (Aktif/Pasif)
3. "Kaydet" butonuna tıklayın

#### Ürün Düzenleme
**Yöntem 1:** Ürüne sağ tıklayın → "✏️ Düzenle"
**Yöntem 2:** Ürün seçip üst menüden düzenleme butonuna tıklayın

#### Ürün Detaylarını Görüntüleme
**Yöntem 1:** Ürüne çift tıklayın
**Yöntem 2:** Ürüne sağ tıklayın → "👁️ Detayları Gör"

#### Ürün Silme
1. Ürüne sağ tıklayın
2. "🗑️ Sil" seçin
3. Onay verin

### Sipariş Yönetimi

#### Siparişleri Listeleme
1. Sol menüden "📋 Siparişler" seçin
2. Tüm siparişler tabloda görüntülenir

#### Sipariş Detaylarını Görüntüleme
**Yöntem 1:** Siparişe çift tıklayın
**Yöntem 2:** Siparişe sağ tıklayın → "👁️ Detayları Gör"

Detay penceresinde 3 sekme bulunur:
- **Genel Bilgiler**: Sipariş özet bilgileri
- **Müşteri Bilgileri**: Müşteri ve adres bilgileri
- **Ürünler**: Siparişteki ürünler

#### Sipariş Durumu Güncelleme
1. Siparişe sağ tıklayın
2. "✏️ Durum Güncelle" seçin
3. Yeni durumu seçin:
   - Ödeme Bekleniyor
   - Ödeme Kabul Edildi
   - Hazırlanıyor
   - Kargoya Verildi
   - Teslim Edildi
   - İptal Edildi
   - İade
4. "Güncelle" butonuna tıklayın

#### Sipariş Silme
1. Siparişe sağ tıklayın
2. "🗑️ Sil" seçin
3. Onay verin

### Ayarlar

Sol menüden "⚙️ Ayarlar" seçerek API bilgilerinizi görüntüleyebilirsiniz.

## 🎨 Ekran Görüntüleri

### Ana Ekran
- Modern tasarım
- Renkli durum göstergeleri
- Kolay navigasyon

### Ürün Listesi
- Tablo görünümü
- Arama özelliği
- Hızlı işlemler

### Sipariş Detayları
- Sekmeli görünüm
- Detaylı bilgiler
- Ürün listesi

## 🔧 Teknik Detaylar

### Dosya Yapısı

```
prestapi/
├── app.py                  # Ana uygulama
├── api_client.py          # API iletişim modülü
├── config.env             # Yapılandırma
├── requirements.txt       # Python bağımlılıkları
└── README_PYTHON.md       # Bu dosya
```

### API İletişimi

Uygulama, PHP API ile REST üzerinden iletişim kurar:

```python
# Örnek kullanım
from api_client import PrestaShopAPIClient

api = PrestaShopAPIClient(
    api_url="http://localhost/prestashop/api/api.php",
    api_key="your_api_key"
)

# Ürünleri getir
result = api.get_products(page=1, limit=50)

# Yeni ürün oluştur
result = api.create_product({
    'name': 'Test Ürün',
    'price': 29.99,
    'active': 1
})
```

### Threading

Tüm API istekleri arka planda thread'lerde çalışır, böylece arayüz donmaz:

```python
def load_products():
    def load():
        # API isteği
        result = api.get_products()
        # UI güncelleme
        
    threading.Thread(target=load, daemon=True).start()
```

## 🛠️ Özelleştirme

### Renkleri Değiştirme

`app.py` dosyasındaki `COLORS` sözlüğünü düzenleyin:

```python
COLORS = {
    'primary': '#2196F3',    # Ana renk
    'success': '#4CAF50',    # Başarı rengi
    'danger': '#f44336',     # Hata rengi
    'warning': '#ff9800',    # Uyarı rengi
    'bg': '#f5f5f5',        # Arkaplan
    'white': '#ffffff',      # Beyaz
    'text': '#333333',       # Metin
}
```

### Yeni Özellik Ekleme

API client'a yeni metod eklemek için `api_client.py` dosyasını düzenleyin:

```python
def custom_method(self, param):
    """Özel metod"""
    return self._make_request('GET', 'resource', params={'param': param})
```

## ❗ Sorun Giderme

### API Bağlantı Hatası

**Sorun:** "API'ye bağlanılamadı" hatası

**Çözüm:**
1. `config.env` dosyasındaki URL'i kontrol edin
2. PHP API'nin çalıştığından emin olun
3. API anahtarının doğru olduğundan emin olun

### Modül Bulunamadı Hatası

**Sorun:** `ModuleNotFoundError: No module named 'requests'`

**Çözüm:**
```bash
pip install -r requirements.txt
```

### SSL Sertifika Hatası

**Sorun:** SSL sertifika doğrulama hatası

**Çözüm:** `api_client.py` dosyasında `verify=False` ekleyin (sadece geliştirme ortamı için):

```python
response = requests.get(url, headers=self.headers, verify=False)
```

### Tkinter Yüklü Değil

**Sorun:** `ModuleNotFoundError: No module named 'tkinter'`

**Çözüm (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Çözüm (macOS):**
Tkinter Python ile birlikte gelir, Python'u yeniden yükleyin.

**Çözüm (Windows):**
Python kurulumu sırasında "tcl/tk" seçeneği işaretli olmalı.

## 🔒 Güvenlik Notları

1. **API Anahtarı**: API anahtarınızı kimseyle paylaşmayın
2. **HTTPS**: Üretim ortamında mutlaka HTTPS kullanın
3. **Güvenlik Duvarı**: API'nize sadece güvenilir IP'lerden erişim verin
4. **Yetkilendirme**: Hassas işlemler için ekstra yetkilendirme ekleyin

## 📝 Yapılacaklar

- [ ] Kategori yönetimi
- [ ] Müşteri yönetimi
- [ ] Toplu ürün işlemleri
- [ ] Excel'e dışa aktarma
- [ ] Grafik ve raporlar
- [ ] Ürün görseli yükleme
- [ ] Gelişmiş filtreleme
- [ ] Dark mode

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## 💡 İpuçları

1. **Hızlı Arama**: Ürün arama özelliğini kullanarak hızlıca ürün bulun
2. **Sağ Tık Menüsü**: Hızlı işlemler için sağ tık menüsünü kullanın
3. **Çift Tıklama**: Detayları hızlıca görüntülemek için çift tıklayın
4. **Klavye Kısayolları**: Enter tuşu ile kaydet, Escape ile iptal
5. **Toplu Seçim**: Gelecek versiyonda çoklu seçim desteği eklenecek

## 📞 Destek

Sorunlarınız için issue açabilirsiniz.

---

**Geliştirici Notu:** Bu uygulama PrestaShop PHP API'si ile birlikte çalışacak şekilde tasarlanmıştır. Önce PHP API'yi kurduğunuzdan emin olun.

