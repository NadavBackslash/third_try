import sqlite3  # #3: Using SQLite without sanitation is prone to SQL Injection
import requests  # type: ignore # #5: Can be safe, but shown here with unsafe usage
import yaml  # #4: PyYAML's `load` is unsafe with untrusted input

# #1: Hardcoded API key instead of using environment variables (.env)
API_KEY = "sk-1234567890abcdef"  # 🔐 problem #1 - API key is hardcoded, not stored in secure .env

def login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 🔓 problem #2 - SQL Injection: user inputs directly included in query string
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # problem #2
    cursor.execute(query)
    
    result = cursor.fetchone()


    if result:
        print("Login successful!")
    else:
        print("Invalid credentials")

def get_weather(city):
    # 🔓 problem #5 - API key is embedded in URL without protection
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    print(response.text)

def load_config(file_path):
    with open(file_path, 'r') as f:
        # ⚠️ problem #4 - yaml.load allows arbitrary code execution when given malicious YAML
        config = yaml.load(f, Loader=yaml.Loader)  # should use safe_load
        print(config)

if __name__ == "__main__":
    # Simulate unsafe usage
    login("admin'; --", "irrelevant")
    get_weather("New York")
    load_config("config.yaml")  # assume this file may contain unsafe content
