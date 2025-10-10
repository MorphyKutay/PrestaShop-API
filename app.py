"""
PrestaShop Yönetim Paneli
Tkinter ile geliştirilmiş modern GUI uygulaması
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from dotenv import load_dotenv
from api_client import PrestaShopAPIClient
from datetime import datetime
import threading

# .env dosyasını yükle
load_dotenv('config.env')

# Renkler ve tema
COLORS = {
    'primary': '#2196F3',
    'success': '#4CAF50',
    'danger': '#f44336',
    'warning': '#ff9800',
    'bg': '#f5f5f5',
    'white': '#ffffff',
    'text': '#333333',
    'text_light': '#757575',
    'border': '#e0e0e0'
}


class ModernButton(tk.Button):
    """Modern stil buton"""
    def __init__(self, parent, text, command=None, color='primary', **kwargs):
        bg_color = COLORS.get(color, COLORS['primary'])
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            **kwargs
        )
        
        self.bind('<Enter>', lambda e: self.config(bg=self._darken_color(bg_color)))
        self.bind('<Leave>', lambda e: self.config(bg=bg_color))
    
    def _darken_color(self, color):
        """Rengi koyulaştırır"""
        colors = {
            COLORS['primary']: '#1976D2',
            COLORS['success']: '#388E3C',
            COLORS['danger']: '#c62828',
            COLORS['warning']: '#f57c00'
        }
        return colors.get(color, color)


class PrestaShopApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PrestaShop Yönetim Paneli")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['bg'])
        
        # API Client
        api_url = os.getenv('API_URL')
        api_key = os.getenv('API_KEY')
        
        if not api_url or not api_key:
            messagebox.showerror("Hata", "config.env dosyasında API_URL ve API_KEY ayarlanmalı!")
            self.root.destroy()
            return
        
        self.api = PrestaShopAPIClient(api_url, api_key)
        
        # UI oluştur
        self.create_ui()
        
        # API bağlantısını test et
        self.test_api_connection()
    
    def test_api_connection(self):
        """API bağlantısını test eder"""
        def test():
            if self.api.test_connection():
                self.status_label.config(
                    text="✓ API Bağlantısı Başarılı", 
                    fg=COLORS['success']
                )
            else:
                self.status_label.config(
                    text="✗ API Bağlantısı Başarısız", 
                    fg=COLORS['danger']
                )
                messagebox.showerror(
                    "Bağlantı Hatası",
                    "API'ye bağlanılamadı!\nconfig.env dosyasını kontrol edin."
                )
        
        threading.Thread(target=test, daemon=True).start()
    
    def create_ui(self):
        """Ana kullanıcı arayüzünü oluşturur"""
        # Üst başlık
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🛒 PrestaShop Yönetim Paneli",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['primary'],
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Durum çubuğu
        status_frame = tk.Frame(self.root, bg=COLORS['white'], height=30)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="API Bağlantısı test ediliyor...",
            font=('Segoe UI', 9),
            bg=COLORS['white'],
            fg=COLORS['text_light']
        )
        self.status_label.pack(side='left', padx=10)
        
        # Ana içerik
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sol menü
        self.create_sidebar()
        
        # Sağ içerik alanı
        self.main_content = tk.Frame(self.content_frame, bg=COLORS['white'])
        self.main_content.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        # Varsayılan olarak ürün yönetimini göster
        self.show_products()
    
    def create_sidebar(self):
        """Yan menü oluşturur"""
        sidebar = tk.Frame(self.content_frame, bg=COLORS['white'], width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        tk.Label(
            sidebar,
            text="MENÜ",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(pady=20)
        
        # Menü butonları
        menu_items = [
            ("📦 Ürünler", self.show_products),
            ("📋 Siparişler", self.show_orders),
            ("⚙️ Ayarlar", self.show_settings),
            ("❌ Çıkış", self.root.quit)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                command=command,
                bg=COLORS['white'],
                fg=COLORS['text'],
                font=('Segoe UI', 11),
                relief='flat',
                cursor='hand2',
                anchor='w',
                padx=20,
                pady=15
            )
            btn.pack(fill='x', padx=5, pady=2)
            
            # Hover efekti
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=COLORS['bg']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=COLORS['white']))
    
    def clear_content(self):
        """İçerik alanını temizler"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def show_products(self):
        """Ürün yönetimi ekranını gösterir"""
        self.clear_content()
        
        # Başlık ve butonlar
        top_frame = tk.Frame(self.main_content, bg=COLORS['white'])
        top_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            top_frame,
            text="Ürün Yönetimi",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(side='left')
        
        btn_frame = tk.Frame(top_frame, bg=COLORS['white'])
        btn_frame.pack(side='right')
        
        ModernButton(
            btn_frame,
            "🔄 Yenile",
            command=lambda: self.load_products(),
            color='primary'
        ).pack(side='left', padx=5)
        
        ModernButton(
            btn_frame,
            "➕ Yeni Ürün",
            command=self.add_product,
            color='success'
        ).pack(side='left', padx=5)
        
        # Arama çubuğu
        search_frame = tk.Frame(self.main_content, bg=COLORS['white'])
        search_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Ara:",
            font=('Segoe UI', 10),
            bg=COLORS['white']
        ).pack(side='left', padx=(0, 10))
        
        self.product_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.product_search_var,
            font=('Segoe UI', 10),
            width=30
        )
        search_entry.pack(side='left', padx=(0, 10))
        
        ModernButton(
            search_frame,
            "Ara",
            command=lambda: self.load_products(search=self.product_search_var.get()),
            color='primary'
        ).pack(side='left')
        
        # Tablo çerçevesi
        table_frame = tk.Frame(self.main_content, bg=COLORS['white'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Ürün Adı', 'Fiyat', 'Stok', 'Durum')
        self.products_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='tree headings',
            yscrollcommand=scrollbar.set,
            height=20
        )
        
        scrollbar.config(command=self.products_tree.yview)
        
        # Sütun ayarları
        self.products_tree.column('#0', width=0, stretch=False)
        self.products_tree.column('ID', width=60, anchor='center')
        self.products_tree.column('Ürün Adı', width=300, anchor='w')
        self.products_tree.column('Fiyat', width=100, anchor='e')
        self.products_tree.column('Stok', width=80, anchor='center')
        self.products_tree.column('Durum', width=100, anchor='center')
        
        # Başlıklar
        for col in columns:
            self.products_tree.heading(col, text=col, anchor='center')
        
        self.products_tree.pack(fill='both', expand=True)
        
        # Sağ tık menüsü
        self.create_product_context_menu()
        
        # Ürünleri yükle
        self.load_products()
    
    def create_product_context_menu(self):
        """Ürün sağ tık menüsü"""
        self.product_menu = tk.Menu(self.root, tearoff=0)
        self.product_menu.add_command(label="👁️ Detayları Gör", command=self.view_product)
        self.product_menu.add_command(label="✏️ Düzenle", command=self.edit_product)
        self.product_menu.add_separator()
        self.product_menu.add_command(label="🗑️ Sil", command=self.delete_product)
        
        self.products_tree.bind('<Button-3>', self.show_product_menu)
        self.products_tree.bind('<Double-Button-1>', lambda e: self.view_product())
    
    def show_product_menu(self, event):
        """Sağ tık menüsünü gösterir"""
        item = self.products_tree.identify_row(event.y)
        if item:
            self.products_tree.selection_set(item)
            self.product_menu.post(event.x_root, event.y_root)
    
    def load_products(self, page=1, search=None):
        """Ürünleri yükler"""
        def load():
            try:
                self.status_label.config(text="Ürünler yükleniyor...", fg=COLORS['text_light'])
                
                result = self.api.get_products(page=page, limit=50, search=search)
                
                if result.get('success'):
                    # Tabloyu temizle
                    for item in self.products_tree.get_children():
                        self.products_tree.delete(item)
                    
                    # Ürünleri ekle
                    products = result['data']['items']
                    for product in products:
                        status = "✓ Aktif" if product.get('active') == '1' else "✗ Pasif"
                        price = f"{product.get('price', '0')} ₺"
                        stock = product.get('stock_quantity', '0')
                        
                        self.products_tree.insert(
                            '',
                            'end',
                            values=(
                                product.get('id_product'),
                                product.get('name', 'İsimsiz'),
                                price,
                                stock,
                                status
                            )
                        )
                    
                    # Sayfalama bilgisi
                    pagination = result['data']['pagination']
                    self.status_label.config(
                        text=f"✓ {pagination['total']} ürün bulundu (Sayfa {pagination['page']}/{pagination['pages']})",
                        fg=COLORS['success']
                    )
                else:
                    messagebox.showerror("Hata", result.get('message', 'Bilinmeyen hata'))
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Ürünler yüklenirken hata: {str(e)}")
                self.status_label.config(text=f"✗ Hata: {str(e)}", fg=COLORS['danger'])
        
        threading.Thread(target=load, daemon=True).start()
    
    def view_product(self):
        """Ürün detaylarını gösterir"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        
        product_id = self.products_tree.item(selection[0])['values'][0]
        
        def load():
            try:
                result = self.api.get_product(product_id)
                if result.get('success'):
                    product = result['data']
                    
                    # Detay penceresi
                    detail_window = tk.Toplevel(self.root)
                    detail_window.title(f"Ürün Detayı - {product.get('name', '')}")
                    detail_window.geometry("600x500")
                    detail_window.configure(bg=COLORS['white'])
                    
                    # Scroll
                    canvas = tk.Canvas(detail_window, bg=COLORS['white'])
                    scrollbar = ttk.Scrollbar(detail_window, orient="vertical", command=canvas.yview)
                    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])
                    
                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )
                    
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)
                    
                    # Bilgiler
                    info = [
                        ("ID", product.get('id_product')),
                        ("Ürün Adı", product.get('name')),
                        ("Referans", product.get('reference', '-')),
                        ("Fiyat", f"{product.get('price', '0')} ₺"),
                        ("Fiyat (KDV Dahil)", product.get('price_formatted', '-')),
                        ("Toptan Fiyat", f"{product.get('wholesale_price', '0')} ₺"),
                        ("EAN13", product.get('ean13', '-')),
                        ("Stok", product.get('stock_quantity', '0')),
                        ("Durum", "Aktif" if product.get('active') == '1' else "Pasif"),
                        ("Kategori ID", product.get('id_category_default', '-')),
                        ("Eklenme Tarihi", product.get('date_add', '-')),
                        ("Güncellenme Tarihi", product.get('date_upd', '-')),
                    ]
                    
                    for i, (label, value) in enumerate(info):
                        tk.Label(
                            scrollable_frame,
                            text=f"{label}:",
                            font=('Segoe UI', 10, 'bold'),
                            bg=COLORS['white'],
                            anchor='w'
                        ).grid(row=i, column=0, sticky='w', padx=20, pady=5)
                        
                        tk.Label(
                            scrollable_frame,
                            text=str(value),
                            font=('Segoe UI', 10),
                            bg=COLORS['white'],
                            anchor='w'
                        ).grid(row=i, column=1, sticky='w', padx=20, pady=5)
                    
                    # Açıklama
                    if product.get('description_short'):
                        row = len(info)
                        tk.Label(
                            scrollable_frame,
                            text="Kısa Açıklama:",
                            font=('Segoe UI', 10, 'bold'),
                            bg=COLORS['white'],
                            anchor='w'
                        ).grid(row=row, column=0, columnspan=2, sticky='w', padx=20, pady=(15, 5))
                        
                        tk.Label(
                            scrollable_frame,
                            text=product.get('description_short', ''),
                            font=('Segoe UI', 9),
                            bg=COLORS['white'],
                            anchor='w',
                            wraplength=500,
                            justify='left'
                        ).grid(row=row+1, column=0, columnspan=2, sticky='w', padx=20, pady=5)
                    
                    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                    scrollbar.pack(side="right", fill="y")
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Ürün detayları yüklenemedi: {str(e)}")
        
        threading.Thread(target=load, daemon=True).start()
    
    def add_product(self):
        """Yeni ürün ekler"""
        ProductDialog(self.root, self.api, callback=lambda: self.load_products())
    
    def edit_product(self):
        """Ürün düzenler"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        
        product_id = self.products_tree.item(selection[0])['values'][0]
        ProductDialog(self.root, self.api, product_id=product_id, 
                     callback=lambda: self.load_products())
    
    def delete_product(self):
        """Ürün siler"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin")
            return
        
        product_id = self.products_tree.item(selection[0])['values'][0]
        product_name = self.products_tree.item(selection[0])['values'][1]
        
        if messagebox.askyesno("Onay", f"'{product_name}' ürününü silmek istediğinizden emin misiniz?"):
            def delete():
                try:
                    result = self.api.delete_product(product_id)
                    if result.get('success'):
                        messagebox.showinfo("Başarılı", "Ürün başarıyla silindi")
                        self.load_products()
                    else:
                        messagebox.showerror("Hata", result.get('message', 'Silinme hatası'))
                except Exception as e:
                    messagebox.showerror("Hata", f"Ürün silinemedi: {str(e)}")
            
            threading.Thread(target=delete, daemon=True).start()
    
    def show_orders(self):
        """Sipariş yönetimi ekranını gösterir"""
        self.clear_content()
        
        # Başlık ve butonlar
        top_frame = tk.Frame(self.main_content, bg=COLORS['white'])
        top_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            top_frame,
            text="Sipariş Yönetimi",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(side='left')
        
        ModernButton(
            top_frame,
            "🔄 Yenile",
            command=lambda: self.load_orders(),
            color='primary'
        ).pack(side='right', padx=5)
        
        # Tablo çerçevesi
        table_frame = tk.Frame(self.main_content, bg=COLORS['white'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Referans', 'Müşteri', 'Toplam', 'Durum', 'Tarih')
        self.orders_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='tree headings',
            yscrollcommand=scrollbar.set,
            height=20
        )
        
        scrollbar.config(command=self.orders_tree.yview)
        
        # Sütun ayarları
        self.orders_tree.column('#0', width=0, stretch=False)
        self.orders_tree.column('ID', width=60, anchor='center')
        self.orders_tree.column('Referans', width=120, anchor='w')
        self.orders_tree.column('Müşteri', width=200, anchor='w')
        self.orders_tree.column('Toplam', width=100, anchor='e')
        self.orders_tree.column('Durum', width=150, anchor='w')
        self.orders_tree.column('Tarih', width=150, anchor='center')
        
        # Başlıklar
        for col in columns:
            self.orders_tree.heading(col, text=col, anchor='center')
        
        self.orders_tree.pack(fill='both', expand=True)
        
        # Sağ tık menüsü
        self.create_order_context_menu()
        
        # Siparişleri yükle
        self.load_orders()
    
    def create_order_context_menu(self):
        """Sipariş sağ tık menüsü"""
        self.order_menu = tk.Menu(self.root, tearoff=0)
        self.order_menu.add_command(label="👁️ Detayları Gör", command=self.view_order)
        self.order_menu.add_command(label="✏️ Durum Güncelle", command=self.update_order_status)
        self.order_menu.add_separator()
        self.order_menu.add_command(label="🗑️ Sil", command=self.delete_order)
        
        self.orders_tree.bind('<Button-3>', self.show_order_menu)
        self.orders_tree.bind('<Double-Button-1>', lambda e: self.view_order())
    
    def show_order_menu(self, event):
        """Sağ tık menüsünü gösterir"""
        item = self.orders_tree.identify_row(event.y)
        if item:
            self.orders_tree.selection_set(item)
            self.order_menu.post(event.x_root, event.y_root)
    
    def load_orders(self, page=1):
        """Siparişleri yükler"""
        def load():
            try:
                self.status_label.config(text="Siparişler yükleniyor...", fg=COLORS['text_light'])
                
                result = self.api.get_orders(page=page, limit=50)
                
                if result.get('success'):
                    # Tabloyu temizle
                    for item in self.orders_tree.get_children():
                        self.orders_tree.delete(item)
                    
                    # Siparişleri ekle
                    orders = result['data']['items']
                    for order in orders:
                        total = f"{order.get('total_paid', '0')} ₺"
                        date = order.get('date_add', '')[:10]  # Sadece tarih
                        
                        self.orders_tree.insert(
                            '',
                            'end',
                            values=(
                                order.get('id_order'),
                                order.get('reference', '-'),
                                order.get('customer_name', 'Bilinmiyor'),
                                total,
                                order.get('status_name', 'Bilinmiyor'),
                                date
                            )
                        )
                    
                    # Sayfalama bilgisi
                    pagination = result['data']['pagination']
                    self.status_label.config(
                        text=f"✓ {pagination['total']} sipariş bulundu (Sayfa {pagination['page']}/{pagination['pages']})",
                        fg=COLORS['success']
                    )
                else:
                    messagebox.showerror("Hata", result.get('message', 'Bilinmeyen hata'))
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Siparişler yüklenirken hata: {str(e)}")
                self.status_label.config(text=f"✗ Hata: {str(e)}", fg=COLORS['danger'])
        
        threading.Thread(target=load, daemon=True).start()
    
    def view_order(self):
        """Sipariş detaylarını gösterir"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir sipariş seçin")
            return
        
        order_id = self.orders_tree.item(selection[0])['values'][0]
        
        def load():
            try:
                result = self.api.get_order(order_id)
                if result.get('success'):
                    order = result['data']
                    
                    # Detay penceresi
                    detail_window = tk.Toplevel(self.root)
                    detail_window.title(f"Sipariş Detayı - {order.get('reference', '')}")
                    detail_window.geometry("700x600")
                    detail_window.configure(bg=COLORS['white'])
                    
                    # Notebook (sekmeler)
                    notebook = ttk.Notebook(detail_window)
                    notebook.pack(fill='both', expand=True, padx=10, pady=10)
                    
                    # Genel Bilgiler Sekmesi
                    general_frame = tk.Frame(notebook, bg=COLORS['white'])
                    notebook.add(general_frame, text='Genel Bilgiler')
                    
                    info = [
                        ("Sipariş ID", order.get('id_order')),
                        ("Referans", order.get('reference')),
                        ("Durum", order.get('status_name')),
                        ("Ödeme", order.get('payment')),
                        ("Toplam Tutar", order.get('total_paid_formatted')),
                        ("Ürün Tutarı", f"{order.get('total_products', '0')} ₺"),
                        ("Kargo", f"{order.get('total_shipping', '0')} ₺"),
                        ("İndirim", f"{order.get('total_discounts', '0')} ₺"),
                        ("Tarih", order.get('date_add')),
                    ]
                    
                    for i, (label, value) in enumerate(info):
                        tk.Label(
                            general_frame,
                            text=f"{label}:",
                            font=('Segoe UI', 10, 'bold'),
                            bg=COLORS['white']
                        ).grid(row=i, column=0, sticky='w', padx=20, pady=5)
                        
                        tk.Label(
                            general_frame,
                            text=str(value),
                            font=('Segoe UI', 10),
                            bg=COLORS['white']
                        ).grid(row=i, column=1, sticky='w', padx=20, pady=5)
                    
                    # Müşteri Sekmesi
                    customer_frame = tk.Frame(notebook, bg=COLORS['white'])
                    notebook.add(customer_frame, text='Müşteri Bilgileri')
                    
                    customer = order.get('customer', {})
                    customer_info = [
                        ("Müşteri ID", customer.get('id_customer')),
                        ("Ad", customer.get('firstname')),
                        ("Soyad", customer.get('lastname')),
                        ("E-posta", customer.get('email')),
                    ]
                    
                    for i, (label, value) in enumerate(customer_info):
                        tk.Label(
                            customer_frame,
                            text=f"{label}:",
                            font=('Segoe UI', 10, 'bold'),
                            bg=COLORS['white']
                        ).grid(row=i, column=0, sticky='w', padx=20, pady=5)
                        
                        tk.Label(
                            customer_frame,
                            text=str(value),
                            font=('Segoe UI', 10),
                            bg=COLORS['white']
                        ).grid(row=i, column=1, sticky='w', padx=20, pady=5)
                    
                    # Adres
                    delivery = order.get('delivery_address', {})
                    tk.Label(
                        customer_frame,
                        text="\nTeslimat Adresi:",
                        font=('Segoe UI', 11, 'bold'),
                        bg=COLORS['white']
                    ).grid(row=len(customer_info), column=0, columnspan=2, sticky='w', padx=20, pady=(15, 5))
                    
                    address_text = f"{delivery.get('firstname', '')} {delivery.get('lastname', '')}\n"
                    address_text += f"{delivery.get('address1', '')}\n"
                    if delivery.get('address2'):
                        address_text += f"{delivery.get('address2')}\n"
                    address_text += f"{delivery.get('postcode', '')} {delivery.get('city', '')}\n"
                    address_text += f"Tel: {delivery.get('phone', '')}"
                    
                    tk.Label(
                        customer_frame,
                        text=address_text,
                        font=('Segoe UI', 9),
                        bg=COLORS['white'],
                        justify='left'
                    ).grid(row=len(customer_info)+1, column=0, columnspan=2, sticky='w', padx=20, pady=5)
                    
                    # Ürünler Sekmesi
                    products_frame = tk.Frame(notebook, bg=COLORS['white'])
                    notebook.add(products_frame, text='Ürünler')
                    
                    # Ürün tablosu
                    tree_frame = tk.Frame(products_frame, bg=COLORS['white'])
                    tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
                    
                    tree_scroll = ttk.Scrollbar(tree_frame)
                    tree_scroll.pack(side='right', fill='y')
                    
                    product_tree = ttk.Treeview(
                        tree_frame,
                        columns=('Ürün', 'Adet', 'Birim Fiyat', 'Toplam'),
                        show='headings',
                        yscrollcommand=tree_scroll.set
                    )
                    tree_scroll.config(command=product_tree.yview)
                    
                    product_tree.heading('Ürün', text='Ürün')
                    product_tree.heading('Adet', text='Adet')
                    product_tree.heading('Birim Fiyat', text='Birim Fiyat')
                    product_tree.heading('Toplam', text='Toplam')
                    
                    product_tree.column('Ürün', width=300)
                    product_tree.column('Adet', width=80, anchor='center')
                    product_tree.column('Birim Fiyat', width=100, anchor='e')
                    product_tree.column('Toplam', width=100, anchor='e')
                    
                    for product in order.get('products', []):
                        product_tree.insert('', 'end', values=(
                            product.get('product_name'),
                            product.get('product_quantity'),
                            f"{product.get('unit_price_tax_incl', '0')} ₺",
                            f"{product.get('total_price_tax_incl', '0')} ₺"
                        ))
                    
                    product_tree.pack(fill='both', expand=True)
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Sipariş detayları yüklenemedi: {str(e)}")
        
        threading.Thread(target=load, daemon=True).start()
    
    def update_order_status(self):
        """Sipariş durumunu günceller"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir sipariş seçin")
            return
        
        order_id = self.orders_tree.item(selection[0])['values'][0]
        
        # Durum seçim penceresi
        status_window = tk.Toplevel(self.root)
        status_window.title("Sipariş Durumu Güncelle")
        status_window.geometry("400x300")
        status_window.configure(bg=COLORS['white'])
        
        tk.Label(
            status_window,
            text="Yeni Durumu Seçin:",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['white']
        ).pack(pady=20)
        
        statuses = {
            "1": "Ödeme Bekleniyor",
            "2": "Ödeme Kabul Edildi",
            "3": "Hazırlanıyor",
            "4": "Kargoya Verildi",
            "5": "Teslim Edildi",
            "6": "İptal Edildi",
            "7": "İade"
        }
        
        status_var = tk.StringVar(value="2")
        
        for status_id, status_name in statuses.items():
            tk.Radiobutton(
                status_window,
                text=status_name,
                variable=status_var,
                value=status_id,
                font=('Segoe UI', 10),
                bg=COLORS['white']
            ).pack(anchor='w', padx=40, pady=5)
        
        def update():
            new_status = int(status_var.get())
            
            def do_update():
                try:
                    result = self.api.update_order_status(order_id, new_status)
                    if result.get('success'):
                        messagebox.showinfo("Başarılı", "Sipariş durumu güncellendi")
                        status_window.destroy()
                        self.load_orders()
                    else:
                        messagebox.showerror("Hata", result.get('message', 'Güncelleme hatası'))
                except Exception as e:
                    messagebox.showerror("Hata", f"Durum güncellenemedi: {str(e)}")
            
            threading.Thread(target=do_update, daemon=True).start()
        
        ModernButton(
            status_window,
            "Güncelle",
            command=update,
            color='success'
        ).pack(pady=20)
    
    def delete_order(self):
        """Sipariş siler"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir sipariş seçin")
            return
        
        order_id = self.orders_tree.item(selection[0])['values'][0]
        order_ref = self.orders_tree.item(selection[0])['values'][1]
        
        if messagebox.askyesno("Onay", f"'{order_ref}' siparişini silmek istediğinizden emin misiniz?"):
            def delete():
                try:
                    result = self.api.delete_order(order_id)
                    if result.get('success'):
                        messagebox.showinfo("Başarılı", "Sipariş başarıyla silindi")
                        self.load_orders()
                    else:
                        messagebox.showerror("Hata", result.get('message', 'Silme hatası'))
                except Exception as e:
                    messagebox.showerror("Hata", f"Sipariş silinemedi: {str(e)}")
            
            threading.Thread(target=delete, daemon=True).start()
    
    def show_settings(self):
        """Ayarlar ekranını gösterir"""
        self.clear_content()
        
        tk.Label(
            self.main_content,
            text="⚙️ Ayarlar",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(padx=20, pady=20)
        
        settings_frame = tk.Frame(self.main_content, bg=COLORS['white'])
        settings_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # API Ayarları
        tk.Label(
            settings_frame,
            text="API Bilgileri",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, 10))
        
        info = [
            ("API URL", os.getenv('API_URL')),
            ("API Key", os.getenv('API_KEY')[:20] + "..." if os.getenv('API_KEY') else ""),
        ]
        
        for label, value in info:
            frame = tk.Frame(settings_frame, bg=COLORS['white'])
            frame.pack(fill='x', pady=5)
            
            tk.Label(
                frame,
                text=f"{label}:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['white'],
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame,
                text=value,
                font=('Segoe UI', 10),
                bg=COLORS['white'],
                anchor='w'
            ).pack(side='left')
        
        tk.Label(
            settings_frame,
            text="\nconfig.env dosyasından düzenleyebilirsiniz.",
            font=('Segoe UI', 9, 'italic'),
            bg=COLORS['white'],
            fg=COLORS['text_light']
        ).pack(anchor='w', pady=10)


class ProductDialog:
    """Ürün ekleme/düzenleme diyaloğu"""
    
    def __init__(self, parent, api, product_id=None, callback=None):
        self.api = api
        self.product_id = product_id
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Yeni Ürün" if not product_id else "Ürün Düzenle")
        self.window.geometry("500x600")
        self.window.configure(bg=COLORS['white'])
        
        self.create_form()
        
        if product_id:
            self.load_product()
    
    def create_form(self):
        """Form oluşturur"""
        # Başlık
        tk.Label(
            self.window,
            text="Yeni Ürün Ekle" if not self.product_id else "Ürün Düzenle",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['white']
        ).pack(pady=20)
        
        # Form alanları
        form_frame = tk.Frame(self.window, bg=COLORS['white'])
        form_frame.pack(fill='both', expand=True, padx=40)
        
        self.fields = {}
        
        fields_config = [
            ('name', 'Ürün Adı *', 'text'),
            ('price', 'Fiyat *', 'text'),
            ('reference', 'Referans', 'text'),
            ('ean13', 'EAN13', 'text'),
            ('quantity', 'Stok Miktarı', 'text'),
            ('description_short', 'Kısa Açıklama', 'text'),
            ('active', 'Durum', 'check'),
        ]
        
        for field_name, label_text, field_type in fields_config:
            frame = tk.Frame(form_frame, bg=COLORS['white'])
            frame.pack(fill='x', pady=10)
            
            tk.Label(
                frame,
                text=label_text,
                font=('Segoe UI', 10),
                bg=COLORS['white']
            ).pack(anchor='w')
            
            if field_type == 'text':
                self.fields[field_name] = tk.Entry(frame, font=('Segoe UI', 10))
                self.fields[field_name].pack(fill='x', pady=(5, 0))
            elif field_type == 'check':
                self.fields[field_name] = tk.BooleanVar(value=True)
                tk.Checkbutton(
                    frame,
                    text="Aktif",
                    variable=self.fields[field_name],
                    font=('Segoe UI', 10),
                    bg=COLORS['white']
                ).pack(anchor='w', pady=(5, 0))
        
        # Butonlar
        btn_frame = tk.Frame(self.window, bg=COLORS['white'])
        btn_frame.pack(pady=20)
        
        ModernButton(
            btn_frame,
            "Kaydet",
            command=self.save_product,
            color='success'
        ).pack(side='left', padx=5)
        
        ModernButton(
            btn_frame,
            "İptal",
            command=self.window.destroy,
            color='danger'
        ).pack(side='left', padx=5)
    
    def load_product(self):
        """Ürün bilgilerini yükler"""
        def load():
            try:
                result = self.api.get_product(self.product_id)
                if result.get('success'):
                    product = result['data']
                    
                    self.fields['name'].insert(0, product.get('name', ''))
                    self.fields['price'].insert(0, product.get('price', ''))
                    self.fields['reference'].insert(0, product.get('reference', ''))
                    self.fields['ean13'].insert(0, product.get('ean13', ''))
                    self.fields['quantity'].insert(0, product.get('stock_quantity', ''))
                    self.fields['description_short'].insert(0, product.get('description_short', ''))
                    self.fields['active'].set(product.get('active') == '1')
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Ürün yüklenemedi: {str(e)}")
        
        threading.Thread(target=load, daemon=True).start()
    
    def save_product(self):
        """Ürünü kaydeder"""
        # Validasyon
        if not self.fields['name'].get():
            messagebox.showwarning("Uyarı", "Ürün adı zorunludur")
            return
        
        if not self.fields['price'].get():
            messagebox.showwarning("Uyarı", "Fiyat zorunludur")
            return
        
        try:
            price = float(self.fields['price'].get())
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçersiz fiyat")
            return
        
        # Veri hazırla
        data = {
            'name': self.fields['name'].get(),
            'price': price,
            'reference': self.fields['reference'].get() or '',
            'ean13': self.fields['ean13'].get() or '',
            'quantity': int(self.fields['quantity'].get() or 0),
            'description_short': self.fields['description_short'].get() or '',
            'active': 1 if self.fields['active'].get() else 0,
            'id_category_default': 2
        }
        
        def save():
            try:
                if self.product_id:
                    result = self.api.update_product(self.product_id, data)
                    msg = "Ürün güncellendi"
                else:
                    result = self.api.create_product(data)
                    msg = "Ürün oluşturuldu"
                
                if result.get('success'):
                    messagebox.showinfo("Başarılı", msg)
                    self.window.destroy()
                    if self.callback:
                        self.callback()
                else:
                    messagebox.showerror("Hata", result.get('message', 'İşlem hatası'))
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
        
        threading.Thread(target=save, daemon=True).start()


def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = PrestaShopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

