
import plotly.graph_objects as go
def f(x): return None if abs(x-2)<1e-12 else x+2
def tabla(xs): return [{"x":f"{x:.4f}","f(x)":f"{f(x):.4f}"} for x in xs]

def figura():
    left=[1+i*.01 for i in range(100)]
    right=[2.01+i*.01 for i in range(100)]
    fig=go.Figure()
    fig.add_scatter(x=left,y=[f(x) for x in left],mode="lines",name="Por izquierda",
                    line={"color":"#39d0ff","width":4},
                    hovertemplate="x=%{x:.3f}<br>f(x)=%{y:.3f}<extra>Desde la izquierda</extra>")
    fig.add_scatter(x=right,y=[f(x) for x in right],mode="lines",name="Por derecha",
                    line={"color":"#63e6be","width":4},
                    hovertemplate="x=%{x:.3f}<br>f(x)=%{y:.3f}<extra>Desde la derecha</extra>")
    fig.add_scatter(x=[2],y=[4],mode="markers",name="Hueco en x=2",
                    marker={"size":16,"color":"#06111a","line":{"color":"#ffea61","width":4},"symbol":"circle-open"},
                    hovertemplate="<b>Hueco en x=2</b><br>f(2) no está definida.<br>El límite estudia lo que ocurre alrededor.<extra></extra>")
    fig.add_vline(x=2,line_dash="dot",line_color="#9aa9b5",annotation_text="x → 2")
    fig.add_hline(y=4,line_dash="dot",line_color="#ffea61",annotation_text="f(x) → 4")
    fig.update_layout(uirevision="limits-v211",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#06111a",
        font_color="white",xaxis={"title":"x","gridcolor":"#214052","range":[1,3]},
        yaxis={"title":"f(x)","gridcolor":"#214052","range":[2.8,5.2]},
        legend={"orientation":"h","y":-0.20},margin={"t":35,"b":95})
    return fig

def recta_numerica():
    # Pedagogical scale: positions are intentionally equidistant so values
    # extremely close to 2 remain readable. Labels preserve the true numbers.
    labels=["1.5","1.9","1.99","1.999","2","2.001","2.01","2.1","2.5"]
    pos=list(range(len(labels)))
    fig=go.Figure()
    fig.add_scatter(x=pos,y=[0]*len(pos),mode="lines",
                    line={"color":"#78909c","width":2},showlegend=False,hoverinfo="skip")
    fig.add_scatter(x=pos[:4],y=[0]*4,mode="markers",name="Se acerca por la izquierda",
                    marker={"size":[8,10,12,14],"color":"#39d0ff"},
                    hovertemplate="x=%{customdata}<br>x < 2<extra>Izquierda</extra>",customdata=labels[:4])
    fig.add_scatter(x=[4],y=[0],mode="markers",name="Punto de aproximación",
                    marker={"size":17,"color":"#ffea61","symbol":"diamond"},
                    hovertemplate="x=2<extra>Punto de aproximación</extra>")
    fig.add_scatter(x=pos[5:],y=[0]*4,mode="markers",name="Se acerca por la derecha",
                    marker={"size":[14,12,10,8],"color":"#63e6be"},
                    hovertemplate="x=%{customdata}<br>x > 2<extra>Derecha</extra>",customdata=labels[5:])
    fig.add_annotation(x=3.45,y=.16,text="→",showarrow=False,font={"size":30})
    fig.add_annotation(x=4.55,y=.16,text="←",showarrow=False,font={"size":30})
    fig.update_layout(uirevision="numberline-v3",height=285,paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#06111a",font_color="white",
        xaxis={"tickmode":"array","tickvals":pos,"ticktext":labels,"range":[-.4,8.4],
               "title":"Los valores reales se acercan a 2; la separación visual se amplió para poder leerlos.",
               "gridcolor":"#214052","fixedrange":True},
        yaxis={"visible":False,"range":[-.25,.28],"fixedrange":True},
        margin={"t":35,"b":70},legend={"orientation":"h","y":-0.42})
    return fig
