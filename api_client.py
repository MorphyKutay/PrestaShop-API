"""
PrestaShop API Client
PHP API ile iletişim kuran Python modülü
"""

import requests
from typing import Dict, List, Optional
import json


class PrestaShopAPIClient:
    """PrestaShop API Client sınıfı"""
    
    def __init__(self, api_url: str, api_key: str):
        """
        API Client'ı başlatır
        
        Args:
            api_url: API URL'i
            api_key: API anahtarı
        """
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, resource: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict:
        """
        API'ye HTTP isteği gönderir
        
        Args:
            method: HTTP metodu
            resource: Resource adı (products, orders)
            data: Gönderilecek veri
            params: URL parametreleri
            
        Returns:
            API yanıtı
        """
        url = f"{self.api_url}?resource={resource}"
        
        # Parametreleri ekle
        if params:
            for key, value in params.items():
                url += f"&{key}={value}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, 
                                       json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, 
                                      json=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, timeout=10)
            else:
                raise ValueError(f"Desteklenmeyen HTTP metodu: {method}")
            
            # JSON yanıtı parse et
            result = response.json()
            
            if response.status_code >= 400:
                raise Exception(result.get('message', 'API hatası'))
            
            return result
            
        except requests.exceptions.Timeout:
            raise Exception("İstek zaman aşımına uğradı")
        except requests.exceptions.ConnectionError:
            raise Exception("API'ye bağlanılamadı. URL'i kontrol edin.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"İstek hatası: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Geçersiz API yanıtı")
    
    # ============= ÜRÜN İŞLEMLERİ =============
    
    def get_products(self, page: int = 1, limit: int = 50, 
                    search: str = None, active: int = None) -> Dict:
        """Ürün listesini getirir"""
        params = {'page': page, 'limit': limit}
        
        if search:
            params['search'] = search
        if active is not None:
            params['active'] = active
        
        return self._make_request('GET', 'products', params=params)
    
    def get_product(self, product_id: int) -> Dict:
        """Tek bir ürünü getirir"""
        return self._make_request('GET', 'products', params={'id': product_id})
    
    def create_product(self, product_data: Dict) -> Dict:
        """Yeni ürün oluşturur"""
        return self._make_request('POST', 'products', data=product_data)
    
    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Ürünü günceller"""
        return self._make_request('PUT', 'products', data=product_data, 
                                 params={'id': product_id})
    
    def delete_product(self, product_id: int) -> Dict:
        """Ürünü siler"""
        return self._make_request('DELETE', 'products', params={'id': product_id})
    
    # ============= SİPARİŞ İŞLEMLERİ =============
    
    def get_orders(self, page: int = 1, limit: int = 50, 
                  status: int = None, customer: int = None) -> Dict:
        """Sipariş listesini getirir"""
        params = {'page': page, 'limit': limit}
        
        if status is not None:
            params['status'] = status
        if customer is not None:
            params['customer'] = customer
        
        return self._make_request('GET', 'orders', params=params)
    
    def get_order(self, order_id: int) -> Dict:
        """Tek bir siparişi getirir"""
        return self._make_request('GET', 'orders', params={'id': order_id})
    
    def update_order_status(self, order_id: int, new_status: int) -> Dict:
        """Sipariş durumunu günceller"""
        return self._make_request('PUT', 'orders', 
                                 data={'current_state': new_status},
                                 params={'id': order_id})
    
    def delete_order(self, order_id: int) -> Dict:
        """Siparişi siler"""
        return self._make_request('DELETE', 'orders', params={'id': order_id})
    
    # ============= TEST =============
    
    def test_connection(self) -> bool:
        """API bağlantısını test eder"""
        try:
            result = self._make_request('GET', 'products', params={'limit': 1})
            return result.get('success', False)
        except:
            return False

