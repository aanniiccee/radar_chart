import pandas as pd
import plotly.graph_objects as go

def handler(request):
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

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row["Name"]
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Competency Radar Chart"
    )

    chart_html = fig.to_html(include_plotlyjs="cdn", full_html=False)

    html = f"""
    <html>
      <head>
        <title>Radar Chart</title>
      </head>
      <body>
        <h1>Competency Radar Chart</h1>
        <div>{chart_html}</div>
      </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }
