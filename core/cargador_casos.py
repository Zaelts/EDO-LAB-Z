
from pathlib import Path
import json
from functools import lru_cache
BASE=Path(__file__).resolve().parents[1]/"casos"

@lru_cache(maxsize=1)
def listar_casos():
    out=[]
    for p in BASE.glob("caso_*/caso.json"):
        with open(p,encoding="utf-8") as f: out.append(json.load(f))
    return tuple(sorted(out,key=lambda c:(c.get("area",""),c.get("subject",""),c.get("topic",""),c.get("case_order",99))))

@lru_cache(maxsize=32)
def cargar_caso(case_id):
    # Las sesiones de Streamlit pueden conservar el identificador anterior
    # mientras se despliega una actualización. Mantén válida esa ruta durante
    # la transición del caso de cubos a potencias del mismo exponente.
    if case_id == "caso_14_suma_diferencia_cubos":
        case_id = "caso_14_suma_diferencia_potencias"
    with open(BASE/case_id/"caso.json",encoding="utf-8") as f:return json.load(f)

@lru_cache(maxsize=1)
def cargar_curriculo():
    with open(BASE/"curriculo.json",encoding="utf-8") as f:return json.load(f)
