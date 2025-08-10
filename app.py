import streamlit as st
from datetime import date, datetime, timedelta
import requests

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="🎂 Age Calculator", page_icon="🎂", layout="centered")

# ---------------------------
# Birthday Balloons + Confetti Animation CSS & HTML
# ---------------------------
st.markdown("""
<style>
/* Background gradient */
body {
    background: linear-gradient(135deg, #ffecd2, #fcb69f);
    color: #333333;
}

/* Balloon shapes */
.balloon {
  position: fixed;
  bottom: -150px;
  width: 40px;
  height: 60px;
  background: radial-gradient(circle at 20% 20%, #ff5f6d, #ffc371);
  border-radius: 20px 20px 30px 30px;
  animation: floatUp 10s linear infinite;
  opacity: 0.8;
  z-index: 0;
  filter: drop-shadow(0 2px 2px rgba(0,0,0,0.15));
}

/* Different balloon colors */
.balloon:nth-child(1) { left: 10%; animation-delay: 0s; background: #ff5f6d;}
.balloon:nth-child(2) { left: 30%; animation-delay: 2s; background: #ffc371;}
.balloon:nth-child(3) { left: 50%; animation-delay: 4s; background: #28c76f;}
.balloon:nth-child(4) { left: 70%; animation-delay: 6s; background: #00cfe8;}
.balloon:nth-child(5) { left: 90%; animation-delay: 8s; background: #7367f0;}

/* Balloon float animation */
@keyframes floatUp {
  0% { bottom: -150px; opacity: 0.8; }
  100% { bottom: 100vh; opacity: 0; }
}

/* Confetti pieces */
.confetti {
  position: fixed;
  width: 10px;
  height: 10px;
  background-color: #ff5f6d;
  opacity: 0.8;
  animation: confettiFall 5s linear infinite;
  border-radius: 2px;
  z-index: 0;
}

.confetti:nth-child(6) { left: 15%; animation-delay: 0s; background: #ffc371;}
.confetti:nth-child(7) { left: 35%; animation-delay: 1s; background: #28c76f;}
.confetti:nth-child(8) { left: 55%; animation-delay: 2s; background: #00cfe8;}
.confetti:nth-child(9) { left: 75%; animation-delay: 3s; background: #7367f0;}
.confetti:nth-child(10) { left: 95%; animation-delay: 4s; background: #ff5f6d;}

@keyframes confettiFall {
  0% { top: -20px; transform: rotate(0deg);}
  100% { top: 100vh; transform: rotate(360deg);}
}

/* Title */
.title {
    font-size: 40px !important;
    font-weight: bold;
    color: #2c2c2c;
    text-align: center;
    margin-bottom: 25px;
}

/* Highlighted text */
.highlight {
    font-size: 24px;
    font-weight: bold;
    color: #e63946;
}

/* Card styling */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    z-index: 1;
    position: relative;
}

/* Famous person container */
.person {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
}

/* Person image styling */
.person img {
    border-radius: 50%;
    width: 60px;
    height: 60px;
    object-fit: cover;
    margin-right: 15px;
    border: 2px solid #e63946;
}

/* Person name link */
.person a {
    font-weight: bold;
    color: #e63946;
    text-decoration: none;
}

.person a:hover {
    text-decoration: underline;
}
</style>

<!-- Balloons -->
<div class="balloon"></div>
<div class="balloon"></div>
<div class="balloon"></div>
<div class="balloon"></div>
<div class="balloon"></div>

<!-- Confetti -->
<div class="confetti"></div>
<div class="confetti"></div>
<div class="confetti"></div>
<div class="confetti"></div>
<div class="confetti"></div>
""", unsafe_allow_html=True)

# ---------------------------
# Helper Functions
# ---------------------------
def get_zodiac(month, day):
    zodiac_dates = [
        ((1, 20), (2, 18), "Aquarius ♒"),
        ((2, 19), (3, 20), "Pisces ♓"),
        ((3, 21), (4, 19), "Aries ♈"),
        ((4, 20), (5, 20), "Taurus ♉"),
        ((5, 21), (6, 20), "Gemini ♊"),
        ((6, 21), (7, 22), "Cancer ♋"),
        ((7, 23), (8, 22), "Leo ♌"),
        ((8, 23), (9, 22), "Virgo ♍"),
        ((9, 23), (10, 22), "Libra ♎"),
        ((10, 23), (11, 21), "Scorpio ♏"),
        ((11, 22), (12, 21), "Sagittarius ♐"),
        ((12, 22), (1, 19), "Capricorn ♑"),
    ]
    for start, end, sign in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "Capricorn ♑"

def get_chinese_zodiac(year):
    animals = ["Rat 🐀", "Ox 🐂", "Tiger 🐅", "Rabbit 🐇", "Dragon 🐉", "Snake 🐍", "Horse 🐎", "Goat 🐐", "Monkey 🐒", "Rooster 🐓", "Dog 🐕", "Pig 🐖"]
    return animals[(year - 1900) % 12]

def get_historical_events(month, day):
    try:
        url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [f"{ev['year']}: {ev['description']}" for ev in data.get("events", [])[:5]]
    except:
        pass
    return ["No events found."]

def get_famous_birthdays_with_images(month, day):
    try:
        url = f"https://byabbe.se/on-this-day/{month}/{day}/births.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            births = data.get("births", [])[:5]  # Top 5
            
            famous_people = []
            for b in births:
                description = b.get("description", "")
                year = b.get("year", "")
                name_guess = description.split(",")[0].strip()
                
                wiki_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name_guess.replace(' ', '_')}"
                img_url = None
                try:
                    wiki_resp = requests.get(wiki_api_url, timeout=5)
                    if wiki_resp.status_code == 200:
                        wiki_data = wiki_resp.json()
                        img_url = wiki_data.get("thumbnail", {}).get("source")
                except:
                    img_url = None
                
                famous_people.append({
                    "year": year,
                    "description": description,
                    "img_url": img_url,
                    "name": name_guess
                })
            return famous_people
    except:
        pass
    return []

# ---------------------------
# Title
# ---------------------------
st.markdown("<h1 class='title'>🎂 Exact Age Calculator</h1>", unsafe_allow_html=True)
st.write("Enter your birthdate to discover fun facts, milestones, and celebrations about your age!")

# ---------------------------
# Date Input
# ---------------------------
birth_date = st.date_input("📅 Select your birthdate", min_value=date(1900, 1, 1), max_value=date.today())

# ---------------------------
# Age Calculations
# ---------------------------
today = date.today()
years = today.year - birth_date.year
months = today.month - birth_date.month
days = today.day - birth_date.day

if days < 0:
    months -= 1
    last_month = today.month - 1 if today.month > 1 else 12
    last_month_year = today.year if today.month > 1 else today.year - 1
    days += (date(last_month_year, last_month + 1, 1) - date(last_month_year, last_month, 1)).days

if months < 0:
    years -= 1
    months += 12

total_days = (today - birth_date).days
total_weeks = total_days // 7
total_seconds = total_days * 24 * 60 * 60
total_heartbeats = total_days * 24 * 60 * 70  # avg 70 bpm
total_breaths = total_days * 24 * 60 * 20     # avg 20 breaths/min

milestone_10000 = birth_date + timedelta(days=10000)
days_until_10000 = (milestone_10000 - today).days

next_birthday = date(today.year, birth_date.month, birth_date.day)
if next_birthday < today:
    next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
days_until_birthday = (next_birthday - today).days

# ---------------------------
# Birthday Celebration
# ---------------------------
if today.month == birth_date.month and today.day == birth_date.day:
    st.balloons()
    st.success(f"🎉 Happy Birthday! You just turned {years} years old! 🎂")

# ---------------------------
# Main Age Card
# ---------------------------
st.markdown(f"<div class='card'><span class='highlight'>You are {years} years, {months} months, {days} days old.</span></div>", unsafe_allow_html=True)

# ---------------------------
# Info Cards
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='card'>📅 Born on: <b>{birth_date.strftime('%A')}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>🌌 Western Zodiac: <b>{get_zodiac(birth_date.month, birth_date.day)}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>🐉 Chinese Zodiac: <b>{get_chinese_zodiac(birth_date.year)}</b></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card'>📆 Days Lived: <b>{total_days:,}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>🎂 Days Until Birthday: <b>{days_until_birthday}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>🏆 Days Until 10,000th Day: <b>{days_until_10000}</b></div>", unsafe_allow_html=True)

# ---------------------------
# Fun Stats
# ---------------------------
st.subheader("✨ Fun Age Stats")
st.write(f"🕒 Seconds lived: {total_seconds:,}")
st.write(f"❤️ Estimated heartbeats: {total_heartbeats:,}")
st.write(f"🌬 Estimated breaths: {total_breaths:,}")

# ---------------------------
# Historical Events
# ---------------------------
st.subheader("📜 Historical Events on Your Birthday")
for event in get_historical_events(birth_date.month, birth_date.day):
    st.write(f"• {event}")

# ---------------------------
# Famous People with Images
# ---------------------------
st.subheader("🌟 Famous People Born on Your Birthday")
famous_people = get_famous_birthdays_with_images(birth_date.month, birth_date.day)
if famous_people:
    for person in famous_people:
        img = person["img_url"] if person["img_url"] else "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"
        st.markdown(f"""
        <div class='person'>
            <img src="{img}" alt="{person['name']}">
            <div><a href="https://en.wikipedia.org/wiki/{person['name'].replace(' ', '_')}" target="_blank">{person['name']}</a><br>{person['year']} — {person['description']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("No famous birthdays found.")

# ---------------------------
# Personalized Message
# ---------------------------
if years < 18:
    st.info("🌱 You are in the exciting growth phase of life. So much ahead!")
elif years < 60:
    st.info("🚀 Prime years! Keep exploring and making memories.")
else:
    st.info("🌟 A wealth of wisdom and experience. Keep inspiring others!")
