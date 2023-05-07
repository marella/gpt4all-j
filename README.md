# [GPT4All-J](https://github.com/marella/gpt4all-j) [![PyPI](https://img.shields.io/pypi/v/gpt4all-j)](https://pypi.org/project/gpt4all-j/) [![tests](https://github.com/marella/gpt4all-j/actions/workflows/tests.yml/badge.svg)](https://github.com/marella/gpt4all-j/actions/workflows/tests.yml)

Python bindings for the [C++ port][gptj.cpp] of GPT4All-J model.

## Installation

```sh
pip install gpt4all-j
```

Download the model from [here](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin).

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
               repeat_penalty=1.0,
               repeat_last_n=64,
               n_batch=8,
               reset=True,
               callback=None)
```

#### `reset`

If `True`, context will be reset. To keep the previous context, use `reset=False`.

```py
model.generate('Write code to sort numbers in Python.')
model.generate('Rewrite the code in JavaScript.', reset=False)
```

#### `callback`

If a callback function is passed, it will be called once per each generated token. To stop generating more tokens, return `False` inside the callback function.

```py
def callback(token):
    print(token)

model.generate('AI is going to', callback=callback)
```

## LangChain

[LangChain](https://python.langchain.com/) is a framework for developing applications powered by language models. A LangChain LLM object for the GPT4All-J model can be created using:

```py
from gpt4allj.langchain import GPT4AllJ

llm = GPT4AllJ(model='/path/to/ggml-gpt4all-j.bin')

print(llm('AI is going to'))
```

If you are getting `illegal instruction` error, try using `instructions='avx'` or `instructions='basic'`:

```py
llm = GPT4AllJ(model='/path/to/ggml-gpt4all-j.bin', instructions='avx')
```

It can be used with other LangChain modules:

```py
from langchain import PromptTemplate, LLMChain

template = """Question: {question}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=['question'])

llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run('What is AI?'))
```

### Parameters

```py
llm = GPT4AllJ(model='/path/to/ggml-gpt4all-j.bin',
               seed=-1,
               n_threads=-1,
               n_predict=200,
               top_k=40,
               top_p=0.9,
               temp=0.9,
               repeat_penalty=1.0,
               repeat_last_n=64,
               n_batch=8,
               reset=True)
```

## C++ Library

To build the C++ library from source, please see [gptj.cpp][gptj.cpp]. Once you have built the shared libraries, you can use them as:

```py
from gpt4allj import Model, load_library

lib = load_library('/path/to/libgptj.so', '/path/to/libggml.so')

model = Model('/path/to/ggml-gpt4all-j.bin', lib=lib)
```

## License

[MIT](https://github.com/marella/gpt4all-j/blob/main/LICENSE)

[gptj.cpp]: https://github.com/marella/gptj.cpp
