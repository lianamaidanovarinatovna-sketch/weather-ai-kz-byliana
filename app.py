import streamlit as st
from datetime import datetime

# =======================
# Настройка страницы
# =======================
st.set_page_config(
    page_title="Weather AI KZ",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =======================
# Данные и города
# =======================
cities = ["Астана", "Алматы", "Шымкент", "Актобе", "Актау", "Атырау", "Караганда", "Костанай", "Уральск"]

# =======================
# Сайдбар
# =======================
st.sidebar.title("Выберите город")
choice = st.sidebar.selectbox("Город:", cities)

st.sidebar.markdown("---")
st.sidebar.write("Лиана Байляна — Weather AI KZ")
st.sidebar.write(f"Дата: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

# =======================
# Дизайн фона в зависимости от погоды
# =======================
# Для примера используем фиктивные значения, позже подключим API
weather_conditions = {
    "Астана": "sunny",
    "Алматы": "rain",
    "Шымкент": "cloudy",
    "Актобе": "snow",
    "Актау": "sunny",
    "Атырау": "rain",
    "Караганда": "cloudy",
    "Костанай": "snow",
    "Уральск": "sunny"
}

condition = weather_conditions.get(choice, "sunny")

if condition == "sunny":
    bg_color = "linear-gradient(135deg, #FFD200, #FF7300)"
    emoji = "☀️"
elif condition == "rain":
    bg_color = "linear-gradient(135deg, #00C6FB, #005BEA)"
    emoji = "🌧️"
elif condition == "cloudy":
    bg_color = "linear-gradient(135deg, #D7D2CC, #304352)"
    emoji = "☁️"
elif condition == "snow":
    bg_color = "linear-gradient(135deg, #E0EAFB, #A6C0FE)"
    emoji = "❄️"
else:
    bg_color = "linear-gradient(135deg, #FFD200, #FF7300)"
    emoji = "🌤️"

# =======================
# Применяем фон через CSS
# =======================
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {bg_color};
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# Главный контент
# =======================
st.title(f"{emoji} Погода в {choice}")
st.subheader("Прогноз AI на сегодня")

# Пример данных, позже можно подключить API
import random
temperature = random.randint(-10, 35)
humidity = random.randint(30, 90)
pressure = random.randint(980, 1030)

st.metric(label="🌡️ Температура", value=f"{temperature}°C")
st.metric(label="💧 Влажность", value=f"{humidity}%")
st.metric(label="🌬️ Давление", value=f"{pressure} hPa")

st.info("⚙️ В будущем сюда можно добавить графики, голосовой AI и прогноз на несколько дней.")
