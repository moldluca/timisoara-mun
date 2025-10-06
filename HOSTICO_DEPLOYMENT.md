# TimișoaraMUN - Deployment pe Hostico

## Pregătirea fișierelor pentru Hostico

### 1. Modificarea main.py pentru producție
```python
#!/usr/bin/python3
import sys
import os

# Adaugă calea către aplicația ta
sys.path.insert(0, '/home/username/public_html/')  # Înlocuiește cu username-ul tău

from main import app

if __name__ == '__main__':
    app.run()
```

### 2. Structura folderelor pe Hostico

```
public_html/ (sau www/)
├── .htaccess
├── app.py (main.py redenumit)
├── models.py
├── requirements.txt
├── static/
│   ├── styles.css
│   ├── error.css
│   ├── faq.css
│   ├── policies.css
│   └── img/
│       └── [toate imaginile]
├── templates/
│   └── [toate template-urile HTML]
└── instance/
    └── db.sqlite3
```

### 3. .htaccess pentru Hostico
```apache
RewriteEngine On

# Redirectează totul către aplicația Python
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !^/static/
RewriteRule ^(.*)$ /app.py/$1 [QSA,L]

# Cache pentru fișierele statice
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 month"
</FilesMatch>

# Compresie GZIP
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
```

### 4. Pașii de deployment

1. **Conectează-te la cPanel Hostico**
2. **File Manager** > Navighează la `public_html`
3. **Upload fișiere** în structura de mai sus
4. **Setează permisiuni**: `app.py` trebuie să aibă permisiuni 755
5. **Testează** accesând domeniul

### 5. Configurări speciale Hostico

- **Python Path**: Hostico folosește Python 3.8+ în mod standard
- **Database**: SQLite funcționează perfect
- **Logs**: Poți accesa logs din cPanel > Error Logs
- **SSL**: Hostico oferă Let's Encrypt gratuit

### 6. Comenzi pentru terminal SSH (dacă ai acces)

```bash
# Instalare dependințe
pip3 install --user -r requirements.txt

# Verificare Python
python3 --version

# Setare permisiuni
chmod 755 app.py
chmod 644 .htaccess
```

## Troubleshooting Hostico

- **Internal Server Error**: Verifică permisiunile fișierelor
- **Module not found**: Adaugă calea corectă în sys.path
- **Database errors**: Verifică permisiunile folderului instance/
- **Static files**: Asigură-te că .htaccess exclude /static/

## Contact Hostico Support

Dacă întâmpini probleme:
- **Email**: support@hostico.ro  
- **Telefon**: 0372.079.000
- **Live Chat**: Disponibil în cPanel