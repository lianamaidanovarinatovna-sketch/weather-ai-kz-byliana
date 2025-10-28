import streamlit as st
import requests
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="Weather AI KZ", layout="wide")

# API ключ
API_KEY = "ВАШ_API_KEY"  # <--- вставь сюда свой ключ OpenWeatherMap

# Города с их цветами и названиями для API
cities = {
    "Астана": {"color": "#A7C7E7", "api": "Astana,KZ"},
    "Алматы": {"color": "#F7E7A9", "api": "Almaty,KZ"},
    "Уральск": {"color": "#C3D9A5", "api": "Oral,KZ"},
    "Шымкент": {"color": "#F9D3B4", "api": "Shymkent,KZ"},
    "Актобе": {"color": "#D0E3F0", "api": "Aktobe,KZ"},
    "Актау": {"color": "#B2E0E4", "api": "Aktau,KZ"},
    "Атырау": {"color": "#F4E1D2", "api": "Atyrau,KZ"},
    "Караганда": {"color": "#E6D0F0", "api": "Karaganda,KZ"},
    "Костанай": {"color": "#E7F0C3", "api": "Kostanay,KZ"},
}

# Разделяем экран
col1, col2 = st.columns([1,2])

with col1:
    st.header("Выбор города")
    city = st.selectbox("Город:", list(cities.keys()))
    
    # Дата и время
    now = datetime.now()
    st.markdown(f"*Дата:* {now.strftime('%d-%m-%Y')}")
    st.markdown(f"*Время:* {now.strftime('%H:%M:%S')}")

with col2:
    # Цвет фона
    bg_color = cities[city]["color"]
    st.markdown(
        f"<div style='background-color:{bg_color}; padding:20px; border-radius:10px;'>",
        unsafe_allow_html=True
    )

    city_api_name = cities[city]["api"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_api_name}&appid={API_KEY}&units=metric&lang=ru"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            description = data["weather"][0]["description"]

            st.markdown(f"<h1 style='text-align:center'>{city}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2>🌡 Температура: {temp} °C</h2>", unsafe_allow_html=True)
            st.markdown(f"<h2>💧 Влажность: {humidity} %</h2>", unsafe_allow_html=True)
            st.markdown(f"<h2>⚖ Давление: {pressure} hPa</h2>", unsafe_allow_html=True)
            st.markdown(f"<h2>🌥 Описание: {description}</h2>", unsafe_allow_html=True)
        else:
            st.error(f"Не удалось получить данные о погоде. Проверьте API Key и название города. Код ошибки: {response.status_code}")

    except Exception as e:
        st.error(f"Ошибка при получении данных: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
