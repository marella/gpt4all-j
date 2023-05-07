import platform
from pathlib import Path
from ctypes import (
    CDLL,
    c_int,
    c_int32,
    c_float,
    c_char_p,
    c_void_p,
    c_bool,
    Structure,
    CFUNCTYPE,
)

gptj_model_context_p = c_void_p
gptj_generate_callback_t = CFUNCTYPE(c_bool, c_char_p)


class gptj_params(Structure):
    _fields_ = [
        ('seed', c_int32),
        ('n_threads', c_int32),
        ('n_predict', c_int32),
        ('top_k', c_int32),
        ('top_p', c_float),
        ('temp', c_float),
        ('repeat_penalty', c_float),
        ('repeat_last_n', c_int32),
        ('n_batch', c_int32),
    ]


def find_library(name, instructions=None):
    system = platform.system()
    if not instructions:
        if platform.processor() == 'arm':
            # Apple silicon doesn't support AVX/AVX2.
            instructions = 'basic' if system == 'Darwin' else ''
        else:
            instructions = 'avx2'

    if system == 'Linux':
        name = f'lib{name}.so'
    elif system == 'Windows':
        name = f'{name}.dll'
    elif system == 'Darwin':
        name = f'lib{name}.dylib'
    else:
        name = ''

    path = Path(__file__).parent.resolve() / 'lib' / instructions / name
    if not path.is_file():
        raise OSError('The current platform is not supported. ' +
                      'Please try building the C++ library from source.')
    return str(path)


def load_library(gptj=None, ggml=None, instructions=None):
    gptj = gptj or find_library('gptj', instructions)
    ggml = ggml or find_library('ggml', instructions)

    CDLL(ggml)
    lib = CDLL(gptj)

    lib.gptj_load_model.argtypes = [c_char_p]
    lib.gptj_load_model.restype = gptj_model_context_p

    lib.gptj_free_model.argtypes = [gptj_model_context_p]
    lib.gptj_free_model.restype = None

    lib.gptj_generate.argtypes = [
        gptj_model_context_p, c_char_p, gptj_params, c_bool,
        gptj_generate_callback_t
    ]
    lib.gptj_generate.restype = c_bool

    lib.gptj_num_tokens.argtypes = [gptj_model_context_p, c_char_p]
    lib.gptj_num_tokens.restype = c_int

    return lib
