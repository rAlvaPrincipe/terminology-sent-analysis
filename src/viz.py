import plotly.graph_objs as go


def prepare_data_points(preds):
    trace = go.Scatter3d(
        x = preds["x"],
        z = preds["z"],
        y = preds["y"],
        text = preds["labels"],
        hovertext = preds["docs"],
        name = preds["legend"],
        textposition = "top center",
        textfont_size = 20,
        mode = 'markers+text',
        marker = {
            'size': 5,
            'opacity': 1,
            'color': preds["color"]
        }
    )
    return trace


def plot_multilegend(models_preds):
    data = []
    for models_preds in models_preds:
        data.append(prepare_data_points(models_preds))
    plot_figure = go.Figure(data = data)
    plot_figure.update_layout(height=800)
    return plot_figure



def plot(embeddings):
    data = prepare_data_points(embeddings)
    plot_figure = go.Figure(data = data)
    return plot_figure
