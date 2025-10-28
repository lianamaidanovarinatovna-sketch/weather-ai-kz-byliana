import streamlit as st
import requests

# -----------------------------
# Настройки API
# -----------------------------
API_KEY = "ВАШ_OPENWEATHERMAP_KEY"  # <-- вставь сюда свой ключ

# -----------------------------
# Города и цвета фона (пастель)
# -----------------------------
cities = {
    "Астана": {"api": "Astana", "color": "#cce6ff"},
    "Алматы": {"api": "Almaty", "color": "#fff0b3"},
    "Уральск": {"api": "Oral", "color": "#d9f2d9"},
    "Шымкент": {"api": "Shymkent", "color": "#ffe6cc"},
    "Актобе": {"api": "Aktobe", "color": "#e6ccff"},
    "Актау": {"api": "Aktau", "color": "#cce0ff"},
    "Атырау": {"api": "Atyrau", "color": "#ffffcc"},
    "Караганда": {"api": "Karaganda", "color": "#ffcccc"},
    "Костанай": {"api": "Kostanay", "color": "#d9ffff"}
}

# -----------------------------
# Интерфейс
# -----------------------------
st.set_page_config(page_title="Weather AI Kazakhstan", layout="wide")

# Левая колонка — выбор города
col1, col2 = st.columns([1, 2])
with col1:
    st.header("Выберите город")
    city = st.selectbox("Город:", list(cities.keys()))

# Правая колонка — данные о погоде
with col2:
    # Цвет фона по выбранному городу
    st.markdown(
        f"<div style='background-color:{cities[city]['color']}; padding:20px; border-radius:10px;'>",
        unsafe_allow_html=True
    )

    # -----------------------------
    # Получение данных о погоде
    # -----------------------------
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

            # Вывод с увеличенным шрифтом
            st.markdown(f"<h2 style='text-align:center'>{city}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3>🌡 Температура: {temp} °C</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>💧 Влажность: {humidity} %</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>⚖ Давление: {pressure} hPa</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3>🌥 Описание: {description}</h3>", unsafe_allow_html=True)
        else:
            st.error("Не удалось получить данные о погоде. Проверьте API Key и название города.")

    except Exception as e:
        st.error(f"Ошибка при получении данных: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
