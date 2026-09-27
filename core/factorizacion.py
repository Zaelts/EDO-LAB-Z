import streamlit as st

from core.progreso import award, record_attempt


LECCIONES = {
    "factor_comun": {
        "definition": "Factorizar por factor común significa reescribir una suma o resta como un producto, sacando fuera el factor que aparece en todos sus términos. Se usa la propiedad distributiva en sentido inverso.",
        "pattern": r"ab+ac=a(b+c)",
        "recognition": "Busca primero el máximo divisor común de los coeficientes. Para cada variable común, toma el menor exponente que aparece en todos los términos. Si eliges un factor común positivo, los signos originales quedan dentro del paréntesis.",
        "example": r"12x^3y-18x^2y^2",
        "steps": [
            "1. Coeficientes: el máximo factor común de 12 y 18 es 6.",
            "2. Variable x: entre x³ y x², el menor exponente es x². Variable y: el menor exponente común es y.",
            "3. El factor común máximo es 6x²y. Divide cada término por él: 12x³y ÷ 6x²y = 2x; y −18x²y² ÷ 6x²y = −3y.",
            "4. Escribe el producto: 6x²y(2x − 3y).",
            "5. Comprueba distribuyendo: 12x³y − 18x²y², que coincide con la expresión inicial.",
        ],
        "warning": "No uses el exponente mayor: el factor debe dividir a todos los términos. Revisa también que el signo quede conservado.",
    },
    "agrupacion": {
        "definition": "La factorización por agrupación separa cuatro o más términos en grupos. Se extrae un factor común en cada grupo hasta obtener el mismo binomio; luego ese binomio se saca como factor común.",
        "pattern": r"ax+ay+bx+by=(a+b)(x+y)",
        "recognition": "Prueba agrupar términos que compartan factores y verifica que, después de extraerlos, aparezca exactamente el mismo binomio. A veces es necesario cambiar el orden de los términos.",
        "example": r"2x^2+6x+xy+3y",
        "steps": [
            "1. Separa en dos pares: (2x² + 6x) + (xy + 3y).",
            "2. En el primer par extrae 2x: 2x(x + 3). En el segundo extrae y: y(x + 3).",
            "3. Ahora la expresión es 2x(x + 3) + y(x + 3). El binomio común es (x + 3).",
            "4. Extráelo: (x + 3)(2x + y).",
            "5. Comprueba: 2x² + xy + 6x + 3y; al reordenar, coincide con la expresión inicial.",
        ],
        "warning": "Si los binomios de los grupos no coinciden, revisa el orden o el signo al extraer el factor común.",
    },
    "trinomio_cuadrado": {
        "definition": "Un trinomio cuadrado perfecto es el desarrollo del cuadrado de un binomio. Sus extremos son cuadrados perfectos y el término central es el doble producto de sus raíces, con signo más o menos.",
        "pattern": r"a^2+2ab+b^2=(a+b)^2\quad;\quad a^2-2ab+b^2=(a-b)^2",
        "recognition": "Saca la raíz cuadrada del primer y del último término. Multiplica esas raíces por 2 y compara con el término central. La igualdad confirma el caso y su signo indica el signo del binomio.",
        "example": r"9p^2-30p+25",
        "steps": [
            "1. El primer término es 9p² = (3p)²; el último es 25 = 5².",
            "2. Calcula el doble producto: 2(3p)(5) = 30p. Su magnitud coincide con el término central.",
            "3. El término central es negativo, −30p, por tanto el binomio lleva resta.",
            "4. La factorización es (3p − 5)².",
            "5. Comprueba: (3p − 5)(3p − 5) = 9p² − 15p − 15p + 25 = 9p² − 30p + 25.",
        ],
        "warning": "Que el primer y el último término sean cuadrados no basta: el término central debe ser exactamente el doble producto.",
    },
    "diferencia_cuadrados": {
        "definition": "La diferencia de cuadrados es una resta entre dos cuadrados perfectos. Se factoriza como el producto de dos binomios conjugados: uno con resta y otro con suma.",
        "pattern": r"a^2-b^2=(a-b)(a+b)",
        "recognition": "Comprueba dos condiciones: hay una resta, y ambos términos tienen raíz cuadrada exacta. Una suma de cuadrados no sigue esta identidad en los números reales.",
        "example": r"4u^2-81v^4",
        "steps": [
            "1. Reconoce los cuadrados: 4u² = (2u)² y 81v⁴ = (9v²)².",
            "2. Nombra sus raíces: a = 2u y b = 9v².",
            "3. Usa la identidad a² − b² = (a − b)(a + b).",
            "4. Sustituye: (2u − 9v²)(2u + 9v²).",
            "5. Comprueba con conjugados: los productos cruzados se cancelan y queda 4u² − 81v⁴.",
        ],
        "warning": "No cambies la resta por suma: los factores conjugados producen diferencia de cuadrados porque sus términos cruzados se cancelan.",
    },
    "trinomio_simple": {
        "definition": "El trinomio mónico tiene la forma x² + bx + c: el coeficiente de x² es 1. Se factoriza buscando dos números cuya suma sea b y cuyo producto sea c.",
        "pattern": r"x^2+bx+c=(x+m)(x+n),\quad m+n=b,\ mn=c",
        "recognition": "El signo de c orienta los signos: si c es positivo, los dos números tienen el mismo signo; si c es negativo, tienen signos opuestos. Su suma debe coincidir con b.",
        "example": r"x^2+2x-15",
        "steps": [
            "1. Identifica b = 2 y c = −15.",
            "2. Busca pares de factores de −15: (1, −15), (−1, 15), (3, −5), (−3, 5).",
            "3. El par que suma 2 es 5 y −3; además, su producto es −15.",
            "4. Coloca esos números en los binomios: (x + 5)(x − 3).",
            "5. Comprueba: x² − 3x + 5x − 15 = x² + 2x − 15.",
        ],
        "warning": "Comprueba a la vez suma y producto. Encontrar solo factores de c no garantiza que sean los correctos.",
    },
    "trinomio_general": {
        "definition": "El trinomio general tiene la forma ax² + bx + c, con a distinto de 1. Los dos binomios deben reproducir el término principal y el independiente; sus productos cruzados deben sumar bx.",
        "pattern": r"ax^2+bx+c=(px+q)(rx+s),\quad pr=a,\quad q\cdot s=c,\quad p\cdot s+q\cdot r=b",
        "recognition": "Puedes usar el método ac: multiplica a·c, busca dos números cuyo producto sea ac y cuya suma sea b. Este procedimiento da factores enteros cuando existe ese par de enteros. Descompón el término central y luego factoriza por agrupación.",
        "example": r"6x^2+7x-3",
        "steps": [
            "1. Multiplica a·c: 6(−3) = −18. Busca dos números con producto −18 y suma 7: 9 y −2.",
            "2. Descompón el término central: 6x² + 9x − 2x − 3.",
            "3. Agrupa: (6x² + 9x) + (−2x − 3).",
            "4. Extrae factores: 3x(2x + 3) − 1(2x + 3). Aparece el binomio común (2x + 3).",
            "5. Factoriza: (2x + 3)(3x − 1). Comprueba que los productos cruzados 9x y −2x suman 7x.",
        ],
        "warning": "Al descomponer bx, los dos números deben tener producto ac y suma b; un signo incorrecto cambia los términos cruzados.",
    },
    "potencias_iguales": {
        "definition": "La diferencia de dos potencias con el mismo exponente siempre puede separarse por la diferencia de sus bases. La suma se factoriza con esta familia cuando el exponente común es impar. En particular, los cubos son un caso frecuente.",
        "pattern": r"a^n-b^n=(a-b)(a^{n-1}+a^{n-2}b+\cdots+b^{n-1})\quad;\quad a^n+b^n=(a+b)(a^{n-1}-a^{n-2}b+\cdots+b^{n-1}),\ n\ impar",
        "recognition": "Comprueba que ambos términos tengan el mismo exponente. Extrae sus raíces n-ésimas, incluidos los coeficientes. Para una suma, verifica que el exponente sea impar; una suma con exponente par no se factoriza mediante esta identidad sobre coeficientes enteros.",
        "example": r"8r^3-27s^3",
        "steps": [
            "1. Ambos términos son cubos: 8r³ = (2r)³ y 27s³ = (3s)³. Las bases son 2r y 3s, y n = 3.",
            "2. Es una diferencia, así que el primer factor es (2r − 3s).",
            "3. Para el trinomio, eleva cada base al cuadrado: (2r)² = 4r² y (3s)² = 9s².",
            "4. Multiplica las bases: (2r)(3s) = 6rs. En la diferencia de cubos, el término central del trinomio es positivo.",
            "5. Resultado: (2r − 3s)(4r² + 6rs + 9s²). Comprueba distribuyendo: los términos mixtos se cancelan y quedan 8r³ − 27s³.",
        ],
        "warning": "La fórmula de suma requiere exponente impar. No apliques la regla de cubos a cualquier potencia ni olvides comprobar las raíces de los coeficientes.",
    },
}


EJERCICIOS = {
    "factor_comun": [
        ("Un taller prepara paneles rectangulares. El área algebraica de un lote es 6x² + 9x. ¿Qué expresión muestra la mayor medida común y el factor que queda?", ["3x(2x + 3)", "3(2x² + 3x)", "x(6x² + 9)"], 0, "El máximo factor común es 3x: se divide cada término por 3x."),
        ("Una cantidad neta se modela como −8a³ + 12a². Extrae el factor común positivo y conserva los signos dentro del paréntesis.", ["4a²(−2a + 3)", "−4a²(2a + 3)", "4a(−2a² + 3a)"], 0, "El factor común positivo es 4a². El signo negativo permanece en el primer término del paréntesis."),
        ("En un diseño de empaques, la expresión es 15m⁴n² − 10m²n³ + 5m²n. Factoriza completamente.", ["5m²n(3m²n − 2n² + 1)", "5mn(3m³n − 2mn² + 1)", "5m²(3m²n² − 2n³ + n)"], 0, "Se toma el menor exponente de cada variable común: m²n; también se extrae 5."),
    ],
    "agrupacion": [
        ("Cuatro módulos de un mosaico aportan ax + ay + bx + by. Agrupa para identificar las dos dimensiones comunes.", ["(a + b)(x + y)", "(a + x)(b + y)", "(a + b + x + y)²"], 0, "Agrupa ax + ay y bx + by: ambos grupos contienen x + y."),
        ("Un ajuste de inventario queda 3x² − 6x + 2xy − 4y. ¿Cuál es la factorización por agrupación?", ["(x − 2)(3x + 2y)", "(x + 2)(3x − 2y)", "(3x − 2)(x + y)"], 0, "Los grupos son 3x(x − 2) y 2y(x − 2). El binomio común es x − 2."),
        ("La expresión de costo compartido es 6ab − 9ac + 4b − 6c. Agrupa sin perder los signos.", ["(2b − 3c)(3a + 2)", "(2b + 3c)(3a + 2)", "(2b − 3c)(3a − 2)"], 0, "Al agrupar, 3a(2b − 3c) + 2(2b − 3c); el factor binomial conserva −3c."),
    ],
    "trinomio_cuadrado": [
        ("Un panel cuadrado tiene área x² + 10x + 25. ¿Qué lado representa el lado repetido?", ["(x + 5)²", "(x − 5)²", "(x + 10)(x + 2.5)"], 0, "Los extremos son x² y 5²; el término medio es 2·x·5, así que el signo es positivo."),
        ("Una variación con términos negativos es 4a² − 12a + 9. Reconoce el trinomio cuadrado perfecto.", ["(2a − 3)²", "(2a + 3)²", "(4a − 3)(a − 3)"], 0, "4a²=(2a)², 9=3² y −12a=2(2a)(−3)."),
        ("El área de una pieza compuesta se expresa 9m² + 24mn + 16n². Factoriza considerando coeficientes y variables.", ["(3m + 4n)²", "(3m − 4n)²", "(9m + 16n)²"], 0, "Los extremos son (3m)² y (4n)²; el término medio confirma el signo positivo."),
    ],
    "diferencia_cuadrados": [
        ("Al comparar dos áreas cuadradas, la diferencia es x² − 49. Escríbela como producto de suma por diferencia.", ["(x − 7)(x + 7)", "(x − 7)²", "(x + 49)(x − 1)"], 0, "Es una diferencia de cuadrados: x² − 7² = (x − 7)(x + 7)."),
        ("Una placa tiene diferencia de áreas 25a⁴ − 16b². Factoriza los cuadrados sin reducir exponentes incorrectamente.", ["(5a² − 4b)(5a² + 4b)", "(5a² − 4b)²", "(25a² − 16b)(a² + b)"], 0, "25a⁴=(5a²)² y 16b²=(4b)²."),
        ("En un cálculo de capacidad aparece 81m⁶n² − q⁴. ¿Cuál es su factorización como diferencia de cuadrados?", ["(9m³n − q²)(9m³n + q²)", "(9m³n − q²)²", "(81m³n − q²)(m³n + q²)"], 0, "La raíz de 81m⁶n² es 9m³n y la de q⁴ es q²."),
    ],
    "trinomio_simple": [
        ("El área de un espacio rectangular se modela con x² + 7x + 12. Busca dos números que sumen 7 y multipliquen 12.", ["(x + 3)(x + 4)", "(x − 3)(x − 4)", "(x + 6)(x + 2)"], 0, "3 + 4 = 7 y 3·4 = 12; ambos signos son positivos."),
        ("Una diferencia de niveles se expresa x² − x − 12. Considera el producto negativo y la suma −1.", ["(x − 4)(x + 3)", "(x + 4)(x − 3)", "(x − 6)(x + 2)"], 0, "−4·3 = −12 y −4 + 3 = −1; los factores tienen signos opuestos."),
        ("Para x² − 9x + 20, el producto debe ser positivo y la suma negativa. ¿Qué factores corresponden?", ["(x − 5)(x − 4)", "(x + 5)(x + 4)", "(x − 10)(x + 2)"], 0, "−5·−4 = 20 y −5 + −4 = −9; ambos factores llevan signo negativo."),
    ],
    "trinomio_general": [
        ("Un área rectangular está dada por 6x² + 11x + 3. El coeficiente principal no es 1.", ["(3x + 1)(2x + 3)", "(6x + 1)(x + 3)", "(3x − 1)(2x − 3)"], 0, "Al multiplicar extremos se obtiene 6x² y 3; los términos cruzados suman 11x."),
        ("La expresión 6x² − x − 2 combina coeficiente principal 6 y término independiente negativo.", ["(3x − 2)(2x + 1)", "(3x + 2)(2x − 1)", "(6x + 1)(x − 2)"], 0, "Los términos cruzados son 3x y −4x, cuya suma es −x; el producto constante es −2."),
        ("Un modelo de material usa 12x² − 7x − 10. Comprueba los signos y coeficientes de los binomios.", ["(3x + 2)(4x − 5)", "(3x − 2)(4x + 5)", "(6x + 5)(2x − 2)"], 0, "Los términos cruzados −15x + 8x suman −7x y 2·(−5)=−10."),
    ],
    "potencias_iguales": [
        ("Un diseño compara dos áreas de cuarto grado: x⁴ − y⁴. Factoriza completamente sobre enteros.", ["(x − y)(x + y)(x² + y²)", "(x² − y²)(x² + y²)", "(x − y)⁴"], 0, "Primero aplica diferencia de cuadrados a x⁴ − y⁴; luego vuelve a factorizar x² − y²."),
        ("Una expresión de volumen simplificada es x⁵ + y⁵. ¿Qué regla permite factorizar esta suma?", ["(x + y)(x⁴ − x³y + x²y² − xy³ + y⁴)", "(x + y)(x⁴ + x³y + x²y² + xy³ + y⁴)", "(x + y)⁵"], 0, "El exponente común 5 es impar: la suma de potencias alterna signos en el segundo factor."),
        ("Una cantidad se expresa como x⁴ + y⁴. ¿Qué conclusión es correcta al intentar usar la suma de potencias iguales sobre enteros?", ["No se factoriza con esa identidad porque el exponente común es par.", "Se factoriza como (x + y)(x³ − x²y + xy² − y³).", "Se factoriza como (x − y)(x³ + x²y + xy² + y³)."], 0, "Distingue la suma del caso impar y la diferencia. No toda suma con exponentes iguales se factoriza por esta regla."),
        ("La diferencia de dos volúmenes es a³ − 27b³. Considera que 27b³ = (3b)³.", ["(a − 3b)(a² + 3ab + 9b²)", "(a + 3b)(a² − 3ab + 9b²)", "(a − 27b)(a² + 9b²)"], 0, "Las raíces cúbicas son a y 3b. Para la diferencia, el binomio resta y el término central del trinomio suma."),
        ("Un prototipo combina volúmenes: 8m³ + 125n³. Reconoce las raíces cúbicas y el patrón de signos.", ["(2m + 5n)(4m² − 10mn + 25n²)", "(2m − 5n)(4m² + 10mn + 25n²)", "(8m + 125n)(m² + n²)"], 0, "Las raíces son 2m y 5n. Para suma de cubos, el binomio suma y el término central del trinomio resta."),
    ],
}

PISTAS = {
    "factor_comun": [
        "Calcula primero el máximo común de 6 y 9. Luego observa que ambos términos contienen x y extrae la menor potencia.",
        "El factor numérico puede ser positivo. Extrae 4a² y comprueba qué queda al dividir cada término, sin borrar el signo menos.",
        "Compara por separado los exponentes de m y n. En el factor común solo puede quedar la potencia menor compartida por todos los términos.",
    ],
    "agrupacion": [
        "Forma dos pares. Busca que al extraer un factor de cada par quede el mismo binomio en ambos.",
        "Prueba agrupar los dos primeros términos y los dos últimos. Revisa qué binomio aparece después de extraer sus factores comunes.",
        "Agrupa 6ab con −9ac, y 4b con −6c. Conserva el signo del segundo término de cada grupo y compara los binomios resultantes.",
    ],
    "trinomio_cuadrado": [
        "Extrae las raíces de los extremos. El término central debe ser dos veces el producto de esas raíces; su signo decide el binomio.",
        "Las raíces de los extremos son 2a y 3. Multiplica 2(2a)(3) y compara su signo con el término central.",
        "Toma las raíces de 9m² y 16n². El doble producto debe tener magnitud 24mn.",
    ],
    "diferencia_cuadrados": [
        "Escribe 49 como un cuadrado perfecto y aplica dos binomios conjugados.",
        "Busca las raíces cuadradas de 25a⁴ y 16b². Después usa una resta y una suma con esas mismas raíces.",
        "Calcula las raíces término a término: la potencia de cada variable debe dividirse entre dos.",
    ],
    "trinomio_simple": [
        "Busca parejas de factores de 12 y elige la que tenga suma 7. Como el producto es positivo y la suma positiva, ambos números son positivos.",
        "Como el producto es −12, los números tienen signos opuestos. Elige el par cuya suma sea −1.",
        "Un producto positivo implica signos iguales; para que la suma sea −9, ambos deben ser negativos.",
    ],
    "trinomio_general": [
        "Multiplica el coeficiente principal por el término independiente. Busca dos factores de ese producto que sumen 11; luego descompón el término central.",
        "Busca dos números cuyo producto sea 6(−2) y cuya suma sea −1. Sus signos deben ser opuestos.",
        "Usa el producto 12(−10) y busca dos números que sumen −7. Comprueba luego los dos productos cruzados.",
    ],
    "potencias_iguales": [
        "Reconoce la diferencia de cuadrados dos veces: x⁴−y⁴=(x²−y²)(x²+y²), y el primer factor aún puede descomponerse.",
        "El exponente 5 es impar. En la suma, el primer factor suma las bases; los signos del segundo factor alternan.",
        "Compara el signo de la operación y la paridad del exponente. La identidad de suma requiere exponente impar.",
        "Expresa 27b³ como el cubo de un monomio. En una diferencia de cubos, el binomio lleva resta.",
        "Identifica qué monomios elevados al cubo producen 8m³ y 125n³. La suma conserva más en el binomio.",
    ],
}


def factorization_mission(case):
    st.session_state.setdefault("factor_step", 0)
    st.session_state.setdefault("factor_correct", 0)
    st.session_state.setdefault("factor_feedback", None)
    st.session_state.setdefault("factor_waiting_next", False)
    bank = EJERCICIOS[case["variant_set"]]
    lesson = LECCIONES[case["variant_set"]]
    step = st.session_state.factor_step
    st.markdown(f'<div class="hero"><b>{case["company"]}</b><h1>{case["title"]}</h1><p>{case["mission"]} · {case["modes"][st.session_state.mode]["label"]}</p></div>', unsafe_allow_html=True)
    st.subheader("1 · ¿Qué caso de factorización es?")
    st.write(lesson["definition"])
    st.caption(lesson["recognition"])
    st.latex(lesson["pattern"])
    st.subheader("2 · Ejemplo resuelto paso a paso")
    st.latex(lesson["example"])
    for instruction in lesson["steps"]:
        st.markdown(instruction)
    st.info("**Error frecuente:** " + lesson["warning"])
    st.subheader("Contexto del caso")
    st.write(case["context"])
    st.progress(step / len(bank), text=f"Reto {min(step + 1, len(bank))} de {len(bank)}")
    if step >= len(bank):
        st.success("Terminaste los retos de este caso. Ya puedes consultar tu informe.")
        if st.button("Cerrar caso y ver mi informe", key="factor_close"):
            award(10, f"{case['id']}_cierre")
            st.session_state.finished = True
            st.session_state.page = "Informes"
            st.rerun()
        return

    if st.session_state.factor_waiting_next:
        feedback = st.session_state.factor_feedback
        st.success("Correcto. " + feedback["explanation"])
        label = "Terminar y ver informe" if step == len(bank) - 1 else "Siguiente reto"
        if st.button(label, key=f"factor_next_{case['id']}_{step}"):
            st.session_state.factor_step += 1
            st.session_state.factor_waiting_next = False
            st.session_state.factor_feedback = None
            if st.session_state.factor_step == len(bank):
                award(10, f"{case['id']}_cierre")
                st.session_state.finished = True
                st.session_state.page = "Informes"
            st.rerun()
        return

    prompt, choices, answer, explanation = bank[step]
    stage = f"Factorización · Reto {step + 1}"
    st.subheader(f"3 · Practica · Reto {step + 1} de {len(bank)}")
    st.markdown(prompt)
    selected = st.radio("Elige la factorización completa:", choices, key=f"factor_choice_{case['id']}_{step}", index=None)
    feedback = st.session_state.factor_feedback
    if feedback and feedback.get("step") == step and not feedback.get("correct"):
        st.error("Esa opción no es correcta. El caso sigue en el mismo reto; inténtalo de nuevo.")
        st.info("**Pista:** " + feedback["hint"])
    if st.button("Comprobar respuesta", key=f"factor_check_{case['id']}_{step}", disabled=selected is None):
        correct = selected == choices[answer]
        record_attempt(stage, correct, f"{case['id']}_{step}" if not correct else None)
        if correct:
            st.session_state.factor_correct += 1
            points = 90 // len(bank) + (1 if step < 90 % len(bank) else 0)
            award(points, f"{case['id']}_reto_{step}")
            st.session_state.eval_scores.setdefault(f"factor_{step}", 1.0)
            st.session_state.factor_feedback = {"step": step, "correct": True, "explanation": explanation}
            st.session_state.factor_waiting_next = True
        else:
            st.session_state.eval_scores.setdefault(f"factor_{step}", 0.0)
            st.session_state.factor_feedback = {"step": step, "correct": False, "hint": PISTAS[case["variant_set"]][step]}
        st.rerun()


def factorization_report(case):
    if not st.session_state.finished:
        st.info("Completa los retos del caso para generar tu informe.")
        return
    st.success(f"Completaste {case['title']}.")
    st.write(case["report"])
    total = len(EJERCICIOS[case["variant_set"]])
    st.metric("Respuestas correctas", f"{st.session_state.factor_correct} de {total}")
    st.subheader("Lo que practicaste")
    for goal in case["learning_goals"]:
        st.write("• " + goal)
    rows = [{"Reto": f"Reto {i + 1}", "Intentos": st.session_state.attempts.get(f"Factorización · Reto {i + 1}", 0)} for i in range(total)]
    st.table(rows)
    if st.session_state.mode == "evaluative":
        rubric = case["modes"]["evaluative"]["rubric"]
        grade = sum(item["weight"] * st.session_state.eval_scores.get(f"factor_{i}", 0.0) for i, item in enumerate(rubric)) / 100 * 5
        st.subheader("Resultado según la rúbrica")
        st.table([{"Criterio": item["label"], "Peso": f'{item["weight"]}%'} for item in rubric])
        st.metric("Tu nota", f"{grade:.2f} / 5.0")
    else:
        st.info("Este caso LAB ofrece retroalimentación y no genera calificación.")
