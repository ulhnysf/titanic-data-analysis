import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Veri yükleme (SQL veritabanını bağlama ve sorgulama) - **Applying SQL to Real-World Problems**, **Analyzing Business Data in SQL**
conn = sqlite3.connect(r"titanicdeneme.db")

query = """
SELECT Pclass, Sex, Age, Fare, Survived 
FROM tested;
"""
df = pd.read_sql_query(query, conn)

# Verilerin hazırlanması ve manipülasyonu - **Data Manipulation with pandas**, **Analyzing Marketing Campaigns with pandas**
df['Age'] = df['Age'].fillna(df['Age'].mean())  # Yaşda eksik veriler için ortalama değer
df['Fare'] = df['Fare'].fillna(df['Fare'].mean())  # Fare'de eksik veriler için ortalama değer

# Kategorik verileri sayısal verilere dönüştürme - **Data Manipulation with pandas**
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# Yaş grubu ve bilet ücreti grubu oluşturma - **Analyzing US Census Data in Python**
df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 40, 80], labels=['Child', 'Adult', 'Senior'])
df['Fare_Group'] = pd.cut(df['Fare'], bins=[0, 10, 50, 100, 600], labels=['Low Fare', 'Medium Fare', 'High Fare', 'Very High Fare'])

# A/B testi için verilerin hazırlanması - **A/B Testing in Python**
ab_test_data = df.groupby('Sex')['Survived'].mean().reset_index()

# Makine öğrenmesi modelinin eğitilmesi - **Introduction to Deep Learning in Python** (model eğitimine dair genel bilgi, ancak derin öğrenme değil, karar ağaçları uyguladım.)
X = df[['Pclass', 'Sex', 'Age', 'Fare']]
y = df['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

# Dash Uygulaması - **Building Dashboards with Dash and Plotly**
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Titanic Veri Analizi", style={"textAlign": "center"}),

    # Model doğruluğu
    html.Div(f"Model Doğruluğu: {accuracy * 100:.2f}%", style={"textAlign": "center"}),

    # Sınıfa göre hayatta kalma oranı
    dcc.Graph(
        id="class-survival-rate",
        figure=px.bar(
            df.groupby("Pclass", observed=False)["Survived"].mean().reset_index(),
            x="Pclass",
            y="Survived",
            labels={"Survived": "Survival Rate", "Pclass": "Passenger Class"},
            title="Sınıfa Göre Hayatta Kalma Oranı"
        )
    ),

    # Cinsiyete göre hayatta kalma oranı
    dcc.Graph(
        id="sex-survival-rate",
        figure=px.pie(
            df, names="Sex", values="Survived",
            title="Cinsiyete Göre Hayatta Kalma Oranı"
        )
    ),

    # Yaş gruplarına göre hayatta kalma oranı
    dcc.Graph(
        id="age-group-survival-rate",
        figure=px.bar(
            df.groupby("Age_Group", observed=False)["Survived"].mean().reset_index(),
            x="Age_Group",
            y="Survived",
            labels={"Survived": "Survival Rate", "Age_Group": "Age Group"},
            title="Yaş Gruplarına Göre Hayatta Kalma Oranı"
        )
    ),

    # Bilet ücreti ve hayatta kalma ilişkisi
    dcc.Graph(
        id="fare-group-survival-rate",
        figure=px.bar(
            df.groupby("Fare_Group", observed=False)["Survived"].mean().reset_index(),
            x="Fare_Group",
            y="Survived",
            labels={"Survived": "Survival Rate", "Fare_Group": "Fare Group"},
            title="Bilet Ücreti ve Hayatta Kalma İlişkisi"
        )
    ),

    # A/B testi sonuçları (Cinsiyete göre hayatta kalma oranı farkı)
    dcc.Graph(
        id="ab-test-results",
        figure=px.bar(
            ab_test_data,
            x="Sex",
            y="Survived",
            labels={"Survived": "Survival Rate", "Sex": "Gender"},
            title="Cinsiyetler Arasında Hayatta Kalma Oranı A/B Testi"
        )
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)


