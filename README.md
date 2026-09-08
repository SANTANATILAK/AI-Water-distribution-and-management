# AI-Based Water Distribution & Demand Forecasting

🔗 **Live Demo:** [https://cuddly-telegram-7vrqxwrpvr46fxgq9-8503.app.github.dev/](https://cuddly-telegram-7vrqxwrpvr46fxgq9-8503.app.github.dev/)

A system that predicts how much water a city or town will need, so supply can be
managed more efficiently — cutting down on wastage, leaks, and the extra energy
spent pumping water that wasn't actually needed.

## The Problem

Water utilities often struggle to match supply with real demand. When they
overestimate, water gets wasted. When they underestimate, pressure drops and
leaks or shortages follow. Both mistakes also waste energy, since pumping water
costs power whether it's needed or not.

## What I Built

- A regression model trained on over 400 historical demand records to forecast
  future water usage
- A feature engineering pipeline that pulls out the usage patterns that
  actually matter for predicting demand
- A way to flag which areas need more or less water, so supply can be
  redirected instead of wasted
- Dashboards to check how accurate the model's predictions are and to spot
  demand trends over time

## Tech Stack

Python, Scikit-Learn, Pandas, NumPy

## Results

- A complete pipeline that takes raw data all the way to an evaluation
  dashboard
- Clear demand patterns that can guide real redistribution decisions

## What's Next

- Add live sensor and IoT data so the model can react to real-time conditions,
  not just historical trends
- Try out models built specifically for time-series data and compare them
  against the current regression approach

## Data Pipeline and AI Assistant

Beyond forecasting, the project includes a small pipeline and a chatbot-style
assistant for exploring the data in plain English.

First, the pipeline takes a CSV of sensor or usage data, cleans up the column
names so they're consistent, and stores everything in a local database. You
just point it at your data file and tell it where to save the database, and it
takes care of the rest.

Next, any maintenance logs or operational reports you have can be dropped into
a documents folder. From there, the project builds a searchable index out of
them, so the assistant can later reference real reports instead of guessing.

Once your data and documents are ready, the assistant itself can be started up
as a small local web service. It's even usable right away without any setup
beyond that — if no Anthropic key is provided, it runs in a local evidence
mode, answering purely from the retrieved documents and statistics rather
than generating a written response. To get full Claude-generated answers
instead, an Anthropic API key just needs to be set in the environment before
the service starts.

From there, you can simply ask it a question, such as what usage and
maintenance issues should be prioritized, and it will respond with an answer
grounded in your actual data. Along with the answer, it shows which documents
it pulled from and which statistics from your data supported the response, so
nothing is left to guesswork.

If you want to point the assistant at a different database, a different
document index, or a different model, those can all be configured through
environment variables rather than changing any code.
