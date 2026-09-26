"""Tres casos de ecuaciones diferenciales exactas en variables normalizadas.

Cada función potencial representa un modelo ilustrativo de un indicador de
estado. Su diferencial total se iguala a cero al estudiar una curva de nivel.
"""
import plotly.graph_objects as go
import streamlit as st

from core.progreso import record_attempt, set_eval_score, weighted_grade


DATA = {
    "exact_concept": {
        "variables": ("t", "q"), "point": (1.0, 1.0), "level": 4.0,
        "potential": lambda t, q: t*t*q + 2*t + q*q,
        "M": lambda t, q: 2*t*q + 2, "N": lambda t, q: t*t + 2*q,
        "formula": r"C(t,q)=t^2q+2t+q^2",
        "differential": r"(2tq+2)\,dt+(t^2+2q)\,dq=0",
        "solution": r"t^2q+2t+q^2=4",
        "context": "Un taller vigila un índice de costo C que depende del tiempo de operación t y del caudal de producción q. Ambas variables y el índice se expresan en unidades normalizadas. Para construir un modelo real se recogen registros de operación y costo, se ajusta una función C(t,q) y se valida con datos nuevos. Aquí usamos una función ilustrativa ya calibrada: C(t,q)=t²q+2t+q².",
        "meaning": "Mantener el índice de costo constante significa moverse sobre una curva de nivel C=4. M mide el cambio local del costo al variar t con q fijo; N mide el cambio al variar q con t fijo. Son contribuciones marginales al mismo indicador, no dos costos independientes.",
        "derivation": r"dC=\frac{\partial C}{\partial t}\,dt+\frac{\partial C}{\partial q}\,dq=(2tq+2)\,dt+(t^2+2q)\,dq.\quad C=\mathrm{constante}\Rightarrow dC=0",
        "cross": r"\frac{\partial M}{\partial q}=2t=\frac{\partial N}{\partial t}",
    },
    "exact_integration": {
        "variables": ("x", "y"), "point": (1.0, 2.0), "level": 7.0,
        "potential": lambda x, y: x*x*y + 3*x + y*y/2,
        "M": lambda x, y: 2*x*y + 3, "N": lambda x, y: x*x + y,
        "formula": r"H(x,y)=x^2y+3x+\frac{y^2}{2}",
        "differential": r"(2xy+3)\,dx+(x^2+y)\,dy=0",
        "solution": r"x^2y+3x+\frac{y^2}{2}=7",
        "context": "En una línea de mezclado, x es una dosis y y es una concentración, ambas normalizadas. Un indicador H combina sus efectos; la operación busca conservar el valor objetivo. Un laboratorio podría estimar M y N como cambios marginales del indicador al variar cada ajuste por separado. Los coeficientes de este ejercicio son ilustrativos.",
        "meaning": "M=2xy+3 mide el efecto local de la dosis; N=x²+y, el de la concentración. Si los efectos son compatibles con un mismo indicador H, su diferencial es exacta.",
        "derivation": r"dH=(2xy+3)\,dx+(x^2+y)\,dy=0",
        "cross": r"\frac{\partial M}{\partial y}=2x=\frac{\partial N}{\partial x}",
    },
    "exact_grouping": {
        "variables": ("x", "y"), "point": (1.0, 1.0), "level": 9.0,
        "potential": lambda x, y: x*x*y + 3*x*y*y + 4*x + y*y,
        "M": lambda x, y: 2*x*y + 3*y*y + 4,
        "N": lambda x, y: x*x + 6*x*y + 2*y,
        "formula": r"Q(x,y)=x^2y+3xy^2+4x+y^2",
        "differential": r"(2xy+3y^2+4)\,dx+(x^2+6xy+2y)\,dy=0",
        "solution": r"x^2y+3xy^2+4x+y^2=9",
        "context": "En un proceso de fabricación, x es el caudal y y la temperatura, ambos normalizados. Un índice de calidad Q aproxima el efecto combinado de los dos ajustes. El control busca mantener el mismo índice durante cambios pequeños; los coeficientes son ilustrativos y requerirían calibración experimental antes de aplicarse a una planta.",
        "meaning": "Cada par de términos se reconoce como la diferencial de un producto del índice Q. Con Q constante, los ajustes permitidos quedan sobre Q=9.",
        "derivation": r"dQ=(2xy+3y^2+4)\,dx+(x^2+6xy+2y)\,dy=0",
        "cross": r"\frac{\partial M}{\partial y}=2x+6y=\frac{\partial N}{\partial x}",
    },
}


def level_figure(d, x, y):
    xs=[i*.075 for i in range(41)]
    ys=[i*.075 for i in range(41)]
    values=[[d["potential"](a,b) for a in xs] for b in ys]
    fig=go.Figure()
    fig.add_trace(go.Contour(x=xs,y=ys,z=values,
        contours={"start":d["level"],"end":d["level"]+.001,"size":1,"coloring":"lines","showlabels":True},
        line={"color":"#42c7ff","width":4},showscale=False,name=f"Nivel {d['level']:g}"))
    a,b=d["point"]
    fig.add_scatter(x=[a],y=[b],mode="markers",name="Estado inicial",
                    marker={"size":14,"color":"#fff176","symbol":"diamond"})
    fig.add_scatter(x=[x],y=[y],mode="markers",name="Estado que exploras",
                    marker={"size":16,"color":"#ff9b42","line":{"color":"white","width":2}})
    fig.update_layout(height=380,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#06111a",
        font_color="white",xaxis={"title":d["variables"][0],"range":[0,3],"gridcolor":"#214052"},
        yaxis={"title":d["variables"][1],"range":[0,3],"gridcolor":"#214052"},
        legend={"orientation":"h","y":-.24},margin={"t":25,"b":105})
    return fig


def check(question, options, correct, stage, score_key, did, hint, widget_key):
    choice=st.radio(question,options,index=None,key=widget_key)
    if st.button("Comprobar y continuar",key=widget_key+"_check"):
        ok=choice==correct
        record_attempt(stage,ok)
        if ok:
            set_eval_score(score_key,1)
            st.session_state.exact_step+=1
            st.rerun()
        st.warning(hint if did else "Revisa la ecuación y el contexto; vuelve a intentarlo.")


def exact_mission(case):
    kind=case["case_type"]
    d=DATA[kind]
    did=st.session_state.mode=="didactic"
    step=st.session_state.exact_step
    if step==1:
        st.markdown(f'<div class="hero"><b>{case["company"]}</b><h1>{case["title"]}</h1><p>{case["mission"]} · {case["modes"][st.session_state.mode]["label"]}</p></div>',unsafe_allow_html=True)
        st.header("1 · Del contexto al modelo")
        st.write(d["context"])
        if kind=="exact_concept":
            st.latex(d["formula"])
            st.write("La función de estado puede obtenerse con datos y una calibración. Derivarla permite calcular cómo cambia ante ajustes pequeños; conservar el presupuesto modelado equivale a imponer dC=0.")
            st.latex(d["derivation"])
        else:
            st.write("Las mediciones marginales conducen al modelo diferencial:")
            st.latex(d["differential"])
            st.info("Una ecuación de la forma M(x,y) dx + N(x,y) dy = 0 es **exacta** si existe una función potencial F con Fₓ=M y Fᵧ=N. Resolverla consiste en encontrar F(x,y)=C.")
        check("¿Por qué aparece el cero al conservar el indicador?",
              ["Porque el cambio total del indicador es cero","Porque cada variable vale cero","Porque M y N tienen que valer cero"],
              "Porque el cambio total del indicador es cero","Exactas · modelación","context",did,
              "Piensa en el cambio total dF al desplazarte sobre una curva con F constante.","exact_context")
    elif step==2:
        st.caption(f"{case['title']} · Etapa 2 de 4")
        st.header("2 · Verificar si es exacta")
        st.latex(r"M(u,v)\,du+N(u,v)\,dv=0\quad\Longrightarrow\quad M_v=N_u")
        st.write("En estos tres modelos polinomiales el dominio es todo el plano y la igualdad de derivadas cruzadas permite recuperar una función potencial global.")
        st.latex(d["differential"])
        if kind=="exact_concept": st.latex(r"M(t,q)=2tq+2,\qquad N(t,q)=t^2+2q")
        elif kind=="exact_integration": st.latex(r"M(x,y)=2xy+3,\qquad N(x,y)=x^2+y")
        else: st.latex(r"M(x,y)=2xy+3y^2+4,\qquad N(x,y)=x^2+6xy+2y")
        if did:
            st.write("Derivamos M respecto de la segunda variable y N respecto de la primera, manteniendo fija la otra variable:")
            st.latex(d["cross"])
        correct={"exact_concept":"Ambas derivadas cruzadas son 2t",
                 "exact_integration":"Ambas derivadas cruzadas son 2x",
                 "exact_grouping":"Ambas derivadas cruzadas son 2x+6y"}[kind]
        check("¿Qué comparación confirma la exactitud?",
              [correct,"Se comparan M y N sin derivar","Basta con que M sea distinto de cero"],correct,
              "Exactas · verificación","verify",did,
              "Calcula la derivada de M respecto a la segunda variable y la de N respecto a la primera.","exact_verify")
    elif step==3:
        st.caption(f"{case['title']} · Etapa 3 de 4")
        st.header("3 · Construir la solución")
        if kind=="exact_concept":
            st.write(d["meaning"])
            st.latex(r"dC=M\,dt+N\,dq=0\quad\Longrightarrow\quad C(t,q)=K")
            st.write("El estado (t,q)=(1,1) fija K=1²·1+2·1+1²=4. Comprueba que derivar la función recupera exactamente M y N.")
            st.latex(d["solution"])
            question="¿Qué representa C(t,q)=4 en el taller?"
            answers=["Todos los estados con el mismo índice de costo modelado","Un costo que crece cuatro unidades por minuto","La afirmación de que t y q permanecen fijos"]
            hint="C es una función de estado: dos ajustes pueden cambiar y conservar su valor total."
        elif kind=="exact_integration":
            st.write("Integramos M con respecto a x **manteniendo y fija**. La parte que depende solo de y queda como h(y):")
            st.latex(r"H(x,y)=\int(2xy+3)\,dx=x^2y+3x+h(y)")
            st.write("Derivamos ahora con respecto a y y comparamos con N:")
            st.latex(r"H_y=x^2+h'(y)=x^2+y\quad\Rightarrow\quad h'(y)=y\quad\Rightarrow\quad h(y)=\frac{y^2}{2}")
            st.write("La constante de h se absorbe en K. Con H(1,2)=1²·2+3·1+2²/2=7:")
            st.latex(d["solution"])
            question="¿Qué término faltaba al integrar M con respecto a x?"
            answers=[r"h(y)=y²/2",r"h(y)=y",r"h(y)=x²"]
            hint="Deriva tu propuesta respecto de y: debe producir el término y de N."
        else:
            st.write("Agrupamos términos que forman diferenciales completas; es una forma de reconocer el potencial sin desarrollar una integral larga:")
            st.latex(r"(2xy\,dx+x^2\,dy)=d(x^2y)")
            st.latex(r"(3y^2\,dx+6xy\,dy)=d(3xy^2)")
            st.latex(r"4\,dx=d(4x),\qquad 2y\,dy=d(y^2)")
            st.latex(r"dQ=d(x^2y)+d(3xy^2)+d(4x)+d(y^2)=0")
            st.write("Al sumar y usar Q(1,1)=1+3+4+1=9 obtenemos:")
            st.latex(d["solution"])
            question="¿Qué término potencial se recupera al agrupar 3y² dx con 6xy dy?"
            answers=["3xy²","3x²y","6xy"]
            hint="Deriva 3xy² con la regla del producto y comprueba ambos coeficientes."
        check(question,answers,answers[0],"Exactas · solución","solve",did,hint,"exact_solve")
    else:
        st.caption(f"{case['title']} · Etapa 4 de 4")
        st.header("4 · Explorar e interpretar una curva de nivel")
        st.write(d["meaning"])
        st.latex(d["solution"])
        u,v=d["variables"]
        a,b=st.columns(2)
        with a: x=st.slider(f"Ajuste {u}",0.0,3.0,d["point"][0],.05,key="exact_x")
        with b: y=st.slider(f"Ajuste {v}",0.0,3.0,d["point"][1],.05,key="exact_y")
        value=d["potential"](x,y)
        st.plotly_chart(level_figure(d,x,y),use_container_width=True,key="exact_level_plot")
        st.metric("Indicador del ajuste seleccionado",f"{value:.2f}")
        st.write(f"Estado inicial: ({d['point'][0]:g}, {d['point'][1]:g}), indicador {d['level']:g}. El contorno azul une estados con ese mismo valor. El punto naranja es tu ajuste; compara los números, pues un punto próximo a la curva no necesariamente está exactamente sobre ella.")
        q=st.radio("¿Qué debe cumplirse para conservar el indicador en otro estado?",
                   [f"Que la función potencial valga {d['level']:g}","Que ambas variables tengan el mismo valor","Que M y N valgan cero"],index=None,key="exact_interpret")
        if not st.session_state.exact_done:
            if st.button("Confirmar interpretación"):
                ok=bool(q and q.startswith("Que la función potencial valga"))
                record_attempt("Exactas · interpretación",ok)
                if ok:
                    set_eval_score("interpret",1)
                    st.session_state.exact_done=True
                    st.rerun()
                st.warning("Compara la función de estado con el valor fijado por el estado inicial.")
        else:
            st.success("Relacionaste la ecuación exacta, su función potencial y el estado operativo.")
            if st.button("Cerrar caso y ver mi informe"):
                st.session_state.finished=True
                st.session_state.page="Informes"
                st.rerun()


def exact_report(case):
    if not st.session_state.finished:
        st.info("Completa el caso para generar tu informe.")
        return
    d=DATA[case["case_type"]]
    st.success(f"Completaste {case['title']}.")
    st.write("Partiste de un indicador contextual, verificaste la exactitud y encontraste su curva de nivel.")
    st.latex(d["solution"])
    stages=["Exactas · modelación","Exactas · verificación","Exactas · solución","Exactas · interpretación"]
    st.table([{"Etapa":s,"Intentos":st.session_state.attempts.get(s,0)} for s in stages])
    tips={stages[0]:"Vuelve a derivar el indicador del contexto: conservarlo significa dF=0.",
          stages[1]:"Recuerda comparar las derivadas cruzadas M_y y N_x en el dominio.",
          stages[2]:"Diferencia tu potencial propuesto respecto de ambas variables para recuperar M y N.",
          stages[3]:"Usa la condición inicial para fijar K y comprueba el indicador en otro estado."}
    st.subheader("Para seguir practicando")
    weak=[s for s in stages if st.session_state.attempts.get(s,0)>1]
    for s in weak or [stages[3]]: st.write("• "+tips[s])
    if st.session_state.mode=="evaluative":
        rubric=case["modes"]["evaluative"]["rubric"]
        st.table([{"Criterio":r["label"],"Peso":f'{r["weight"]}%',
                   "Logro":f'{st.session_state.eval_scores.get(r["key"],0)*100:.0f}%'} for r in rubric])
        st.metric("Tu nota",f'{weighted_grade(rubric,5.0):.2f} / 5.0')
    else:
        st.info("Este caso fue didáctico y no genera calificación.")
