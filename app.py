# app.py
# app.py — финальная версия: 9 городов, пастельные цвета, две колонки, аккуратный вывод погоды
import streamlit as st
import requests
from datetime import datetime

# -----------------------
# Настройки (вставь свой ключ или оставь пустым для тестовых данных)
# -----------------------
API_KEY = ""  # <- вставь сюда OpenWeather API ключ, или оставь пустым для тестовых (демо) данных
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -----------------------
# Города + корректные имена для API + пастельные цвета
# -----------------------
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

# -----------------------
# Вспомогательные функции
# -----------------------
def fetch_weather(api_name: str):
    """
    Возвращает dict:
      - если ok: {"ok": True, "temp":..., "humidity":..., "pressure":..., "desc":..., "name":...}
      - при ошибке: {"ok": False, "error": "текст ошибки"}
    Никаких исключений наружу — все ошибки обрабатываются и возвращаются в поле error.
    """
    # Если ключ пустой — возвращаем демонстрационные данные (чтобы интерфейс всегда показывал)
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
    except requests.RequestException as e:
        return {"ok": False, "error": "Сетевая ошибка при подключении к API."}

    # Безопасная обработка ответа
    try:
        data = r.json()
    except ValueError:
        return {"ok": False, "error": "Неправильный ответ от сервера API."}

    if r.status_code != 200:
        # читаем сообщение ошибки (коротко)
        msg = data.get("message") or data.get("detail") or f"HTTP {r.status_code}"
        return {"ok": False, "error": f"API ошибка: {msg}"}

    try:
        return {
            "ok": True,
            "name": data.get("name", api_name),
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "desc": data["weather"][0]["description"]
        }
    except Exception:
        return {"ok": False, "error": "Неожиданный формат ответа от API."}

# -----------------------
# Интерфейс Streamlit
# -----------------------
st.set_page_config(page_title="Weather AI Kazakhstan", layout="wide", initial_sidebar_state="collapsed")
st.title("🌤 Weather AI — Казахстан")

# Две колонки: левая уже, правая шире
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Выбор города")
    city = st.selectbox("", list(cities.keys()))
    now = datetime.now()
    st.markdown(f"<div style='font-size:16px; margin-top:8px;'>📅 <b>{now.strftime('%d.%m.%Y')}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:16px;'>⏰ <b>{now.strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)
    st.caption("Если API ключ не задан — показываются демонстрационные данные.")

with col_right:
    # Контейнер во всю правую область — фон будет на всю ширину колонки
    color = cities[city]["color"]
    outer_html = f"""
      <div style="
         width:100%;
         min-height:420px;
         padding:18px;
         border-radius:10px;
         background: {color};
         box-sizing: border-box;
      ">
    """
    st.markdown(outer_html, unsafe_allow_html=True)

    # Получаем данные (без выброса исключений наружу)
    info = fetch_weather(cities[city]["api"])

    if not info.get("ok"):
        # дружелюбное сообщение об ошибке (никаких траекторий/лога)
        err = info.get("error", "Неизвестная ошибка")
        st.markdown(f"<div style='color:#800; font-size:16px; text-align:center; padding:20px;'><b>Ошибка:</b> {err}</div>", unsafe_allow_html=True)
    else:
        # Заголовок города
        st.markdown(f"<h1 style='margin:4px 0 6px 0; text-align:center;'>{city}</h1>", unsafe_allow_html=True)

        # Большие карточки с метриками
        metric_html = f"""
        <div style="display:flex; gap:18px; flex-wrap:wrap; justify-content:center; align-items:center; margin-top:6px;">
          <div style="min-width:160px; padding:12px; border-radius:8px; background:rgba(255,255,255,0.78); text-align:center;">
            <div style="font-size:14px;"><b>🌡 Температура</b></div>
            <div style="font-size:26px; margin-top:6px;">{info['temp']} °C</div>
          </div>
          <div style="min-width:160px; padding:12px; border-radius:8px; background:rgba(255,255,255,0.78); text-align:center;">
            <div style="font-size:14px;"><b>💧 Влажность</b></div>
            <div style="font-size:26px; margin-top:6px;">{info['humidity']} %</div>
          </div>
          <div style="min-width:160px; padding:12px; border-radius:8px; background:rgba(255,255,255,0.78); text-align:center;">
            <div style="font-size:14px;"><b>⚖ Давление</b></div>
            <div style="font-size:26px; margin-top:6px;">{info['pressure']} hPa</div>
          </div>
        </div>
        <div style="text-align:center; margin-top:14px; font-size:18px;">
          <b>Погодное состояние:</b> {info['desc'].capitalize()}
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    # Закрываем контейнер
    st.markdown("</div>", unsafe_allow_html=True)

# Ничего лишнего ниже — чтобы при скриншоте не было системных логов в интерфейсе
