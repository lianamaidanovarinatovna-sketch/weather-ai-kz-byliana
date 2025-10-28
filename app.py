# app.py — финальный вариант: один цветной блок с метриками внутри
import streamlit as st
import requests
from datetime import datetime

API_KEY = ""  # <- вставь свой OpenWeather API ключ или оставь пустым для демонстрации
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Города + пастельные цвета
cities = {
    "Астана":    {"api": "Astana",     "color": "#cce6ff"},
    "Алматы":    {"api": "Almaty",     "color": "#fff6d6"},
    "Уральск":   {"api": "Oral",       "color": "#e8f6e8"},
    "Шымкент":   {"api": "Shymkent",   "color": "#fff0e0"},
    "Актобе":    {"api": "Aktobe",     "color": "#e9e8ff"},
    "Актау":     {"api": "Aktau",      "color": "#dff3ff"},
    "Атырау":    {"api": "Atyrau",     "color": "#fff8e6"},
    "Караганда": {"api": "Karaganda",  "color": "#ffeef6"},
    "Костанай":  {"api": "Kostanay",   "color": "#eaffff"},
}

def fetch_weather(api_name: str):
    if not API_KEY:
        return {
            "ok": True,
            "name": api_name,
            "temp": round(10 + (hash(api_name) % 20) - 5, 1),
            "humidity": 50 + (hash(api_name) % 40),
            "pressure": 990 + (hash(api_name) % 40),
            "desc": "частичная облачность"
        }
    try:
        params = {"q": f"{api_name},KZ", "appid": API_KEY, "units": "metric", "lang": "ru"}
        r = requests.get(BASE_URL, params=params, timeout=7)
        data = r.json()
        if r.status_code != 200:
            return {"ok": False, "error": data.get("message", f"HTTP {r.status_code}")}
        return {
            "ok": True,
            "name": data.get("name", api_name),
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "desc": data["weather"][0]["description"]
        }
    except Exception:
        return {"ok": False, "error": "Ошибка при получении данных от API."}

st.set_page_config(page_title="Weather AI Kazakhstan", layout="wide")
st.title("🌤 Weather AI — Казахстан")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Выбор города")
    city = st.selectbox("", list(cities.keys()))
    now = datetime.now()
    st.markdown(f"<div style='font-size:16px; margin-top:8px;'>📅 <b>{now.strftime('%d.%m.%Y')}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:16px;'>⏰ <b>{now.strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)
    st.caption("Если API ключ не задан — показываются демонстрационные данные.")

with col_right:
    color = cities[city]["color"]
    info = fetch_weather(cities[city]["api"])

    if not info.get("ok"):
        err = info.get("error", "Неизвестная ошибка")
        st.markdown(f"""
        <div style='width:100%; min-height:400px; background:{color}; border-radius:12px; display:flex; justify-content:center; align-items:center;'>
            <div style='font-size:18px; color:#800;'>{err}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='width:100%; min-height:400px; background:{color}; border-radius:12px; padding:24px; box-sizing:border-box;'>
            <h1 style='text-align:center; margin-bottom:12px;'>{city}</h1>
            <div style='text-align:center; font-size:18px; margin-bottom:6px;'>🌡 Температура: {info['temp']} °C</div>
            <div style='text-align:center; font-size:18px; margin-bottom:6px;'>💧 Влажность: {info['humidity']} %</div>
            <div style='text-align:center; font-size:18px; margin-bottom:6px;'>⚖ Давление: {info['pressure']} hPa</div>
            <div style='text-align:center; font-size:18px; margin-top:12px;'>Погодное состояние: {info['desc'].capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
