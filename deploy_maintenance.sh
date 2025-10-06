#!/bin/bash

# 🚧 Script deployment MENTENANȚĂ pe Hostico

echo "🚧 Pregătirea pentru deployment MENTENANȚĂ pe Hostico..."
echo ""

# Afișează fișierele pregătite
echo "📁 Fișiere pregătite în 'maintenance_deployment/':"
ls -la maintenance_deployment/
echo ""

echo "📋 PAȘI PENTRU DEPLOYMENT PE HOSTICO:"
echo ""
echo "1. 🔐 Conectează-te la cPanel Hostico"
echo "   - Acces la panoul de control"
echo "   - Deschide File Manager"
echo ""

echo "2. 📂 Backup site-ul existent (OBLIGATORIU!)"
echo "   - Navighează la public_html (sau www)"
echo "   - Selectează toate fișierele"
echo "   - Descarcă ca arhivă ZIP"
echo "   - SAU creează folder 'backup_$(date +%Y%m%d)' și mută fișierele"
echo ""

echo "3. 🚧 Deploy pagina de mentenanță"
echo "   - Șterge index.html existent"
echo "   - Upload 'maintenance.html' din folderul maintenance_deployment/"
echo "   - Redenumește 'maintenance.html' → 'index.html'"
echo ""

echo "4. ✅ Testare"
echo "   - Accesează domeniul tău"
echo "   - Verifică că pagina de mentenanță apare"
echo "   - Testează pe mobil și desktop"
echo ""

echo "5. 🔄 Pentru a reveni la site-ul normal mai târziu"
echo "   - Șterge index.html (pagina de mentenanță)"
echo "   - Restaurează backup-ul original"
echo ""

echo "📧 Contact afișat: luca.moldovan@timisoara-mun.ro"
echo "📞 Support Hostico: support@hostico.ro | 0372.079.000"
echo ""

echo "⏱️  Timp estimat deployment: Sub 5 minute"
echo "✨ Succes cu deployment-ul!"