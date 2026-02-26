# AI-Water-distribution-and-management

The project aims to improve water distribution systems by using AI to address issues such as wastage, leakage, and energy consumption and swapping the water where it is needed.

Below is a simple demo included in this repository which trains a linear regression model
on sample data to predict water demand from temperature and population.

## Getting Started

1. Create a virtual environment and install dependencies:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Train a model using the sample data:

```sh
python water_demand.py train --data data/sample.csv --model model.joblib
```

3. Make a single prediction:

```sh
python water_demand.py predict --temp 30 --pop 1200 --model model.joblib
```

4. Batch predictions from CSV:

```sh
python water_demand.py batch-predict --input data/sample.csv --output results.csv --model model.joblib
```

The sample CSV is provided under `data/sample.csv`. Feel free to replace it with your own data.

