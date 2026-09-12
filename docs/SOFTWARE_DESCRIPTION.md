# Software Description

**Title:** Text Sentiment Analysis System Based on RNN, LSTM and GRU
**Short name:** DeepSentiment

## Summary

DeepSentiment is an integrated inference software system for binary
(Positive/Negative) sentiment classification of text. It packages three
recurrent neural network architectures — SimpleRNN, LSTM and GRU — as
components of one software product, sharing a common preprocessing
pipeline, API surface and user interface, rather than existing as three
separate, unrelated programs.

## Functional components

- User interface (Vue 3 single-page application, "Liquid Glass" visual design)
- Text preprocessing (cleaning, stopword removal, Snowball stemming)
- Tokenization (per-model Keras `Tokenizer` instances)
- Model management (on-demand loading and in-memory caching of trained models)
- Sentiment prediction (single-model inference endpoint)
- Model comparison (all three models against the same input)
- Result visualization (confidence, probability, processed text)
- System information (reports which model/tokenizer files are present and loaded)

## Non-goals

This system intentionally does not include: a database, user accounts or
authentication, payment processing, cloud storage, social-media scraping,
real-time external APIs, chatbot functionality, transformer/LLM-based
models, multilingual translation, emotion classification, sarcasm
detection, or medical/diagnostic functionality.

## Research foundation

The three models originate from research/development notebooks
(`notebooks/RNN_Level1.ipynb`, `notebooks/LSTM_Level2.ipynb`,
`notebooks/GRU_Level3.ipynb`) documenting training on the Sentiment140
dataset with 300-dimensional GloVe embeddings. No accuracy, F1, or other
performance figures are asserted by this document — such metrics are
only meaningful once you have actually trained and evaluated the models
yourself, and should be reported from your own results, not invented.
