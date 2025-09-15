from flask import Flask, Response
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/")
def radar_chart():
    # ดึงข้อมูลจาก Google Sheets
    sheet_id = "1BmMyzeeSO8C0Q7wtpoAUFS_rbryQJs79wc2OibgZ8wU"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(csv_url)

    stats = [
        "Service Excellence Mindset",
        "Team Communication",
        "Results with Responsibility",
        "Innovative Process Excellence",
        "Digital & Technology Proficiency"
    ]

    fig = go.Figure()

    for _, row in df.iterrows():
        values = row[stats].tolist()
        values += values[:1]
        categories = stats + [stats[0]]

        if row["Name"].lower() == "before":
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                name="Before",
                line=dict(color="yellow", dash="solid", width=3),  # เส้นประสีเหลือง
                fill=None
            ))
        else:  # After
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                name="After",
                line=dict(color="purple", dash="solid", width=3),  # เส้นทึบสีม่วง
                fill='toself',
                fillcolor="rgba(128,0,128,0.2)"  # ม่วงโปร่งใส
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Competency Before vs After"
    )

    html = fig.to_html(include_plotlyjs="cdn")
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run()
