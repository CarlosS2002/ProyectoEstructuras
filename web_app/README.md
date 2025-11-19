# Análisis de Facturación Médica - Web App

Sistema web interactivo para análisis de datos de facturación médica. Sube o pega archivos JSON de facturas y admisiones para obtener análisis completo con estadísticas y visualizaciones.

## 🚀 Características

- ✅ Carga de archivos JSON (facturas y admisiones)
- ✅ Opción de pegar JSON directamente en la interfaz
- ✅ Análisis estadístico completo (media, mediana, desviación estándar, cuartiles)
- ✅ Visualizaciones interactivas con Chart.js
- ✅ Análisis de prestaciones médicas
- ✅ Estadísticas por aseguradora, clase de episodio y estado
- ✅ Dashboard responsive y moderno
- ✅ 100% Cliente-side (sin backend necesario)

## 📦 Estructura de Archivos

```
web_app/
├── index.html      # Página principal
├── styles.css      # Estilos CSS
├── app.js          # Lógica JavaScript
└── README.md       # Este archivo
```

## 🌐 Deploy en la Nube

### Opción 1: Netlify (Recomendado - Gratis)

1. Crea una cuenta en [Netlify](https://netlify.com)
2. Arrastra la carpeta `web_app` completa a Netlify Drop
3. ¡Listo! Tu aplicación estará en línea en segundos

**O usando Netlify CLI:**
```bash
npm install -g netlify-cli
cd web_app
netlify deploy --prod
```

### Opción 2: Vercel (Gratis)

1. Crea una cuenta en [Vercel](https://vercel.com)
2. Instala Vercel CLI: `npm install -g vercel`
3. Ejecuta:
```bash
cd web_app
vercel
```

### Opción 3: GitHub Pages (Gratis)

1. Crea un repositorio en GitHub
2. Sube la carpeta `web_app`
3. Ve a Settings → Pages
4. Selecciona la rama y carpeta
5. Guarda y espera el deployment

### Opción 4: Azure Static Web Apps (Gratis)

1. Cuenta en [Azure](https://azure.microsoft.com)
2. Crea un Static Web App
3. Conecta tu repositorio o sube los archivos

## 💻 Uso Local

1. Abre `index.html` en tu navegador
2. O usa un servidor local:

```bash
# Con Python
cd web_app
python -m http.server 8000

# Con Node.js
npx http-server
```

3. Navega a `http://localhost:8000`

## 📊 Formato de Datos

### Facturas JSON
```json
{
  "success": true,
  "datos": [
    {
      "episodio": "0008017558",
      "nrO_FACTURA": "6801303112",
      "prestaciones": [
        {
          "noM_PRESTACION": "Consulta Urgencias",
          "valoR_NETO": "24400.00",
          "tipO_PRESTACION": "Consulta"
        }
      ]
    }
  ]
}
```

### Admisiones JSON
```json
{
  "success": true,
  "datos": [
    {
      "episodio": "0008034508",
      "clasE_EPISODIO": "2",
      "staT_FACTURA": "2",
      "aseguradora": "NUEVA EPS SA",
      "noM_PACIENTE": "FERNANDEZ DORYS"
    }
  ]
}
```

## 🎯 Análisis Incluidos

### Overview
- Total de episodios, facturas y prestaciones
- Monto total y promedio
- Gráfico de episodios por aseguradora
- Distribución de montos

### Facturas
- Análisis de montos
- Top 10 prestaciones más costosas
- Estadísticas descriptivas

### Admisiones
- Episodios por aseguradora
- Distribución por clase de episodio
- Estados de factura

### Prestaciones
- Total y tipos de prestaciones
- Análisis por tipo
- Prestaciones más costosas

### Estadísticas
- Media, mediana, moda
- Desviación estándar
- Cuartiles (Q1, Q3)
- Rango intercuartílico
- Coeficiente de variación

## 🛠️ Tecnologías

- HTML5
- CSS3 (Diseño moderno y responsive)
- JavaScript ES6+
- Chart.js 4.4.0 (Visualizaciones)

## 📱 Responsive

La aplicación es completamente responsive y funciona en:
- 📱 Móviles
- 💻 Tablets
- 🖥️ Escritorio

## 🔒 Privacidad

Todos los datos se procesan en el navegador del cliente. No se envían datos a ningún servidor externo.

## 📝 Licencia

MIT License - Libre para uso personal y comercial

## 👨‍💻 Soporte

Para problemas o sugerencias, contacta al equipo de desarrollo.

---

**¡Despliega en la nube en menos de 5 minutos! 🚀**
