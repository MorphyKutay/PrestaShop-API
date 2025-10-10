<?php
/**
 * PrestaShop API Yapılandırması
 * Bu dosyayı kendi ayarlarınıza göre düzenleyin
 */

define('PS_ROOT_DIR', dirname(__FILE__) . '/../'); // PrestaShop kök dizini
define('API_KEY', 'fwfdewrewewrewr'); // API güvenlik anahtarı
define('ALLOWED_IPS', []); // İzin verilen IP adresleri (boş array = herkese açık)

// Veritabanı ayarları (PrestaShop'tan farklı kullanmak isterseniz)
define('DB_SERVER', 'localhost');
define('DB_USER', 'user');
define('DB_PASSWD', 'pass');
define('DB_NAME', '1');
define('DB_PREFIX', 'ps_'); // Veritabanı tablo prefix'i

// API Ayarları
define('API_DEBUG', true); // Debug modu
define('API_CORS_ENABLED', true); // CORS desteği
define('API_RATE_LIMIT', 100); // Dakikada maksimum istek sayısı

