# ☁ Skyglass — Weather Dashboard

A clean, minimal weather dashboard built with vanilla HTML, CSS, and JavaScript. Shows real-time weather conditions and a 5-day forecast for any city worldwide.

![Skyglass Preview](preview.png)

## ✨ Features

- 🔍 Search any city in the world
- 🌡️ Real-time temperature, humidity, wind, visibility & pressure
- 📅 5-day forecast with daily high/low
- 🌙 Animated dark UI with ambient background effects
- 📱 Fully responsive (mobile-friendly)
- ⚡ Demo mode works without an API key

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/skyglass-weather.git
cd skyglass-weather
```

### 2. Get a free API key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Go to **API Keys** in your account dashboard
3. Copy your key

### 3. Add your API key

Open `app.js` and replace the placeholder on line 5:

```js
const API_KEY = "YOUR_API_KEY_HERE"; // ← paste here
```

### 4. Open in browser

Just open `index.html` directly in your browser — no build step needed!

```bash
open index.html       # macOS
start index.html      # Windows
xdg-open index.html   # Linux
```

> **Note:** The app runs in demo mode automatically if no API key is set, so you can preview it right away.

## 🗂️ Project Structure

```
skyglass-weather/
├── index.html     # App layout & structure
├── style.css      # All styling & animations
├── app.js         # Weather API logic & rendering
└── README.md      # You're reading this!
```

## 🛠️ Tech Stack

- **HTML5** — semantic structure
- **CSS3** — custom properties, animations, grid & flexbox
- **Vanilla JS** — Fetch API, async/await, DOM manipulation
- **OpenWeatherMap API** — live weather & forecast data

## 📸 Screenshots

| Current Weather | 5-Day Forecast |
|---|---|
| *(Add your own screenshots here)* | *(Add your own screenshots here)* |

## 🔮 Possible Improvements

- [ ] Toggle between °C and °F
- [ ] Geolocation support (use your current location)
- [ ] Hourly forecast chart
- [ ] Save favourite cities with localStorage
- [ ] Dark/light theme toggle

## 📄 License

MIT — free to use and modify.

---

Built with ☁ and vanilla JS.
