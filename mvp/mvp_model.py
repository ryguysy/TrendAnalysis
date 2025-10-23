import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

if __name__ == "__main__":
    df = pd.read_csv('../data/mvp_dataset.csv', index_col='Date', parse_dates=True)

    features = ['MA_7', 'MA_14', 'Sentiment']
    df = df.dropna(subset=features)

    X = df[features]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model accuracy: {acc:.2f}")
    print(classification_report(y_test, y_pred, digits=3))
