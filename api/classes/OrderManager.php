<?php
/**
 * Sipariş Yönetim Sınıfı
 * PrestaShop siparişlerini yönetir
 */

class OrderManager
{
    /**
     * Tüm siparişleri getir
     */
    public function getAll($params)
    {
        $page = isset($params['page']) ? (int)$params['page'] : 1;
        $limit = isset($params['limit']) ? (int)$params['limit'] : 50;
        $limit = min($limit, 100);
        $offset = ($page - 1) * $limit;

        // Filtreleme
        $where = 'WHERE 1=1';

        if (isset($params['customer'])) {
            $where .= ' AND o.id_customer = ' . (int)$params['customer'];
        }

        if (isset($params['status'])) {
            $where .= ' AND o.current_state = ' . (int)$params['status'];
        }

        if (isset($params['date_from'])) {
            $dateFrom = pSQL($params['date_from']);
            $where .= " AND o.date_add >= '" . $dateFrom . "'";
        }

        if (isset($params['date_to'])) {
            $dateTo = pSQL($params['date_to']);
            $where .= " AND o.date_add <= '" . $dateTo . "'";
        }

        // Toplam sayı
        $sql = "SELECT COUNT(*) as total
                FROM " . _DB_PREFIX_ . "orders o
                $where";

        $total = (int)Db::getInstance()->getValue($sql);

        // Siparişleri getir
        $sql = "SELECT 
                    o.id_order,
                    o.reference,
                    o.id_customer,
                    o.current_state,
                    o.total_paid,
                    o.total_paid_tax_incl,
                    o.total_paid_tax_excl,
                    o.total_products,
                    o.total_shipping,
                    o.payment,
                    o.date_add,
                    o.date_upd,
                    CONCAT(c.firstname, ' ', c.lastname) as customer_name,
                    c.email as customer_email,
                    osl.name as status_name,
                    os.color as status_color
                FROM " . _DB_PREFIX_ . "orders o
                LEFT JOIN " . _DB_PREFIX_ . "customer c ON o.id_customer = c.id_customer
                LEFT JOIN " . _DB_PREFIX_ . "order_state_lang osl ON o.current_state = osl.id_order_state 
                    AND osl.id_lang = " . (int)Context::getContext()->language->id . "
                LEFT JOIN " . _DB_PREFIX_ . "order_state os ON o.current_state = os.id_order_state
                $where
                ORDER BY o.id_order DESC
                LIMIT $offset, $limit";

        $orders = Db::getInstance()->executeS($sql);

        // Her sipariş için ürün sayısını ekle
        foreach ($orders as &$order) {
            $order['product_count'] = $this->getOrderProductCount($order['id_order']);
            // Basit fiyat formatı (Tools::displayPrice yerine)
            $order['total_paid_formatted'] = number_format((float)$order['total_paid'], 2, ',', '.') . ' ₺';
        }

        Response::paginated($orders, $total, $page, $limit, 'Siparişler başarıyla getirildi');
    }

    /**
     * Tek bir siparişi getir
     */
    public function getOne($id)
    {
        $idLang = Context::getContext()->language->id;
        
        // Doğrudan SQL ile sipariş bilgilerini al
        $sql = "SELECT 
                    o.*,
                    osl.name as status_name,
                    CONCAT(c.firstname, ' ', c.lastname) as customer_name,
                    c.firstname as customer_firstname,
                    c.lastname as customer_lastname,
                    c.email as customer_email,
                    ad.firstname as delivery_firstname,
                    ad.lastname as delivery_lastname,
                    ad.address1 as delivery_address1,
                    ad.address2 as delivery_address2,
                    ad.postcode as delivery_postcode,
                    ad.city as delivery_city,
                    ad.phone as delivery_phone,
                    ad.phone_mobile as delivery_phone_mobile,
                    ai.firstname as invoice_firstname,
                    ai.lastname as invoice_lastname,
                    ai.address1 as invoice_address1,
                    ai.address2 as invoice_address2,
                    ai.postcode as invoice_postcode,
                    ai.city as invoice_city,
                    car.name as carrier_name
                FROM " . _DB_PREFIX_ . "orders o
                LEFT JOIN " . _DB_PREFIX_ . "customer c ON o.id_customer = c.id_customer
                LEFT JOIN " . _DB_PREFIX_ . "order_state_lang osl ON o.current_state = osl.id_order_state AND osl.id_lang = $idLang
                LEFT JOIN " . _DB_PREFIX_ . "address ad ON o.id_address_delivery = ad.id_address
                LEFT JOIN " . _DB_PREFIX_ . "address ai ON o.id_address_invoice = ai.id_address
                LEFT JOIN " . _DB_PREFIX_ . "carrier car ON o.id_carrier = car.id_carrier
                WHERE o.id_order = " . (int)$id;
        
        $order = Db::getInstance()->getRow($sql);
        
        if (!$order) {
            Response::error('Sipariş bulunamadı', 404);
        }

        $orderData = [
            'id_order' => $order['id_order'],
            'reference' => $order['reference'],
            'id_customer' => $order['id_customer'],
            'current_state' => $order['current_state'],
            'status_name' => $order['status_name'],
            'payment' => $order['payment'],
            'module' => $order['module'],
            'total_paid' => $order['total_paid'],
            'total_paid_tax_incl' => $order['total_paid_tax_incl'],
            'total_paid_tax_excl' => $order['total_paid_tax_excl'],
            'total_products' => $order['total_products'],
            'total_products_wt' => $order['total_products_wt'],
            'total_shipping' => $order['total_shipping'],
            'total_shipping_tax_incl' => $order['total_shipping_tax_incl'],
            'total_discounts' => $order['total_discounts'],
            'total_paid_formatted' => number_format((float)$order['total_paid'], 2, ',', '.') . ' ₺',
            'customer' => [
                'id_customer' => $order['id_customer'],
                'firstname' => $order['customer_firstname'],
                'lastname' => $order['customer_lastname'],
                'email' => $order['customer_email'],
            ],
            'delivery_address' => [
                'firstname' => $order['delivery_firstname'],
                'lastname' => $order['delivery_lastname'],
                'address1' => $order['delivery_address1'],
                'address2' => $order['delivery_address2'],
                'postcode' => $order['delivery_postcode'],
                'city' => $order['delivery_city'],
                'phone' => $order['delivery_phone'],
                'phone_mobile' => $order['delivery_phone_mobile'],
            ],
            'invoice_address' => [
                'firstname' => $order['invoice_firstname'],
                'lastname' => $order['invoice_lastname'],
                'address1' => $order['invoice_address1'],
                'address2' => $order['invoice_address2'],
                'postcode' => $order['invoice_postcode'],
                'city' => $order['invoice_city'],
            ],
            'carrier' => [
                'id_carrier' => $order['id_carrier'],
                'name' => $order['carrier_name'],
            ],
            'currency' => [
                'id_currency' => $order['id_currency'],
            ],
            'products' => $this->getOrderProducts($id),
            'date_add' => $order['date_add'],
            'date_upd' => $order['date_upd'],
        ];

        Response::success($orderData, 'Sipariş başarıyla getirildi');
    }

    /**
     * Yeni sipariş oluştur
     */
    public function create($data)
    {
        Response::error('Sipariş oluşturma işlevi henüz implementasyonu yapılmadı. PrestaShop\'ta sipariş oluşturma karmaşık bir süreçtir.', 501);
    }

    /**
     * Siparişi güncelle (genelde sadece durum güncellemesi yapılır)
     */
    public function update($id, $data)
    {
        $order = new Order($id);

        if (!Validate::isLoadedObject($order)) {
            Response::error('Sipariş bulunamadı', 404);
        }

        // Sipariş durumunu güncelle
        if (isset($data['current_state'])) {
            $newState = (int)$data['current_state'];
            
            // Durum değişikliği için OrderHistory kullan
            $history = new OrderHistory();
            $history->id_order = $order->id;
            $history->changeIdOrderState($newState, $order, true);

            if (!$history->addWithemail(true)) {
                Response::error('Sipariş durumu güncellenemedi', 500);
            }
        }

        // Ödeme bilgilerini güncelle
        if (isset($data['payment'])) {
            $order->payment = $data['payment'];
            $order->update();
        }

        Response::success([
            'id_order' => $order->id,
            'message' => 'Sipariş başarıyla güncellendi'
        ], 'Sipariş güncellendi');
    }

    /**
     * Siparişi sil (dikkatli kullanılmalı!)
     */
    public function delete($id)
    {
        $order = new Order($id);

        if (!Validate::isLoadedObject($order)) {
            Response::error('Sipariş bulunamadı', 404);
        }

        if (!$order->delete()) {
            Response::error('Sipariş silinemedi', 500);
        }

        Response::success([
            'id_order' => $id,
            'message' => 'Sipariş başarıyla silindi'
        ], 'Sipariş silindi');
    }

    /**
     * Siparişteki ürünleri getir
     */
    private function getOrderProducts($idOrder)
    {
        // Doğrudan SQL ile sipariş ürünlerini al
        $sql = "SELECT 
                    od.id_order_detail,
                    od.product_id,
                    od.product_name,
                    od.product_quantity,
                    od.product_price,
                    od.unit_price_tax_incl,
                    od.unit_price_tax_excl,
                    od.total_price_tax_incl,
                    od.total_price_tax_excl,
                    od.product_reference,
                    od.product_ean13
                FROM " . _DB_PREFIX_ . "order_detail od
                WHERE od.id_order = " . (int)$idOrder;
        
        $products = Db::getInstance()->executeS($sql);
        
        $productData = [];
        foreach ($products as $product) {
            $productData[] = [
                'id_order_detail' => $product['id_order_detail'],
                'product_id' => $product['product_id'],
                'product_name' => $product['product_name'],
                'product_quantity' => $product['product_quantity'],
                'product_price' => $product['product_price'],
                'unit_price_tax_incl' => $product['unit_price_tax_incl'],
                'unit_price_tax_excl' => $product['unit_price_tax_excl'],
                'total_price_tax_incl' => $product['total_price_tax_incl'],
                'total_price_tax_excl' => $product['total_price_tax_excl'],
                'product_reference' => $product['product_reference'],
                'product_ean13' => $product['product_ean13'],
            ];
        }

        return $productData;
    }

    /**
     * Siparişteki ürün sayısını getir
     */
    private function getOrderProductCount($idOrder)
    {
        $sql = "SELECT COUNT(*) 
                FROM " . _DB_PREFIX_ . "order_detail 
                WHERE id_order = " . (int)$idOrder;
        
        return (int)Db::getInstance()->getValue($sql);
    }
}

