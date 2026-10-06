from flask import Flask, request, render_template_string

app = Flask(__name__)

# Exact text data arrays mapping Source File 6 parameters
PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": (
            "Mon: Back Squat 5x5 + Core\n"
            "Tue: EMOM 20min Assault Bike\n"
            "Wed: Bench Press + 21-15-9\n"
            "Thu: Deadlift + Box Jumps\n"
            "Fri: Zone 2 Cardio 30min"
        ),
        "diet": (
            "Breakfast: Egg Whites + Oats\n"
            "Lunch: Grilled Chicken + Brown Rice\n"
            "Dinner: Fish Curry + Millet Roti\n"
            "Target: ~2000 kcal"
        ),
        "color": "#e74c3c",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": (
            "Mon: Squat 5x5\n"
            "Tue: Bench 5x5\n"
            "Wed: Deadlift 4x6\n"
            "Thu: Front Squat 4x8\n"
            "Fri: Incline Press 4x10\n"
            "Sat: Barbell Rows 4x10"
        ),
        "diet": (
            "Breakfast: Eggs + Peanut Butter Oats\n"
            "Lunch: Chicken Biryani\n"
            "Dinner: Mutton Curry + Rice\n"
            "Target: ~3200 kcal"
        ),
        "color": "#2ecc71",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": (
            "Full Body Circuit:\n"
            "- Air Squats\n"
            "- Ring Rows\n"
            "- Push-ups\n"
            "Focus: Technique & Consistency"
        ),
        "diet": (
            "Balanced Tamil Meals\n"
            "Idli / Dosa / Rice + Dal\n"
            "Protein Target: 120g/day"
        ),
        "color": "#3498db",
        "calorie_factor": 26
    }
}

# The embedded single-file visual markup architecture (Premium Dark Theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACEest Fitness & Performance</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #1a1a1a; color: white; margin: 0; padding: 0; }
        header { background-color: #d4af37; color: black; text-align: center; padding: 20px 0; font-weight: bold; font-size: 24px; letter-spacing: 1px; }
        .main-container { display: flex; max-width: 1150px; margin: 20px auto; padding: 0 20px; gap: 20px; }
        .left-panel { width: 300px; border: 2px solid #d4af37; border-radius: 5px; padding: 20px; background-color: #1a1a1a; box-sizing: border-box; }
        .panel-title { color: #d4af37; font-size: 18px; font-weight: bold; margin-top: 0; margin-bottom: 15px; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-size: 14px; color: #d4af37; font-weight: bold; }
        input[type="text"], input[type="number"], select { 
            width: 100%; padding: 8px; background-color: #333; color: white; border: 1px solid #555; border-radius: 4px; box-sizing: border-box; 
        }
        input[type="range"] { width: 100%; }
        .btn { width: 100%; padding: 10px; background-color: #d4af37; color: black; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .btn:hover { background-color: #bfa030; }
        .right-panel { flex-grow: 1; display: flex; flex-direction: column; gap: 20px; }
        .display-frame { border: 1px solid #d4af37; border-radius: 5px; padding: 15px; background-color: #1a1a1a; }
        .frame-title { color: #d4af37; font-size: 16px; margin-top: 0; margin-bottom: 10px; font-weight: bold; }
        .content-box { white-space: pre-line; font-size: 15px; line-height: 1.5; padding: 10px; min-height: 120px; background-color: #111; border-radius: 4px; }
        .placeholder { color: #666; font-style: italic; }
        .calorie-label { text-align: center; font-size: 18px; color: #d4af37; font-weight: bold; margin-top: 10px; padding: 10px; border: 1px dashed #d4af37; border-radius: 4px; }
        .alert-box { background-color: #2b2b1a; border: 1px solid #d4af37; color: #d4af37; padding: 10px; border-radius: 4px; margin-bottom: 15px; text-align: center; font-size: 14px; }
    </style>
</head>
<body>

    <header>ACEest FUNCTIONAL FITNESS SYSTEM</header>

    <div class="main-container">
        <!-- LEFT PANEL – CLIENT PROFILE INPUTS -->
        <div class="left-panel">
            <div class="panel-title">Client Profile</div>
            
            {% if flash_message %}
                <div class="alert-box">{{ flash_message }}</div>
            {% endif %}

            <form method="POST" action="/">
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" value="{{ form_data.name }}" placeholder="Enter Name">
                </div>
                
                <div class="form-group">
                    <label for="age">Age</label>
                    <input type="number" id="age" name="age" value="{{ form_data.age }}" placeholder="0">
                </div>
                
                <div class="form-group">
                    <label for="weight">Weight (kg)</label>
                    <input type="number" step="0.1" id="weight" name="weight" value="{{ form_data.weight }}" placeholder="0.0">
                </div>

                <div class="form-group">
                    <label for="program">Program</label>
                    <select name="program" id="program" onchange="this.form.submit()">
                        <option value="" disabled {% if not form_data.program %}selected{% endif %}>-- Select Program --</option>
                        {% for p in programs %}
                            <option value="{{ p }}" {% if form_data.program == p %}selected{% endif %}>{{ p }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="form-group">
                    <label for="adherence">Weekly Adherence (<span id="rangeVal">{{ form_data.adherence }}</span>%)</label>
                    <input type="range" id="adherence" name="adherence" min="0" max="100" value="{{ form_data.adherence }}" oninput="document.getElementById('rangeVal').innerText=this.value">
                </div>

                <button type="submit" name="action" value="save" class="btn">Save Client</button>
                <button type="submit" name="action" value="reset" class="btn" style="background-color: #555; color: white;">Reset</button>
            </form>
        </div>

        <!-- RIGHT PANEL – TRACKING AND DETAILS VIEWPORTS -->
        <div class="right-panel">
            <!-- Workout Display Frame Structure -->
            <div class="display-frame">
                <div class="frame-title">Weekly Training Plan</div>
                <div class="content-box" {% if selected_data %}style="color: {{ selected_data.color }}; font-weight: bold;"{% endif %}>
                    {% if selected_data %}
                        {{ selected_data.workout }}
                    {% else %}
                        <span class="placeholder">Select a profile to view workout</span>
                    {% endif %}
                </div>
            </div>

            <!-- Nutrition Display Frame Structure -->
            <div class="display-frame">
                <div class="frame-title">Nutrition Plan (TN Context)</div>
                <div class="content-box">
                    {% if selected_data %}
                        {{ selected_data.diet }}
                    {% else %}
                        <span class="placeholder">Select a profile to view diet</span>
                    {% endif %}
                </div>
            </div>

            <div class="calorie-label">
                Estimated Calories: {{ estimated_calories }}
            </div>
        </div>
    </div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    form_data = {"name": "", "age": "", "weight": "", "program": "", "adherence": "0"}
    selected_data = None
    estimated_calories = "--"
    flash_message = None

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "reset":
            return render_template_string(
                HTML_TEMPLATE, programs=PROGRAMS.keys(), form_data=form_data,
                selected_data=selected_data, estimated_calories=estimated_calories, flash_message=flash_message
            )

        form_data["name"] = request.form.get("name", "")
        form_data["age"] = request.form.get("age", "")
        form_data["weight"] = request.form.get("weight", "")
        form_data["program"] = request.form.get("program", "")
        form_data["adherence"] = request.form.get("adherence", "0")

        if form_data["program"] in PROGRAMS:
            selected_data = PROGRAMS[form_data["program"]]
            
            if form_data["weight"]:
                try:
                    weight_val = float(form_data["weight"])
                    if weight_val > 0:
                        calories = int(weight_val * selected_data["calorie_factor"])
                        estimated_calories = f"{calories} kcal"
                except ValueError:
                    pass

        if action == "save":
            if not form_data["name"] or not form_data["program"]:
                flash_message = "⚠️ Incomplete: Please fill client name and program."
            else:
                flash_message = f"ℹ️ Saved: Client {form_data['name']} saved successfully. Adherence: {form_data['adherence']}%"

    return render_template_string(
        HTML_TEMPLATE, 
        programs=PROGRAMS.keys(), 
        form_data=form_data, 
        selected_data=selected_data, 
        estimated_calories=estimated_calories,
        flash_message=flash_message
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
