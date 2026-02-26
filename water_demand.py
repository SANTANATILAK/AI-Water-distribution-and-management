#!/usr/bin/env python3
"""water_demand.py

Train and use a simple linear regression model to predict water demand
based on temperature and population.

Usage examples:
    # train a model from a CSV file and save to disk
    ./water_demand.py train --data data/sample.csv --model model.joblib

    # make a single prediction
    ./water_demand.py predict --temp 30 --pop 1200 --model model.joblib

    # batch prediction from a CSV with Temperature and Population columns
    ./water_demand.py batch-predict --input data/to_predict.csv \
        --output results.csv --model model.joblib

The CSVs are expected to have headers matching the column names.
"""

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

MODEL_DEFAULT = "model.joblib"


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def train_model(data_path: Path) -> LinearRegression:
    df = load_data(data_path)
    required = ["Temperature", "Population", "Water_Demand"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Data file missing columns: {missing}")
    X = df[["Temperature", "Population"]]
    y = df["Water_Demand"]
    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_single(model: LinearRegression, temp: float, pop: float) -> float:
    return model.predict([[temp, pop]])[0]


def predict_batch(model: LinearRegression, input_path: Path) -> pd.DataFrame:
    df = load_data(input_path)
    if "Temperature" not in df.columns or "Population" not in df.columns:
        raise ValueError("Input file must contain Temperature and Population columns")
    preds = model.predict(df[["Temperature", "Population"]])
    df_out = df.copy()
    df_out["Predicted_Water_Demand"] = preds
    return df_out


def main():
    parser = argparse.ArgumentParser(description="Water demand prediction CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # train subcommand
    tparser = sub.add_parser("train", help="train a model from data")
    tparser.add_argument("--data", "-d", type=Path, required=True,
                         help="CSV file with training data")
    tparser.add_argument("--model", "-m", type=Path, default=MODEL_DEFAULT,
                         help="where to save the trained model")

    # predict subcommand
    pp = sub.add_parser("predict", help="make a single prediction")
    pp.add_argument("--temp", type=float, required=True,
                    help="temperature value")
    pp.add_argument("--pop", type=float, required=True,
                    help="population value")
    pp.add_argument("--model", "-m", type=Path, default=MODEL_DEFAULT,
                    help="path to a saved model")

    # batch predict
    bp = sub.add_parser("batch-predict", help="predict from CSV file")
    bp.add_argument("--input", "-i", type=Path, required=True,
                    help="CSV file with rows to predict")
    bp.add_argument("--output", "-o", type=Path, required=True,
                    help="path to write output CSV")
    bp.add_argument("--model", "-m", type=Path, default=MODEL_DEFAULT,
                    help="path to a saved model")

    args = parser.parse_args()

    if args.cmd == "train":
        model = train_model(args.data)
        joblib.dump(model, args.model)
        print(f"Model trained and saved to {args.model}")

    elif args.cmd == "predict":
        if not args.model.exists():
            print(f"Model file {args.model} not found", file=sys.stderr)
            sys.exit(1)
        model = joblib.load(args.model)
        if args.temp < 0 or args.pop < 0:
            print("Error: values must be non-negative", file=sys.stderr)
            sys.exit(1)
        val = predict_single(model, args.temp, args.pop)
        print(f"Predicted Water Demand: {val:.2f} liters")

    elif args.cmd == "batch-predict":
        if not args.model.exists():
            print(f"Model file {args.model} not found", file=sys.stderr)
            sys.exit(1)
        model = joblib.load(args.model)
        df_out = predict_batch(model, args.input)
        df_out.to_csv(args.output, index=False)
        print(f"Batch prediction complete, results written to {args.output}")


if __name__ == "__main__":
    main()
