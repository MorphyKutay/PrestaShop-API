<?php
/**
 * API Response Yöneticisi
 * JSON formatında yanıt döndürür
 */

class Response
{
    /**
     * Başarılı yanıt döndür
     */
    public static function success($data, $message = 'İşlem başarılı', $code = 200)
    {
        self::send([
            'success' => true,
            'message' => $message,
            'data' => $data
        ], $code);
    }

    /**
     * Hata yanıtı döndür
     */
    public static function error($message, $code = 400, $errors = null)
    {
        self::send([
            'success' => false,
            'message' => $message,
            'errors' => $errors
        ], $code);
    }

    /**
     * JSON yanıt gönder
     */
    private static function send($data, $code = 200)
    {
        // CORS başlıkları
        if (API_CORS_ENABLED) {
            header('Access-Control-Allow-Origin: *');
            header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
            header('Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key');
        }

        header('Content-Type: application/json; charset=utf-8');
        http_response_code($code);
        echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        exit;
    }

    /**
     * Sayfalama bilgisiyle birlikte yanıt döndür
     */
    public static function paginated($data, $total, $page, $limit, $message = 'İşlem başarılı')
    {
        self::success([
            'items' => $data,
            'pagination' => [
                'total' => (int)$total,
                'page' => (int)$page,
                'limit' => (int)$limit,
                'pages' => (int)ceil($total / $limit)
            ]
        ], $message);
    }
}

