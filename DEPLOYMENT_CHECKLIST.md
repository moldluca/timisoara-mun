# ✅ CHECKLIST DEPLOYMENT HOSTICO - TimișoaraMUN

## Pregătire (✅ Completat)
- [x] Fișiere create în `hostico_deployment/`
- [x] Permisiuni setate corect
- [x] .htaccess configurat pentru Flask
- [x] app.py optimizat pentru producție

## Pași de deployment pe Hostico

### 1. 🔐 Acces cPanel
- [ ] Conectează-te la cPanel Hostico
- [ ] Username: _____________
- [ ] Domeniu: _____________

### 2. 📁 Upload fișiere
- [ ] Deschide File Manager în cPanel
- [ ] Navighează la `public_html` (sau `www`)
- [ ] **BACKUP**: Descarcă conținutul existent (dacă există)
- [ ] Șterge fișierele vechi din `public_html`
- [ ] Uploadează TOT conținutul din `hostico_deployment/`

### 3. ⚙️ Configurări importante
- [ ] Editează `.env` și completează:
  - [ ] `SECRET_KEY` (generează unul nou, sigur!)
  - [ ] `MAIL_USERNAME` (email-ul tău)
  - [ ] `MAIL_PASSWORD` (app password pentru Gmail)
- [ ] Verifică permisiuni:
  - [ ] `app.py` → 755
  - [ ] `.htaccess` → 644
  - [ ] `.env` → 644

### 4. 🐍 Python setup pe Hostico
- [ ] În cPanel → "Python App" sau "Setup Python App"
- [ ] Selectează Python 3.8+ 
- [ ] Setează calea către `public_html`
- [ ] Instalează dependințele din `requirements.txt`

### 5. 🗄️ Baza de date
- [ ] Folderul `instance/` este creat
- [ ] Permisiuni write pentru `instance/` (755)
- [ ] SQLite se va crea automat la prima rulare

### 6. 📧 Configurare email
- [ ] Activează "Less secure app access" pentru Gmail SAU
- [ ] Generează "App Password" pentru Gmail (recomandat)
- [ ] Testează trimiterea email-urilor din admin

### 7. 🔒 SSL și securitate
- [ ] Activează SSL în cPanel (Let's Encrypt gratuit)
- [ ] Testează HTTPS
- [ ] Verifică că toate resursele se încarcă pe HTTPS

### 8. 🧪 Testare finală
- [ ] Accesează domeniul → Homepage se încarcă
- [ ] Testează toate paginile din meniu
- [ ] Testează formularul de înregistrare
- [ ] Testează login admin
- [ ] Testează pagina 404
- [ ] Testează pe mobil

### 9. 🚨 Pentru mentenanță temporară
Pentru a afișa doar pagina de mentenanță:
- [ ] Uploadează doar `maintenance.html`
- [ ] Redenumește în `index.html`
- [ ] Când ești gata, înlocuiește cu site-ul complet

## 🆘 Troubleshooting

### Internal Server Error 500
1. Verifică logs în cPanel → Error Logs
2. Verifică permisiunile fișierelor
3. Verifică că Python path-ul este corect în app.py

### Email nu funcționează
1. Verifică credențialele în .env
2. Folosește App Password pentru Gmail
3. Testează cu alt provider SMTP

### Static files nu se încarcă
1. Verifică că folderul `static/` există
2. Verifică .htaccess - linia cu `/static/`
3. Clear cache browser

### Database errors
1. Verifică permisiunile folderului `instance/`
2. Verifică că SQLite poate scrie în folder

## 📞 Contact Support
- **Hostico**: support@hostico.ro
- **Telefon**: 0372.079.000
- **Live Chat**: Disponibil în cPanel

## 🎉 La final
- [ ] Site-ul funcționează perfect
- [ ] Toate funcționalitățile testate
- [ ] SSL activ și funcțional
- [ ] Email-urile se trimit corect