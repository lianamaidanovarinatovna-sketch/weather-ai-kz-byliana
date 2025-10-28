# app.py
import streamlit as st
import requests
from datetime import datetime

# ======================
# Настройки
# ======================
API_KEY = ""  # <- Вставь свой OpenWeatherMap API ключ сюда. Если пусто — будут тестовые данные.
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Города + имя для API (надёжные названия) + пастельный цвет
cities = {
    "Астана":     {"api": "Astana",     "color": "#cce6ff"},
    "Алматы":     {"api": "Almaty",     "color": "#fff0b3"},
    "Уральск":    {"api": "Oral",       "color": "#d9f2d9"},
    "Шымкент":    {"api": "Shymkent",   "color": "#ffe6cc"},
    "Актобе":     {"api": "Aktobe",     "color": "#e6ccff"},
    "Актау":      {"api": "Aktau",      "color": "#cce0ff"},
    "Атырау":     {"api": "Atyrau",     "color": "#ffffcc"},
    "Караганда":  {"api": "Karaganda",  "color": "#ffdfe8"},
    "Костанай":   {"api": "Kostanay",   "color": "#d9ffff"}
}

# ======================
# Помощники
# ======================
def get_weather_for(city_api_name):
    """Возвращает dict с погодой или None (если ошибка)."""
    if not API_KEY:
        # тестовые данные, если ключ не задан — так ты всегда увидишь вывод
        return {
            "ok": True,
            "name": city_api_name,
            "temp": 12.3,
            "humidity": 62,
            "pressure": 1008,
            "desc": "облачно"
        }
    try:
        params = {"q": city_api_name + ",KZ", "appid": API_KEY, "units": "metric", "lang": "ru"}
        r = requests.get(BASE_URL, params=params, timeout=6)
        if r.status_code != 200:
            return {"ok": False, "error": f"HTTP {r.status_code}: {r.text}"}
        d = r.json()
        return {
            "ok": True,
            "name": d.get("name", city_api_name),
            "temp": d["main"]["temp"],
            "humidity": d["main"]["humidity"],
            "pressure": d["main"]["pressure"],
            "desc": d["weather"][0]["description"]
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ======================
# Интерфейс
# ======================
st.set_page_config(page_title="Weather AI Kazakhstan", layout="wide")
st.title("🌤 Weather AI — Казахстан (простой, надёжный)")

# делим экран: левая узкая, правая широкая
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Выбор")
    city = st.selectbox("Город:", list(cities.keys()))
    now = datetime.now()
    # дата и время большими буквами
    st.markdown(f"<div style='font-size:18px; margin-top:10px;'>📅 <b>{now.strftime('%d.%m.%Y')}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:18px;'>⏰ <b>{now.strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)
    st.write("")  # отступ
    if not API_KEY:
        st.warning("API key не задан. Показаны тестовые данные. Вставь ключ в app.py для реальных данных.")

with col_right:
    # чтобы фон занимал всю правую область — используем div с width:100% и min-height
    color = cities[city]["color"]
    container_html = f"""
    <div style="
        width:100%;
        min-height:420px;
        padding:18px;
        border-radius:10px;
        background:{color};
        box-sizing:border-box;
    ">
    """
    st.markdown(container_html, unsafe_allow_html=True)

    # Получаем погоду
    info = get_weather_for(cities[city]["api"])

    if not info or not info.get("ok"):
        err = info.get("error") if info else "неизвестная ошибка"
        st.markdown(f"<div style='color:#900; font-size:18px;'><b>Ошибка получения погоды:</b> {err}</div>", unsafe_allow_html=True)
    else:
        # выводим крупным шрифтом — ровно то, что просила
        st.markdown(f"<h1 style='margin:6px 0 6px 0; text-align:center;'>{city}</h1>", unsafe_allow_html=True)

        # карточки по строкам (большой шрифт)
        metric_html = f"""
        <div style="display:flex; gap:20px; flex-wrap:wrap; justify-content:center; align-items:center;">
          <div style="min-width:170px; padding:12px; border-radius:8px; background:rgba(255,255,255,0.7);">
            <div style="font-size:16px;"><b>🌡 Температура</b></div>
            <div style="font-size:24px; margin-top:6px;">{info['temp']} °C</div>
          </div>
          <div style="min-width:170px; padding:12px; border-radius:8px; background:rgba(255,255,255,0.7);">
            <div style="font-size:16px;"><b>💧 Влажность</b></div>
            <div style="font-size:24px; margin-top:6px;">{info['humidity']} %</div>
          </div>
          <div style="min-width:170px; padding:12px; border-radius:8px; background:rgba(255,255,255,0.7);">
            <div style="font-size:16px;"><b>⚖ Давление</b></div>
            <div style="font-size:24px; margin-top:6px;">{info['pressure']} hPa</div>
          </div>
        </div>
        <div style="text-align:center; margin-top:16px; font-size:18px;">
          <b>Описание:</b> {info['desc'].capitalize()}
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    # закрываем контейнер
    st.markdown("</div>", unsafe_allow_html=True)

# Конец
