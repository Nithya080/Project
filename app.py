from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
# Load dataset
data = pd.read_csv("Test.csv")

# Clean data
data['Item_Type'] = data['Item_Type'].astype(str).str.strip().str.title()
data['Outlet_Identifier'] = data['Outlet_Identifier'].astype(str).str.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    store_id = request.form['store_id'].strip()
    category = request.form['category'].strip().title()
    min_price = float(request.form['min_price'])
    max_price = float(request.form['max_price'])

    filtered_data = data[
        (data['Outlet_Identifier'] == store_id) &
        (data['Item_Type'] == category) &
        (data['Item_MRP'] >= min_price) &
        (data['Item_MRP'] <= max_price)
    ]

    if filtered_data.empty:
        prediction = "No matching products found"
    else:
        prediction = round(filtered_data['Item_MRP'].mean() * 10, 2)

    return render_template(
        "result.html",
        store_id=store_id,
        category=category,
        prediction=prediction
    )

if __name__ == "__main__":
    app.run(debug=True)