# Deployment Guide pentru TimișoaraMUN pe cPanel

## Pregătirea pentru deployment

### 1. Crearea fișierelor necesare pentru cPanel

#### requirements.txt
```
Flask==3.0.0
Flask-SQLAlchemy==3.0.5
python-dotenv==1.0.0
```

#### .htaccess (pentru public_html)
```
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /cgi-bin/main.py/$1 [QSA,L]
```

#### main.py (modificat pentru cPanel)
- Schimbă `app.run(debug=True, port=5050)` cu `app.run()`
- Adaugă la început: `#!/usr/bin/python3`

### 2. Structura folderelor pe cPanel

```
public_html/
├── .htaccess
├── static/
│   ├── styles.css
│   ├── error.css
│   ├── faq.css
│   ├── policies.css
│   └── img/
│       └── [toate imaginile]
├── templates/
│   └── [toate template-urile HTML]
└── cgi-bin/
    ├── main.py
    ├── models.py
    └── instance/
        └── db.sqlite3
```

### 3. Pașii de deployment

1. **Upload fișiere**:
   - Uploadează toate fișierele în structura de mai sus
   - Asigură-te că `main.py` are permisiuni de execuție (755)

2. **Configurare Python**:
   - Verifică versiunea Python disponibilă pe server
   - Instalează dependințele din requirements.txt

3. **Testare**:
   - Accesează domeniul pentru a verifica funcționarea
   - Testează toate rutele și funcționalitățile

## Comenzi utile pentru cPanel terminal (dacă disponibil)

```bash
# Instalare dependințe
pip3 install -r requirements.txt

# Setare permisiuni
chmod 755 cgi-bin/main.py

# Verificare Python
python3 --version
```

## Note importante

- Unii provideri de hosting nu suportă Flask direct
- Verifică dacă hosting-ul suportă Python/Flask applications
- Pentru hosting shared, poate fi nevoie de configurări speciale
- Consideră folosirea unui VPS sau cloud hosting pentru Flask apps
```