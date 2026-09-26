# EDO·LAB Z — Z-V5.25.09.2026

Aplicación educativa de matemáticas en Python, Streamlit y Plotly. Incluye la ruta de Límites y cuatro casos de Ecuaciones Diferenciales, tres de ellos dedicados a ecuaciones exactas. Conserva los modos LAB (práctica) y EVAL (rúbrica y nota).

## Novedades de esta entrega

- Explicación y experimento interactivo del límite bilateral: dos controles permiten hacer coincidir o separar los destinos laterales.
- Gráficas con azul continuo y naranja discontinuo, más etiquetas de dirección. Los huecos usan un círculo grande con centro oscuro y borde amarillo visible. En el caso térmico, `T(5)=46 °C` aparece como **punto lleno**; el destino izquierdo `40 °C`, como **círculo abierto**.
- Tres casos de ecuaciones exactas: obtención de un modelo de costo y verificación; reconstrucción por integración de un indicador de mezcla; solución por agrupación de un índice de calidad. Los escenarios usan variables e índices **normalizados** y coeficientes ilustrativos, no datos reales de una planta.

## Abrir y ejecutar en Windows

1. Descomprime el ZIP y abre **esta carpeta**, la que contiene `app.py`, en Visual Studio Code.
2. Abre una terminal PowerShell en esa carpeta y ejecuta:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

   Python 3.11 también sirve: reemplaza `-3.12` por `-3.11`. Streamlit imprimirá la dirección local para abrir la aplicación en el navegador. En las siguientes sesiones puedes ejecutar `run_edolab.bat` después de crear `.venv`.

## Continuar el trabajo con Codex

Abre esta misma carpeta en Codex o usa su extensión desde Visual Studio Code. Si tienes la CLI instalada, abre la terminal **dentro de esta carpeta** y ejecuta `codex`. Codex tomará el directorio actual como proyecto. El archivo `AGENTS.md` resume las reglas pedagógicas, los casos y las comprobaciones para futuras ediciones.

Una primera petición útil para Codex:

> Revisa AGENTS.md y README.md. Ejecuta las comprobaciones de test_exactas.py, revisa la navegación móvil y propón una mejora para explicar límites bilaterales sin cambiar la rúbrica ni las soluciones matemáticas.

## Estructura

- `app.py`: navegación, límites, EDO de crecimiento e informes anteriores.
- `core/exactas.py`: tres misiones de ecuaciones exactas y sus curvas de nivel.
- `core/limites.py`, `core/limites_avanzados.py`: tablas y gráficas de límites.
- `casos/curriculo.json` y `casos/caso_*/caso.json`: ruta y fichas de misiones.
- `tests/test_exactas.py`: comprobaciones de potencial, derivadas cruzadas y condiciones iniciales.

Para comprobar las matemáticas desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Autor:** Yeison J. Aragón · **Asistencia en desarrollo:** ChatGPT · OpenAI.
