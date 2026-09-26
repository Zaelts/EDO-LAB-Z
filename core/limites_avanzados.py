
import plotly.graph_objects as go

def thermal_value(t):
    return 40 + .8*(t-5) if t < 5 else 46 + .8*(t-5)

def thermal_table(times):
    return [{"t (min)":f"{t:.2f}","T(t) °C":f"{thermal_value(t):.2f}"} for t in times]

def thermal_figure():
    left=[3+i*.02 for i in range(100)]
    right=[5.02+i*.02 for i in range(100)]
    fig=go.Figure()
    fig.add_scatter(x=left,y=[thermal_value(x) for x in left],mode="lines",name="Régimen antes de 5 min",
                    line={"width":4,"color":"#42c7ff"})
    fig.add_scatter(x=right,y=[thermal_value(x) for x in right],mode="lines",name="Régimen después de 5 min",
                    line={"width":4,"color":"#ff9b42","dash":"dash"})
    fig.add_scatter(x=[5],y=[40],mode="markers",name="Círculo abierto · izquierda (40 °C)",
                    marker={"size":23,"symbol":"circle","line":{"width":5,"color":"#fff176"},"color":"#06111a"})
    fig.add_scatter(x=[5],y=[46],mode="markers",name="Punto lleno · T(5)=46 °C",
                    marker={"size":19,"symbol":"circle","line":{"width":3,"color":"#ffffff"},"color":"#ff9b42"})
    fig.add_vline(x=5,line_dash="dot",line_color="#ffea61",annotation_text="cambio de régimen")
    fig.update_layout(uirevision="thermal-v1",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#06111a",
        font_color="white",xaxis={"title":"Tiempo t (min)","range":[3,7],"gridcolor":"#214052"},
        yaxis={"title":"Indicador térmico (°C)","range":[37,49],"gridcolor":"#214052"},
        legend={"orientation":"h","y":-0.2},margin={"b":90})
    return fig

def secant_slope(a,h):
    return ((a+h)**2-a**2)/h

def derivative_table(a,hs):
    return [{"h":f"{h:g}","t=2+h":f"{a+h:g}","velocidad promedio (m/s)":f"{secant_slope(a,h):.4f}"} for h in hs]

def derivative_figure(a,h):
    xs=[x/20 for x in range(0,101)]
    ys=[x*x for x in xs]
    p=a*a; q=(a+h)**2; m=secant_slope(a,h)
    secx=[max(0,a-1.2),min(5,a+h+1)]
    secy=[p+m*(x-a) for x in secx]
    tangent=[2*a*(x-a)+p for x in secx]
    fig=go.Figure()
    fig.add_scatter(x=xs,y=ys,mode="lines",name="posición s(t)=t²",line={"width":4,"color":"#42c7ff"})
    fig.add_scatter(x=secx,y=secy,mode="lines",name=f"secante · pendiente {m:.3f}",line={"dash":"dash","width":3,"color":"#ffea61"})
    fig.add_scatter(x=secx,y=tangent,mode="lines",name="tangente límite · pendiente 4",line={"width":3,"color":"#ff9b42"})
    fig.add_scatter(x=[a,a+h],y=[p,q],mode="markers+text",text=["P","Q"],textposition="top center",
                    name="P y Q",marker={"size":13,"color":"#ffffff"})
    fig.update_layout(uirevision="derivative-v1",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#06111a",
        font_color="white",xaxis={"title":"Tiempo t (s)","range":[0,5],"gridcolor":"#214052"},
        yaxis={"title":"Posición s(t) (m)","range":[0,26],"gridcolor":"#214052"},
        legend={"orientation":"h","y":-0.2},margin={"b":90})
    return fig
