# User Manual

## Dashboard (`/`)

Landing page introducing the system: hero section, the three model cards
(RNN, LSTM, GRU), and system highlights. Use the "Analyze text" or
"Compare models" buttons to jump into the tool.

## Sentiment Analysis (`/analysis`)

1. Type or paste text into the textarea (up to 5,000 characters).
2. Choose a model: RNN, LSTM or GRU.
3. Click **Analyze text**.
4. The result card shows the selected model, predicted sentiment
   (Positive/Negative), confidence percentage, raw probability, and the
   preprocessed text that was actually fed to the model.

If the input becomes empty after preprocessing (e.g. it was only a URL or
stopwords), or the selected model/tokenizer is not available, a clear
error message is shown instead of a fabricated result.

## Model Comparison (`/comparison`)

1. Enter text once.
2. Click **Compare models**.
3. Three cards are shown — one per architecture — each with its own
   sentiment, confidence and probability. If a model is unavailable
   (missing file, load error), its card clearly states **Model
   unavailable** with the reason, rather than displaying a fake result.

## Methodology (`/methodology`)

A static reference page walking through the full pipeline: dataset,
preprocessing, tokenization, GloVe embeddings, and each of the three
architectures.

## About (`/about`)

Background on the DeepSentiment software system: purpose, architecture,
components, technology stack, and the research notebooks it is built on.
