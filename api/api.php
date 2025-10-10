<?php
/**
 * PrestaShop REST API
 * Ürün ve Sipariş Yönetimi için RESTful API
 * 
 * Kullanım:
 * GET    /api.php?resource=products              - Tüm ürünleri listele
 * GET    /api.php?resource=products&id=1         - ID'ye göre ürün getir
 * POST   /api.php?resource=products              - Yeni ürün oluştur
 * PUT    /api.php?resource=products&id=1         - Ürün güncelle
 * DELETE /api.php?resource=products&id=1         - Ürün sil
 * 
 * Aynı işlemler orders için de geçerli
 */

require_once 'config.php';
require_once 'classes/ApiHandler.php';
require_once 'classes/ProductManager.php';
require_once 'classes/OrderManager.php';
require_once 'classes/Response.php';

// PrestaShop çekirdeğini yükle
if (file_exists(PS_ROOT_DIR . 'config/config.inc.php')) {
    require_once PS_ROOT_DIR . 'config/config.inc.php';
    
    // Context'i başlat (Kernel Container hatası için gerekli)
    if (class_exists('Context') && !Context::getContext()->shop) {
        try {
            Context::getContext()->shop = new Shop(1);
        } catch (Exception $e) {
            // Shop başlatılamazsa devam et
        }
    }
} else {
    // PrestaShop bulunamazsa, kendi DB bağlantımızı kullan
    if (!defined('_DB_PREFIX_')) {
        define('_DB_PREFIX_', DB_PREFIX);
    }
    // Manuel DB bağlantısı gerekirse buraya eklenebilir
    Response::error('PrestaShop bulunamadı. config.php dosyasındaki PS_ROOT_DIR yolunu kontrol edin.', 500);
}

// API Handler'ı başlat
$api = new ApiHandler();

// İsteği işle
$api->handleRequest();

