# 🚧 DEPLOYMENT MENTENANȚĂ - Hostico

## Pași simpli pentru pagina de mentenanță

### 1. 🔐 Acces cPanel Hostico
- Conectează-te la cPanel Hostico
- Deschide **File Manager**

### 2. 📁 Backup site-ul existent (IMPORTANT!)
- Navighează la `public_html` (sau `www`)
- **DESCARCĂ** tot conținutul existent ca backup
- Sau creează un folder `backup_original` și mută fișierele acolo

### 3. 🚧 Upload pagina de mentenanță
- Șterge `index.html` existent (după backup!)
- Uploadează fișierul `maintenance.html`
- **Redenumește** `maintenance.html` → `index.html`

### 4. ✅ Testare
- Accesează domeniul tău
- Pagina de mentenanță ar trebui să apară

### 5. 🔄 Când ești gata să revii la site-ul normal
- Șterge `index.html` (pagina de mentenanță)
- Restaurează fișierele originale din backup
- Sau uploadează site-ul Flask complet

## 📋 Checklist rapid
- [ ] Backup făcut la site-ul existent
- [ ] `maintenance.html` uploadat în `public_html`
- [ ] Redenumit în `index.html`
- [ ] Testat accesul la domeniu
- [ ] Pagina de mentenanță se afișează corect

## 📧 Contact din pagina de mentenanță
Pagina afișează: `luca.moldovan@timisoara-mun.ro`

## ⏰ Estimare timp
- **Deployment**: 2-3 minute
- **Testare**: 1 minut
- **Total**: Sub 5 minute

## 🆘 În caz de probleme
- **Hostico Support**: support@hostico.ro
- **Telefon**: 0372.079.000
- **Restaurare**: Pune înapoi fișierele din backup