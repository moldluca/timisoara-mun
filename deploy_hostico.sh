#!/bin/bash

# Script de pregătire pentru deployment pe Hostico
echo "📦 Pregătirea fișierelor pentru deployment pe Hostico..."

# Creează folderul de deployment
mkdir -p hostico_deployment

# Copiază toate fișierele necesare
echo "📁 Copierea fișierelor..."

# Fișierele principale
cp app.py hostico_deployment/
cp models.py hostico_deployment/
cp requirements.txt hostico_deployment/
cp .htaccess hostico_deployment/
cp .env.production hostico_deployment/.env

# Folderele
cp -r static hostico_deployment/
cp -r templates hostico_deployment/
cp -r instance hostico_deployment/ 2>/dev/null || mkdir hostico_deployment/instance

# Setează permisiunile corecte (pentru dezvoltare locală)
chmod 755 hostico_deployment/app.py
chmod 644 hostico_deployment/.htaccess
chmod 644 hostico_deployment/.env

echo "✅ Fișierele sunt pregătite în folderul 'hostico_deployment'"
echo ""
echo "📋 Următorii pași:"
echo "1. Conectează-te la cPanel Hostico"
echo "2. Deschide File Manager"
echo "3. Navighează la public_html (sau www)"
echo "4. Uploadează tot conținutul din hostico_deployment"
echo "5. Editează .env cu datele tale reale (email, secret key)"
echo "6. Testează site-ul accesând domeniul tău"
echo ""
echo "🔧 Configurări importante:"
echo "- Schimbă SECRET_KEY în .env"
echo "- Configurează email-ul în .env"
echo "- Verifică că app.py are permisiuni 755"
echo "- Activează SSL în cPanel dacă nu e deja activ"
echo ""
echo "📞 Support Hostico: support@hostico.ro | 0372.079.000"