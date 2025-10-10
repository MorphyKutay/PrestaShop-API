<?php
/**
 * PrestaShop API Test Dosyası
 * API'nizin çalışıp çalışmadığını test etmek için bu dosyayı kullanabilirsiniz
 */

// API yapılandırması
$apiUrl = 'http://localhost/prestashop/api/api.php'; // Kendi URL'nizi yazın
$apiKey = 'your_secret_api_key_here'; // config.php'deki API key

/**
 * API isteği gönder
 */
function makeRequest($method, $resource, $data = null, $id = null) {
    global $apiUrl, $apiKey;
    
    $url = $apiUrl . '?resource=' . $resource;
    if ($id) {
        $url .= '&id=' . $id;
    }
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'X-API-Key: ' . $apiKey,
        'Content-Type: application/json'
    ]);
    
    if ($data) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    return [
        'code' => $httpCode,
        'data' => json_decode($response, true)
    ];
}

?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrestaShop API Test</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #007bff;
        }
        .test-section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .test-section h2 {
            color: #007bff;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .result {
            background: #fff;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            border: 1px solid #ddd;
        }
        .success {
            border-left: 4px solid #28a745;
            background: #d4edda;
        }
        .error {
            border-left: 4px solid #dc3545;
            background: #f8d7da;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-top: 10px;
            font-size: 12px;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }
        .badge-success { background: #28a745; color: white; }
        .badge-error { background: #dc3545; color: white; }
        .badge-info { background: #17a2b8; color: white; }
        .config {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .config strong { color: #856404; }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 PrestaShop API Test Arayüzü</h1>
        
        <div class="config">
            <strong>⚙️ Yapılandırma:</strong><br>
            API URL: <code><?php echo $apiUrl; ?></code><br>
            API Key: <code><?php echo substr($apiKey, 0, 20) . '...'; ?></code>
            <br><br>
            <small>Bu bilgileri test.php dosyasından değiştirebilirsiniz.</small>
        </div>

        <?php
        // Test 1: Ürün Listeleme
        echo '<div class="test-section">';
        echo '<h2>📦 Test 1: Ürün Listeleme (GET /products)</h2>';
        $result = makeRequest('GET', 'products');
        
        if ($result['code'] == 200 && $result['data']['success']) {
            echo '<div class="result success">';
            echo '<span class="badge badge-success">✓ BAŞARILI</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            echo '<p><strong>Mesaj:</strong> ' . $result['data']['message'] . '</p>';
            if (isset($result['data']['data']['pagination'])) {
                $pagination = $result['data']['data']['pagination'];
                echo '<p><strong>Toplam Ürün:</strong> ' . $pagination['total'] . '</p>';
                echo '<p><strong>Sayfa:</strong> ' . $pagination['page'] . ' / ' . $pagination['pages'] . '</p>';
            }
            echo '</div>';
        } else {
            echo '<div class="result error">';
            echo '<span class="badge badge-error">✗ HATA</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            echo '<p>' . ($result['data']['message'] ?? 'Bilinmeyen hata') . '</p>';
            echo '</div>';
        }
        echo '<pre>' . json_encode($result['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . '</pre>';
        echo '</div>';

        // Test 2: Tek Ürün Getirme
        echo '<div class="test-section">';
        echo '<h2>🔍 Test 2: Tek Ürün Getirme (GET /products/1)</h2>';
        $result = makeRequest('GET', 'products', null, 1);
        
        if ($result['code'] == 200 && $result['data']['success']) {
            echo '<div class="result success">';
            echo '<span class="badge badge-success">✓ BAŞARILI</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            if (isset($result['data']['data']['name'])) {
                echo '<p><strong>Ürün:</strong> ' . $result['data']['data']['name'] . '</p>';
                echo '<p><strong>Fiyat:</strong> ' . $result['data']['data']['price'] . '</p>';
            }
            echo '</div>';
        } else {
            echo '<div class="result error">';
            echo '<span class="badge badge-error">✗ HATA</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            echo '<p>' . ($result['data']['message'] ?? 'Bilinmeyen hata') . '</p>';
            echo '</div>';
        }
        echo '<pre>' . json_encode($result['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . '</pre>';
        echo '</div>';

        // Test 3: Sipariş Listeleme
        echo '<div class="test-section">';
        echo '<h2>📋 Test 3: Sipariş Listeleme (GET /orders)</h2>';
        $result = makeRequest('GET', 'orders');
        
        if ($result['code'] == 200 && $result['data']['success']) {
            echo '<div class="result success">';
            echo '<span class="badge badge-success">✓ BAŞARILI</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            if (isset($result['data']['data']['pagination'])) {
                $pagination = $result['data']['data']['pagination'];
                echo '<p><strong>Toplam Sipariş:</strong> ' . $pagination['total'] . '</p>';
            }
            echo '</div>';
        } else {
            echo '<div class="result error">';
            echo '<span class="badge badge-error">✗ HATA</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            echo '<p>' . ($result['data']['message'] ?? 'Bilinmeyen hata') . '</p>';
            echo '</div>';
        }
        echo '<pre>' . json_encode($result['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . '</pre>';
        echo '</div>';

        // Test 4: Yanlış API Key
        echo '<div class="test-section">';
        echo '<h2>🔒 Test 4: Yanlış API Key Testi</h2>';
        $oldKey = $apiKey;
        $apiKey = 'yanlis_api_key';
        $result = makeRequest('GET', 'products');
        $apiKey = $oldKey;
        
        if ($result['code'] == 401) {
            echo '<div class="result success">';
            echo '<span class="badge badge-success">✓ BAŞARILI</span>';
            echo '<span class="badge badge-info">HTTP ' . $result['code'] . '</span>';
            echo '<p>Güvenlik kontrolü çalışıyor - Yetkisiz erişim engellendi</p>';
            echo '</div>';
        } else {
            echo '<div class="result error">';
            echo '<span class="badge badge-error">✗ HATA</span>';
            echo '<p>Güvenlik açığı! Yanlış API key ile erişim sağlandı.</p>';
            echo '</div>';
        }
        echo '<pre>' . json_encode($result['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . '</pre>';
        echo '</div>';
        ?>

        <div style="margin-top: 30px; padding: 20px; background: #e7f3ff; border-radius: 5px; border-left: 4px solid #2196F3;">
            <h3 style="color: #1976D2; margin-bottom: 10px;">📚 Sonraki Adımlar</h3>
            <ul style="margin-left: 20px; color: #333;">
                <li>Testler başarılıysa API kullanıma hazır!</li>
                <li>Detaylı kullanım için README.md dosyasına bakın</li>
                <li>Üretim ortamında API_DEBUG modunu kapatın</li>
                <li>Güçlü bir API anahtarı kullanın</li>
                <li>HTTPS kullanmayı unutmayın</li>
            </ul>
        </div>
    </div>
</body>
</html>

