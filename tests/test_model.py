from gpt4allj import Model


class TestModel():

    def test_generate(self, model, instructions):
        model = Model(model, instructions=instructions)
        response = model.generate('AI is going to', seed=10, n_predict=3)
        assert response == " be the new"
