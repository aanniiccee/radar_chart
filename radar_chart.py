import pandas as pd
import plotly.graph_objects as go

# ---- 1. ดึงข้อมูลจาก Google Sheets (ต้องเปิดแชร์แบบ Anyone with link -> Viewer) ----
sheet_id = "1BmMyzeeSO8C0Q7wtpoAUFS_rbryQJs79wc2OibgZ8wU"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"

df = pd.read_csv(csv_url)

# ---- 2. ระบุ column ที่เป็น stats (ไม่รวม Name) ----
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def"]

# ---- 3. วาด Radar Chart ----
fig = go.Figure()

for i, row in df.iterrows():
    values = row[stats].tolist()
    values += values[:1]  # ปิดกราฟ (กลับไปที่ค่าแรก)

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
    title="Pokemon Stats Radar Chart"
)

# ---- 4. เซฟเป็น HTML สำหรับเอาขึ้น GitHub Pages / Embed Looker Studio ----
fig.write_html("radar_chart.html", include_plotlyjs="cdn")

print("✅ สร้าง radar_chart.html เรียบร้อยแล้ว")
