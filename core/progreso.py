
import streamlit as st

DEFAULTS = {
    "page":"Acceso","stage":1,"score":0,"done":set(),
    "student_name":"","area":"","subject":"","topic":"",
    "case_id":"caso_01_planta_limite","mode":"didactic","mission_started":False,
    "var_ok":False,"model_ok":False,"purpose_ok":False,"class_ok":False,
    "method_ok":False,"sim_ok":False,"finished":False,"ending":None,
    "decision_confirm_pending":False,"reflection":"",
    "attempts":{},"mistakes":{},"general_attempt":1,
    "eval_scores":{},"limit_step":1,"limit_done":False,"limit2_step":1,"limit2_done":False,"deriv_step":1,"deriv_done":False,
    "exact_step":1,"exact_done":False,
    "factor_step":0,"factor_correct":0
}

def init_state():
    for k,v in DEFAULTS.items():
        if k not in st.session_state:
            if isinstance(v,set): st.session_state[k]=set(v)
            elif isinstance(v,dict): st.session_state[k]=dict(v)
            else: st.session_state[k]=v

def award(points,key):
    if key not in st.session_state.done:
        st.session_state.score += points
        st.session_state.done.add(key)

def record_attempt(stage, correct, error_key=None):
    st.session_state.attempts[stage] = st.session_state.attempts.get(stage,0)+1
    if not correct and error_key:
        st.session_state.mistakes[error_key] = st.session_state.mistakes.get(error_key,0)+1

def set_eval_score(key, fraction):
    if key not in st.session_state.eval_scores:
        st.session_state.eval_scores[key] = max(0.0,min(1.0,float(fraction)))

def go_stage(n):
    st.session_state.stage=n
    st.rerun()

def reset_mission(increment=True):
    keep = {
        "student_name":st.session_state.student_name,
        "area":st.session_state.area,
        "subject":st.session_state.subject,
        "topic":st.session_state.topic,
        "case_id":st.session_state.case_id,
        "mode":st.session_state.mode,
        "general_attempt":st.session_state.general_attempt + (1 if increment else 0)
    }
    for k in list(DEFAULTS):
        if k in keep: continue
        v=DEFAULTS[k]
        if isinstance(v,set): st.session_state[k]=set(v)
        elif isinstance(v,dict): st.session_state[k]=dict(v)
        else: st.session_state[k]=v
    for k,v in keep.items(): st.session_state[k]=v
    st.session_state.page="Misiones"
    st.session_state.mission_started=True

def weighted_grade(rubric, scale):
    total=0.0
    for item in rubric:
        total += item["weight"] * st.session_state.eval_scores.get(item["key"],0.0)/100
    return total*scale
