import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

MONTH_NAME = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]


def build_matrix_figure(df10, years, monthly_max, monthly_min, colorscale='RdYlBu_r'):
    rows, cols = 12, len(years)

    fig = make_subplots(
        rows=rows,
        cols=cols,
        horizontal_spacing=0.01,
        vertical_spacing=0.01
    )

    global_min = np.nanmin(df10[["min_temperature", "max_temperature"]].to_numpy())
    global_max = np.nanmax(df10[["min_temperature", "max_temperature"]].to_numpy())

    # sparkline y range
    y0 = np.min(df10[['min_temperature', 'max_temperature']].to_numpy())
    y1 = np.max(df10[['min_temperature', 'max_temperature']].to_numpy())

    vis_max, vis_min = [], []
    for col_idx, year in enumerate(years, start=1):
        for row_idx, month in enumerate(range(1, 13), start=1):
            sub = df10[(df10["year"] == year) & (df10["month"] == month)].sort_values("day")

            mv_max = float(monthly_max.get((year, month), np.nan))
            mv_min = float(monthly_min.get((year, month), np.nan))

            x_bg, y_bg = [1, 31], [y0, y1]

            # ---------- background: MAX ----------
            hm_max = go.Heatmap(
                z=[[mv_max, mv_max],
                   [mv_max, mv_max]] if np.isfinite(mv_max) else [[None, None], [None, None]],
                x=x_bg, y=y_bg,
                zmin=global_min, zmax=global_max,
                colorscale=colorscale,
                showscale=False,
                hoverinfo="skip",
            )
            fig.add_trace(hm_max, row=row_idx, col=col_idx)

            # prepare customdata for BOTH sparklines (hover shows date + max/min)
            date_str = sub["date"].dt.strftime("%Y-%m-%d").to_numpy()
            custom = np.column_stack([
                date_str,
                sub["max_temperature"].astype(int).to_numpy(),
                sub["min_temperature"].astype(int).to_numpy()
            ])

            # ---------- sparkline: MAX ----------
            ln_max = go.Scatter(
                x=sub["day"],
                y=sub["max_temperature"],
                mode="lines",
                line=dict(width=1.5, color='green'),
                customdata=custom,
                hovertemplate="Date %{customdata[0]}, max: %{customdata[1]}℃, min: %{customdata[2]}℃<extra></extra>",
                showlegend=False,
            )
            fig.add_trace(ln_max, row=row_idx, col=col_idx)

            # ---------- background: MIN ----------
            hm_min = go.Heatmap(
                z=[[mv_min, mv_min],
                   [mv_min, mv_min]] if np.isfinite(mv_min) else [[None, None], [None, None]],
                x=x_bg, y=y_bg,
                zmin=global_min, zmax=global_max,
                colorscale=colorscale,
                showscale=False,
                hoverinfo="skip",
            )
            fig.add_trace(hm_min, row=row_idx, col=col_idx)

            # ---------- sparkline: MIN ----------
            ln_min = go.Scatter(
                x=sub["day"],
                y=sub["min_temperature"],
                mode="lines",
                line=dict(width=1.5, color='blue'),
                customdata=custom,
                hovertemplate="Date %{customdata[0]}, max: %{customdata[1]}℃, min: %{customdata[2]}℃<extra></extra>",
                showlegend=False,
            )
            fig.add_trace(ln_min, row=row_idx, col=col_idx)

            # Make each cell look like a compact tile
            fig.update_xaxes(
                row=row_idx, col=col_idx,
                range=[1, 31],
                showgrid=False, zeroline=False, showticklabels=False
            )
            fig.update_yaxes(
                row=row_idx, col=col_idx,
                range=[y0, y1],
                showgrid=False, zeroline=False, showticklabels=False
            )

            vis_max.extend([True, True, False, True])
            vis_min.extend([False, True, True, True])

    # legend
    dummy = go.Scatter(
        x=[0], y=[0],
        mode="markers",
        marker=dict(
            size=0.1,
            color=[global_min, global_max],
            colorscale=colorscale,
            cmin=global_min, cmax=global_max,
            showscale=True,
            colorbar=dict(title="Temperature (°C)", len=0.85, y=0.5, yanchor="middle"),
        ),
        hoverinfo="skip",
        showlegend=False,
    )
    fig.add_trace(dummy)
    vis_max.append(True)
    vis_min.append(True)

    # month labels
    for i, name in enumerate(MONTH_NAME, start=1):
        y_center = 1 - (i - 0.5) / 12
        fig.add_annotation(
            xref="paper", yref="paper",
            x=-0.02, y=y_center,
            text=name,
            showarrow=False,
            font=dict(size=12),
            xanchor="right"
        )

    # year labels
    for j, year in enumerate(years):
        x_center = (j + 0.5) / len(years)
        fig.add_annotation(
            xref="paper", yref="paper",
            x=x_center, y=1.03,
            text=str(year),
            showarrow=False,
            font=dict(size=12),
            xanchor="center"
        )

    fig.update_layout(
        title=dict(
            text="Hong Kong Monthly Temperature Matrix (Last 10 years) — MAX Background",
            x=0.5,
            xanchor="center"
        ),
        height=900,
        margin=dict(l=120, r=120, t=90, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white",
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.0, y=1.09,
                xanchor="left",
                buttons=[
                    dict(
                        label="MAX",
                        method="update",
                        args=[
                            {"visible": vis_max},
                            {"title.text": "Hong Kong Monthly Temperature Matrix (Last 10 years) — MAX Background"}
                        ],
                    ),
                    dict(
                        label="MIN",
                        method="update",
                        args=[
                            {"visible": vis_min},
                            {"title.text": "Hong Kong Monthly Temperature Matrix (Last 10 years) — MIN Background"}
                        ],
                    ),
                ],
            )
        ],
    )

    fig.update_traces(visible=False)
    for trace, visible in zip(fig.data, vis_max):
        trace.visible = visible

    return fig

