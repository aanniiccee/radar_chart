from flask import Flask, Response
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/")
def radar_chart_before():
    # ดึงข้อมูล "ก่อน evolve"
    sheet_id = "1BmMyzeeSO8C0Q7wtpoAUFS_rbryQJs79wc2OibgZ8wU"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(csv_url)

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def"]
    fig = go.Figure()
    for i, row in df.iterrows():
        values = row[stats].tolist()
        values += values[:1]
        categories = stats + [stats[0]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row["Name"]
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Radar Chart Before Evolution"
    )

    html = fig.to_html(include_plotlyjs="cdn")
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run()
