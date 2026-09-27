import streamlit as st
from core.cargador_casos import listar_casos,cargar_caso,cargar_curriculo
from core.progreso import init_state,award,record_attempt,set_eval_score,go_stage,reset_mission,weighted_grade
from core.navegacion import sidebar
from core.simulacion import demanda,derivada,tiempo_capacidad,figura_simulacion
from core.limites import tabla as tabla_limites, figura as figura_limites, recta_numerica, figura_bilateral_interactiva
from core.limites_avanzados import thermal_table,thermal_figure,derivative_table,derivative_figure,secant_slope
from core.exactas import exact_mission, exact_report
from core.factorizacion import factorization_mission, factorization_report

VERSION="Z-V5.27.09.2026"
AUTHOR="Yeison J. Aragón"
EMAIL="yjab08@gmail.com"

st.set_page_config(page_title=f"EDO·LAB Z | {VERSION}",page_icon="Z",layout="wide")
st.markdown("""<style>
.stApp{background:#061521;color:#eef7fb}.block-container{padding-top:4.7rem!important;max-width:1450px}
[data-testid="stSidebar"]{background:#06131e;border-right:1px solid #155274}
.brand{display:flex;gap:12px;align-items:center;border-bottom:1px solid #155274;padding:8px 0 18px}
.z{width:46px;height:46px;border:1px solid #1684b4;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:900;font-style:italic;color:#43c6ff;background:#0b3044}
.bt{font-size:26px;font-weight:800}.bt span{color:#00aeea}.sub{font-size:10px;letter-spacing:1.7px;color:#9eb5c3}
.top,.hero,.box{border:1px solid #155274;background:#0a2130;border-radius:15px;padding:18px;margin-bottom:18px}
.top{display:flex;justify-content:space-between}.cyan{color:#43c6ff}.ok{color:#27d49a}
.step{border-left:3px solid #1b5d7d;padding:8px 12px;margin:6px 0}.active{border-color:#00aeea;font-weight:700}.done{border-color:#27d49a;color:#c9f8e9}
div.stButton>button{width:100%;min-height:46px;border:1px solid #008fc7;background:#092b3e;color:white}
.footer{border-top:1px solid #155274;margin-top:25px;padding-top:12px;color:#7895a4;font-size:11px}
</style>""",unsafe_allow_html=True)

init_state()
case=cargar_caso(st.session_state.case_id)
if st.session_state.page not in {"Acceso","Ficha"}: sidebar(VERSION,AUTHOR,case)

def access():
    st.markdown('<div class="hero"><h1>Bienvenido a <span class="cyan">EDO·LAB Z</span></h1><p>Aprende, modela, experimenta y toma decisiones.</p></div>',unsafe_allow_html=True)
    name=st.text_input("¿Cómo quieres que te llamemos?",placeholder="Escribe tu nombre")
    if st.button("Comenzar"):
        if len(name.strip())<2: st.warning("Escribe el nombre que quieres usar durante esta sesión.")
        else:
            st.session_state.student_name=name.strip()
            st.session_state.page="Explorar"; st.rerun()

def home():
    st.markdown(f'<div class="hero"><h1>Hola, <span class="cyan">{st.session_state.student_name}</span>.</h1><p>Tu espacio para explorar modelos matemáticos mediante casos interactivos.</p></div>',unsafe_allow_html=True)
    if st.session_state.mission_started:
        if st.button("Continuar misión actual"): st.session_state.page="Misiones"; st.rerun()
    if st.button("Explorar contenidos"): st.session_state.page="Explorar"; st.rerun()

def explore():
    st.header("Explorar contenidos")
    curr=cargar_curriculo(); cases=listar_casos()
    areas=sorted(curr["areas"],key=lambda x:x["order"]); area=st.selectbox("1 · Área de conocimiento",[x["label"] for x in areas])
    area_obj=next(x for x in areas if x["label"]==area); subjects=sorted(area_obj["subjects"],key=lambda x:x["order"])
    subject=st.selectbox("2 · Asignatura",[x["label"] for x in subjects]); subj=next(x for x in subjects if x["label"]==subject)
    st.session_state.area,st.session_state.subject=area,subject
    st.subheader(f"Ruta de aprendizaje · {subject}")
    st.caption("El orden es recomendado, no obligatorio. Puedes entrar a un tema si ya cuentas con los conocimientos previos.")
    topics=sorted(subj["topics"],key=lambda x:x["order"]); available=[]
    topic_rows=[]
    for t in topics:
        n=sum(1 for c in cases if c.get("subject_id")==subj["id"] and c.get("topic_id")==t["id"])
        status=(f"{n} caso disponible" if n==1 else f"{n} casos disponibles") if n else "Próximamente"
        topic_rows.append({"Orden":f'{t["order"]:02d}',"Tema":t["label"],"Estado":status})
        if n: available.append(t)
    with st.expander("Ver ruta completa de temas y disponibilidad",expanded=False):
        st.table(topic_rows)
        st.caption("La ruta muestra el orden recomendado. Los temas sin caso permanecen visibles como referencia curricular.")
    if not available: st.info("Todavía no hay casos disponibles para esta asignatura."); return
    chosen=st.selectbox("3 · Tema que deseas trabajar",[t["label"] for t in available]); topic=next(t for t in available if t["label"]==chosen)
    st.session_state.topic=chosen
    if topic.get("prerequisites"): st.info("**Conocimientos recomendados:** "+", ".join(topic["prerequisites"])+". Puedes continuar si ya los manejas.")
    filtered=[c for c in cases if c.get("subject_id")==subj["id"] and c.get("topic_id")==topic["id"]]
    st.subheader("4 · Casos disponibles")
    for c in filtered:
        st.markdown(f'<div class="box"><b>{c["mission"]}</b><h2>{c["title"]}</h2><p>{c["company"]}</p><p><b>Dificultad:</b> {c["difficulty"]} · <b>Tiempo estimado:</b> {c["estimated_time"]}</p></div>',unsafe_allow_html=True)
        x,y=st.columns(2)
        with x:
            if st.button("LAB · Ver caso didáctico",key=c["id"]+"_lab"):
                st.session_state.case_id=c["id"]; st.session_state.mode="didactic"; st.session_state.page="Ficha"; st.rerun()
        with y:
            if st.button("EVAL · Ver evaluación",key=c["id"]+"_eval"):
                st.session_state.case_id=c["id"]; st.session_state.mode="evaluative"; st.session_state.page="Ficha"; st.rerun()

def mission_card():
    c=cargar_caso(st.session_state.case_id); mode=c["modes"][st.session_state.mode]
    st.header(c["title"]); st.write(c["company"])
    st.markdown(f"**{mode['label']}** — {mode['description']}")
    st.write(f"**Área:** {c['area']}  \n**Asignatura:** {c['subject']}  \n**Tema:** {c['topic']}  \n**Dificultad:** {c['difficulty']}  \n**Tiempo estimado:** {c['estimated_time']}")
    if c.get("prerequisites"):
        st.info("**Antes de comenzar:** se recomienda manejar "+", ".join(c["prerequisites"])+". No es un bloqueo: puedes continuar si ya cuentas con estas bases.")
    st.subheader("En esta misión trabajarás en:")
    for g in c["learning_goals"]: st.write("• "+g)
    if st.session_state.mode=="evaluative":
        st.subheader("Rúbrica de evaluación")
        st.write("Conocerás estos criterios antes de comenzar. Escala del caso: 0,0 a 5,0.")
        st.table([{"Criterio":x["label"],"Peso":f'{x["weight"]}%'} for x in mode["rubric"]])
        st.warning("En modo EVAL la asistencia es reducida. La decisión final queda registrada al confirmarla.")
    else:
        st.info("Este caso es de aprendizaje: puedes recibir pistas y tus intentos se usan para darte retroalimentación. No genera nota.")
    if st.button("Iniciar misión"):
        reset_mission(increment=False)
        st.session_state.page="Misiones"
        st.rerun()

def feedback_diagnostic(selected,c):
    correct={"Primer orden","Lineal","Separable"}
    messages=[]
    for wrong in set(selected)-correct:
        if wrong in c["diagnostic_feedback"]: messages.append(c["diagnostic_feedback"][wrong])
    for missing in correct-set(selected):
        key="missing_"+missing
        if key in c["diagnostic_feedback"]: messages.append(c["diagnostic_feedback"][key])
    return messages

def limits_mission():
    c=case; sc=c["scenario"]; did=st.session_state.mode=="didactic"; step=st.session_state.limit_step
    if step==1:
        st.markdown(f'<div class="hero"><b>{c["company"]}</b><h1>{c["title"]}</h1><p>{c["mission"]} · {c["modes"][st.session_state.mode]["label"]}</p></div>',unsafe_allow_html=True)
        st.write(sc["story"])
        st.markdown("""
### Caso de contexto · Sensor de nivel
Un **sistema de llenado automático** vigila el nivel de un tanque. Cerca del instante crítico `x = 2`, el sensor no entrega una lectura válida exactamente en ese punto, pero sí registra mediciones inmediatamente antes y después. Tu tarea es decidir si aun así podemos anticipar **hacia qué nivel se dirige el sistema**.

En situaciones reales, esta idea permite interpretar procesos cerca de un umbral aun cuando una medición puntual falte. El mismo razonamiento será útil después para velocidad instantánea, continuidad y derivadas.
""")
        st.info("Un límite describe el valor **L** al que se aproxima f(x) cuando **x se acerca a a**. No exige que x sea exactamente a ni que f(a) exista.")
        st.latex(r"\lim_{x\to a}f(x)=L")
        st.markdown("El comportamiento normalizado del sensor se representa mediante:")
        st.latex(sc["function_latex"])
    else:
        st.caption(f"**{c['mission']} · {c['title']}**  |  Etapa {step} de 4  |  Caso: sensor de nivel cerca del instante crítico x=2")
    if step==1:
        st.header("1 · Comprender la aproximación")
        st.write("Antes de operar, observa cómo podemos acercarnos a 2 desde números menores y desde números mayores.")
        st.plotly_chart(recta_numerica(),use_container_width=True,key="number_line_limits")
        st.markdown("""
**Desde la izquierda:** `1.5 → 1.9 → 1.99 → 1.999 → 2`

**Desde la derecha:** `2 ← 2.001 ← 2.01 ← 2.1 ← 2.5`

Los números no tienen que llegar a 2. Lo importante es que pueden quedar **tan cerca de 2 como queramos**. Ahora preguntaremos qué ocurre simultáneamente con **f(x)**.
""")
        st.subheader("Antes de sustituir")
        q=st.radio("¿Qué ocurre si sustituyes directamente x=2?",["Se obtiene 4","Aparece la forma 0/0","El límite necesariamente no existe","La función vale infinito"],key="lim_q1")
        if st.button("Validar observación"):
            ok=q=="Aparece la forma 0/0"; record_attempt("Límite · observación inicial",ok,q if not ok else None)
            if ok: set_eval_score("concept",1); st.session_state.limit_step=2; st.rerun()
            elif did: st.warning("Calcula numerador y denominador por separado. Sustituir en el punto no es todavía estudiar el comportamiento alrededor.")
            else: st.warning("Revisa numerador y denominador al sustituir x=2.")
    elif step==2:
        st.header("2 · Acercarnos por ambos lados")
        st.write("La recta numérica mostraba el movimiento de **x**. Las tablas añaden la segunda parte: para cada x cercano a 2 calculamos su correspondiente **f(x)**.")
        st.info("**Bilateral** significa mirar los dos lados del punto. El límite en x=2 existe si el destino por la izquierda y el destino por la derecha existen y son el **mismo número**. El valor exacto f(2) no decide esta comparación.")
        st.latex(r"\lim_{x\to2}f(x)=L\quad\Longleftrightarrow\quad\lim_{x\to2^-}f(x)=L=\lim_{x\to2^+}f(x)")
        with st.expander("Experimenta: ¿qué pasa si los dos lados llegan a alturas diferentes?",expanded=did):
            a,b=st.columns(2)
            with a: izq=st.slider("Destino por la izquierda (azul)",2,6,4,key="bilat_izq")
            with b: der=st.slider("Destino por la derecha (naranja)",2,6,4,key="bilat_der")
            st.plotly_chart(figura_bilateral_interactiva(izq,der),use_container_width=True,key="bilateral_lab")
            if izq==der: st.success(f"Ambos lados llegan a {izq}: el límite bilateral **existe** y vale {izq}, incluso si no conocemos f(2).")
            else: st.warning(f"Izquierda → {izq}; derecha → {der}. Como los destinos difieren, **no existe** un único límite bilateral. No se promedian.")
            st.caption("Modelo de comparación: mueve un control por vez. Los círculos de borde amarillo señalan valores a los que se acerca cada rama; no son mediciones en x=2.")
        st.markdown("**¿De dónde sale un valor de la tabla?** Por ejemplo, para una medición inmediatamente anterior, `x = 1.9`:")
        st.latex(r"f(1.9)=\frac{(1.9)^2-4}{1.9-2}=\frac{3.61-4}{-0.1}=\frac{-0.39}{-0.1}=3.9")
        st.caption("Las demás filas se calculan de la misma forma. En el caso del sensor, cada fila simula una lectura tomada cada vez más cerca del instante crítico.")
        x,y=st.columns(2)
        with x: st.write("**Por la izquierda**"); st.table(tabla_limites(sc["left"]))
        with y: st.write("**Por la derecha**"); st.table(tabla_limites(sc["right"]))
        q=st.radio("¿A qué valor se acercan los valores de f(x)?",["0","2","4","No muestran tendencia"],key="lim_q2")
        if st.button("Validar aproximación"):
            ok=q=="4"; record_attempt("Límite · tabla y laterales",ok,q if not ok else None)
            if ok: set_eval_score("sides",1); set_eval_score("graph",.5); st.session_state.limit_step=3; st.rerun()
            elif did: st.warning("Observa los últimos valores de ambas tablas: buscamos el destino de f(x), no f(2).")
            else: st.warning("Observa especialmente los valores más cercanos a x=2.")
    elif step==3:
        st.header("3 · Ver el comportamiento")
        st.plotly_chart(figura_limites(),use_container_width=True,key="limits_behavior_graph")
        st.markdown("""
La gráfica reúne lo que observaste en las tablas. La línea **azul continua** representa `x < 2`; la **naranja discontinua**, `x > 2`. El círculo de centro oscuro y borde amarillo es un **círculo abierto**: la expresión original **no está definida exactamente en x=2**. Sin embargo, ambas ramas se acercan a la misma altura: **4**.

Puedes mover, ampliar o seleccionar la gráfica. Esas acciones sirven para explorarla y no modifican la respuesta matemática.
""")
        q=st.radio("Hay un hueco en x=2. ¿Qué podemos concluir?",["Por tener un hueco, el límite no existe","El límite puede existir aunque f(2) no esté definida","El límite es 2","Solo existe por la izquierda"],key="lim_q3")
        if st.button("Validar interpretación"):
            ok=q=="El límite puede existir aunque f(2) no esté definida"; record_attempt("Límite · gráfica",ok,q if not ok else None)
            if ok: set_eval_score("graph",1); set_eval_score("distinction",1); st.session_state.limit_step=4; st.rerun()
            elif did: st.warning("El límite estudia qué ocurre cerca del punto. Comprueba si ambas ramas se aproximan al mismo valor.")
            else: st.warning("Distingue el comportamiento alrededor de x=2 del valor exacto de la función.")
    else:
        st.header("4 · Construir la conclusión")
        st.write("Para x≠2 podemos factorizar y simplificar:")
        st.latex(r"\frac{x^2-4}{x-2}=\frac{(x-2)(x+2)}{x-2}=x+2,\qquad x\neq2")
        st.markdown("""
**¿Qué ocurrió al factorizar?** El numerador `x²−4` es una diferencia de cuadrados, por eso se escribe `(x−2)(x+2)`. Para valores **distintos de 2**, el factor `(x−2)` aparece arriba y abajo y puede simplificarse. Así descubrimos que, alrededor del punto problemático, la expresión se comporta como `x+2`.

Esto **no cambia la función original en x=2** ni rellena el hueco: allí el denominador original sigue siendo cero. La simplificación solamente nos permite estudiar con claridad lo que ocurre **cerca** de 2.

**Volvamos al sensor:** aunque la lectura exacta del instante crítico falte, las mediciones inmediatamente anteriores y posteriores se aproximan al mismo nivel normalizado, `4`. Por eso el límite permite anticipar el comportamiento del proceso sin inventar una medición que no existe.
""")
        q=st.radio("Selecciona la conclusión:",["El límite es 0 porque aparece 0/0","El límite no existe porque f(2) no está definida","El límite es 4 porque ambos lados se aproximan a 4","El límite es 2 porque x se aproxima a 2"],key="lim_q4")
        if not st.session_state.limit_done:
            if st.button("Confirmar conclusión"):
                ok=q.startswith("El límite es 4"); record_attempt("Límite · conclusión",ok,q if not ok else None)
                if ok: set_eval_score("conclusion",1); st.session_state.limit_done=True; st.rerun()
                elif did: st.warning("Compara el destino de la función por izquierda y por derecha.")
                else: st.warning("Revisa la evidencia tabular y gráfica.")
        else:
            st.success("✓ Construiste la conclusión con evidencia tabular, gráfica y algebraica.")
            st.latex(r"\boxed{\lim_{x\to2}\frac{x^2-4}{x-2}=4}")
            st.info("Idea clave: el límite describe a qué valor se aproxima f(x). No exige que la función esté definida exactamente allí.")
            if st.button("Cerrar caso y ver mi informe"):
                st.session_state.finished=True; st.session_state.page="Informes"; st.rerun()

def limits_sides_mission():
    c=case; sc=c["scenario"]; did=st.session_state.mode=="didactic"; step=st.session_state.limit2_step
    if step==1:
        st.markdown(f'<div class="hero"><b>{c["company"]}</b><h1>{c["title"]}</h1><p>{c["mission"]} · {c["modes"][st.session_state.mode]["label"]}</p></div>',unsafe_allow_html=True)
        st.write(sc["story"])
        st.markdown("""
### El reto
En el caso anterior, izquierda y derecha se aproximaban al mismo valor. Ahora el sistema **cambia de régimen** en `t=5 min`. Debes comprobar si las mediciones de ambos lados cuentan la misma historia.

En un proceso real esto importa: si el comportamiento antes y después de un umbral es diferente, resumir ambos lados con un único valor puede ocultar una discontinuidad relevante.
""")
        st.latex(r"\lim_{t\to5^-}T(t)\quad\text{y}\quad\lim_{t\to5^+}T(t)")
        if st.button("Examinar las mediciones"): st.session_state.limit2_step=2; st.rerun()
    elif step==2:
        st.caption(f"**{c['mission']} · {c['title']}** | Etapa 2 de 4 | transición térmica en t=5 min")
        st.header("2 · Leer cada lado por separado")
        a,b=st.columns(2)
        with a: st.write("**Antes de 5 min · izquierda**"); st.table(thermal_table(sc["left_times"]))
        with b: st.write("**Después de 5 min · derecha**"); st.table(thermal_table(sc["right_times"]))
        st.markdown("Ejemplo: cuando `t=4.9`, el régimen anterior da `T(4.9)=40+0.8(4.9−5)=39.92 °C`. Al acercarnos más a 5 por ese lado, las lecturas se aproximan a **40 °C**.")
        q1=st.radio("¿A qué valor se aproxima T(t) por la izquierda?",["40 °C","43 °C","46 °C","5 °C"],key="l2q1")
        q2=st.radio("¿Y por la derecha?",["40 °C","43 °C","46 °C","5 °C"],key="l2q2")
        if st.button("Validar límites laterales"):
            ok=q1=="40 °C" and q2=="46 °C"; record_attempt("Laterales · identificación",ok)
            if ok:
                set_eval_score("left",1);set_eval_score("right",1);st.session_state.limit2_step=3;st.rerun()
            elif did: st.warning("Lee los valores más cercanos a 5 en cada tabla. No los promedies: cada lado se analiza por separado.")
            else: st.warning("Revisa por separado las mediciones inmediatamente anteriores y posteriores.")
    elif step==3:
        st.caption(f"**{c['mission']} · {c['title']}** | Etapa 3 de 4 | ¿existe un único límite?")
        st.header("3 · Ver la transición")
        st.plotly_chart(thermal_figure(),use_container_width=True,key="thermal_limit_graph")
        st.info("La línea azul continua llega a un **círculo abierto** en 40 °C: ese valor no se alcanza desde el régimen anterior en t=5. La línea naranja discontinua se aproxima a 46 °C y el **punto lleno** muestra T(5)=46 °C. Los destinos laterales son distintos.")
        q=st.radio("Si los límites laterales son diferentes, ¿qué ocurre con el límite bilateral?",[
            "Existe y vale el promedio 43 °C","No existe un único límite bilateral","Vale 46 °C porque ocurre después","Vale 40 °C porque ocurre antes"],key="l2q3")
        if st.button("Validar existencia"):
            ok=q=="No existe un único límite bilateral";record_attempt("Laterales · existencia",ok)
            if ok:
                set_eval_score("graph",1);set_eval_score("existence",1);st.session_state.limit2_step=4;st.rerun()
            elif did: st.warning("Para que exista un límite bilateral, izquierda y derecha deben aproximarse al mismo valor.")
            else: st.warning("Compara los dos destinos laterales.")
    else:
        st.caption(f"**{c['mission']} · {c['title']}** | Etapa 4 de 4 | decisión del equipo")
        st.header("4 · Interpretar el resultado en el caso")
        st.latex(r"\lim_{t\to5^-}T(t)=40,\qquad \lim_{t\to5^+}T(t)=46")
        st.write("Como los dos valores son distintos, no existe un único número L al que T(t) se aproxime desde ambos lados.")
        q=st.radio("¿Qué debería reportar el equipo?",[
            "Una temperatura límite única de 43 °C","Que la transición presenta comportamientos laterales distintos y no hay límite bilateral",
            "Que faltan datos y no puede decirse nada","Que el valor correcto siempre es el del régimen posterior"],key="l2q4")
        if not st.session_state.limit2_done:
            if st.button("Confirmar interpretación"):
                ok=q.startswith("Que la transición presenta");record_attempt("Laterales · contexto",ok)
                if ok:
                    set_eval_score("context",1);st.session_state.limit2_done=True;st.rerun()
                elif did: st.warning("La conclusión debe conservar la información de ambos lados, no esconderla en un promedio.")
                else: st.warning("Relaciona la conclusión matemática con la transición del sistema.")
        else:
            st.success("✓ Identificaste que la existencia de un límite bilateral exige acuerdo entre ambos límites laterales.")
            st.info("Idea clave: que la función tenga valores a ambos lados no garantiza que exista un único límite.")
            if st.button("Cerrar caso y ver mi informe",key="close_l2"):
                st.session_state.finished=True;st.session_state.page="Informes";st.rerun()

def derivative_limit_mission():
    c=case; sc=c["scenario"]; did=st.session_state.mode=="didactic"; step=st.session_state.deriv_step; a=sc["a"]
    if step==1:
        st.markdown(f'<div class="hero"><b>{c["company"]}</b><h1>{c["title"]}</h1><p>{c["mission"]} · {c["modes"][st.session_state.mode]["label"]}</p></div>',unsafe_allow_html=True)
        st.write(sc["story"])
        st.markdown("""
### De una pregunta física a una idea matemática
Entre dos instantes sí podemos calcular una **velocidad promedio**. El problema aparece cuando queremos la velocidad en un solo instante: un intervalo de duración cero produciría una división entre cero.

La estrategia será usar límites: calcularemos velocidades promedio en intervalos cada vez más pequeños y observaremos hacia qué valor se aproximan.
""")
        st.latex(r"s(t)=t^2")
        st.latex(r"v_{\mathrm{prom}}=\frac{s(2+h)-s(2)}{h}")
        if st.button("Comenzar con un intervalo"): st.session_state.deriv_step=2;st.rerun()
    elif step==2:
        st.caption(f"**{c['mission']} · {c['title']}** | Etapa 2 de 4 | velocidades promedio")
        st.header("2 · Acortar el intervalo")
        st.markdown("Por ejemplo, con `h=1`, comparamos `t=2` con `t=3`:")
        st.latex(r"\frac{s(3)-s(2)}{3-2}=\frac{9-4}{1}=5\ \mathrm{m/s}")
        st.table(derivative_table(a,sc["h_values"]))
        q=st.radio("Cuando h se hace cada vez más pequeño, ¿a qué valor parecen acercarse las velocidades promedio?",["2 m/s","4 m/s","5 m/s","0 m/s"],key="dlimq1")
        if st.button("Validar tendencia"):
            ok=q=="4 m/s";record_attempt("Derivada · velocidades promedio",ok)
            if ok:
                set_eval_score("average",1);set_eval_score("limit",.5);st.session_state.deriv_step=3;st.rerun()
            elif did: st.warning("Observa las últimas filas: 4.5, 4.1, 4.01... ¿qué número parece ser el destino?")
            else: st.warning("Observa especialmente los intervalos más pequeños.")
    elif step==3:
        st.caption(f"**{c['mission']} · {c['title']}** | Etapa 3 de 4 | secante → tangente")
        st.header("3 · Manipular la secante")
        h=st.slider("Tamaño del intervalo h",0.05,2.0,1.0,0.05,key="derivative_h")
        st.plotly_chart(derivative_figure(a,h),use_container_width=True,key="derivative_secant_graph")
        st.metric("Pendiente de la secante / velocidad promedio",f"{secant_slope(a,h):.3f} m/s")
        st.write("Reduce `h`. El punto Q se acerca a P y la secante se aproxima a la tangente. Al mismo tiempo, su pendiente se aproxima a 4.")
        q=st.radio("¿Qué representa geométricamente la velocidad promedio?",[
            "La pendiente de la recta secante entre P y Q","La altura de la curva","El área bajo la curva","La pendiente del eje horizontal"],key="dlimq2")
        if st.button("Validar interpretación geométrica"):
            ok=q.startswith("La pendiente de la recta secante");record_attempt("Derivada · secante",ok)
            if ok:
                set_eval_score("secant",1);set_eval_score("tangent",1);st.session_state.deriv_step=4;st.rerun()
            elif did: st.warning("La razón cambio de posición / cambio de tiempo es una pendiente entre dos puntos.")
            else: st.warning("Relaciona el cociente incremental con la pendiente entre P y Q.")
    else:
        st.caption(f"**{c['mission']} · {c['title']}** | Etapa 4 de 4 | nace la derivada")
        st.header("4 · Del límite a la derivada")
        st.write("Ahora podemos nombrar el valor que apareció cuando el intervalo se hizo arbitrariamente pequeño: la **derivada**.")
        st.latex(r"s'(2)=\lim_{h\to0}\frac{s(2+h)-s(2)}{h}")
        st.latex(r"=\lim_{h\to0}\frac{(2+h)^2-4}{h}=\lim_{h\to0}(4+h)=4\ \mathrm{m/s}")
        st.markdown("Factorizar/simplificar aquí no significa usar `h=0` en la fracción original. Trabajamos con `h≠0` y luego estudiamos qué ocurre **cuando h se aproxima a 0**.")
        q=st.radio("Completa la idea central:",[
            "La derivada es el límite de velocidades promedio cuando el intervalo tiende a cero",
            "La derivada se obtiene sustituyendo h=0 desde el inicio",
            "La derivada siempre es igual a la posición","Un límite y una derivada no están relacionados"],key="dlimq3")
        if not st.session_state.deriv_done:
            if st.button("Confirmar puente hacia derivadas"):
                ok=q.startswith("La derivada es el límite");record_attempt("Derivada · definición",ok)
                if ok:
                    set_eval_score("limit",1);set_eval_score("definition",1);st.session_state.deriv_done=True;st.rerun()
                elif did: st.warning("Piensa en lo que hiciste: calculaste cocientes promedio y estudiaste su límite cuando h→0.")
                else: st.warning("Relaciona el cociente incremental con el proceso de límite.")
        else:
            st.success("✓ Construiste la derivada desde el concepto de límite.")
            st.info("Puente curricular: en el tema Derivadas podrás generalizar esta idea, estudiar reglas de derivación y resolver nuevas aplicaciones.")
            if st.button("Cerrar caso y ver mi informe",key="close_deriv"):
                st.session_state.finished=True;st.session_state.page="Informes";st.rerun()

def mission():
    if case.get("case_type") == "factorization": return factorization_mission(case)
    if case.get("case_type")=="limit_intro": return limits_mission()
    if case.get("case_type")=="limit_sides": return limits_sides_mission()
    if case.get("case_type")=="derivative_limit": return derivative_limit_mission()
    if case.get("case_type"," ").startswith("exact_"): return exact_mission(case)
    c=case; s=st.session_state.stage; did=st.session_state.mode=="didactic"
    st.markdown(f'<div class="hero"><b>{c["company"]}</b><h1>🏭 {c["title"]}</h1><p>{c["mission"]} · {c["modes"][st.session_state.mode]["label"]}</p></div>',unsafe_allow_html=True)
    if s==1:
        st.header("1 · Contexto operativo")
        for p in c["briefing"]: st.write(p)
        d=c["data"]; a,b,z=st.columns(3)
        a.metric("Demanda inicial",f'{d["initial_demand"]:,.0f} u/mes'.replace(",",".")); b.metric("Capacidad actual",f'{d["capacity"]:,.0f} u/mes'.replace(",",".")); z.metric("Escenario de crecimiento",f'{d["growth_rate"]*100:.0f} % mensual')
        if st.button("Aceptar misión → Identificar variables"): award(5,"contexto"); go_stage(2)

    elif s==2:
        st.header("2 · Identificación de variables")
        a=st.radio("¿Cuál es la variable principal que necesitamos modelar?",["Número de trabajadores","Demanda mensual","Costo de producción","Capacidad de la planta"])
        if not st.session_state.var_ok:
            if st.button("Validar respuesta"):
                ok=a=="Demanda mensual"; record_attempt("Variables",ok,a if not ok else None)
                if ok:
                    award(10,"var"); st.session_state.var_ok=True; set_eval_score("variables",1.0); st.rerun()
                elif did: st.warning("La variable debe representar la cantidad que queremos proyectar a través del tiempo.")
                else: st.warning("Respuesta registrada. Revisa el objetivo del problema e inténtalo de nuevo.")
        else:
            st.success("✓ D(t) representa la demanda mensual en el tiempo t."); st.latex(r"D(t)=\text{demanda mensual en el tiempo }t")
            if st.button("Continuar → Construir modelo"): go_stage(3)

    elif s==3:
        st.header("3 · Construcción del modelo")
        st.write("El escenario base afirma que la rapidez de crecimiento de la demanda es proporcional a la demanda existente.")
        b=st.radio("¿Qué comportamiento expresa esa afirmación?",["Permanece constante","Es aproximadamente lineal","Presenta crecimiento proporcional","Disminuye"])
        m=st.radio("Completa el modelo: dD/dt = ?",["0.08","0.08 D","8 D","D + 0.08"])
        if not st.session_state.model_ok:
            if st.button("Validar modelo"):
                ok=b=="Presenta crecimiento proporcional" and m=="0.08 D"; record_attempt("Modelo",ok,"modelo" if not ok else None)
                if ok:
                    award(20,"model"); st.session_state.model_ok=True; set_eval_score("model",1.0); st.rerun()
                elif did:
                    st.warning("Pista: 'proporcional a la demanda' significa que la tasa depende de D. Además, 8 % = 0,08.")
                else: st.warning("El modelo aún no es consistente con el enunciado. Revisa proporcionalidad y unidades.")
        else:
            st.success("✓ Modelo construido."); st.latex(r"\frac{dD}{dt}=0.08D")
            if st.button("Continuar → Analizar cómo resolverlo"): go_stage(4)

    elif s==4:
        st.header("4 · Del modelo a la solución")
        st.info("Antes de elegir un método, debemos reconocer la estructura de la EDO. Clasificarla no es un fin aislado: nos ayuda a decidir qué herramientas matemáticas son apropiadas.")
        purpose=st.radio("¿Qué significa resolver este modelo?",["Encontrar solo la derivada","Encontrar una función D(t) que describa la demanda en el tiempo","Eliminar t","Convertir D en una constante"],key="purpose")
        if not st.session_state.purpose_ok:
            if st.button("Validar propósito"):
                ok=purpose=="Encontrar una función D(t) que describa la demanda en el tiempo"; record_attempt("Propósito de resolución",ok,"proposito" if not ok else None)
                if ok: st.session_state.purpose_ok=True; st.rerun()
                elif did: st.warning("La organización necesita estimar la demanda en distintos instantes. ¿Qué objeto matemático permitiría hacerlo?")
                else: st.warning("Revisa qué información debe producir una solución de la EDO.")
        else:
            st.success("✓ Buscamos una función D(t) que podamos evaluar.")
            st.subheader("4.2 · Diagnosticar la ecuación")
            st.write("Observa el modelo y selecciona **todas las características que puedas justificar a partir de su forma**. Este diagnóstico servirá para elegir el método.")
            st.latex(r"\frac{dD}{dt}=0.08D")
            opts=["Primer orden","Lineal","Separable","Exacta en la forma mostrada","Segundo orden","No lineal"]
            selected=st.multiselect("Características del modelo:",opts,key="classification")
            if not st.session_state.class_ok:
                if st.button("Validar diagnóstico"):
                    ok=set(selected)=={"Primer orden","Lineal","Separable"}; record_attempt("Diagnóstico",ok,"diagnostico" if not ok else None)
                    if ok:
                        award(10,"class"); st.session_state.class_ok=True; st.rerun()
                    elif did:
                        for msg in feedback_diagnostic(selected,c): st.warning(msg)
                    else: st.warning("El diagnóstico no está completo o contiene una clasificación que requiere revisión.")
            else:
                st.success("✓ Primer orden, lineal y separable.")
                st.info("Una EDO puede admitir más de un método. Aquí variables separables resulta especialmente directo; también puede tratarse como lineal de primer orden.")
                method=st.radio("¿Qué método elegirías para este desarrollo?",["Variables separables","Ecuaciones exactas","Cauchy–Euler","Transformada de Laplace"],key="method")
                if not st.session_state.method_ok:
                    if st.button("Validar método"):
                        ok=method=="Variables separables"; record_attempt("Método",ok,method if not ok else None)
                        if ok:
                            st.session_state.method_ok=True; set_eval_score("method",1.0); st.rerun()
                        elif did and method=="Ecuaciones exactas": st.warning("Las exactas serán importantes en otros casos. Aquí intenta primero reorganizar la ecuación: ¿puedes dejar D y dD en un lado y t y dt en el otro?")
                        elif did: st.warning("Busca un método que aproveche directamente que las variables pueden quedar en lados distintos.")
                        else: st.warning("El método elegido no es el más directo para el desarrollo solicitado.")
                else:
                    st.success("✓ Variables separables.")
                    st.latex(r"\frac{1}{D}\,dD=0.08\,dt")
                    st.subheader("4.3 · Integrar y despejar")
                    st.latex(r"\int\frac{1}{D}\,dD=\int0.08\,dt")
                    st.latex(r"\ln|D|=0.08t+C")
                    st.write("Para deshacer el logaritmo natural aplicamos la función exponencial a ambos lados:")
                    st.latex(r"e^{\ln|D|}=e^{0.08t+C}")
                    st.latex(r"|D|=e^{0.08t}e^C")
                    st.write("Como C es constante, también lo es $e^C$. Podemos llamarla K. Al absorber el signo del valor absoluto en una constante no nula:")
                    st.latex(r"D(t)=Ke^{0.08t}")
                    st.write("Es habitual volver a llamar **C** a esa nueva constante. Por eso la solución general también se escribe:")
                    st.latex(r"D(t)=Ce^{0.08t}")
                    st.subheader("4.4 · ¿Qué es una familia de soluciones?")
                    st.write("La EDO fija la **ley de crecimiento**, pero todavía no fija el valor desde el que comienza la demanda. Por eso distintos valores de la constante producen distintas curvas que satisfacen la misma ecuación:")
                    a,b,z=st.columns(3)
                    a.latex(r"D_1(t)=3000e^{0.08t}"); b.latex(r"D_2(t)=5000e^{0.08t}"); z.latex(r"D_3(t)=7000e^{0.08t}")
                    st.info("Estas curvas forman una familia: comparten la misma regla de cambio, pero tienen condiciones iniciales diferentes.")
                    st.subheader("4.5 · La condición inicial selecciona una curva")
                    st.write("Para este caso sabemos que D(0)=5000. Esa información elige, entre toda la familia, la curva que representa la situación analizada.")
                    st.latex(r"D(0)=5000\Rightarrow 5000=Ke^0\Rightarrow K=5000")
                    st.latex(r"\boxed{D(t)=5000e^{0.08t}}")
                    if st.button("Continuar → Laboratorio de simulación"):
                        award(15,"solve"); set_eval_score("solution",1.0); go_stage(5)

    elif s==5:
        st.header("5 · Laboratorio de simulación")
        d=c["data"]; a,b,z=st.columns(3)
        with a: d0=st.number_input("Demanda inicial",1000,20000,d["initial_demand"],500)
        with b: rp=st.slider("Crecimiento mensual (%)",1.0,15.0,d["growth_rate"]*100,.5)
        with z: cap=st.number_input("Capacidad",5000,30000,d["capacity"],500)
        k=rp/100
        st.write("La gráfica conecta la solución con su tasa instantánea de cambio:")
        st.latex(fr"D(t)={d0}e^{{{k:.3f}t}}\qquad D'(t)={k:.3f}D(t)")
        t=st.slider("Analizar el comportamiento en el mes t",0.0,12.0,6.0,.5)
        fam=st.checkbox("Mostrar familia de soluciones",True)
        st.plotly_chart(figura_simulacion(d0,k,cap,t,fam),use_container_width=True)
        x,y,q=st.columns(3)
        x.metric(f"D({t:g})",f"{demanda(t,d0,k):,.0f} u/mes"); y.metric(f"D'({t:g})",f"{derivada(t,d0,k):,.0f} u/mes²")
        tc=tiempo_capacidad(d0,k,cap); q.metric("Tiempo hasta capacidad",f"{tc:.2f} meses" if tc else "No aplica")
        st.info("Explora la gráfica: cambia demanda inicial, tasa de crecimiento, capacidad y tiempo. Pasa el cursor sobre curvas, punto y tangente. Interpreta cada cambio como una decisión o supuesto del escenario real; la línea discontinua representa la capacidad máxima configurada.")
        with st.expander("Conectar familia, condición inicial y gráfica"):
            st.write("Las curvas discontinuas obedecen la misma ley D'=kD pero parten de valores iniciales diferentes. La curva destacada corresponde al valor D(0) seleccionado. La condición inicial convierte una familia de soluciones en una solución particular.")
        if st.button("Confirmar análisis → Decisión final"):
            record_attempt("Simulación e interpretación",True); set_eval_score("interpretation",1.0); go_stage(6)

    else:
        st.header("6 · Decisión final")
        d=c["data"]; tc=tiempo_capacidad(d["initial_demand"],d["growth_rate"],d["capacity"])
        st.metric("Punto crítico estimado en el escenario base",f"{tc:.2f} meses")
        st.warning("Una proyección depende de sus supuestos. Considera también incertidumbre y tiempo de implementación.")
        labels=[o["label"] for o in c["decision_options"]]
        choice=st.radio("¿Qué recomendarías a partir del análisis?",labels,key="decision_choice",disabled=bool(st.session_state.ending))
        if not st.session_state.ending:
            if not st.session_state.decision_confirm_pending:
                if st.button("Revisar y confirmar decisión"):
                    st.session_state.decision_confirm_pending=True; st.rerun()
            else:
                st.warning("Esta decisión cerrará este intento de la misión. Para explorar otro desenlace tendrás que iniciar un nuevo intento y resolver nuevamente el caso.")
                a,b=st.columns(2)
                with a:
                    if st.button("Volver y revisar"):
                        st.session_state.decision_confirm_pending=False; st.rerun()
                with b:
                    if st.button("Confirmar decisión final"):
                        selected=next(o for o in c["decision_options"] if o["label"]==choice)
                        st.session_state.ending=selected["id"]; record_attempt("Decisión final",True)
                        # decision score: rewards evidence-aware option, but all outcomes remain explainable
                        set_eval_score("decision",1.0 if selected["id"]=="C" else (.7 if selected["id"]=="B" else .4))
                        st.rerun()
        else:
            selected=next(o for o in c["decision_options"] if o["id"]==st.session_state.ending)
            if selected["ending"]=="final_favorable": st.success(f'### {selected["title"]}\n{selected["story"]}')
            elif selected["ending"]=="final_intermedio": st.warning(f'### {selected["title"]}\n{selected["story"]}')
            else: st.error(f'### {selected["title"]}\n{selected["story"]}')
            st.info("**Qué puedes aprender de este desenlace:** "+selected["lesson"])
            st.session_state.reflection=st.text_area("Antes de cerrar: ¿qué dato, supuesto o riesgo fue decisivo en tu recomendación?",value=st.session_state.reflection)
            if st.button("Cerrar misión y ver mi informe"):
                if len(st.session_state.reflection.strip())<30: st.warning("Escribe una reflexión un poco más completa para cerrar tu análisis.")
                else:
                    award(20,"final"); st.session_state.finished=True; st.session_state.page="Informes"; st.rerun()

def progress():
    st.header(f"Tu progreso, {st.session_state.student_name}")
    st.metric("Puntaje de recorrido",f"{st.session_state.score}/100")
    st.progress(min(st.session_state.score/100,1.0))
    if st.session_state.attempts:
        st.subheader("Intentos registrados en esta misión")
        st.table([{"Etapa":k,"Intentos":v} for k,v in st.session_state.attempts.items()])

def reports():
    st.header(f"Tu informe de misión, {st.session_state.student_name}")
    if case.get("case_type") == "factorization": return factorization_report(case)
    if case.get("case_type"," ").startswith("exact_"): return exact_report(case)
    if case.get("case_type") in {"limit_sides","derivative_limit"}:
        if not st.session_state.finished:
            st.info("Completa el caso para generar tu informe."); return
        st.success(f"Completaste {case['title']}.")
        if case.get("case_type")=="limit_sides":
            st.write("Analizaste una transición real separando el comportamiento por izquierda y por derecha.")
            st.latex(r"\lim_{t\to5^-}T(t)=40\neq46=\lim_{t\to5^+}T(t)")
            stages=["Laterales · identificación","Laterales · existencia","Laterales · contexto"]
            tips={
              "Laterales · identificación":"Refuerza la lectura separada de aproximaciones por izquierda y derecha.",
              "Laterales · existencia":"Recuerda: el límite bilateral existe solo si ambos límites laterales existen y coinciden.",
              "Laterales · contexto":"Practica traducir una conclusión matemática al significado que tiene en el sistema real."
            }
        else:
            st.write("Construiste la idea de velocidad instantánea a partir de velocidades promedio y del límite cuando el intervalo se hace pequeño.")
            st.latex(r"s'(2)=\lim_{h\to0}\frac{s(2+h)-s(2)}{h}=4")
            stages=["Derivada · velocidades promedio","Derivada · secante","Derivada · definición"]
            tips={
              "Derivada · velocidades promedio":"Practica el cociente de cambio promedio y observa qué unidades representa.",
              "Derivada · secante":"Refuerza la conexión entre cociente incremental y pendiente de una secante.",
              "Derivada · definición":"Explica con tus palabras por qué h se aproxima a cero sin sustituir h=0 en la fracción original."
            }
        rows=[{"Etapa":x,"Intentos":st.session_state.attempts.get(x,0)} for x in stages if st.session_state.attempts.get(x,0)]
        if rows: st.table(rows)
        st.subheader("Recomendaciones para seguir mejorando")
        weak=[x for x in stages if st.session_state.attempts.get(x,0)>1]
        if weak:
            for x in weak: st.write("• "+tips[x])
        else:
            st.write("• Tu recorrido fue consistente. Intenta justificar el resultado sin mirar las opciones y crea un ejemplo propio con el mismo concepto.")
        if case.get("case_type")=="derivative_limit":
            st.info("**Siguiente paso:** has construido el puente hacia Derivadas. La próxima unidad podrá partir de esta interpretación antes de introducir reglas de derivación.")
        if st.session_state.mode=="evaluative":
            rubric=case["modes"]["evaluative"]["rubric"];scale=case["modes"]["evaluative"]["grade_scale"];grade=weighted_grade(rubric,scale)
            st.subheader("Resultado según la rúbrica")
            st.table([{"Criterio":i["label"],"Peso":f'{i["weight"]}%',"Logro":f'{st.session_state.eval_scores.get(i["key"],0)*100:.0f}%'} for i in rubric])
            st.metric("Tu nota",f"{grade:.2f} / {scale:.1f}")
        else: st.info("Este caso fue didáctico y no genera calificación.")
        return
    if case.get("case_type")=="limit_intro":
        if not st.session_state.finished: st.info("Completa el caso para generar tu informe."); return
        st.success(f"Completaste {case['title']}.")
        st.write("Exploraste el límite mediante tabla, gráfica y álgebra. El objetivo fue justificar el comportamiento, no solo obtener un número.")
        st.latex(r"\lim_{x\to2}\frac{x^2-4}{x-2}=4")
        st.subheader("Idea que debes conservar")
        st.info("El límite estudia el comportamiento cerca de un punto. El valor de f(a) y el límite cuando x→a no son el mismo concepto.")
        rows=[{"Etapa":k,"Intentos":v} for k,v in st.session_state.attempts.items() if k.startswith("Límite")]
        if rows: st.table(rows)
        st.subheader("Recomendaciones para seguir mejorando")
        recs=[]
        if st.session_state.attempts.get("Límite · observación inicial",0)>1:
            recs.append("Practica primero la sustitución directa y reconoce que `0/0` es una indeterminación: no es la respuesta del límite.")
        if st.session_state.attempts.get("Límite · tabla y laterales",0)>1:
            recs.append("Refuerza la lectura de aproximaciones laterales: distingue el valor al que se acerca **x** del valor al que se acerca **f(x)**.")
        if st.session_state.attempts.get("Límite · gráfica",0)>1:
            recs.append("Practica la lectura gráfica de puntos abiertos y recuerda que un hueco no impide por sí solo que exista el límite.")
        if st.session_state.attempts.get("Límite · conclusión",0)>1:
            recs.append("Conecta las tres evidencias —tabla, gráfica y simplificación algebraica— antes de formular la conclusión.")
        if not recs:
            recs.append("Tu recorrido fue consistente. Como siguiente reto, explica con tus propias palabras por qué el límite puede existir aunque la función no esté definida en el punto.")
            recs.append("Intenta reconocer este mismo patrón en otra función con un hueco removible para comprobar que comprendiste la idea y no solo este ejemplo.")
        for r in recs: st.write("• "+r)
        st.info("**Conexión con el caso:** el sensor no entregó una lectura exacta en el instante crítico, pero las mediciones cercanas permitieron anticipar el nivel hacia el que se dirigía el proceso.")
        if st.session_state.mode=="evaluative":
            rubric=case["modes"]["evaluative"]["rubric"]; scale=case["modes"]["evaluative"]["grade_scale"]; grade=weighted_grade(rubric,scale)
            st.subheader("Resultado según la rúbrica")
            st.table([{"Criterio":i["label"],"Peso":f'{i["weight"]}%',"Logro":f'{st.session_state.eval_scores.get(i["key"],0)*100:.0f}%'} for i in rubric])
            st.metric("Tu nota",f"{grade:.2f} / {scale:.1f}")
        else: st.info("Este caso fue didáctico y no genera calificación.")
        return
    if not st.session_state.finished:
        st.info("Completa la misión para generar tu informe.")
        return
    st.success(f"Completaste {case['title']} · Intento general #{st.session_state.general_attempt}")
    st.write("Llegaste desde el contexto hasta una decisión utilizando un modelo diferencial. Este informe está pensado para ayudarte a reconocer lo que ya dominas y dónde conviene practicar un poco más.")
    st.subheader("Tu modelo")
    st.latex(r"\frac{dD}{dt}=0.08D\qquad\Rightarrow\qquad D(t)=5000e^{0.08t}")
    st.subheader("Cómo fue tu recorrido")
    rows=[]
    for stage in ["Variables","Modelo","Propósito de resolución","Diagnóstico","Método","Simulación e interpretación","Decisión final"]:
        n=st.session_state.attempts.get(stage,0)
        if n: rows.append({"Etapa":stage,"Intentos":n})
    if rows: st.table(rows)
    diag=st.session_state.attempts.get("Diagnóstico",0)
    method=st.session_state.attempts.get("Método",0)
    if diag>1:
        st.info("**Para reforzar:** el diagnóstico necesitó varios intentos. Antes de elegir un método, revisa orden, linealidad y si las variables pueden separarse.")
    else:
        st.success("**Fortaleza:** reconociste con seguridad la estructura necesaria para orientar el método.")
    if method>1:
        st.info("**Siguiente objetivo:** practica relacionar la estructura de una EDO con los métodos disponibles, en lugar de escogerlos por memoria.")
    selected=next(o for o in case["decision_options"] if o["id"]==st.session_state.ending)
    st.subheader("Tu decisión y su consecuencia")
    st.write(f"**{selected['title']}** — {selected['story']}")
    st.write("**Aprendizaje clave:** "+selected["lesson"])
    st.write("**Tu reflexión:** "+st.session_state.reflection)
    if st.session_state.mode=="evaluative":
        rubric=case["modes"]["evaluative"]["rubric"]; scale=case["modes"]["evaluative"]["grade_scale"]
        grade=weighted_grade(rubric,scale)
        st.subheader("Resultado según la rúbrica")
        details=[]
        for item in rubric:
            frac=st.session_state.eval_scores.get(item["key"],0.0)
            details.append({"Criterio":item["label"],"Peso":f'{item["weight"]}%',"Logro":f'{frac*100:.0f}%'})
        st.table(details)
        st.metric("Tu nota",f"{grade:.2f} / {scale:.1f}")
        st.caption("La nota se calcula con la rúbrica que viste antes de comenzar el caso.")
    else:
        st.info("Este fue un caso didáctico: tus intentos se utilizan para darte retroalimentación y no generan una calificación.")
    st.subheader("¿Quieres volver a intentarlo?")
    st.write("Un nuevo intento reinicia la misión completa y conserva el número de intento general.")
    if st.button("Iniciar un nuevo intento desde el comienzo"):
        reset_mission(increment=True); st.rerun()

def help_page():
    st.header("Ayuda y soporte")
    st.markdown(f"""### Cómo se organiza EDO·LAB Z
Explora contenidos mediante **Área de conocimiento → Asignatura → Tema → Caso**.

**LAB** es una modalidad didáctica con retroalimentación y sin nota.  
**EVAL** presenta una rúbrica antes de comenzar y genera una calificación al finalizar.

### Soporte
**Autor:** {AUTHOR}  
**Correo:** {EMAIL}

### Créditos
**Concepción, autoría y dirección:** {AUTHOR}  
**Asistencia en desarrollo y diseño:** ChatGPT · OpenAI
""")

if st.session_state.page=="Acceso":
    access()
else:
    st.markdown(f'<div class="top"><b>EDO·LAB Z · Laboratorio interactivo</b><span><span class="cyan">{VERSION}</span> &nbsp; <span class="ok">● SISTEMA ACTIVO</span></span></div>',unsafe_allow_html=True)
    if st.session_state.page=="Ficha": mission_card()
    else:
        {"Inicio":home,"Explorar":explore,"Misiones":mission,"Progreso":progress,"Informes":reports,"Ayuda":help_page}.get(st.session_state.page,home)()
    st.markdown(f'<div class="footer">EDO·LAB Z · Autor: {AUTHOR} · Asistencia en desarrollo: ChatGPT · OpenAI · {VERSION}</div>',unsafe_allow_html=True)
