
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
            for i,x in enumerate(STAGES,1):
                css="done" if i<st.session_state.stage else ("active" if i==st.session_state.stage else "")
                icon="✓" if i<st.session_state.stage else ("●" if i==st.session_state.stage else "○")
                st.markdown(f'<div class="step {css}">{icon} {x}</div>',unsafe_allow_html=True)
        st.markdown("---")
        st.caption(f"Versión {version}")
        st.caption(f"Autor · {author}")
