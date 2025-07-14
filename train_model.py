import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib
from preprocess import clean_text


def main():
    df = pd.read_csv("text_emotions.csv")
    X = df["content"].apply(clean_text)
    y = df["sentiment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )

    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2), min_df=5, max_df=0.85, max_features=10000
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    solver="liblinear", class_weight="balanced", max_iter=1000
                ),
            ),
        ]
    )

    param_grid = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__max_df": [0.75, 0.85, 1.0],
        "clf__C": [0.1, 1, 10],
        "clf__penalty": ["l2"],
    }

    grid = GridSearchCV(
        model, param_grid, cv=5, scoring="f1_macro", n_jobs=-1, verbose=2
    )
    grid.fit(X_train, y_train)
    model = grid.best_estimator_

    y_pred = model.predict(X_test)

    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(model, "best_model.pkl")


if __name__ == "__main__":
    main()
