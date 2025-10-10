# 🛒 PrestaShop Management System

Modern, fast, and user-friendly **REST API** and **Python Desktop Application** developed for PrestaShop e-commerce platform.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PHP](https://img.shields.io/badge/PHP-7.2+-purple.svg)
![PrestaShop](https://img.shields.io/badge/PrestaShop-1.7%2B-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Installation](#-installation)
  - [PHP API Setup](#1-php-api-setup)
  - [Python Application Setup](#2-python-application-setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Python Application](#-python-application)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔌 PHP REST API

- ✅ **RESTful Architecture**: Standard HTTP methods (GET, POST, PUT, DELETE)
- ✅ **Product Management**: Full CRUD operations
- ✅ **Order Management**: View orders and update status
- ✅ **Secure**: API Key authentication, IP restriction
- ✅ **CORS Support**: Cross-origin resource sharing
- ✅ **JSON Format**: All responses in standard JSON format
- ✅ **Pagination**: Automatic pagination for large datasets
- ✅ **Filtering**: Flexible search and filtering options
- ✅ **SQL Optimization**: High performance with direct SQL queries
- ✅ **Error Handling**: Detailed and clear error messages

### 🖥️ Python Desktop Application

- ✅ **Modern Interface**: User-friendly GUI with Tkinter
- ✅ **Product Management**: Add, edit, delete, search products
- ✅ **Order Management**: View orders, update status
- ✅ **Detailed View**: View product and order details
- ✅ **Context Menus**: Right-click menus for quick access
- ✅ **Async Operations**: Non-blocking UI with threading
- ✅ **Auto Connection Test**: API status monitoring
- ✅ **Multi-language**: Supports internationalization

---

## 🛠️ Technologies

### Backend (PHP API)
- **PHP** 7.2+
- **PrestaShop** 1.7.x / 8.x
- **MySQL / MariaDB**
- **Apache / Nginx**

### Frontend (Python Desktop)
- **Python** 3.8+
- **Tkinter** (GUI)
- **Requests** (HTTP Client)
- **python-dotenv** (Configuration)

---

## 📥 Installation

### Requirements

- PrestaShop installed web server
- PHP 7.2 or higher
- Python 3.8 or higher
- MySQL/MariaDB database

---

## 1️⃣ PHP API Setup

### Step 1: Upload Files

Create a folder in your PrestaShop root directory:

```
/your-prestashop/
  ├── prestapi/           # API folder
  │   ├── api.php
  │   ├── config.php
  │   ├── .htaccess
  │   ├── test.php
  │   └── classes/
  │       ├── ApiHandler.php
  │       ├── Response.php
  │       ├── ProductManager.php
  │       └── OrderManager.php
```

### Step 2: Configure config.php

Open `config.php` and configure your settings:

```php
<?php
// PrestaShop root directory
define('PS_ROOT_DIR', dirname(__FILE__) . '/../');

// Generate a secure API key
define('API_KEY', 'your_secret_api_key_here');

// Allowed IP addresses (empty array = public access)
define('ALLOWED_IPS', []); 

// Database settings
define('DB_SERVER', 'localhost');
define('DB_USER', 'your_db_user');
define('DB_PASSWD', 'your_db_password');
define('DB_NAME', 'your_db_name');
define('DB_PREFIX', 'ps_');

// API Settings
define('API_DEBUG', true);  // Development: true, Production: false
define('API_CORS_ENABLED', true);
```

### Step 3: Test API

Open the test page in your browser:

```
https://yourstore.com/prestapi/test.php
```

or test the API directly:

```
https://yourstore.com/prestapi/api.php?resource=products&api_key=your_api_key
```

✅ If you get a successful response, PHP API is ready!

---

## 2️⃣ Python Application Setup

### Step 1: Install Python Packages

```bash
# Navigate to project directory
cd prestapi

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure config.env

Edit the `config.env` file:

```env
# PrestaShop API Configuration
API_URL=https://yourstore.com/prestapi/api.php
API_KEY=your_secret_api_key_here
```

**⚠️ Important:** API_KEY must match the API_KEY in PHP API (`config.php`)!

### Step 3: Run Application

```bash
python app.py
```

✅ Application opens and API connection is automatically tested!

---

## 📚 Usage

### Python Desktop Application

#### Product Operations

**List Products:**
1. Select "📦 Products" from left menu
2. All products displayed in table

**Search Products:**
1. Type product name in search box
2. Click "Search" button

**Add New Product:**
1. Click "➕ New Product" button
2. Fill the form:
   - Product Name (required)
   - Price (required)
   - Reference, EAN13, Stock Quantity
   - Short Description
   - Status (Active/Inactive)
3. Click "Save" button

**Edit Product:**
- Right-click on product → "✏️ Edit"
- or select product and click edit button

**View Product Details:**
- Double-click on product
- or right-click → "👁️ View Details"

**Delete Product:**
- Right-click → "🗑️ Delete" → Confirm

#### Order Operations

**List Orders:**
1. Select "📋 Orders" from left menu
2. Recent orders displayed in table

**View Order Details:**
- Double-click on order
- 3 tabs open:
  - **General Info**: Order summary
  - **Customer Info**: Customer and address
  - **Products**: Products in order

**Update Order Status:**
1. Right-click → "✏️ Update Status"
2. Select new status:
   - Awaiting Payment (1)
   - Payment Accepted (2)
   - Processing (3)
   - Shipped (4)
   - Delivered (5)
   - Canceled (6)
   - Refunded (7)
3. Click "Update" button

---

## 🔌 API Documentation

### Authentication

API key must be sent with all requests:

**Method 1: Header (Recommended)**
```bash
curl -H "X-API-Key: your_api_key" https://yourstore.com/prestapi/api.php?resource=products
```

**Method 2: Query String**
```bash
curl https://yourstore.com/prestapi/api.php?resource=products&api_key=your_api_key
```

### Product Endpoints

#### List All Products
```http
GET /api.php?resource=products
```

**Parameters:**
- `page` - Page number (default: 1)
- `limit` - Products per page (default: 50, max: 100)
- `active` - Status filter (0 or 1)
- `category` - Category ID
- `search` - Search in product name

**Example:**
```bash
curl -H "X-API-Key: your_api_key" \
  "https://yourstore.com/prestapi/api.php?resource=products&page=1&limit=10&search=tshirt"
```

**Response:**
```json
{
  "success": true,
  "message": "Products retrieved successfully",
  "data": {
    "items": [
      {
        "id_product": "1",
        "name": "Sample T-Shirt",
        "price": "29.99",
        "stock_quantity": "100",
        "active": "1",
        "price_formatted": "29.99 ₺"
      }
    ],
    "pagination": {
      "total": 150,
      "page": 1,
      "limit": 10,
      "pages": 15
    }
  }
}
```

#### Get Single Product
```http
GET /api.php?resource=products&id=1
```

#### Create New Product
```http
POST /api.php?resource=products
Content-Type: application/json

{
  "name": "New Product",
  "price": 49.99,
  "reference": "REF123",
  "quantity": 100,
  "active": 1
}
```

#### Update Product
```http
PUT /api.php?resource=products&id=1
Content-Type: application/json

{
  "price": 59.99,
  "quantity": 150
}
```

#### Delete Product
```http
DELETE /api.php?resource=products&id=1
```

### Order Endpoints

#### List All Orders
```http
GET /api.php?resource=orders
```

**Parameters:**
- `page` - Page number
- `limit` - Orders per page
- `customer` - Customer ID
- `status` - Order status
- `date_from` - Start date (YYYY-MM-DD)
- `date_to` - End date (YYYY-MM-DD)

#### Get Single Order
```http
GET /api.php?resource=orders&id=1
```

#### Update Order Status
```http
PUT /api.php?resource=orders&id=1
Content-Type: application/json

{
  "current_state": 3
}
```

### Response Format

**Success:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "message": "Error message",
  "errors": null
}
```

### HTTP Status Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (Invalid API key)
- `403` - Forbidden (IP restriction)
- `404` - Not Found
- `500` - Internal Server Error

---

## 🔒 Security

### API Key

Generate a strong API key:

```php
// Generate random key with PHP
define('API_KEY', bin2hex(random_bytes(32)));
```

### IP Restriction

Allow access only from specific IPs:

```php
define('ALLOWED_IPS', [
    '192.168.1.100',  // Office
    '203.0.113.50'    // Server
]);
```

### HTTPS

⚠️ **Always use HTTPS in production!**

### Debug Mode

Disable debug mode in production:

```php
define('API_DEBUG', false);
```

---

## 🐛 Troubleshooting

### API Connection Error

**Problem:** "Cannot connect to API"

**Solution:**
1. Check URL in `config.env`
2. Verify API key is correct
3. Ensure server is accessible

### Kernel Container Error

**Problem:** "Kernel Container is not available"

**Solution:** ✅ This issue is resolved! API no longer depends on PrestaShop Kernel.

### SQL Syntax Error

**Problem:** SQL syntax error

**Solution:** Check database prefix (`config.php` → `DB_PREFIX`)

### Tkinter Not Installed

**Problem:** `ModuleNotFoundError: No module named 'tkinter'`

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
Reinstall Python (includes Tkinter)

**Windows:**
Ensure "tcl/tk" option is checked during Python installation

### Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📊 Project Structure

```
prestapi/
├── 📁 PHP API (Backend)
│   ├── api.php                 # Main endpoint
│   ├── config.php              # Configuration
│   ├── test.php                # Test interface
│   ├── .htaccess               # URL rewriting
│   └── classes/
│       ├── ApiHandler.php      # Request handler
│       ├── Response.php        # Response handler
│       ├── ProductManager.php  # Product operations
│       └── OrderManager.php    # Order operations
│
├── 🐍 Python Desktop (Frontend)
│   ├── app.py                  # Main application
│   ├── api_client.py           # API client
│   ├── config.env              # Configuration
│   └── requirements.txt        # Python dependencies
│
└── 📄 Documentation
    ├── README.md               # This file
    └── README_PYTHON.md        # Python app details
```

---

## 🎯 Features and Development

### Current Features ✅

- [x] REST API
- [x] Product CRUD operations
- [x] Order management
- [x] Python desktop application
- [x] API security
- [x] Pagination and filtering
- [x] HTML sanitization
- [x] SQL optimization

### Planned Features 🚀

- [ ] Category management
- [ ] Customer management
- [ ] Stock tracking
- [ ] Bulk operations
- [ ] Excel export
- [ ] Charts and reports
- [ ] Product image upload
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Real-time updates with WebSocket

---

## 🤝 Contributing

We welcome contributions! 

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

PrestaShop API & Desktop Manager

---

## 🙏 Acknowledgments

- PrestaShop community
- Python Tkinter developers
- All contributors

---

## 📞 Contact

For questions or suggestions, please open an issue.

---

## 📸 Screenshots

### Python Desktop Application

#### Main Screen
- Modern and clean design
- Colorful status indicators
- Easy navigation

#### Product Management
- Table view
- Search functionality
- Context menus
- Quick editing

#### Order Management
- Detailed order view
- Customer information
- Product list
- Status updates

### PHP API Test Interface
- Automatic API tests
- Visual result display
- Error details

---

## 🚀 Quick Start

### For Developers

```bash
# Clone repository
git clone https://github.com/yourusername/prestapi.git

# Install PHP API
cd prestapi
# Upload to PrestaShop server

# Install Python app
pip install -r requirements.txt
python app.py
```

### For Users

1. Download latest release
2. Follow installation guide above
3. Configure `config.php` and `config.env`
4. Run `python app.py`

---

## 💡 Tips

1. **Quick Search**: Use product search for fast lookup
2. **Context Menu**: Right-click for quick operations
3. **Double Click**: View details quickly
4. **Keyboard Shortcuts**: Enter to save, Escape to cancel
5. **Multi-select**: Planned for future versions

---

## 📈 Performance

- **Fast API**: Direct SQL queries for optimal performance
- **Efficient Pagination**: Handle large datasets smoothly
- **Async Operations**: Non-blocking UI operations
- **Optimized Queries**: Minimized database calls

---

## 🔧 Configuration Options

### PHP API

- `PS_ROOT_DIR` - PrestaShop root directory
- `API_KEY` - API authentication key
- `ALLOWED_IPS` - IP whitelist
- `DB_PREFIX` - Database table prefix
- `API_DEBUG` - Debug mode
- `API_CORS_ENABLED` - CORS support

### Python Application

- `API_URL` - API endpoint URL
- `API_KEY` - Authentication key

---

## 🌐 Localization

Currently supports:
- Turkish (tr)
- English (en)

Want to add more languages? Contributions welcome!

---

## 📦 Dependencies

### PHP
- PrestaShop 1.7+
- PHP 7.2+
- MySQL/MariaDB

### Python
- Python 3.8+
- requests
- python-dotenv
- tkinter (included with Python)

---

## ⚡ Advanced Usage

### Bulk Operations (Planned)

```python
# Future feature
api.bulk_update_products([
    {'id': 1, 'price': 29.99},
    {'id': 2, 'price': 39.99}
])
```

### Webhooks (Planned)

```php
// Future feature
$api->registerWebhook('order.created', 'https://yourapp.com/webhook');
```

---

## 🎓 Learning Resources

- [PrestaShop Documentation](https://devdocs.prestashop.com/)
- [Python Tkinter Guide](https://docs.python.org/3/library/tkinter.html)
- [REST API Best Practices](https://restfulapi.net/)

---

**⭐ If you like this project, please give it a star!**

**Made with ❤️ for PrestaShop community**

