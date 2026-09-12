# DeepSentiment Model Artifacts

DeepSentiment is an inference application. The source package contains the application code and the three research notebooks, but the trained model/tokenizer binaries are kept outside this source archive because they were not included in the provided project package.

Place the following files before running inference:

```text
backend/models/rnn_final_model.h5
backend/models/lstm_final_model.h5
backend/models/gru_final_model.h5

backend/tokenizers/tokenizer.pkl
backend/tokenizers/tokenizer_lstm.pkl
backend/tokenizers/tokenizer_gru.pkl
```

Optional training/development asset:

```text
backend/embeddings/glove.6B.300d.txt
```

The filenames above match the training notebooks and the application configuration. Do not rename `tokenizer.pkl` to `tokenizer_rnn.pkl` unless the notebook and configuration are intentionally changed together.
