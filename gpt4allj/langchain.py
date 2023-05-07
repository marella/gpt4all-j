try:
    from langchain.llms.base import LLM
except ImportError:
    raise ImportError(
        'To use the gpt4allj.langchain module, please install the '
        'langchain package: pip install langchain')

from functools import partial
from typing import Any, Dict, List, Optional

from pydantic import Field, root_validator
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.utils import enforce_stop_tokens

from . import Model


class GPT4AllJ(LLM):
    client: Any  #: :meta private:
    model: str
    lib: Optional[Any] = None
    instructions: Optional[str] = None

    seed: int = Field(-1, alias='seed')
    n_threads: int = Field(-1, alias='n_threads')
    n_predict: int = Field(200, alias='n_predict')
    top_k: int = Field(40, alias='top_k')
    top_p: float = Field(0.9, alias='top_p')
    temp: float = Field(0.9, alias='temp')
    repeat_penalty: float = Field(1.0, alias='repeat_penalty')
    repeat_last_n: int = Field(64, alias='repeat_last_n')
    n_batch: int = Field(8, alias='n_batch')
    reset: bool = Field(True, alias='reset')

    @property
    def _default_params(self) -> Dict[str, Any]:
        return {
            'seed': self.seed,
            'n_threads': self.n_threads,
            'n_predict': self.n_predict,
            'top_k': self.top_k,
            'top_p': self.top_p,
            'temp': self.temp,
            'repeat_penalty': self.repeat_penalty,
            'repeat_last_n': self.repeat_last_n,
            'n_batch': self.n_batch,
            'reset': self.reset,
        }

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {'model': self.model, **self._default_params}

    @property
    def _llm_type(self) -> str:
        return 'gpt4all-j'

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values['client'] = Model(model=values['model'],
                                 lib=values['lib'],
                                 instructions=values['instructions'])
        return values

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        callback = partial(run_manager.on_llm_new_token,
                           verbose=self.verbose) if run_manager else None
        text = self.client.generate(prompt,
                                    callback=callback,
                                    **self._default_params)
        if stop is not None:
            text = enforce_stop_tokens(text, stop)
        return text
