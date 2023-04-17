import sys
from pathlib import Path
from ctypes import (
    CDLL,
    c_int32,
    c_float,
    c_char_p,
    c_void_p,
    c_bool,
    Structure,
)

gptj_model_context_p = c_void_p


class gptj_params(Structure):
    _fields_ = [
        ('seed', c_int32),
        ('n_threads', c_int32),
        ('n_predict', c_int32),
        ('top_k', c_int32),
        ('n_batch', c_int32),
        ('top_p', c_float),
        ('temp', c_float),
    ]


def find_library(name):
    if sys.platform.startswith('linux'):
        name = f'lib{name}.so'
    elif sys.platform.startswith('win32'):
        name = f'{name}.dll'
    elif sys.platform.startswith('darwin'):
        name = f'lib{name}.dylib'
    else:
        raise OSError('The current platform is not supported. ' +
                      'Please try building the C++ library from source.')
    return Path(__file__).parent.resolve() / 'lib' / name


def load_library(gptj=None, ggml=None):
    if gptj is None:
        gptj = find_library('gptj')
    if ggml is None:
        ggml = find_library('ggml')

    CDLL(ggml)
    lib = CDLL(gptj)

    lib.gptj_load_model.argtypes = [c_char_p]
    lib.gptj_load_model.restype = gptj_model_context_p

    lib.gptj_free_model.argtypes = [gptj_model_context_p]
    lib.gptj_free_model.restype = None

    lib.gptj_generate.argtypes = [
        gptj_model_context_p, c_char_p, gptj_params, c_char_p
    ]
    lib.gptj_generate.restype = c_bool

    return lib
