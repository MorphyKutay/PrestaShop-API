<?php
/**
 * Ürün Yönetim Sınıfı
 * PrestaShop ürünlerini yönetir
 */

class ProductManager
{
    /**
     * Tüm ürünleri getir
     */
    public function getAll($params)
    {
        $page = isset($params['page']) ? (int)$params['page'] : 1;
        $limit = isset($params['limit']) ? (int)$params['limit'] : 50;
        $limit = min($limit, 100); // Maksimum 100
        $offset = ($page - 1) * $limit;

        $idLang = Context::getContext()->language->id;
        $idShop = Context::getContext()->shop->id;

        // Filtreleme
        $where = 'WHERE 1=1';

        if (isset($params['active'])) {
            $where .= ' AND p.active = ' . (int)$params['active'];
        }

        if (isset($params['category'])) {
            $where .= ' AND cp.id_category = ' . (int)$params['category'];
        }

        if (isset($params['search'])) {
            $searchTerm = pSQL($params['search']);
            $where .= " AND pl.name LIKE '%" . $searchTerm . "%'";
        }

        // Toplam sayı
        $sql = "SELECT COUNT(DISTINCT p.id_product) as total
                FROM " . _DB_PREFIX_ . "product p
                LEFT JOIN " . _DB_PREFIX_ . "category_product cp ON p.id_product = cp.id_product
                LEFT JOIN " . _DB_PREFIX_ . "product_lang pl ON p.id_product = pl.id_product AND pl.id_lang = $idLang
                $where";

        $total = (int)Db::getInstance()->getValue($sql);

        // Ürünleri getir
        $sql = "SELECT DISTINCT 
                    p.id_product,
                    pl.name,
                    pl.description,
                    pl.description_short,
                    p.price,
                    p.wholesale_price,
                    p.reference,
                    p.ean13,
                    p.active,
                    p.quantity,
                    p.id_category_default,
                    sa.quantity as stock_quantity,
                    cl.name as category_name,
                    p.date_add,
                    p.date_upd
                FROM " . _DB_PREFIX_ . "product p
                LEFT JOIN " . _DB_PREFIX_ . "product_lang pl ON p.id_product = pl.id_product AND pl.id_lang = $idLang
                LEFT JOIN " . _DB_PREFIX_ . "stock_available sa ON p.id_product = sa.id_product AND sa.id_shop = $idShop
                LEFT JOIN " . _DB_PREFIX_ . "category_product cp ON p.id_product = cp.id_product
                LEFT JOIN " . _DB_PREFIX_ . "category_lang cl ON p.id_category_default = cl.id_category AND cl.id_lang = $idLang
                $where
                ORDER BY p.id_product DESC
                LIMIT $offset, $limit";

        $products = Db::getInstance()->executeS($sql);

        // Ürün resimlerini ekle ve HTML temizle
        foreach ($products as &$product) {
            $product['images'] = $this->getProductImages($product['id_product']);
            // HTML etiketlerini temizle
            $product['description'] = strip_tags($product['description']);
            $product['description_short'] = strip_tags($product['description_short']);
            // Basit fiyat formatı (Tools::displayPrice yerine)
            $product['price_formatted'] = number_format((float)$product['price'], 2, ',', '.') . ' ₺';
        }

        Response::paginated($products, $total, $page, $limit, 'Ürünler başarıyla getirildi');
    }

    /**
     * Tek bir ürünü getir
     */
    public function getOne($id)
    {
        $idLang = Context::getContext()->language->id;
        
        // Doğrudan SQL ile ürün bilgilerini al (PrestaShop metodları cart context gerektirir)
        $sql = "SELECT 
                    p.id_product,
                    pl.name,
                    pl.description,
                    pl.description_short,
                    p.price,
                    p.wholesale_price,
                    p.reference,
                    p.ean13,
                    p.upc,
                    p.active,
                    p.quantity,
                    p.id_category_default,
                    p.id_tax_rules_group,
                    p.date_add,
                    p.date_upd,
                    sa.quantity as stock_quantity
                FROM " . _DB_PREFIX_ . "product p
                LEFT JOIN " . _DB_PREFIX_ . "product_lang pl ON p.id_product = pl.id_product AND pl.id_lang = $idLang
                LEFT JOIN " . _DB_PREFIX_ . "stock_available sa ON p.id_product = sa.id_product
                WHERE p.id_product = " . (int)$id;
        
        $product = Db::getInstance()->getRow($sql);
        
        if (!$product) {
            Response::error('Ürün bulunamadı', 404);
        }
        
        // Varsayılan vergi oranı %20 (Türkiye KDV)
        $taxRate = 20;
        
        // Fiyat hesaplama
        $basePrice = (float)$product['price'];
        $priceWithTax = $basePrice * 1.20; // KDV Dahil
        
        // Kategorileri al
        $categoriesSql = "SELECT id_category FROM " . _DB_PREFIX_ . "category_product WHERE id_product = " . (int)$id;
        $categories = array_column(Db::getInstance()->executeS($categoriesSql), 'id_category');
        
        $productData = [
            'id_product' => $product['id_product'],
            'name' => $product['name'],
            'description' => strip_tags($product['description']),
            'description_short' => strip_tags($product['description_short']),
            'price' => $product['price'],
            'wholesale_price' => $product['wholesale_price'],
            'tax_rate' => $taxRate,
            'price_with_tax' => number_format($priceWithTax, 2, '.', ''),
            'price_formatted' => number_format($priceWithTax, 2, ',', '.') . ' ₺',
            'reference' => $product['reference'],
            'ean13' => $product['ean13'],
            'upc' => $product['upc'],
            'active' => $product['active'],
            'quantity' => $product['quantity'],
            'stock_quantity' => $product['stock_quantity'],
            'id_category_default' => $product['id_category_default'],
            'categories' => $categories,
            'images' => $this->getProductImages($id),
            'date_add' => $product['date_add'],
            'date_upd' => $product['date_upd'],
        ];

        Response::success($productData, 'Ürün başarıyla getirildi');
    }

    /**
     * Yeni ürün oluştur
     */
    public function create($data)
    {
        if (!$data || !isset($data['name'])) {
            Response::error('Ürün adı zorunludur', 400);
        }

        $product = new Product();
        
        // Zorunlu alanlar
        $product->name = $data['name'];
        $product->id_category_default = isset($data['id_category_default']) ? $data['id_category_default'] : 2;
        $product->link_rewrite = isset($data['link_rewrite']) ? $data['link_rewrite'] : Tools::link_rewrite($data['name']);
        
        // Opsiyonel alanlar
        if (isset($data['description'])) $product->description = $data['description'];
        if (isset($data['description_short'])) $product->description_short = $data['description_short'];
        if (isset($data['price'])) $product->price = (float)$data['price'];
        if (isset($data['wholesale_price'])) $product->wholesale_price = (float)$data['wholesale_price'];
        if (isset($data['reference'])) $product->reference = $data['reference'];
        if (isset($data['ean13'])) $product->ean13 = $data['ean13'];
        if (isset($data['active'])) $product->active = (int)$data['active'];
        if (isset($data['quantity'])) $product->quantity = (int)$data['quantity'];

        // Ürünü kaydet
        if (!$product->add()) {
            Response::error('Ürün oluşturulamadı', 500);
        }

        // Kategorileri ekle
        if (isset($data['categories']) && is_array($data['categories'])) {
            $product->updateCategories($data['categories']);
        }

        // Stok güncelle
        if (isset($data['quantity'])) {
            StockAvailable::setQuantity($product->id, 0, (int)$data['quantity']);
        }

        Response::success([
            'id_product' => $product->id,
            'message' => 'Ürün başarıyla oluşturuldu'
        ], 'Ürün oluşturuldu', 201);
    }

    /**
     * Ürünü güncelle
     */
    public function update($id, $data)
    {
        $product = new Product($id);

        if (!Validate::isLoadedObject($product)) {
            Response::error('Ürün bulunamadı', 404);
        }

        // Güncellenecek alanlar
        if (isset($data['name'])) $product->name = $data['name'];
        if (isset($data['description'])) $product->description = $data['description'];
        if (isset($data['description_short'])) $product->description_short = $data['description_short'];
        if (isset($data['price'])) $product->price = (float)$data['price'];
        if (isset($data['wholesale_price'])) $product->wholesale_price = (float)$data['wholesale_price'];
        if (isset($data['reference'])) $product->reference = $data['reference'];
        if (isset($data['ean13'])) $product->ean13 = $data['ean13'];
        if (isset($data['active'])) $product->active = (int)$data['active'];
        if (isset($data['link_rewrite'])) $product->link_rewrite = $data['link_rewrite'];

        // Ürünü güncelle
        if (!$product->update()) {
            Response::error('Ürün güncellenemedi', 500);
        }

        // Kategorileri güncelle
        if (isset($data['categories']) && is_array($data['categories'])) {
            $product->updateCategories($data['categories']);
        }

        // Stok güncelle
        if (isset($data['quantity'])) {
            StockAvailable::setQuantity($product->id, 0, (int)$data['quantity']);
        }

        Response::success([
            'id_product' => $product->id,
            'message' => 'Ürün başarıyla güncellendi'
        ], 'Ürün güncellendi');
    }

    /**
     * Ürünü sil
     */
    public function delete($id)
    {
        $product = new Product($id);

        if (!Validate::isLoadedObject($product)) {
            Response::error('Ürün bulunamadı', 404);
        }

        if (!$product->delete()) {
            Response::error('Ürün silinemedi', 500);
        }

        Response::success([
            'id_product' => $id,
            'message' => 'Ürün başarıyla silindi'
        ], 'Ürün silindi');
    }

    /**
     * Ürün resimlerini getir
     */
    private function getProductImages($idProduct)
    {
        $images = Image::getImages(Context::getContext()->language->id, $idProduct);
        $imageData = [];

        foreach ($images as $image) {
            $imageObj = new Image($image['id_image']);
            $imageData[] = [
                'id_image' => $image['id_image'],
                'position' => $image['position'],
                'cover' => $image['cover'],
                'url' => Context::getContext()->link->getImageLink($image['id_product'], $image['id_image'], 'large_default')
            ];
        }

        return $imageData;
    }
}

