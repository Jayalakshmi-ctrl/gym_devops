from flask import Flask, request, render_template_string

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "B: 3 Egg Whites + Oats Idli\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: 2,000 kcal",
        "color": "#e74c3c"
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "B: 4 Eggs + PB Oats\nL: Chicken Biryani (250g Chicken)\nD: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal",
        "color": "#2ecc71"
    },
    "Beginner (BG)": {
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups.\nFocus: Technique Mastery & Form (90% Threshold)",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati.\nProtein: 120g/day",
        "color": "#3498db"
    }
}

# This is the raw string Flask uses to communicate with your web browser
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ACEest Fitness</title>
    <style>
        body { background: #1a1a1a; color: white; font-family: Arial; margin: 0; }
        header { background: #d4af37; color: black; text-align: center; padding: 15px; font-size: 22px; font-weight: bold; }
        .container { display: flex; padding: 20px; gap: 20px; max-width: 1100px; margin: auto; }
        .left { width: 300px; border: 2px solid #d4af37; padding: 20px; border-radius: 5px; }
        .right { flex: 1; display: flex; flex-direction: column; gap: 20px; }
        .box { border: 1px solid #d4af37; padding: 15px; border-radius: 5px; white-space: pre-line; }
        select { width: 100%; padding: 8px; background: #333; color: white; border: 1px solid #555; }
    </style>
</head>
<body>
    <header>ACEest FUNCTIONAL FITNESS</header>
    <div class="container">
        <div class="left">
            <h3>Client Profile</h3>
            <form method="POST">
                <label>Select Program:</label>
                <select name="program" onchange="this.form.submit()">
                    <option value="" disabled {% if not selected %}selected{% endif %}>-- Select --</option>
                    {% for p in programs %}
                        <option value="{{ p }}" {% if selected == p %}selected{% endif %}>{{ p }}</option>
                    {% endfor %}
                </select>
            </form>
            <p style="margin-top: 50px; background: #333; padding: 10px; font-family: monospace;">
                CAPACITY: 150 Users<br>AREA: 10,000 sq ft<br>BREAK-EVEN: 250 Members
            </p>
        </div>
        <div class="right">
            <div class="box">
                <h4>Weekly Workout Chart</h4>
                {% if data %}
                    <span style="color: {{ data.color }}; font-weight: bold;">{{ data.workout }}</span>
                {% else %}
                    <span style="color: #666;">Select a profile to view workout</span>
                {% endif %}
            </div>
            <div class="box">
                <h4>Daily Nutrition Plan (Tamil Nadu Context)</h4>
                {% if data %}
                    {{ data.diet }}
                {% else %}
                    <span style="color: #666;">Select a profile to view diet</span>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    selected = request.form.get("program") if request.method == "POST" else None
    data = PROGRAMS.get(selected) if selected in PROGRAMS else None
    
    return render_template_string(
        BASE_HTML, 
        programs=PROGRAMS.keys(), 
        selected=selected, 
        data=data
    )

if __name__ == "__main__":
    # host='0.0.0.0' tells Flask to accept external connections from your machine
    app.run(debug=True, host='0.0.0.0', port=5000)

