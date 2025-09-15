from flask import Flask, Response
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

@app.route("/")
def radar_charts():
    # ---- ดึงข้อมูล "ก่อน evolve" ----
    sheet_id_before = "SHEET_ID_BEFORE"
    csv_url_before = f"https://docs.google.com/spreadsheets/d/{sheet_id_before}/export?format=csv&gid=0"
    df_before = pd.read_csv(csv_url_before)

    # ---- ดึงข้อมูล "หลัง evolve" ----
    sheet_id_after = "SHEET_ID_AFTER"
    csv_url_after = f"https://docs.google.com/spreadsheets/d/{sheet_id_after}/export?format=csv&gid=0"
    df_after = pd.read_csv(csv_url_after)

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def"]

    # ---- สร้าง subplot สำหรับ radar chart 2 ตัว ----
    fig = make_subplots(rows=1, cols=2, specs=[[{"type":"polar"},{"type":"polar"}]])

    # Radar chart ก่อน evolve
    for i, row in df_before.iterrows():
        values = row[stats].tolist()
        values += values[:1]
        categories = stats + [stats[0]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row["Name"]
        ), row=1, col=1)

    # Radar chart หลัง evolve
    for i, row in df_after.iterrows():
        values = row[stats].tolist()
        values += values[:1]
        categories = stats + [stats[0]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row["Name"]
        ), row=1, col=2)

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title_text="Radar Chart Before & After Evolution",
    )

    html = fig.to_html(include_plotlyjs="cdn")
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run()
