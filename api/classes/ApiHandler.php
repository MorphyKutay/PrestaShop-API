<?php
/**
 * API İstek Yöneticisi
 * HTTP isteklerini yönetir ve ilgili manager'a yönlendirir
 */

class ApiHandler
{
    private $method;
    private $resource;
    private $id;
    private $params;
    private $body;

    public function __construct()
    {
        // OPTIONS isteğini hemen yanıtla (CORS preflight)
        if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
            Response::success([], 'OK');
        }

        $this->method = $_SERVER['REQUEST_METHOD'];
        $this->parseRequest();
        $this->authenticate();
    }

    /**
     * İsteği parse et
     */
    private function parseRequest()
    {
        // Resource ve ID'yi al
        $this->resource = isset($_GET['resource']) ? $_GET['resource'] : null;
        $this->id = isset($_GET['id']) ? (int)$_GET['id'] : null;

        // Query parametrelerini al
        $this->params = $_GET;
        unset($this->params['resource'], $this->params['id']);

        // Request body'yi al (POST/PUT için)
        if (in_array($this->method, ['POST', 'PUT', 'PATCH'])) {
            $input = file_get_contents('php://input');
            $this->body = json_decode($input, true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                Response::error('Geçersiz JSON formatı', 400);
            }
        }
    }

    /**
     * API anahtarı kontrolü
     */
    private function authenticate()
    {
        // IP kontrolü
        if (!empty(ALLOWED_IPS) && !in_array($_SERVER['REMOTE_ADDR'], ALLOWED_IPS)) {
            Response::error('Bu IP adresinden erişim izni yok', 403);
        }

        // API Key kontrolü
        $apiKey = null;
        
        // Header'dan al
        if (isset($_SERVER['HTTP_X_API_KEY'])) {
            $apiKey = $_SERVER['HTTP_X_API_KEY'];
        }
        // Query string'den al
        elseif (isset($_GET['api_key'])) {
            $apiKey = $_GET['api_key'];
        }
        // Authorization header'dan al
        elseif (isset($_SERVER['HTTP_AUTHORIZATION'])) {
            $apiKey = str_replace('Bearer ', '', $_SERVER['HTTP_AUTHORIZATION']);
        }

        if ($apiKey !== API_KEY) {
            Response::error('Geçersiz API anahtarı', 401);
        }
    }

    /**
     * İsteği ilgili manager'a yönlendir
     */
    public function handleRequest()
    {
        if (!$this->resource) {
            Response::error('Resource belirtilmedi. Kullanım: ?resource=products veya ?resource=orders', 400);
        }

        try {
            switch ($this->resource) {
                case 'products':
                case 'product':
                    $manager = new ProductManager();
                    $this->route($manager);
                    break;

                case 'orders':
                case 'order':
                    $manager = new OrderManager();
                    $this->route($manager);
                    break;

                case 'categories':
                case 'category':
                    Response::error('Kategori yönetimi henüz eklenmedi', 501);
                    break;

                default:
                    Response::error('Geçersiz resource: ' . $this->resource, 404);
            }
        } catch (Exception $e) {
            if (API_DEBUG) {
                Response::error($e->getMessage(), 500, [
                    'file' => $e->getFile(),
                    'line' => $e->getLine(),
                    'trace' => $e->getTraceAsString()
                ]);
            } else {
                Response::error('Sunucu hatası', 500);
            }
        }
    }

    /**
     * HTTP metoduna göre yönlendir
     */
    private function route($manager)
    {
        switch ($this->method) {
            case 'GET':
                if ($this->id) {
                    $manager->getOne($this->id);
                } else {
                    $manager->getAll($this->params);
                }
                break;

            case 'POST':
                $manager->create($this->body);
                break;

            case 'PUT':
            case 'PATCH':
                if (!$this->id) {
                    Response::error('Güncelleme için ID gerekli', 400);
                }
                $manager->update($this->id, $this->body);
                break;

            case 'DELETE':
                if (!$this->id) {
                    Response::error('Silme için ID gerekli', 400);
                }
                $manager->delete($this->id);
                break;

            default:
                Response::error('Desteklenmeyen HTTP metodu: ' . $this->method, 405);
        }
    }
}

