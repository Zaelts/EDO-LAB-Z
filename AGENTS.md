# EDO·LAB Z: guía para Codex

- Preserva los nombres EDO·LAB Z, autor Yeison J. Aragón y las dos modalidades LAB/EVAL.
- Mantén la ruta Área → Asignatura → Tema → Caso y el diseño utilizable en pantallas de celular. No elimines misiones anteriores.
- Al editar una misión, comprueba su contexto, ecuación, derivadas cruzadas, función potencial, condición inicial, rúbrica e informe.
- Distingue el límite por izquierda del límite por derecha; el bilateral existe si los dos valores existen y coinciden. El valor de la función en el punto puede diferir o faltar.
- En gráficas usa además de colores diferentes trazos y etiquetas. Para un hueco usa un círculo de centro oscuro y borde claro; un punto definido usa relleno sólido.
- Los tres modelos de ecuaciones exactas son ejemplos didácticos con variables normalizadas y coeficientes ilustrativos. No presentes los modelos como calibraciones reales.
- Ejecuta `python -m unittest discover -s tests -v` y revisa `streamlit run app.py` al modificar la navegación o los casos.
- Fuente de verdad: `casos/curriculo.json` contiene la ruta; cada caso tiene su ficha `caso.json`; `core/exactas.py` define las tres ecuaciones exactas y `core/factorizacion.py` contiene el banco de variantes y la interacción de factorización.
