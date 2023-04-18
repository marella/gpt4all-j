from ctypes import create_string_buffer

from .lib import load_library, gptj_params


class Model:

    def __init__(self, model, lib=None):
        self._ctx = None
        self._lib = load_library() if lib is None else lib
        self._ctx = self._lib.gptj_load_model(model.encode())
        if self._ctx is None:
            raise RuntimeError(f'Failed to load model from "{model}"')

    def generate(self,
                 prompt,
                 seed=-1,
                 n_threads=-1,
                 n_predict=200,
                 n_batch=1,
                 top_k=40,
                 top_p=0.9,
                 temp=0.9,
                 response_buffer_size=10000):
        prompt = prompt.encode()
        params = gptj_params(seed=seed,
                             n_threads=n_threads,
                             n_predict=n_predict,
                             n_batch=n_batch,
                             top_k=top_k,
                             top_p=top_p,
                             temp=temp)
        response = create_string_buffer(response_buffer_size)
        status = self._lib.gptj_generate(self._ctx, prompt, params, response)
        if not status:
            raise RuntimeError(f'Failed to generate response for "{prompt}"')
        return response.value.decode()

    def __del__(self):
        if self._ctx is not None:
            self._lib.gptj_free_model(self._ctx)
