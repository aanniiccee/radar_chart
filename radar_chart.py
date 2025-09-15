from flask import Flask
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

def make_chart(csv_url, title):
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
        values += values[:1]  # ปิดกราฟกลับไปจุดแรก
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
        title=title
    )

    return fig.to_html(include_plotlyjs="cdn", full_html=False)


@app.route("/")
def index():
    sheet_id = "1BmMyzeeSO8C0Q7wtpoAUFS_rbryQJs79wc2OibgZ8wU"

    # worksheet แรก (gid=0)
    csv_url1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    chart1 = make_chart(csv_url1, "Competency (Before Evolution)")

    # worksheet ที่สอง (เปลี่ยน gid ตามจริง เช่น gid=123456789)
    csv_url2 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=123456789"
    chart2 = make_chart(csv_url2, "Competency (After Evolution)")

    return f"""
    <html>
      <head>
        <title>Radar Charts</title>
      </head>
      <body>
        <h1>Radar Charts from Google Sheets</h1>
        <div>{chart1}</div>
        <hr>
        <div>{chart2}</div>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
