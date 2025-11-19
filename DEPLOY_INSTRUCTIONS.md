# 📊 Sistema de Análisis de Facturación Médica

Sistema web completo para análisis de datos de facturación médica con Python/NumPy/Pandas en el backend y visualizaciones interactivas.

## 🚀 Deploy en Render.com (GRATIS)

### Paso 1: Sube el código a GitHub

1. Ve a [GitHub](https://github.com) y crea un nuevo repositorio llamado `analisis-facturacion-medica`
2. No inicialices con README (ya lo tienes)
3. Copia la URL del repositorio

### Paso 2: Sube el código

```bash
cd c:\Users\carda\Downloads\ProyectoEstructuras
git init
git add .
git commit -m "Aplicación de análisis médico con Flask y NumPy"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/analisis-facturacion-medica.git
git push -u origin main
```

### Paso 3: Deploy en Render

1. Ve a [Render.com](https://render.com) y crea una cuenta (gratis)
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name**: `analisis-facturacion-medica`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd web_app && gunicorn app_backend:app`
   - **Plan**: Free

5. Click "Create Web Service"
6. Espera 2-3 minutos
7. ¡Listo! Tu app estará en: `https://analisis-facturacion-medica.onrender.com`

---

## 🌟 Opción 2: Railway.app (GRATIS - 500 horas/mes)

1. Ve a [Railway.app](https://railway.app)
2. Conecta GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detecta Flask automáticamente
6. ¡Listo en 1 minuto!

URL: `https://tu-app.up.railway.app`

---

## ☁️ Opción 3: PythonAnywhere (GRATIS - Siempre activo)

1. Crea cuenta en [PythonAnywhere](https://www.pythonanywhere.com)
2. Ve a "Web" → "Add a new web app"
3. Selecciona "Flask" y Python 3.10
4. Sube tus archivos a `/home/tuusuario/mysite/`
5. Edita `/var/www/tuusuario_pythonanywhere_com_wsgi.py`:

```python
import sys
path = '/home/tuusuario/ProyectoEstructuras'
if path not in sys.path:
    sys.path.append(path)

from web_app.app_backend import app as application
```

6. Reload y visita: `https://tuusuario.pythonanywhere.com`

---

## 📦 Estructura del Proyecto

```
ProyectoEstructuras/
├── web_app/
│   ├── app_backend.py       # Servidor Flask con NumPy/Pandas
│   ├── static/
│   │   ├── styles.css       # Estilos
│   │   └── app.js           # Frontend JavaScript
│   └── templates/
│       └── index.html       # Página principal
├── src/                     # Módulos Python originales
├── data/                    # Archivos JSON de datos
├── requirements.txt         # Dependencias Python
├── Procfile                 # Para Render/Railway
└── runtime.txt              # Versión Python

```

## 🎯 Características

✅ Backend Python con NumPy, Pandas, Scipy  
✅ Análisis estadístico completo  
✅ Visualizaciones interactivas con Chart.js  
✅ Carga de archivos JSON o pegar directo  
✅ Responsive design  
✅ Gratis en la nube  

## 💻 Desarrollo Local

```bash
cd ProyectoEstructuras
pip install -r requirements.txt
python web_app/app_backend.py
```

Abre: `http://localhost:5000`

---

**¡Tu aplicación ya está lista para la nube! 🚀**
