
import streamlit as st
STAGES=["Contexto","Variables","Modelo","Resolución","Simulación","Decisión"]

def sidebar(version,author,case):
    with st.sidebar:
        st.markdown('<div class="brand"><div class="z">Z</div><div><div class="bt">EDO<span>·LAB Z</span></div><div class="sub">LABORATORIO DE MODELACIÓN</div></div></div>',unsafe_allow_html=True)
        if st.session_state.student_name:
            st.markdown(f"**Hola, {st.session_state.student_name}.**")
        opts=["Inicio","Explorar","Misiones","Progreso","Informes","Ayuda"]
        current=st.session_state.page if st.session_state.page in opts else "Inicio"
        st.session_state.page=st.radio("Navegación",opts,index=opts.index(current),label_visibility="collapsed")
        if st.session_state.mission_started:
            st.markdown("---")
            st.markdown(f"**{case['mission']} · Intento #{st.session_state.general_attempt}**")
            if case.get("case_type") == "factorization":
                completed = st.session_state.factor_step
                challenge_count = case.get("challenge_count", 3)
                labels = ["Contexto"] + [f"Reto {i}" for i in range(1, challenge_count + 1)] + ["Informe"]
                active = min(completed + 2, len(labels))
            else:
                labels = STAGES
                active = st.session_state.stage
            for i,x in enumerate(labels,1):
                css="done" if i<active else ("active" if i==active else "")
                icon="✓" if i<active else ("●" if i==active else "○")
                st.markdown(f'<div class="step {css}">{icon} {x}</div>',unsafe_allow_html=True)
        st.markdown("---")
        st.caption(f"Versión {version}")
        st.caption(f"Autor · {author}")
