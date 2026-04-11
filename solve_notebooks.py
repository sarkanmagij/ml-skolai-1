#!/usr/bin/env python3
"""Fill blanks in all course notebooks (by explicit cell replacement)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def to_src(text: str) -> list[str]:
    if not text:
        return []
    lines = text.splitlines(keepends=True)
    return lines


def write_nb(path: Path, nb: dict) -> None:
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def load_nb(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def set_code_cell(nb: dict, index: int, source: str) -> None:
    cell = nb["cells"][index]
    assert cell["cell_type"] == "code", (index, cell["cell_type"])
    cell["source"] = to_src(source)


def main() -> None:
    # ----- 1: EDA — Palmer Penguins -----
    p = ROOT / "1/02_EDA_Penguins_assignment_unsolved.ipynb"
    if p.is_file():
        nb = load_nb(p)
        for i, s in [
            (
                4,
                """df = sns.load_dataset("penguins")
df.head()
""",
            ),
            (7, "print(df.shape)\n"),
            (9, "df.dtypes\n"),
            (11, "df.info()\n"),
            (14, "df.isnull().sum()\n"),
            (16, "(df.isnull().sum() / len(df) * 100).round(2)\n"),
            (
                18,
                """df_clean = df.dropna()
print(df_clean.shape)
""",
            ),
            (21, "df_clean.describe()\n"),
            (
                23,
                """df_clean.groupby("species")[["bill_length_mm", "bill_depth_mm"]].mean()
""",
            ),
            (25, 'df_clean["island"].value_counts()\n'),
            (
                28,
                """sns.histplot(data=df_clean, x="flipper_length_mm", hue="species", bins=30)
plt.title("Distribution of Flipper Length by Species")
plt.show()
""",
            ),
            (
                30,
                """sns.boxplot(data=df_clean, x="species", y="body_mass_g")
plt.title("Body Mass by Species")
plt.show()
""",
            ),
            (
                32,
                """sns.scatterplot(data=df_clean, x="bill_length_mm", y="bill_depth_mm", hue="species")
plt.title("Bill Length vs. Bill Depth")
plt.show()
""",
            ),
            (
                34,
                """corr = df_clean.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()
""",
            ),
            (
                36,
                """sns.pairplot(df_clean, hue="species")
plt.show()
""",
            ),
            (
                39,
                """sns.countplot(data=df_clean, x="island", hue="species")
plt.title("Penguin Species Count per Island")
plt.show()
""",
            ),
        ]:
            set_code_cell(nb, i, s)
        write_nb(p, nb)

    # ----- 2: Linear regression (ensure solved; patch only code cell sources) -----
    p2 = ROOT / "2/05_LinearRegression_AutoMPG_unsolved.ipynb"
    nb = load_nb(p2)
    reps = [
        ("sns.load_dataset(___)", 'sns.load_dataset("mpg")'),
        ('print("Shape:", df.___)', 'print("Shape:", df.shape)'),
        ("df.isnull().___()", "df.isnull().sum()"),
        ("df_clean = df.___()", "df_clean = df.dropna()"),
        ('include="number").___()', 'include="number").corr()'),
        ("sns.___(corr", "sns.heatmap(corr"),
        ("x=___, y=___", 'x="weight", y="mpg"'),
        ("df_clean[[___]]", 'df_clean[["weight"]]'),
        ('df_clean[___]', 'df_clean["mpg"]'),
        ("test_size=___, random_state=___", "test_size=0.2, random_state=42"),
        ("model.___(X_train, y_train)", "model.fit(X_train, y_train)"),
        ("y_pred = model.___(X_test)", "y_pred = model.predict(X_test)"),
        ("mean_squared_error(y_test, ___", "mean_squared_error(y_test, y_pred"),
        ("mean_absolute_error(y_test, ___", "mean_absolute_error(y_test, y_pred"),
        ("r2_score(y_test, ___", "r2_score(y_test, y_pred"),
        ("plt.ylabel(___)", 'plt.ylabel("Predicted MPG")'),
        ("model.___(X_sorted)", "model.predict(X_sorted)"),
        ("{model.___[0]", "{model.coef_[0]"),
        ("{model.___:.4f}", "{model.intercept_:.4f}"),
    ]
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        s = "".join(cell.get("source", []))
        for a, b in reps:
            s = s.replace(a, b)
        cell["source"] = to_src(s)
    write_nb(p2, nb)

    # ----- 3: Logistic Iris -----
    p = ROOT / "3/06_LogisticRegression_Iris_unsolved.ipynb"
    nb = load_nb(p)
    for i, s in [
        (
            4,
            """iris = load_iris(as_frame=True)
df = iris.frame
df.head()
""",
        ),
        (
            7,
            """print("Shape:", df.shape)
print()
print(df.isnull().sum())
""",
        ),
        (
            9,
            """print(df["target"].value_counts())
print()
print("Class names:", iris.target_names)
""",
        ),
        (11, """sns.pairplot(df, hue="target")
plt.show()
"""),
        (
            14,
            """X = df.drop(columns=["target"])
y = df["target"]

print("X shape:", X.shape)
print("y shape:", y.shape)
""",
        ),
        (
            17,
            """X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train:", X_train.shape, "  Test:", X_test.shape)
""",
        ),
        (
            20,
            """scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)
""",
        ),
        (
            23,
            """model = LogisticRegression(max_iter=200)
model.fit(X_train_sc, y_train)
""",
        ),
        (26, "y_pred = model.predict(X_test_sc)\ny_pred\n"),
        (29, """acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.4f}")
"""),
        (
            31,
            """cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm, display_labels=iris.target_names).plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()
""",
        ),
        (
            33,
            """print(classification_report(y_test, y_pred, target_names=iris.target_names))
""",
        ),
        (
            36,
            """proba = model.predict_proba(X_test_sc)
pd.DataFrame(proba, columns=iris.target_names).head()
""",
        ),
        (
            38,
            """print(f"Sum of first row: {proba[0].sum():.4f}")
# Each row is a probability vector over classes, so it sums to 1.
""",
        ),
        (
            41,
            """# Select two features
X2 = df[["petal length (cm)", "petal width (cm)"]]
y2 = df["target"]

X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y2, test_size=0.2, random_state=42, stratify=y2
)

scaler2 = StandardScaler()
X2_train_sc = scaler2.fit_transform(X2_train)
X2_test_sc  = scaler2.transform(X2_test)

model2 = LogisticRegression(max_iter=200)
model2.fit(X2_train_sc, y2_train)

# ── Plot decision boundary (provided) ──
h = 0.02
x_min, x_max = X2_train_sc[:, 0].min() - 1, X2_train_sc[:, 0].max() + 1
y_min, y_max = X2_train_sc[:, 1].min() - 1, X2_train_sc[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                      np.arange(y_min, y_max, h))
Z = model2.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap="Set2")
scatter = plt.scatter(X2_train_sc[:, 0], X2_train_sc[:, 1],
                      c=y2_train, cmap="Set2", edgecolors="k", s=50)
plt.xlabel("Petal Length (scaled)")
plt.ylabel("Petal Width (scaled)")
plt.title("Decision Boundary — 2-Feature Logistic Regression")
plt.colorbar(scatter, ticks=[0, 1, 2], label="Species")
plt.show()
""",
        ),
    ]:
        set_code_cell(nb, i, s)
    write_nb(p, nb)

    # ----- 4: Decision trees -----
    p = ROOT / "4/07_decision_trees_exercise.ipynb"
    nb = load_nb(p)
    set_code_cell(
        nb,
        2,
        """import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
""",
    )
    for i, s in [
        (
            4,
            """wine = load_wine()

df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['target'] = wine.target

print(f"Shape: {df.shape}")
df.head()
""",
        ),
        (
            6,
            """X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"Training samples: {X_train.shape[0]}")
print(f"Test samples:     {X_test.shape[0]}")
""",
        ),
        (
            8,
            """clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

print("Model trained successfully!")
""",
        ),
        (
            10,
            """y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2%}")
print()
print(classification_report(y_test, y_pred, target_names=wine.target_names))
""",
        ),
        (
            12,
            """plt.figure(figsize=(16, 8))
plot_tree(
    clf,
    feature_names=wine.feature_names,
    class_names=list(wine.target_names),
    filled=True,
    rounded=True,
    fontsize=9,
)
plt.title("Decision Tree — Wine Dataset (max_depth=3)")
plt.tight_layout()
plt.show()
""",
        ),
        (
            14,
            """importances = pd.Series(clf.feature_importances_, index=wine.feature_names)
importances = importances.sort_values(ascending=True)

plt.figure(figsize=(8, 5))
importances.plot(kind='barh', color='steelblue')
plt.title("Feature Importances")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()
""",
        ),
        (
            16,
            """depths = range(1, 11)
train_acc = []
test_acc = []

for d in depths:
    model = DecisionTreeClassifier(max_depth=d, random_state=42)
    model.fit(X_train, y_train)
    train_acc.append(accuracy_score(y_train, model.predict(X_train)))
    test_acc.append(accuracy_score(y_test, model.predict(X_test)))

plt.figure(figsize=(8, 4))
plt.plot(depths, train_acc, 'o-', label='Train')
plt.plot(depths, test_acc, 's--', label='Test')
plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('Train vs Test Accuracy by Tree Depth')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
""",
        ),
    ]:
        set_code_cell(nb, i, s)
    write_nb(p, nb)

    # ----- 5: Random Forest -----
    p = ROOT / "5/08_Exercise_02_RandomForest_RockOrMine_UNSOLVED (1).ipynb"
    nb = load_nb(p)
    set_code_cell(
        nb,
        2,
        "# OpenML is used here so the notebook runs without the UCI ML Repo API.\n"
        "# (Original exercise used: pip install ucimlrepo)\n",
    )
    set_code_cell(
        nb,
        4,
        """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

np.random.seed(42)
""",
    )
    set_code_cell(
        nb,
        6,
        """from sklearn.datasets import fetch_openml

sonar = fetch_openml(data_id=40, as_frame=True, parser="auto")
X_raw = sonar.data
y_labels = sonar.target.map({"Mine": "M", "Rock": "R"})

df = pd.concat([X_raw.reset_index(drop=True), y_labels.rename("target")], axis=1)
df.columns = [*range(60), "target"]

print(f"Shape: {df.shape}")
df.head()
""",
    )
    set_code_cell(
        nb,
        8,
        """print(df["target"].value_counts())
print()
print(df.describe().T.head(10))
""",
    )
    set_code_cell(
        nb,
        11,
        """X = df.drop("target", axis=1)
y = df["target"]

print("X shape:", X.shape)
print("y shape:", y.shape)
""",
    )
    set_code_cell(
        nb,
        13,
        """X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print("Train:", X_train.shape, "| Test:", X_test.shape)
""",
    )
    set_code_cell(
        nb,
        15,
        """rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
)
rf.fit(X_train, y_train)
""",
    )
    set_code_cell(nb, 17, "y_pred = rf.predict(X_test)\n")
    set_code_cell(
        nb,
        19,
        """acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.4f}\\n")
print(classification_report(y_test, y_pred))
""",
    )
    set_code_cell(
        nb,
        20,
        """cm = confusion_matrix(y_test, y_pred, labels=["M", "R"])
disp = ConfusionMatrixDisplay(cm, display_labels=["Mine", "Rock"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()
""",
    )
    set_code_cell(
        nb,
        22,
        """importances = pd.Series(rf.feature_importances_, index=X.columns)
top15 = importances.nlargest(15)

plt.figure(figsize=(8, 5))
top15.sort_values().plot.barh(color="steelblue")
plt.xlabel("Importance")
plt.title("Top 15 Feature Importances")
plt.tight_layout()
plt.show()
""",
    )
    set_code_cell(
        nb,
        24,
        """rf2 = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    random_state=42,
)
rf2.fit(X_train, y_train)
y_pred2 = rf2.predict(X_test)
print(f"New accuracy: {accuracy_score(y_test, y_pred2):.4f}")
""",
    )
    write_nb(p, nb)

    # ----- 6: XGBoost -----
    p = ROOT / "6/11_XGBoost_unsolved.ipynb"
    nb = load_nb(p)
    set_code_cell(
        nb,
        2,
        """import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
""",
    )
    set_code_cell(
        nb,
        4,
        """from sklearn.datasets import load_iris

data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
""",
    )
    set_code_cell(nb, 6, "dtrain = xgb.DMatrix(X_train, label=y_train)\ndtest = xgb.DMatrix(X_test, label=y_test)\n")
    set_code_cell(
        nb,
        8,
        """params = {
    'objective': 'multi:softmax',
    'num_class': 3,
    'max_depth': 4,
    'eta': 0.1,
    'eval_metric': 'mlogloss'
}
""",
    )
    set_code_cell(nb, 10, "num_round = 80\nbst = xgb.train(params, dtrain, num_round)\n")
    set_code_cell(nb, 12, "y_pred = bst.predict(dtest).astype(int)\n")
    set_code_cell(
        nb,
        14,
        """accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
""",
    )
    set_code_cell(
        nb,
        16,
        """from xgboost import XGBClassifier

xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
xgb_model.fit(X_train, y_train)

y_pred = xgb_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
""",
    )
    write_nb(p, nb)

    # ----- 7: GBM -----
    p = ROOT / "7/GBM_Comparison_UNSOLVED.ipynb"
    nb = load_nb(p)
    set_code_cell(nb, 2, "# pip install xgboost lightgbm catboost scikit-learn pandas matplotlib seaborn\n")
    set_code_cell(
        nb,
        5,
        """from pathlib import Path

df = pd.read_csv(Path("bank.csv"))
if "deposit" in df.columns and "y" not in df.columns:
    df = df.rename(columns={"deposit": "y"})
""",
    )
    set_code_cell(
        nb,
        6,
        """print('Column types:')
print(df.dtypes)

numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.drop('y').tolist()

print(f'\\nNumerical columns: {numerical_cols}')
print(f'Categorical columns: {categorical_cols}')
""",
    )
    set_code_cell(
        nb,
        7,
        """print('Target distribution:')
print(df['y'].value_counts())
print(f'\\nPositive class ratio: {(df["y"] == "yes").mean():.1%}')
""",
    )
    set_code_cell(
        nb,
        8,
        """print('Missing values per column:')
print(df.isnull().sum())
""",
    )
    set_code_cell(
        nb,
        11,
        """df['target'] = (df['y'] == 'yes').astype(int)

X = df.drop(columns=['y', 'target'])
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f'Training set: {X_train.shape[0]} samples')
print(f'Test set:     {X_test.shape[0]} samples')
print(f'Positive class in train: {y_train.mean():.1%}')
print(f'Positive class in test:  {y_test.mean():.1%}')
""",
    )
    set_code_cell(
        nb,
        12,
        """X_train_xgb = X_train.copy()
X_test_xgb = X_test.copy()

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X_train_xgb[col] = le.fit_transform(X_train_xgb[col])
    X_test_xgb[col] = le.transform(X_test_xgb[col])
    label_encoders[col] = le

print('XGBoost data ready (label encoded)')
X_train_xgb.head()
""",
    )
    set_code_cell(
        nb,
        13,
        """X_train_lgb = X_train_xgb.copy()
X_test_lgb = X_test_xgb.copy()

for col in categorical_cols:
    X_train_lgb[col] = X_train_lgb[col].astype('category')
    X_test_lgb[col] = X_test_lgb[col].astype('category')

print('LightGBM data ready (category dtype)')
print(X_train_lgb.dtypes)
""",
    )
    set_code_cell(
        nb,
        14,
        """X_train_cat = X_train.copy()
X_test_cat = X_test.copy()

cat_feature_indices = [X_train_cat.columns.get_loc(col) for col in categorical_cols]

print('CatBoost data ready (raw categorical features)')
print(f'Categorical feature indices: {cat_feature_indices}')
X_train_cat.head()
""",
    )
    set_code_cell(
        nb,
        18,
        """xgb_model = XGBClassifier(
    n_estimators=N_ESTIMATORS,
    learning_rate=LEARNING_RATE,
    max_depth=MAX_DEPTH,
    random_state=RANDOM_STATE,
    eval_metric='logloss',
    use_label_encoder=False,
    verbosity=0
)

start_time = time.time()
xgb_model.fit(X_train_xgb, y_train)
xgb_train_time = time.time() - start_time

xgb_pred = xgb_model.predict(X_test_xgb)
xgb_pred_proba = xgb_model.predict_proba(X_test_xgb)[:, 1]

results['XGBoost'] = {
    'accuracy': accuracy_score(y_test, xgb_pred),
    'roc_auc': roc_auc_score(y_test, xgb_pred_proba),
    'train_time': xgb_train_time,
    'model': xgb_model
}

print(f'XGBoost trained in {xgb_train_time:.2f} seconds')
print(f'Accuracy: {results["XGBoost"]["accuracy"]:.4f}')
print(f'ROC AUC:  {results["XGBoost"]["roc_auc"]:.4f}')
""",
    )
    set_code_cell(
        nb,
        20,
        """lgb_model = LGBMClassifier(
    n_estimators=N_ESTIMATORS,
    learning_rate=LEARNING_RATE,
    max_depth=MAX_DEPTH,
    random_state=RANDOM_STATE,
    verbose=-1
)

start_time = time.time()
lgb_model.fit(X_train_lgb, y_train)
lgb_train_time = time.time() - start_time

lgb_pred = lgb_model.predict(X_test_lgb)
lgb_pred_proba = lgb_model.predict_proba(X_test_lgb)[:, 1]

results['LightGBM'] = {
    'accuracy': accuracy_score(y_test, lgb_pred),
    'roc_auc': roc_auc_score(y_test, lgb_pred_proba),
    'train_time': lgb_train_time,
    'model': lgb_model
}

print(f'LightGBM trained in {lgb_train_time:.2f} seconds')
print(f'Accuracy: {results["LightGBM"]["accuracy"]:.4f}')
print(f'ROC AUC:  {results["LightGBM"]["roc_auc"]:.4f}')
""",
    )
    set_code_cell(
        nb,
        22,
        """cat_model = CatBoostClassifier(
    iterations=N_ESTIMATORS,
    learning_rate=LEARNING_RATE,
    depth=MAX_DEPTH,
    random_state=RANDOM_STATE,
    cat_features=cat_feature_indices,
    verbose=0
)

start_time = time.time()
cat_model.fit(X_train_cat, y_train)
cat_train_time = time.time() - start_time

cat_pred = cat_model.predict(X_test_cat).astype(int)
cat_pred_proba = cat_model.predict_proba(X_test_cat)[:, 1]

results['CatBoost'] = {
    'accuracy': accuracy_score(y_test, cat_pred),
    'roc_auc': roc_auc_score(y_test, cat_pred_proba),
    'train_time': cat_train_time,
    'model': cat_model
}

print(f'CatBoost trained in {cat_train_time:.2f} seconds')
print(f'Accuracy: {results["CatBoost"]["accuracy"]:.4f}')
print(f'ROC AUC:  {results["CatBoost"]["roc_auc"]:.4f}')
""",
    )
    set_code_cell(
        nb,
        24,
        """comparison_df = pd.DataFrame({
    'Model': ['XGBoost', 'LightGBM', 'CatBoost'],
    'Accuracy': [results[m]['accuracy'] for m in ['XGBoost', 'LightGBM', 'CatBoost']],
    'ROC AUC': [results[m]['roc_auc'] for m in ['XGBoost', 'LightGBM', 'CatBoost']],
    'Training Time (s)': [results[m]['train_time'] for m in ['XGBoost', 'LightGBM', 'CatBoost']]
})

comparison_df = comparison_df.set_index('Model')
comparison_df.style.highlight_max(axis=0, subset=['Accuracy', 'ROC AUC'], color='lightgreen') \\
                    .highlight_min(axis=0, subset=['Training Time (s)'], color='lightgreen') \\
                    .format('{:.4f}', subset=['Accuracy', 'ROC AUC']) \\
                    .format('{:.2f}', subset=['Training Time (s)'])
""",
    )
    set_code_cell(
        nb,
        27,
        """fig, ax = plt.subplots(figsize=(8, 6))

RocCurveDisplay.from_predictions(y_test, xgb_pred_proba, name='XGBoost', ax=ax, color='#3498db')
RocCurveDisplay.from_predictions(y_test, lgb_pred_proba, name='LightGBM', ax=ax, color='#2ecc71')
RocCurveDisplay.from_predictions(y_test, cat_pred_proba, name='CatBoost', ax=ax, color='#f39c12')

ax.set_title('ROC Curves — All Three Models', fontsize=14, fontweight='bold')
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
plt.tight_layout()
plt.show()
""",
    )
    set_code_cell(
        nb,
        28,
        """fig, axes = plt.subplots(1, 3, figsize=(16, 4))

for ax, (name, pred) in zip(axes, [('XGBoost', xgb_pred), ('LightGBM', lgb_pred), ('CatBoost', cat_pred)]):
    ConfusionMatrixDisplay.from_predictions(y_test, pred, ax=ax, cmap='Blues', colorbar=False)
    ax.set_title(name, fontsize=13, fontweight='bold')

plt.suptitle('Confusion Matrices', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
""",
    )
    set_code_cell(
        nb,
        30,
        """fig, axes = plt.subplots(1, 3, figsize=(18, 6))

xgb_imp = pd.Series(xgb_model.feature_importances_, index=X_train_xgb.columns).nlargest(10)
xgb_imp.plot(kind='barh', ax=axes[0], color='#3498db')
axes[0].set_title('XGBoost — Top 10 Features', fontweight='bold')
axes[0].invert_yaxis()

lgb_imp = pd.Series(lgb_model.feature_importances_, index=X_train_lgb.columns).nlargest(10)
lgb_imp.plot(kind='barh', ax=axes[1], color='#2ecc71')
axes[1].set_title('LightGBM — Top 10 Features', fontweight='bold')
axes[1].invert_yaxis()

cat_imp = pd.Series(cat_model.feature_importances_, index=X_train_cat.columns).nlargest(10)
cat_imp.plot(kind='barh', ax=axes[2], color='#f39c12')
axes[2].set_title('CatBoost — Top 10 Features', fontweight='bold')
axes[2].invert_yaxis()

plt.suptitle('Feature Importance Comparison', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
""",
    )
    set_code_cell(
        nb,
        32,
        """for name, pred in [('XGBoost', xgb_pred), ('LightGBM', lgb_pred), ('CatBoost', cat_pred)]:
    print(f'\\n{"=" * 50}')
    print(f'{name} Classification Report')
    print('=' * 50)
    print(classification_report(y_test, pred, target_names=['No Deposit', 'Deposit']))
""",
    )
    write_nb(p, nb)

    # ----- 8: k-means -----
    p = ROOT / "8/09_k-means_unsolved.ipynb"
    nb = load_nb(p)
    set_code_cell(
        nb,
        4,
        "# Running locally: place Mall_Customers.csv next to this notebook (no Google Drive).\n",
    )
    for i, s in [
        (
            5,
            """DATA_PATH = "Mall_Customers.csv"
df = pd.read_csv(DATA_PATH)
""",
        ),
        (7, "df.head()\n"),
        (
            8,
            """print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
""",
        ),
        (9, "df.describe()\n"),
        (
            11,
            """X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
""",
        ),
        (
            13,
            """inertia = []
k_values = range(1, 11)

for k in k_values:
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X_scaled)
    inertia.append(model.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(list(k_values), inertia, "o-", color="steelblue")
plt.xlabel("k (number of clusters)")
plt.ylabel("Inertia (within-cluster sum of squares)")
plt.title("Elbow Method")
plt.xticks(list(k_values))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
""",
        ),
        (
            15,
            """sil = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42)
    labels = km.fit_predict(X_scaled)
    sil.append(silhouette_score(X_scaled, labels))

plt.figure(figsize=(8, 5))
plt.plot(range(2, 11), sil, "o-", color="darkorange")
plt.xlabel("k")
plt.ylabel("Silhouette score")
plt.title("Silhouette score vs k")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
""",
        ),
        (
            17,
            """optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

df['Cluster'] = clusters
""",
        ),
        (
            19,
            """centroids_orig = scaler.inverse_transform(kmeans.cluster_centers_)

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=df,
    x="Annual Income (k$)",
    y="Spending Score (1-100)",
    hue="Cluster",
    palette="Set2",
    s=60,
)
plt.scatter(
    centroids_orig[:, 0],
    centroids_orig[:, 1],
    c="red",
    s=200,
    marker="X",
    label="Centroids",
)
plt.title("Customer segments (k-means)")
plt.legend()
plt.tight_layout()
plt.show()
""",
        ),
        (
            21,
            """cluster_summary = df.groupby("Cluster")[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].mean()
cluster_summary
""",
        ),
    ]:
        set_code_cell(nb, i, s)
    write_nb(p, nb)

    # ----- 9: PCA -----
    p = ROOT / "9/Exercise_PCA_Basics_UNSOLVED (1).ipynb"
    nb = load_nb(p)
    set_code_cell(
        nb,
        2,
        """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

np.random.seed(42)
plt.rcParams["figure.figsize"] = (8, 5)
""",
    )
    for i, s in [
        (5, 'df = sns.load_dataset("penguins").dropna()\n\nprint(f"Shape: {df.shape}")\ndf.head()\n'),
        (7, """numeric_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
df[numeric_cols].describe()
"""),
        (
            10,
            """X = df[numeric_cols].values
y = df["species"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Mean after scaling:  {X_scaled.mean(axis=0).round(2)}")
print(f"Std after scaling:   {X_scaled.std(axis=0).round(2)}")
""",
        ),
        (
            13,
            """pca_full = PCA(n_components=None)
pca_full.fit(X_scaled)

print("Explained variance ratio per component:")
for i, ratio in enumerate(pca_full.explained_variance_ratio_):
    print(f"  PC{i+1}: {ratio:.4f}  ({ratio:.2%})")

print(f"\\nTotal: {pca_full.explained_variance_ratio_.sum():.4f}")
""",
        ),
        (
            15,
            """evr = pca_full.explained_variance_ratio_
cumulative = np.cumsum(evr)

fig, ax = plt.subplots()
x = np.arange(1, len(evr) + 1)

ax.bar(x, evr, color="steelblue", label="Individual")
ax.plot(x, cumulative, "o-", color="darkorange", label="Cumulative")
ax.axhline(y=0.95, color="red", linestyle="--", alpha=0.6, label="95% threshold")

ax.set_xlabel("Principal Component")
ax.set_ylabel("Explained Variance Ratio")
ax.set_title("Scree Plot — Palmer Penguins")
ax.set_xticks(x)
ax.set_xticklabels([f"PC{i}" for i in x])
ax.legend()
plt.tight_layout()
plt.show()
""",
        ),
        (
            17,
            """cum = np.cumsum(pca_full.explained_variance_ratio_)
n_95 = int(np.searchsorted(cum, 0.95, side="left") + 1)
print(f"Components needed for >=95% variance: {n_95}")
""",
        ),
        (
            20,
            """pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
species_list = ["Adelie", "Chinstrap", "Gentoo"]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

for name, color in zip(species_list, colors):
    mask = y == name
    plt.scatter(X_2d[mask, 0], X_2d[mask, 1],
                label=name, color=color, alpha=0.7, edgecolors="k", s=60)

plt.xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]:.2%} variance)")
plt.ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]:.2%} variance)")
plt.title("Palmer Penguins — PCA 2D Projection")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
""",
        ),
        (
            22,
            """# Gentoo separates most clearly in PC space; Adelie and Chinstrap overlap the most.
""",
        ),
        (
            25,
            """loadings = pd.DataFrame(
    pca_2d.components_,
    columns=numeric_cols,
    index=["PC1", "PC2"],
)
loadings.round(3)
""",
        ),
        (27, """plt.figure(figsize=(8, 3))
sns.heatmap(loadings, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("PCA Loadings Heatmap")
plt.tight_layout()
plt.show()
"""),
        (
            30,
            """X_reconstructed = pca_2d.inverse_transform(X_2d)

mse = np.mean((X_scaled - X_reconstructed) ** 2)
print(f"Reconstruction MSE (2 components): {mse:.4f}")
""",
        ),
        (
            32,
            """mse_list = []
for k in range(1, 5):
    pca_k = PCA(n_components=k)
    X_k = pca_k.fit_transform(X_scaled)
    X_rec = pca_k.inverse_transform(X_k)
    mse_k = np.mean((X_scaled - X_rec) ** 2)
    mse_list.append(mse_k)
    print(f"k={k}  MSE={mse_k:.4f}")

plt.figure()
plt.plot(range(1, 5), mse_list, "o-", color="steelblue")
plt.xlabel("Number of Components")
plt.ylabel("Reconstruction MSE")
plt.title("Reconstruction Error vs Number of Components")
plt.xticks(range(1, 5))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
""",
        ),
        (
            34,
            """from sklearn.datasets import load_wine

wine = load_wine()
X_wine = StandardScaler().fit_transform(wine.data)

pca_wine = PCA()
pca_wine.fit(X_wine)

cumvar_wine = np.cumsum(pca_wine.explained_variance_ratio_)
n_90 = int(np.searchsorted(cumvar_wine, 0.90) + 1)
print(f"Components for >=90% variance: {n_90} out of {wine.data.shape[1]}")

X_wine_2d = PCA(n_components=2).fit_transform(X_wine)

plt.figure(figsize=(8, 6))
for cls in range(3):
    mask = wine.target == cls
    plt.scatter(X_wine_2d[mask, 0], X_wine_2d[mask, 1],
                label=wine.target_names[cls], alpha=0.7, edgecolors="k", s=60)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Wine Dataset — PCA 2D Projection")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
""",
        ),
    ]:
        set_code_cell(nb, i, s)
    write_nb(p, nb)

    # ----- 10: Prophet -----
    p = ROOT / "10/13_Prophet_unsolved (1).ipynb"
    nb = load_nb(p)
    set_code_cell(
        nb,
        2,
        """import pandas as pd
import matplotlib.pyplot as plt

from prophet import Prophet
""",
    )
    set_code_cell(nb, 4, 'df = pd.read_csv("Microsoft_Stock.csv")\n\ndf.head()\n')
    set_code_cell(nb, 5, 'df = df[["Date", "Close"]]\ndf.columns = ["ds", "y"]\n')
    set_code_cell(nb, 10, "model = Prophet(yearly_seasonality=True)\n\nmodel.fit(df)\n")
    set_code_cell(nb, 12, "future = model.make_future_dataframe(periods=90, freq='B')\n\nprint(f\"Future dataframe shape: {future.shape}\")\nfuture.tail()\n")
    write_nb(p, nb)

    # GBM discussion markdown (replace placeholders)
    p = ROOT / "7/GBM_Comparison_UNSOLVED.ipynb"
    nb = load_nb(p)
    nb["cells"][33]["source"] = to_src(
        """## Step 8: Summary and Discussion Questions

### Key Observations

Fill in based on your results (use the comparison table and plots above):

1. **Fastest model:** Compare **Training Time (s)** — often **LightGBM** is fastest among the three.
2. **Best ROC AUC:** Compare **ROC AUC** column — typically all three are close on this dataset.
3. **Least preprocessing needed:** **CatBoost** (raw categoricals + `cat_features` only).
4. **Most important features (across all models):** Often **duration**, **balance**, and campaign-related fields rank highly — check the importance bar charts.

### Discussion Questions

1. Which model would you deploy in a bank's production system? Why?
2. How did each model handle the categorical features differently? What was the impact on preprocessing effort?
3. Why might the feature importance rankings differ between models?
4. The dataset is imbalanced (~11% positive). How could you improve recall for the minority class?
5. If the dataset had 500 categorical features with high cardinality, which model would you choose?
"""
    )
    write_nb(p, nb)

    print("All notebooks patched.")


if __name__ == "__main__":
    main()
