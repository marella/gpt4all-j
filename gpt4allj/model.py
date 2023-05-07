from .lib import load_library, gptj_params, gptj_generate_callback_t


class Model:

    def __init__(self, model, lib=None, instructions=None):
        self._ctx = None
        self._lib = lib or load_library(instructions=instructions)
        self._ctx = self._lib.gptj_load_model(model.encode())
        if self._ctx is None:
            raise RuntimeError(f'Failed to load model from "{model}"')

    def generate(self,
                 prompt,
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
                 callback=None):
        prompt = prompt.encode()
        params = gptj_params(seed=seed,
                             n_threads=n_threads,
                             n_predict=n_predict,
                             top_k=top_k,
                             top_p=top_p,
                             temp=temp,
                             repeat_penalty=repeat_penalty,
                             repeat_last_n=repeat_last_n,
                             n_batch=n_batch)
        callback = callback or (lambda token: True)
        response = []

        @gptj_generate_callback_t
        def cb(token):
            token = token.decode()
            response.append(token)
            return callback(token) is not False

        status = self._lib.gptj_generate(self._ctx, prompt, params, reset, cb)
        if not status:
            raise RuntimeError(f'Failed to generate response for "{prompt}"')
        return ''.join(response)

    def num_tokens(self, prompt):
        prompt = prompt.encode()
        return self._lib.gptj_num_tokens(self._ctx, prompt)

    def __del__(self):
        if self._ctx is not None:
            self._lib.gptj_free_model(self._ctx)
