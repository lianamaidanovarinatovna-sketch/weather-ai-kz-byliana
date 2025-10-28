import streamlit as st
import requests
from PIL import Image, ImageDraw

# --- Настройки страницы ---
st.set_page_config(page_title="Weather AI Kazakhstan", layout="centered")

st.title("🌤 Прогноз погоды Казахстан")

# --- Список городов ---
cities = ["Астана", "Алматы", "Уральск", "Шымкент", "Актобе", "Актау", "Атырау", "Караганда", "Костанай"]
city = st.selectbox("Выберите город", cities)

# --- Функция генерации градиента (замена фона) ---
def generate_gradient(width=800, height=400, top_color="#87CEEB", bottom_color="#FFFFFF"):
    img = Image.new("RGB", (width, height), top_color)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(int(top_color[1:3],16)(1 - y/height) + int(bottom_color[1:3],16)(y/height))
        g = int(int(top_color[3:5],16)(1 - y/height) + int(bottom_color[3:5],16)(y/height))
        b = int(int(top_color[5:7],16)(1 - y/height) + int(bottom_color[5:7],16)(y/height))
        draw.line([(0,y),(width,y)], fill=(r,g,b))
    return img

# --- Настройка цветов для городов ---
city_colors = {
    "Астана": ("#a0c4ff", "#ffffff"),
    "Алматы": ("#90be6d", "#d9f0a3"),
    "Уральск": ("#f9c74f", "#fefae0"),
    "Шымкент": ("#f8961e", "#fce8c2"),
    "Актобе": ("#577590", "#bcd4e6"),
    "Актау": ("#43aa8b", "#c7f0e3"),
    "Атырау": ("#f94144", "#fcd6d6"),
    "Караганда": ("#6a4c93", "#d9d2e9"),
    "Костанай": ("#f3722c", "#fde2d2")
}

top_color, bottom_color = city_colors.get(city, ("#87CEEB","#FFFFFF"))
bg_img = generate_gradient(top_color=top_color, bottom_color=bottom_color)
st.image(bg_img, use_column_width=True)

# --- Погода через OpenWeatherMap API (нужно свой API ключ) ---
api_key = "ТВОЙ_API_KEY"
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=ru"

try:
    data = requests.get(weather_url).json()
    if data.get("cod") != 200:
        st.error("Ошибка получения данных о погоде!")
    else:
        st.subheader(f"{data['name']}, {data['sys']['country']}")
        st.write(f"🌡 Температура: {data['main']['temp']} °C")
        st.write(f"💧 Влажность: {data['main']['humidity']} %")
        st.write(f"🌬 Ветер: {data['wind']['speed']} м/с")
        st.write(f"☁ Погода: {data['weather'][0]['description'].capitalize()}")
except:
    st.error("Не удалось подключиться к API. Проверьте ключ и интернет.")
