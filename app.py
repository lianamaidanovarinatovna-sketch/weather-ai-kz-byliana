import streamlit as st
import requests
from PIL import Image, ImageDraw

# ========================
# Настройки API
# ========================
API_KEY = "ваш_ключ_OpenWeatherMap"  # Вставь сюда свой API ключ OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ========================
# Города Казахстана
# ========================
cities = {
    "Астана": {"top_color": "#87CEFA", "bottom_color": "#FFFFFF"},       # светло-голубой → белый
    "Алматы": {"top_color": "#228B22", "bottom_color": "#ADFF2F"},      # лесной зеленый → светло-зеленый
    "Шымкент": {"top_color": "#FFD700", "bottom_color": "#FFA500"},     # золотой → оранжевый
    "Актобе": {"top_color": "#4682B4", "bottom_color": "#B0C4DE"},      # стальной синий → светло-голубой
    "Актау": {"top_color": "#1E90FF", "bottom_color": "#00BFFF"},       # голубое море
    "Атырау": {"top_color": "#20B2AA", "bottom_color": "#98FB98"},      # бирюзовый → светло-зеленый
    "Караганда": {"top_color": "#708090", "bottom_color": "#D3D3D3"},   # серо-голубой
    "Костанай": {"top_color": "#87CEEB", "bottom_color": "#F0E68C"}     # небесно-голубой → светло-хаки
}

# ========================
# Функция для генерации градиентного фона
# ========================
def generate_gradient(width=800, height=400, top_color="#87CEFA", bottom_color="#FFFFFF"):
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(int(top_color[1:3],16)(1 - y/height) + int(bottom_color[1:3],16)(y/height))
        g = int(int(top_color[3:5],16)(1 - y/height) + int(bottom_color[3:5],16)(y/height))
        b = int(int(top_color[5:7],16)(1 - y/height) + int(bottom_color[5:7],16)(y/height))
        draw.line([(0,y),(width,y)], fill=(r,g,b))
    return img

# ========================
# Интерфейс Streamlit
# ========================
st.set_page_config(page_title="Погода Казахстан", layout="wide")
st.title("🌤 Прогноз погоды по городам Казахстана")

# Выбор города
city = st.selectbox("Выберите город:", list(cities.keys()))
colors = cities[city]

# Генерация фона
bg_img = generate_gradient(top_color=colors["top_color"], bottom_color=colors["bottom_color"])
st.image(bg_img, use_column_width=True)

# ========================
# Получение погоды
# ========================
params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric",
    "lang": "ru"
}

response = requests.get(BASE_URL, params=params)
if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    weather_desc = data["weather"][0]["description"]

    st.subheader(f"Погода в {city}: {weather_desc.capitalize()}")
    st.write(f"🌡 Температура: {temp} °C")
    st.write(f"💧 Влажность: {humidity} %")
    st.write(f"⚖ Давление: {pressure} hPa")
else:
    st.error("Ошибка при получении данных о погоде!")

# ========================
# Современные визуальные элементы
# ========================
st.markdown("---")
st.markdown("*Интерактивный прогноз погоды с градиентным фоном для каждого города!*")
