// ─────────────────────────────────────────
//  🔑  PASTE YOUR API KEY HERE
//  Get one free at https://openweathermap.org/api
// ─────────────────────────────────────────
const API_KEY = "YOUR_API_KEY_HERE";
const BASE_URL = "https://api.openweathermap.org/data/2.5";

// ── DOM refs ──────────────────────────────
const cityInput     = document.getElementById("cityInput");
const searchBtn     = document.getElementById("searchBtn");
const weatherCard   = document.getElementById("weatherCard");
const forecastSec   = document.getElementById("forecastSection");
const errorMsg      = document.getElementById("errorMsg");

// ── Weather icon mapping ──────────────────
const iconMap = {
  "01d": "☀️",  "01n": "🌙",
  "02d": "⛅",  "02n": "🌥️",
  "03d": "☁️",  "03n": "☁️",
  "04d": "☁️",  "04n": "☁️",
  "09d": "🌧️", "09n": "🌧️",
  "10d": "🌦️", "10n": "🌧️",
  "11d": "⛈️", "11n": "⛈️",
  "13d": "❄️",  "13n": "❄️",
  "50d": "🌫️", "50n": "🌫️",
};

function getIcon(code) {
  return iconMap[code] || "🌡️";
}

// ── Fetch current weather ─────────────────
async function fetchWeather(city) {
  const res = await fetch(
    `${BASE_URL}/weather?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`
  );
  if (!res.ok) throw new Error("City not found");
  return res.json();
}

// ── Fetch 5-day forecast ──────────────────
async function fetchForecast(city) {
  const res = await fetch(
    `${BASE_URL}/forecast?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`
  );
  if (!res.ok) throw new Error("Forecast unavailable");
  return res.json();
}

// ── Render current weather ────────────────
function renderWeather(data) {
  document.getElementById("cityName").textContent   = data.name;
  document.getElementById("country").textContent    = data.sys.country;
  document.getElementById("temp").textContent       = Math.round(data.main.temp);
  document.getElementById("desc").textContent       = data.weather[0].description;
  document.getElementById("feels").textContent      = `Feels like ${Math.round(data.main.feels_like)}°C`;
  document.getElementById("humidity").textContent   = `${data.main.humidity}%`;
  document.getElementById("wind").textContent       = `${Math.round(data.wind.speed)} m/s`;
  document.getElementById("visibility").textContent = `${(data.visibility / 1000).toFixed(1)} km`;
  document.getElementById("pressure").textContent   = `${data.main.pressure} hPa`;
  document.getElementById("weatherIcon").textContent = getIcon(data.weather[0].icon);

  weatherCard.classList.remove("hidden");
}

// ── Render 5-day forecast ─────────────────
function renderForecast(data) {
  const grid = document.getElementById("forecastGrid");
  grid.innerHTML = "";

  // Pick one reading per day (noon-ish), skip today
  const days = {};
  data.list.forEach(item => {
    const date = new Date(item.dt * 1000);
    const dayKey = date.toDateString();
    const hour = date.getHours();
    if (!days[dayKey] && hour >= 11 && hour <= 14) {
      days[dayKey] = item;
    }
  });

  // Fallback: just take first occurrence per day
  if (Object.keys(days).length < 2) {
    data.list.forEach(item => {
      const dayKey = new Date(item.dt * 1000).toDateString();
      if (!days[dayKey]) days[dayKey] = item;
    });
  }

  const entries = Object.values(days).slice(0, 5);

  entries.forEach(item => {
    const date = new Date(item.dt * 1000);
    const dayName = date.toLocaleDateString("en-US", { weekday: "short" });

    const card = document.createElement("div");
    card.className = "forecast-card";
    card.innerHTML = `
      <div class="fc-day">${dayName}</div>
      <div class="fc-icon">${getIcon(item.weather[0].icon)}</div>
      <div class="fc-temp">${Math.round(item.main.temp_max)}°</div>
      <div class="fc-min">${Math.round(item.main.temp_min)}°</div>
    `;
    grid.appendChild(card);
  });

  forecastSec.classList.remove("hidden");
}

// ── Main search handler ───────────────────
async function search() {
  const city = cityInput.value.trim();
  if (!city) return;

  errorMsg.classList.add("hidden");
  weatherCard.classList.add("hidden");
  forecastSec.classList.add("hidden");

  if (API_KEY === "YOUR_API_KEY_HERE") {
    showDemo(city);
    return;
  }

  try {
    const [weatherData, forecastData] = await Promise.all([
      fetchWeather(city),
      fetchForecast(city),
    ]);
    renderWeather(weatherData);
    renderForecast(forecastData);
  } catch (err) {
    errorMsg.classList.remove("hidden");
  }
}

// ── Demo mode (no API key needed) ─────────
function showDemo(city) {
  const demoWeather = {
    name: city || "London",
    sys: { country: "GB" },
    main: { temp: 18, feels_like: 16, humidity: 72, pressure: 1013 },
    wind: { speed: 4.2 },
    visibility: 9000,
    weather: [{ description: "partly cloudy", icon: "02d" }],
  };
  const days = ["Mon","Tue","Wed","Thu","Fri"];
  const icons = ["01d","02d","10d","03d","01d"];
  const temps = [22,18,14,16,21];
  const mins  = [13,11, 9,10,14];

  renderWeather(demoWeather);

  const grid = document.getElementById("forecastGrid");
  grid.innerHTML = "";
  days.forEach((d, i) => {
    const card = document.createElement("div");
    card.className = "forecast-card";
    card.innerHTML = `
      <div class="fc-day">${d}</div>
      <div class="fc-icon">${getIcon(icons[i])}</div>
      <div class="fc-temp">${temps[i]}°</div>
      <div class="fc-min">${mins[i]}°</div>
    `;
    grid.appendChild(card);
  });
  forecastSec.classList.remove("hidden");
}

// ── Event listeners ───────────────────────
searchBtn.addEventListener("click", search);
cityInput.addEventListener("keydown", e => {
  if (e.key === "Enter") search();
});

// ── Load a default city on start ──────────
window.addEventListener("DOMContentLoaded", () => {
  cityInput.value = "London";
  search();
});
