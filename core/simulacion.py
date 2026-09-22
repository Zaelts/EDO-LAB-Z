
import math
import plotly.graph_objects as go

def demanda(t,d0,k): return d0*math.exp(k*t)
def derivada(t,d0,k): return k*demanda(t,d0,k)
def tiempo_capacidad(d0,k,capacidad):
    if k<=0 or capacidad<=d0: return None
    return math.log(capacidad/d0)/k

def figura_simulacion(d0,k,capacidad,t_analisis,mostrar_familia=True):
    xs=[i/10 for i in range(121)]
    fig=go.Figure()
    palette=["#f4b942","#b388ff","#63e6be"]
    if mostrar_familia:
        bases=[0.6*d0,d0,1.4*d0]
        for base,color in zip(bases,palette):
            if base==d0: continue
            ys=[demanda(t,base,k) for t in xs]
            fig.add_scatter(
                x=xs,y=ys,mode="lines",name=f"Familia · D(0)={base:,.0f}",
                line={"color":color,"width":2,"dash":"dash"},opacity=.85,
                customdata=[[base]]*len(xs),
                hovertemplate="<b>Otra solución de la misma familia</b><br>D(0)=%{customdata[0]:,.0f}<br>Mes %{x:.1f}<br>D(t)=%{y:,.0f} u/mes<extra></extra>"
            )
    ys=[demanda(t,d0,k) for t in xs]
    fig.add_scatter(
        x=xs,y=ys,mode="lines",name="Solución particular del caso",
        line={"color":"#39d0ff","width":4},
        hovertemplate="<b>Solución particular</b><br>Mes %{x:.1f}<br>Demanda %{y:,.0f} u/mes<extra></extra>"
    )
    fig.add_hline(y=capacidad,line_dash="dash",line_color="#ff6b6b",line_width=3,
                  annotation_text=f"Capacidad · {capacidad:,.0f} u/mes",annotation_font_color="#ffb3b3")
    y0=demanda(t_analisis,d0,k); slope=derivada(t_analisis,d0,k)
    span=1.25; tx=[max(0,t_analisis-span),min(12,t_analisis+span)]
    ty=[y0+slope*(x-t_analisis) for x in tx]
    fig.add_scatter(
        x=tx,y=ty,mode="lines",name="Recta tangente",
        line={"color":"#ffffff","dash":"dot","width":3},
        hovertemplate="<b>Recta tangente</b><br>Representa la pendiente instantánea<br>Pendiente ≈ "+f"{slope:,.0f} u/mes²"+"<extra></extra>"
    )
    fig.add_scatter(
        x=[t_analisis],y=[y0],mode="markers",name="Punto analizado",
        marker={"size":13,"color":"#ffea61","line":{"color":"white","width":2}},
        hovertemplate="<b>Punto analizado</b><br>t=%{x:.1f}<br>D(t)=%{y:,.0f}<br>D'(t)="+f"{slope:,.0f}"+" u/mes²<extra></extra>"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#06111a",font_color="white",
        xaxis={"title":"Meses","gridcolor":"#214052"},
        yaxis={"title":"Unidades/mes","gridcolor":"#214052"},
        legend={"orientation":"h","y":-0.25},margin={"t":25,"b":115},
        hoverlabel={"bgcolor":"#102c3d","font_color":"white"}
    )
    return fig
