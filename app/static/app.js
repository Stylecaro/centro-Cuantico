async function cargarEstado() {
    const res = await fetch('/estado');
    const data = await res.json();
    let html = `<h2>Estado del Centro de Datos</h2>`;
    html += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    document.getElementById('panel').innerHTML = html;
    cargarAnalisis();
}

async function cargarAnalisis() {
    const res = await fetch('/analisis');
    const data = await res.json();
    let html = `<h2>Análisis Inteligente</h2>`;
    if (data.alertas.length > 0) {
        html += `<ul style='color:red;'>`;
        for (const alerta of data.alertas) {
            html += `<li>${alerta}</li>`;
        }
        html += `</ul>`;
    } else {
        html += `<p style='color:green;'>Todo correcto. No hay alertas críticas.</p>`;
    }
    document.getElementById('panel').innerHTML += html;
}

window.onload = cargarEstado;
