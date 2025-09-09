from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import uvicorn


iris = load_iris()
x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size=0.2,random_state=42)
model = LogisticRegression(max_iter=200)
model.fit(x_train,y_train)

app = FastAPI()

class IrisInput(BaseModel):
    sepal_length : float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict(data: IrisInput):
        x = [[data.sepal_length,data.sepal_width,data.petal_length,data.petal_width]]
        prediction = model.predict(x)[0]
        return {"prediction": iris.target_names[prediction]}

@app.get("/",response_class=HTMLResponse)
def home():
        return """
    <!DOCTYPE html>
    <html>
<head>
    <title>Iris Predictor</title>
</head>

<body>
    <h2>Iris Flower Prediction</h2>
    <input id="sl" placeholder="sepal length">
    <input id="sw" placeholder="Sepal width">
    <input id="pl" placeholder="Peta length">
    <input id="pw" placeholder="Petal width">
    <button onclick="predict()">predict</button>
    <p id="result"></p>

    <script>
        async function predict() {
            let data = {
                sepal_length: parseFloat(document.getElementById("sl").value),
                sepal_width: parseFloat(document.getElementById("sw").value),
                petal_length: parseFloat(document.getElementById("pl").value),
                petal_width: parseFloat(document.getElementById("pw").value)
            };
            let res = await
                fetch("/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
            });
            let result = await res.json();
            document.getElementById("result").innerText = "Prediction: " + result.prediction;

        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run("app:app",host="127.0.0.1",port =8000,reload=True)