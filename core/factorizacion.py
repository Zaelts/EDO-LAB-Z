import streamlit as st

from core.progreso import award, record_attempt, set_eval_score


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
    "cubos": [
        ("Una suma de volúmenes se representa como x³ + 8. Aplica la identidad de suma de cubos.", ["(x + 2)(x² − 2x + 4)", "(x − 2)(x² + 2x + 4)", "(x + 2)³"], 0, "a³+b³=(a+b)(a²−ab+b²); los signos del trinomio alternan −,+."),
        ("La diferencia de volúmenes es a³ − 27b³. Ten en cuenta que 27b³=(3b)³.", ["(a − 3b)(a² + 3ab + 9b²)", "(a + 3b)(a² − 3ab + 9b²)", "(a − 27b)(a² + 9b²)"], 0, "a³−b³=(a−b)(a²+ab+b²), con b=3b."),
        ("Un prototipo combina volúmenes: 8m³ + 125n³. Reconoce las raíces cúbicas de ambos términos.", ["(2m + 5n)(4m² − 10mn + 25n²)", "(2m − 5n)(4m² + 10mn + 25n²)", "(8m + 125n)(m² + n²)"], 0, "8m³=(2m)³ y 125n³=(5n)³; para suma de cubos el término medio del trinomio es negativo."),
    ],
}


def factorization_mission(case):
    st.session_state.setdefault("factor_step", 0)
    st.session_state.setdefault("factor_correct", 0)
    bank = EJERCICIOS[case["variant_set"]]
    step = st.session_state.factor_step
    st.markdown(f'<div class="hero"><b>{case["company"]}</b><h1>{case["title"]}</h1><p>{case["mission"]} · {case["modes"][st.session_state.mode]["label"]}</p></div>', unsafe_allow_html=True)
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

    prompt, choices, answer, explanation = bank[step]
    stage = f"Factorización · Reto {step + 1}"
    st.subheader(f"{step + 1} · Factoriza y comprueba")
    st.markdown(prompt)
    selected = st.radio("Elige la factorización completa:", choices, key=f"factor_choice_{case['id']}_{step}", index=None)
    didactic = st.session_state.mode == "didactic"
    if didactic:
        with st.expander("Pista"):
            st.write("Observa primero el factor común o la identidad notable. Después verifica multiplicando los factores.")
    if st.button("Comprobar respuesta", key=f"factor_check_{case['id']}_{step}", disabled=selected is None):
        correct = selected == choices[answer]
        record_attempt(stage, correct, f"{case['id']}_{step}" if not correct else None)
        if correct:
            st.session_state.factor_correct += 1
            award(30, f"{case['id']}_reto_{step}")
            set_eval_score(f"factor_{step}", 1.0)
            st.success("Correcto. " + explanation)
        else:
            set_eval_score(f"factor_{step}", 0.0)
            if didactic:
                st.warning("Revisa los signos, exponentes y coeficientes. " + explanation)
            else:
                st.error("La factorización no reproduce todos los términos al multiplicar.")
        st.session_state.factor_step += 1
        st.rerun()


def factorization_report(case):
    if not st.session_state.finished:
        st.info("Completa los retos del caso para generar tu informe.")
        return
    st.success(f"Completaste {case['title']}.")
    st.write(case["report"])
    st.metric("Respuestas correctas", f"{st.session_state.factor_correct} de 3")
    st.subheader("Lo que practicaste")
    for goal in case["learning_goals"]:
        st.write("• " + goal)
    rows = [{"Reto": f"Reto {i + 1}", "Intentos": st.session_state.attempts.get(f"Factorización · Reto {i + 1}", 0)} for i in range(3)]
    st.table(rows)
    if st.session_state.mode == "evaluative":
        rubric = case["modes"]["evaluative"]["rubric"]
        grade = sum(item["weight"] * st.session_state.eval_scores.get(f"factor_{i}", 0.0) for i, item in enumerate(rubric)) / 100 * 5
        st.subheader("Resultado según la rúbrica")
        st.table([{"Criterio": item["label"], "Peso": f'{item["weight"]}%'} for item in rubric])
        st.metric("Tu nota", f"{grade:.2f} / 5.0")
    else:
        st.info("Este caso LAB ofrece retroalimentación y no genera calificación.")
