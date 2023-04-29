# [GPT4All-J](https://github.com/marella/gpt4all-j) [![tests](https://github.com/marella/gpt4all-j/actions/workflows/tests.yml/badge.svg)](https://github.com/marella/gpt4all-j/actions/workflows/tests.yml)

Python bindings for the [C++ port][gptj.cpp] of GPT4All-J model.

## Installation

```sh
pip install gpt4all-j
```

Download the model from [here](https://gpt4all.io/models/ggml-gpt4all-j.bin).

## Usage

```py
from gpt4allj import Model

model = Model('/path/to/ggml-gpt4all-j.bin')

print(model.generate('AI is going to'))
```

[Run in Google Colab](https://colab.research.google.com/drive/1bd38-i1Qlx6_MvJyCTJOy7t8eHSNnqAx)

If you are getting `illegal instruction` error, try using `instructions='avx'` or `instructions='basic'`:

```py
model = Model('/path/to/ggml-gpt4all-j.bin', instructions='avx')
```

If it is running slow, try building the C++ library from source. [Learn more](https://github.com/marella/gpt4all-j#c-library)

### Parameters

```py
model.generate(prompt,
               seed=-1,
               n_threads=-1,
               n_predict=200,
               top_k=40,
               top_p=0.9,
               temp=0.9,
               n_batch=8,
               callback=None)
```

### `callback`

If a callback function is passed to `model.generate()`, it will be called once per each generated token. To stop generating more tokens, return `False` inside the callback function.

```py
def callback(token):
    print(token)

model.generate('AI is going to', callback=callback)
```

### C++ Library

To build the C++ library from source, please see [gptj.cpp][gptj.cpp]. Once you have built the shared libraries, you can use them as:

```py
from gpt4allj import Model, load_library

lib = load_library('/path/to/libgptj.so', '/path/to/libggml.so')

model = Model('/path/to/ggml-gpt4all-j.bin', lib=lib)
```

## License

[MIT](https://github.com/marella/gpt4all-j/blob/main/LICENSE)

[gptj.cpp]: https://github.com/marella/gptj.cpp
