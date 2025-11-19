// Variables globales
let facturasData = null;
let admisionesData = null;
let charts = {};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Archivos
    document.getElementById('facturasFile').addEventListener('change', handleFileUpload);
    document.getElementById('admisionesFile').addEventListener('change', handleFileUpload);
    
    // Botón analizar
    document.getElementById('analyzeBtn').addEventListener('click', analyzeData);
    
    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    const fileType = event.target.id;
    
    if (file) {
        document.getElementById(fileType + 'Name').textContent = file.name;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                if (fileType === 'facturasFile') {
                    facturasData = data;
                } else {
                    admisionesData = data;
                }
            } catch (error) {
                showError(`Error al leer ${file.name}: ${error.message}`);
            }
        };
        reader.readAsText(file);
    }
}

function analyzeData() {
    hideError();
    
    // Verificar si hay datos pegados en los textareas
    const facturasTextarea = document.getElementById('facturasJson').value.trim();
    const admisionesTextarea = document.getElementById('admisionesJson').value.trim();
    
    try {
        if (facturasTextarea) {
            facturasData = JSON.parse(facturasTextarea);
        }
        if (admisionesTextarea) {
            admisionesData = JSON.parse(admisionesTextarea);
        }
    } catch (error) {
        showError('Error al parsear JSON: ' + error.message);
        return;
    }
    
    // Validar que haya al menos uno de los dos
    if (!facturasData && !admisionesData) {
        showError('Por favor carga o pega al menos un archivo JSON (facturas o admisiones)');
        return;
    }
    
    // Mostrar loading
    showLoading(true);
    
    // Enviar datos al backend Python
    fetch('/api/analizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            facturas: facturasData,
            admisiones: admisionesData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            processDataFromBackend(data);
            showLoading(false);
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Error desconocido');
        }
    })
    .catch(error => {
        showLoading(false);
        showError('Error al procesar datos con Python: ' + error.message);
    });
}

function processData() {
    // Limpiar charts anteriores
    Object.values(charts).forEach(chart => chart?.destroy());
    charts = {};
    
    // Procesar facturas
    const facturasAnalysis = analyzeFacturas(facturasData);
    
    // Procesar admisiones
    const admisionesAnalysis = analyzeAdmisiones(admisionesData);
    
    // Análisis combinado
    const combinedAnalysis = combinedDataAnalysis(facturasAnalysis, admisionesAnalysis);
    
    // Renderizar resultados
    renderOverview(combinedAnalysis);
    renderFacturasTab(facturasAnalysis);
    renderAdmisionesTab(admisionesAnalysis);
    renderPrestacionesTab(facturasAnalysis);
    renderEstadisticasTab(combinedAnalysis);
}

function processDataFromBackend(data) {
    // Limpiar charts anteriores
    Object.values(charts).forEach(chart => chart?.destroy());
    charts = {};
    
    // Usar datos procesados por Python/numpy
    const combinedAnalysis = {
        totalEpisodios: data.overview.totalEpisodios,
        totalFacturas: data.overview.totalFacturas,
        totalPrestaciones: data.overview.totalPrestaciones,
        montoTotal: data.overview.montoTotal,
        facturas: data.facturas,
        admisiones: data.admisiones
    };
    
    // Renderizar resultados
    renderOverview(combinedAnalysis);
    renderFacturasTab(data.facturas);
    renderAdmisionesTab(data.admisiones);
    renderPrestacionesTab(data.facturas);
    renderEstadisticasTabFromBackend(data.facturas);
}

function analyzeFacturas(data) {
    if (!data || !data.datos) return { exists: false };
    
    const facturas = data.datos;
    const prestaciones = [];
    const montos = [];
    
    facturas.forEach(factura => {
        if (factura.prestaciones && Array.isArray(factura.prestaciones)) {
            factura.prestaciones.forEach(prest => {
                prestaciones.push({
                    ...prest,
                    episodio: factura.episodio,
                    nro_factura: factura.nrO_FACTURA
                });
                
                const valor = parseFloat(prest.valoR_NETO);
                if (!isNaN(valor)) {
                    montos.push(valor);
                }
            });
        }
    });
    
    // Agrupar prestaciones por tipo
    const prestacionesPorTipo = {};
    prestaciones.forEach(p => {
        const tipo = p.tipO_PRESTACION || 'Sin tipo';
        prestacionesPorTipo[tipo] = (prestacionesPorTipo[tipo] || 0) + 1;
    });
    
    // Top 10 prestaciones más costosas
    const topPrestaciones = prestaciones
        .filter(p => p.valoR_NETO)
        .sort((a, b) => parseFloat(b.valoR_NETO) - parseFloat(a.valoR_NETO))
        .slice(0, 10);
    
    return {
        exists: true,
        total: facturas.length,
        prestaciones: prestaciones,
        totalPrestaciones: prestaciones.length,
        prestacionesPorTipo,
        topPrestaciones,
        montos,
        montoTotal: montos.reduce((a, b) => a + b, 0),
        montoPromedio: montos.length > 0 ? montos.reduce((a, b) => a + b, 0) / montos.length : 0
    };
}

function analyzeAdmisiones(data) {
    if (!data || !data.datos) return { exists: false };
    
    const admisiones = data.datos;
    
    // Agrupar por aseguradora
    const porAseguradora = {};
    admisiones.forEach(adm => {
        const aseg = adm.aseguradora || 'Sin aseguradora';
        porAseguradora[aseg] = (porAseguradora[aseg] || 0) + 1;
    });
    
    // Agrupar por clase de episodio
    const porClase = {};
    admisiones.forEach(adm => {
        const clase = adm.clasE_EPISODIO || 'Sin clase';
        porClase[clase] = (porClase[clase] || 0) + 1;
    });
    
    // Agrupar por estado de factura
    const porEstado = {};
    admisiones.forEach(adm => {
        const estado = adm.staT_FACTURA || 'Sin estado';
        porEstado[estado] = (porEstado[estado] || 0) + 1;
    });
    
    return {
        exists: true,
        total: admisiones.length,
        porAseguradora,
        porClase,
        porEstado,
        episodios: admisiones
    };
}

function combinedDataAnalysis(facturas, admisiones) {
    return {
        totalEpisodios: admisiones.exists ? admisiones.total : 0,
        totalFacturas: facturas.exists ? facturas.total : 0,
        totalPrestaciones: facturas.exists ? facturas.totalPrestaciones : 0,
        montoTotal: facturas.exists ? facturas.montoTotal : 0,
        facturas,
        admisiones
    };
}

function renderOverview(analysis) {
    // Estadísticas principales
    document.getElementById('totalEpisodios').textContent = analysis.totalEpisodios.toLocaleString();
    document.getElementById('totalFacturas').textContent = analysis.totalFacturas.toLocaleString();
    document.getElementById('totalPrestaciones').textContent = analysis.totalPrestaciones.toLocaleString();
    document.getElementById('montoTotal').textContent = formatCurrency(analysis.montoTotal);
    
    // Chart de aseguradoras
    if (analysis.admisiones.exists && analysis.admisiones.porAseguradora) {
        const ctx = document.getElementById('aseguradoraChart');
        const labels = Object.keys(analysis.admisiones.porAseguradora);
        const values = Object.values(analysis.admisiones.porAseguradora);
        
        charts.aseguradora = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.map(l => l.length > 20 ? l.substring(0, 20) + '...' : l),
                datasets: [{
                    label: 'Episodios',
                    data: values,
                    backgroundColor: 'rgba(37, 99, 235, 0.7)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
    
    // Chart de distribución de montos
    if (analysis.facturas.exists && analysis.facturas.montos.length > 0) {
        const ctx = document.getElementById('montosChart');
        const montos = analysis.facturas.montos;
        
        // Crear bins para histograma
        const bins = createHistogramBins(montos, 10);
        
        charts.montos = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: bins.labels,
                datasets: [{
                    label: 'Frecuencia',
                    data: bins.counts,
                    backgroundColor: 'rgba(124, 58, 237, 0.7)',
                    borderColor: 'rgba(124, 58, 237, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
}

function renderFacturasTab(analysis) {
    const container = document.getElementById('facturasAnalysis');
    
    if (!analysis.exists) {
        container.innerHTML = '<p class="info-item">No hay datos de facturas disponibles</p>';
        return;
    }
    
    container.innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <strong>Total de Facturas</strong>
                ${analysis.total.toLocaleString()}
            </div>
            <div class="info-item">
                <strong>Total Prestaciones</strong>
                ${analysis.totalPrestaciones.toLocaleString()}
            </div>
            <div class="info-item">
                <strong>Monto Total</strong>
                ${formatCurrency(analysis.montoTotal)}
            </div>
            <div class="info-item">
                <strong>Monto Promedio</strong>
                ${formatCurrency(analysis.montoPromedio)}
            </div>
        </div>
    `;
    
    // Chart top facturas
    if (analysis.topPrestaciones.length > 0) {
        const ctx = document.getElementById('topFacturasChart');
        const top = analysis.topPrestaciones;
        
        charts.topFacturas = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: top.map(p => (p.noM_PRESTACION || 'Sin nombre').substring(0, 30)),
                datasets: [{
                    label: 'Valor',
                    data: top.map(p => parseFloat(p.valoR_NETO)),
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
}

function renderAdmisionesTab(analysis) {
    const container = document.getElementById('admisionesAnalysis');
    
    if (!analysis.exists) {
        container.innerHTML = '<p class="info-item">No hay datos de admisiones disponibles</p>';
        return;
    }
    
    const topAseguradoras = Object.entries(analysis.porAseguradora)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    container.innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <strong>Total Episodios</strong>
                ${analysis.total.toLocaleString()}
            </div>
            <div class="info-item">
                <strong>Aseguradoras Diferentes</strong>
                ${Object.keys(analysis.porAseguradora).length}
            </div>
            <div class="info-item">
                <strong>Clases de Episodio</strong>
                ${Object.keys(analysis.porClase).length}
            </div>
        </div>
        
        <h4 style="margin: 20px 0; color: var(--primary-color);">Top 5 Aseguradoras</h4>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Aseguradora</th>
                        <th>Cantidad</th>
                    </tr>
                </thead>
                <tbody>
                    ${topAseguradoras.map(([aseg, cant]) => `
                        <tr>
                            <td>${aseg}</td>
                            <td>${cant}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    // Chart clase de episodio
    const ctxClase = document.getElementById('claseEpisodioChart');
    charts.clase = new Chart(ctxClase, {
        type: 'pie',
        data: {
            labels: Object.keys(analysis.porClase).map(k => 'Clase ' + k),
            datasets: [{
                data: Object.values(analysis.porClase),
                backgroundColor: [
                    'rgba(37, 99, 235, 0.7)',
                    'rgba(124, 58, 237, 0.7)',
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(245, 158, 11, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
    
    // Chart estado
    const ctxEstado = document.getElementById('estatusChart');
    charts.estatus = new Chart(ctxEstado, {
        type: 'doughnut',
        data: {
            labels: Object.keys(analysis.porEstado).map(k => 'Estado ' + k),
            datasets: [{
                data: Object.values(analysis.porEstado),
                backgroundColor: [
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(239, 68, 68, 0.7)',
                    'rgba(245, 158, 11, 0.7)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function renderPrestacionesTab(analysis) {
    const container = document.getElementById('prestacionesAnalysis');
    
    if (!analysis.exists || analysis.totalPrestaciones === 0) {
        container.innerHTML = '<p class="info-item">No hay datos de prestaciones disponibles</p>';
        return;
    }
    
    const topPorTipo = Object.entries(analysis.prestacionesPorTipo)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    container.innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <strong>Total Prestaciones</strong>
                ${analysis.totalPrestaciones.toLocaleString()}
            </div>
            <div class="info-item">
                <strong>Tipos Diferentes</strong>
                ${Object.keys(analysis.prestacionesPorTipo).length}
            </div>
            <div class="info-item">
                <strong>Monto Total</strong>
                ${formatCurrency(analysis.montoTotal)}
            </div>
        </div>
        
        <h4 style="margin: 20px 0; color: var(--primary-color);">Top 10 Prestaciones Más Costosas</h4>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Tipo</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    ${analysis.topPrestaciones.map(p => `
                        <tr>
                            <td>${p.noM_PRESTACION || 'Sin nombre'}</td>
                            <td>${p.tipO_PRESTACION || 'Sin tipo'}</td>
                            <td>${formatCurrency(parseFloat(p.valoR_NETO))}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    // Chart por tipo
    const ctx = document.getElementById('prestacionesTipoChart');
    charts.prestacionesTipo = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topPorTipo.map(([tipo]) => tipo.substring(0, 25)),
            datasets: [{
                label: 'Cantidad',
                data: topPorTipo.map(([, cant]) => cant),
                backgroundColor: 'rgba(245, 158, 11, 0.7)',
                borderColor: 'rgba(245, 158, 11, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

function renderEstadisticasTab(analysis) {
    const container = document.getElementById('estadisticasTable');
    
    if (!analysis.facturas.exists || analysis.facturas.montos.length === 0) {
        container.innerHTML = '<p class="info-item">No hay suficientes datos para calcular estadísticas</p>';
        return;
    }
    
    const montos = analysis.facturas.montos;
    const stats = calculateStatistics(montos);
    
    container.innerHTML = `
        <h4 style="margin-bottom: 20px; color: var(--primary-color);">Estadísticas Descriptivas de Montos</h4>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Métrica</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Media</td><td>${formatCurrency(stats.mean)}</td></tr>
                    <tr><td>Mediana</td><td>${formatCurrency(stats.median)}</td></tr>
                    <tr><td>Desviación Estándar</td><td>${formatCurrency(stats.std)}</td></tr>
                    <tr><td>Mínimo</td><td>${formatCurrency(stats.min)}</td></tr>
                    <tr><td>Máximo</td><td>${formatCurrency(stats.max)}</td></tr>
                    <tr><td>Q1 (Percentil 25)</td><td>${formatCurrency(stats.q1)}</td></tr>
                    <tr><td>Q3 (Percentil 75)</td><td>${formatCurrency(stats.q3)}</td></tr>
                    <tr><td>Rango Intercuartílico</td><td>${formatCurrency(stats.iqr)}</td></tr>
                    <tr><td>Coeficiente de Variación</td><td>${stats.cv.toFixed(2)}%</td></tr>
                    <tr><td>Total de Observaciones</td><td>${stats.count.toLocaleString()}</td></tr>
                </tbody>
            </table>
        </div>
    `;
}

function renderEstadisticasTabFromBackend(facturasData) {
    const container = document.getElementById('estadisticasTable');
    
    if (!facturasData.exists || !facturasData.estadisticas) {
        container.innerHTML = '<p class="info-item">No hay suficientes datos para calcular estadísticas</p>';
        return;
    }
    
    const stats = facturasData.estadisticas;
    const iqr = stats.q3 - stats.q1;
    
    container.innerHTML = `
        <h4 style="margin-bottom: 20px; color: var(--primary-color);">Estadísticas Descriptivas de Montos (Procesado con NumPy/Pandas)</h4>
        <div class="info-item" style="background: #dbeafe; border-left-color: #2563eb; margin-bottom: 20px;">
            <strong>✅ Análisis realizado con Python, NumPy y Pandas</strong>
        </div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Métrica</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Media <strong>(np.mean)</strong></td><td>${formatCurrency(stats.mean)}</td></tr>
                    <tr><td>Mediana <strong>(np.median)</strong></td><td>${formatCurrency(stats.median)}</td></tr>
                    <tr><td>Desviación Estándar <strong>(np.std)</strong></td><td>${formatCurrency(stats.std)}</td></tr>
                    <tr><td>Mínimo <strong>(np.min)</strong></td><td>${formatCurrency(stats.min)}</td></tr>
                    <tr><td>Máximo <strong>(np.max)</strong></td><td>${formatCurrency(stats.max)}</td></tr>
                    <tr><td>Q1 - Percentil 25 <strong>(np.percentile)</strong></td><td>${formatCurrency(stats.q1)}</td></tr>
                    <tr><td>Q3 - Percentil 75 <strong>(np.percentile)</strong></td><td>${formatCurrency(stats.q3)}</td></tr>
                    <tr><td>Rango Intercuartílico <strong>(IQR)</strong></td><td>${formatCurrency(iqr)}</td></tr>
                    <tr><td>Coeficiente de Variación</td><td>${stats.cv.toFixed(2)}%</td></tr>
                    <tr><td>Total de Observaciones</td><td>${facturasData.total.toLocaleString()}</td></tr>
                </tbody>
            </table>
        </div>
    `;
    
    // Generar gráficas adicionales
    renderEstadisticasCharts(facturasData);
}

function renderEstadisticasCharts(facturasData) {
    if (!facturasData.montos || facturasData.montos.length === 0) return;
    
    const stats = facturasData.estadisticas;
    const montos = facturasData.montos;
    const iqr = stats.q3 - stats.q1;
    
    // 1. Histograma mejorado
    const ctxHist = document.getElementById('histogramaChart');
    const bins = createHistogramBins(montos, 15);
    
    if (charts.histograma) charts.histograma.destroy();
    charts.histograma = new Chart(ctxHist, {
        type: 'bar',
        data: {
            labels: bins.labels,
            datasets: [{
                label: 'Frecuencia',
                data: bins.counts,
                backgroundColor: 'rgba(59, 130, 246, 0.7)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Cantidad: ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Frecuencia' }
                },
                x: {
                    title: { display: true, text: 'Rango de Montos' },
                    ticks: { maxRotation: 45, minRotation: 45 }
                }
            }
        }
    });
    
    // 2. Box Plot (simulado con bar chart horizontal)
    const ctxBox = document.getElementById('boxPlotChart');
    if (charts.boxPlot) charts.boxPlot.destroy();
    
    const lowerWhisker = Math.max(stats.min, stats.q1 - 1.5 * iqr);
    const upperWhisker = Math.min(stats.max, stats.q3 + 1.5 * iqr);
    
    charts.boxPlot = new Chart(ctxBox, {
        type: 'bar',
        data: {
            labels: ['Box Plot'],
            datasets: [
                {
                    label: 'Mínimo',
                    data: [stats.min],
                    backgroundColor: 'rgba(239, 68, 68, 0.7)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Q1 (25%)',
                    data: [stats.q1],
                    backgroundColor: 'rgba(245, 158, 11, 0.7)',
                    borderColor: 'rgba(245, 158, 11, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Mediana',
                    data: [stats.median],
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Q3 (75%)',
                    data: [stats.q3],
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Máximo',
                    data: [stats.max],
                    backgroundColor: 'rgba(124, 58, 237, 0.7)',
                    borderColor: 'rgba(124, 58, 237, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: true, position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + formatCurrency(context.parsed.x);
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: { display: true, text: 'Valor' },
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000).toFixed(0) + 'K';
                        }
                    }
                }
            }
        }
    });
    
    // 3. Gráfica de Cuartiles
    const ctxQuartiles = document.getElementById('quartilesChart');
    if (charts.quartiles) charts.quartiles.destroy();
    
    const p10 = percentile(montos.slice().sort((a, b) => a - b), 10);
    const p50 = stats.median;
    const p90 = percentile(montos.slice().sort((a, b) => a - b), 90);
    
    charts.quartiles = new Chart(ctxQuartiles, {
        type: 'line',
        data: {
            labels: ['Min', 'P10', 'Q1', 'Mediana', 'Media', 'Q3', 'P90', 'Max'],
            datasets: [{
                label: 'Valores',
                data: [stats.min, p10, stats.q1, stats.median, stats.mean, stats.q3, p90, stats.max],
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + formatCurrency(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Valor ($)' },
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000).toFixed(0) + 'K';
                        }
                    }
                },
                x: {
                    title: { display: true, text: 'Percentiles' }
                }
            }
        }
    });
    
    // 4. Outliers
    const ctxOutliers = document.getElementById('outliersChart');
    if (charts.outliers) charts.outliers.destroy();
    
    const lowerBound = stats.q1 - 1.5 * iqr;
    const upperBound = stats.q3 + 1.5 * iqr;
    const outliers = montos.filter(m => m < lowerBound || m > upperBound);
    const normalValues = montos.filter(m => m >= lowerBound && m <= upperBound);
    
    charts.outliers = new Chart(ctxOutliers, {
        type: 'bar',
        data: {
            labels: ['Valores Normales', 'Outliers'],
            datasets: [{
                label: 'Cantidad',
                data: [normalValues.length, outliers.length],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const percentage = ((context.parsed.y / montos.length) * 100).toFixed(1);
                            return 'Cantidad: ' + context.parsed.y + ' (' + percentage + '%)';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Cantidad de Valores' }
                }
            }
        }
    });
}

// Funciones auxiliares
function calculateStatistics(data) {
    const sorted = [...data].sort((a, b) => a - b);
    const n = sorted.length;
    
    const mean = sorted.reduce((a, b) => a + b, 0) / n;
    const median = n % 2 === 0 
        ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2 
        : sorted[Math.floor(n / 2)];
    
    const variance = sorted.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / n;
    const std = Math.sqrt(variance);
    
    const q1 = percentile(sorted, 25);
    const q3 = percentile(sorted, 75);
    const iqr = q3 - q1;
    
    const cv = (std / mean) * 100;
    
    return {
        mean,
        median,
        std,
        min: sorted[0],
        max: sorted[n - 1],
        q1,
        q3,
        iqr,
        cv,
        count: n
    };
}

function percentile(sorted, p) {
    const index = (p / 100) * (sorted.length - 1);
    const lower = Math.floor(index);
    const upper = Math.ceil(index);
    const weight = index - lower;
    
    if (lower === upper) {
        return sorted[lower];
    }
    
    return sorted[lower] * (1 - weight) + sorted[upper] * weight;
}

function createHistogramBins(data, numBins) {
    const min = Math.min(...data);
    const max = Math.max(...data);
    const binSize = (max - min) / numBins;
    
    const bins = Array(numBins).fill(0);
    const labels = [];
    
    for (let i = 0; i < numBins; i++) {
        const start = min + i * binSize;
        const end = start + binSize;
        labels.push(`${formatCurrency(start, false)} - ${formatCurrency(end, false)}`);
    }
    
    data.forEach(val => {
        let binIndex = Math.floor((val - min) / binSize);
        if (binIndex >= numBins) binIndex = numBins - 1;
        bins[binIndex]++;
    });
    
    return { labels, counts: bins };
}

function formatCurrency(value, includeSymbol = true) {
    if (isNaN(value)) return '$0';
    
    const formatted = Math.round(value).toLocaleString('es-CO');
    return includeSymbol ? '$' + formatted : formatted;
}

function switchTab(tabName) {
    // Actualizar botones
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Actualizar contenido
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
        if (content.id === tabName) {
            content.classList.add('active');
        }
    });
}

function showLoading(show) {
    document.getElementById('loadingIndicator').style.display = show ? 'flex' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = '⚠️ ' + message;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}
