# EDO·LAB Z — Z-V5.27.09.2026

Aplicación educativa de matemáticas en Python, Streamlit y Plotly. Incluye la ruta de Límites, cuatro casos de Ecuaciones Diferenciales (tres dedicados a ecuaciones exactas) y siete casos de factorización en Matemática básica. Conserva los modos LAB (práctica) y EVAL (rúbrica y nota).

## Novedades de esta entrega

- Explicación y experimento interactivo del límite bilateral: dos controles permiten hacer coincidir o separar los destinos laterales.
- Gráficas con azul continuo y naranja discontinuo, más etiquetas de dirección. Los huecos usan un círculo grande con centro oscuro y borde amarillo visible. En el caso térmico, `T(5)=46 °C` aparece como **punto lleno**; el destino izquierdo `40 °C`, como **círculo abierto**.
- Tres casos de ecuaciones exactas: obtención de un modelo de costo y verificación; reconstrucción por integración de un indicador de mezcla; solución por agrupación de un índice de calidad. Los escenarios usan variables e índices **normalizados** y coeficientes ilustrativos, no datos reales de una planta.
- Nueva asignatura **Matemática básica** con el tema **Factorización** y siete casos: factor común, agrupación, trinomio cuadrado perfecto, diferencia de cuadrados, trinomio mónico, trinomio con coeficiente principal distinto de 1, y suma/diferencia de potencias iguales (incluidos los cubos). Los casos proponen retos con variantes de signos, coeficientes y exponentes; LAB incluye pistas y retroalimentación, y EVAL usa rúbrica.
- En cada caso de factorización la misión comienza con definición, criterio para reconocer el método, identidad algebraica, un ejemplo resuelto paso a paso y errores frecuentes. En la práctica una respuesta incorrecta muestra una pista sin avanzar; una correcta muestra retroalimentación y espera que el estudiante solicite el siguiente reto.

## Abrir y ejecutar en Windows

1. Descomprime el ZIP y abre **esta carpeta**, la que contiene `app.py`, en Visual Studio Code.
2. Abre una terminal PowerShell en esa carpeta y ejecuta:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

   Python 3.11 también sirve: reemplaza `-3.12` por `-3.11`. Streamlit imprimirá la dirección local para abrir la aplicación en el navegador. En las siguientes sesiones puedes ejecutar `run_edolab.bat` después de crear `.venv`.

### Si `.venv` deja de funcionar

`.venv` guarda la ruta de la instalación de Python con la que fue creado; no es una carpeta portable ni contiene el código fuente. Una ruta bajo `WindowsApps` puede ser normal para Python instalado desde Microsoft Store. Antes de reparar nada, ejecuta estos comandos en la terminal local de VS Code:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m streamlit --version
```

Si ambos funcionan, el entorno está disponible y no hay que recrearlo. Si fallan también en la terminal local (un `Acceso denegado` dentro del sandbox de Codex no basta para concluir que está roto), instala Python 3.12 con el lanzador `py` habilitado y luego renombra o elimina únicamente `.venv`; créalo con `py -3.12 -m venv .venv` e instala las dependencias indicadas arriba. `requirements.txt` es la lista reproducible de paquetes, así que reconstruir el entorno no altera el código de la aplicación. La revisión del 2026-09-27 confirmó Python 3.13.14 y Streamlit 1.64.0 en el `.venv` actual.

## Continuar el trabajo con Codex

Abre esta misma carpeta en Codex o usa su extensión desde Visual Studio Code. Si tienes la CLI instalada, abre la terminal **dentro de esta carpeta** y ejecuta `codex`. Codex tomará el directorio actual como proyecto. El archivo `AGENTS.md` resume las reglas pedagógicas, los casos y las comprobaciones para futuras ediciones.

Una primera petición útil para Codex:

> Revisa AGENTS.md y README.md. Ejecuta las comprobaciones de test_exactas.py, revisa la navegación móvil y propón una mejora para explicar límites bilaterales sin cambiar la rúbrica ni las soluciones matemáticas.

## Estructura

- `app.py`: navegación, límites, EDO de crecimiento e informes anteriores.
- `core/exactas.py`: tres misiones de ecuaciones exactas y sus curvas de nivel.
- `core/factorizacion.py`: banco de variantes algebraicas y flujo de los siete casos de factorización.
- `core/limites.py`, `core/limites_avanzados.py`: tablas y gráficas de límites.
- `casos/curriculo.json` y `casos/caso_*/caso.json`: ruta y fichas de misiones; las variantes de factorización se identifican allí y sus ejercicios residen en `core/factorizacion.py`.
- `tests/test_exactas.py`: comprobaciones de potencial, derivadas cruzadas y condiciones iniciales.

Para comprobar las matemáticas desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Autor:** Yeison J. Aragón · **Asistencia en desarrollo:** ChatGPT · OpenAI.
