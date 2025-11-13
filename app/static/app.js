async function cargarEstado() {
    const res = await fetch('/estado');
    const data = await res.json();
    let html = `<h2>🔮 Estado del Centro de Datos</h2>`;
    html += `<p><strong>Centro:</strong> ${data.centro_datos || 'N/A'}</p>`;
    html += `<p><strong>Cristales:</strong> ${data.cristales || 0}</p>`;
    html += `<p><strong>Servidor:</strong> ${data.servidor_red?.activo ? '✅ Activo' : '❌ Inactivo'} (Puerto ${data.servidor_red?.puerto || 'N/A'})</p>`;
    
    // Mostrar métricas de IA si existen
    if (data.ia_cuantica) {
        html += `<h3>🤖 Métricas de IA Cuántica</h3>`;
        html += `<ul>`;
        html += `<li>Errores detectados: ${data.ia_cuantica.errores_detectados || 0}</li>`;
        html += `<li>Errores corregidos: ${data.ia_cuantica.errores_corregidos || 0}</li>`;
        html += `<li>Tasa de éxito: ${data.ia_cuantica.tasa_exito || 'N/A'}</li>`;
        html += `<li>Operaciones optimizadas: ${data.ia_cuantica.operaciones_optimizadas || 0}</li>`;
        html += `</ul>`;
    }
    
    document.getElementById('panel').innerHTML = html;
    cargarAnalisis();
    cargarIAStatus();
}

async function cargarAnalisis() {
    const res = await fetch('/analisis');
    const data = await res.json();
    let html = `<h2>📊 Análisis Inteligente</h2>`;
    
    if (data.alertas.length > 0) {
        html += `<h3>⚠️ Alertas</h3><ul style='color:red;'>`;
        for (const alerta of data.alertas) {
            html += `<li>${alerta}</li>`;
        }
        html += `</ul>`;
    }
    
    if (data.recomendaciones_ia && data.recomendaciones_ia.length > 0) {
        html += `<h3>🤖 Recomendaciones de IA</h3><ul style='color:blue;'>`;
        for (const rec of data.recomendaciones_ia) {
            html += `<li>${rec}</li>`;
        }
        html += `</ul>`;
    }
    
    if (data.alertas.length === 0 && (!data.recomendaciones_ia || data.recomendaciones_ia.length === 0)) {
        html += `<p style='color:green;'>✅ Todo correcto. No hay alertas críticas.</p>`;
    }
    
    document.getElementById('panel').innerHTML += html;
}

async function cargarIAStatus() {
    try {
        const res = await fetch('/ia-status');
        const data = await res.json();
        let html = `<h2>🤖 Estado Detallado de IA</h2>`;
        html += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        
        // Botón para optimizar con IA
        html += `<button onclick="optimizarConIA()" style="padding:10px; background:#4CAF50; color:white; border:none; cursor:pointer; margin-top:10px;">
            🤖 Ejecutar Optimización con IA
        </button>`;
        
        document.getElementById('ia-panel').innerHTML = html;
    } catch (e) {
        console.error('Error cargando estado de IA:', e);
    }
}

async function optimizarConIA() {
    document.getElementById('ia-panel').innerHTML += `<p>⏳ Optimizando...</p>`;
    try {
        const res = await fetch('/ia-optimize');
        const data = await res.json();
        let html = `<h3>✅ Optimización Completada</h3>`;
        html += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        document.getElementById('ia-panel').innerHTML += html;
        
        // Recargar estado después de optimizar
        setTimeout(cargarEstado, 2000);
    } catch (e) {
        document.getElementById('ia-panel').innerHTML += `<p style='color:red;'>❌ Error: ${e.message}</p>`;
    }
}

window.onload = cargarEstado;
