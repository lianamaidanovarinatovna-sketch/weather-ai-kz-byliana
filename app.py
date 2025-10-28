import streamlit as st
import requests
from PIL import Image
from datetime import datetime

# ========================
# API ключ OpenWeatherMap
# ========================
API_KEY = "ваш_ключ_OpenWeatherMap"  # вставьте свой ключ
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ========================
# Города Казахстана и их пастельные цвета
# ========================
cities = {
    "Астана": "#B0E0E6",
    "Алматы": "#FFFACD",
    "Шымкент": "#E6E6FA",
    "Актобе": "#F5DEB3",
    "Актау": "#AFEEEE",
    "Атырау": "#F0E68C",
    "Караганда": "#D8BFD8",
    "Костанай": "#FFE4E1",
    "Уральск": "#FFF0F5"
}

# ========================
# Генерация сплошного цвета
# ========================
def generate_background(color, width=800, height=400):
    img = Image.new("RGB", (width, height), color)
    return img

# ========================
# Интерфейс Streamlit
# ========================
st.set_page_config(page_title="Погода Казахстан", layout="wide")
st.title("🌤 Прогноз погоды по городам Казахстана")

# Разделение на две колонки
col1, col2 = st.columns([1, 2])  # левая уже, правая шире

# ========================
# Левая колонка: выбор города и дата
# ========================
with col1:
    city = st.selectbox("Выберите город:", list(cities.keys()))
    today = datetime.today().strftime("%d.%m.%Y")
    st.write(f"📅 Сегодня: {today}")

# ========================
# Правая колонка: погода
# ========================
with col2:
    bg_color = cities[city]
    bg_img = generate_background(bg_color, width=800, height=400)
    st.image(bg_img, use_column_width=True)

    # Получаем данные о погоде
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
