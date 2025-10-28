import streamlit as st
import requests
from PIL import Image, ImageDraw

# ========================
# API ключ OpenWeatherMap
# ========================
API_KEY = "ваш_ключ_OpenWeatherMap"  # Вставьте свой ключ
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ========================
# Города Казахстана и их постельные цвета
# ========================
cities = {
    "Астана": "#B0E0E6",        # пастельный голубой
    "Алматы": "#FFFACD",        # пастельный желтый
    "Шымкент": "#E6E6FA",       # пастельный лавандовый
    "Актобе": "#F5DEB3",        # пастельный бежевый
    "Актау": "#AFEEEE",         # пастельный бирюзовый
    "Атырау": "#F0E68C",        # пастельный хаки
    "Караганда": "#D8BFD8",     # пастельный сиреневый
    "Костанай": "#FFE4E1",      # пастельный розовый
    "Уральск": "#FFF0F5"        # пастельный лиловый
}

# ========================
# Функция для генерации сплошного цвета
# ========================
def generate_background(color, width=800, height=400):
    img = Image.new("RGB", (width, height), color)
    return img

# ========================
# Интерфейс Streamlit
# ========================
st.set_page_config(page_title="Погода Казахстан", layout="wide")
st.title("🌤 Прогноз погоды по городам Казахстана")

# Выбор города
city = st.selectbox("Выберите город:", list(cities.keys()))
bg_color = cities[city]

# Показ фона
bg_img = generate_background(bg_color)
st.image(bg_img, use_column_width=True)

# ========================
# Получение погоды через API
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
