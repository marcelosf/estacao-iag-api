from estacao.repositories.temperatura import TemperaturaRepository
from datetime import datetime
from estacao.models import Consolidado
from estacao.normalize import Normalize


class TestTemperaturaMinRepository:
    def test_instance(self):
        assert isinstance(TemperaturaRepository(), TemperaturaRepository)

    def test_has_get_temperatura_min_attribute(self):
        assert hasattr(TemperaturaRepository(), 'get_temperatura_min')

    def test_temperatura_min(self, consolidado):
        repository = TemperaturaRepository()
        temperatura_min = repository.get_temperatura_min('2017-12-31', '2018-02-01')
        expected = [(datetime(2018, 1, 1, 13, 48, 10), 12.0, 12.0)]
        assert expected == temperatura_min


class TestTemperaturaMaxRepository:
    def test_has_get_temperatura_max_attribute(self):
        assert hasattr(TemperaturaRepository(), 'get_temperatura_max')

    def test_temperatura_min(self, consolidado):
        repository = TemperaturaRepository()
        temepratura_max = repository.get_temperatura_max('2017-12-31', '2018-02-01')
        expected = [(datetime(2018, 1, 1, 13, 48, 10), 50.0, 50.0)]
        assert expected == temepratura_max


class TestCurrentConditionsRepository:
    def test_has_get_conditions_attribute(self, current_conditions):
        assert hasattr(current_conditions, 'get_conditions')

    def test_has_model_attribute(self, current_conditions):
        assert hasattr(current_conditions, 'model')

    def test_model_instance(self, current_conditions):
        assert isinstance(current_conditions.model(), Consolidado)

    def test_load_data(self, current_conditions):
        current_values = ('tipob', 20, 'tipom', 'tipoa')
        current_conditions.load_data()
        response = current_conditions.data
        for expected in current_values:
            assert expected in response

    def test_get_conditions_data_type(self, current_conditions,
                                      consolidado_fixed):
        resp = current_conditions.get_conditions()
        assert isinstance(resp, dict)

    def test_to_dict(self, current_conditions):
        current_conditions.load_data()
        current_conditions.to_dict()
        assert isinstance(current_conditions.data, dict)

    def test_map_data(self, consolidado_fixed, current_conditions):
        current_conditions.load_data()
        current_conditions.to_dict()
        current_conditions.format_date()
        current_conditions.normalize()
        current_conditions.map_data()
        current_conditions.round_data()
        data = consolidado_fixed[-1:][0].to_dict()
        expected = self.make_current_conditions(data)
        assert current_conditions.data == expected

    def test_get_conditions(self, current_conditions, consolidado_fixed):
        data = consolidado_fixed[-1:][0].to_dict()
        expected = self.make_current_conditions(data)
        resp = current_conditions.get_conditions()
        for item in expected.keys():
            assert expected.get(item) == resp.get(item)

    def test_load_temperature(self, current_conditions):
        current_conditions.load_temperature('min', 'tmin')
        date, tmin = current_conditions.tmin
        assert tmin == 20.0

    def make_current_conditions(self, data):
        normalize = Normalize()
        float_round = 2
        pressao_hpa = normalize.trans_p(data.get('pressao'), data.get('temp_bar'))
        temp_orvalho = normalize.td(data.get('tseco'), data.get('tumido'), pressao_hpa)
        umidade_relativa = normalize.rh_tw(data.get('tseco'), data.get('tumido'), pressao_hpa)
        current_conditions = {
            'data': data.get('data'),
            'temperatura_ar': round(data.get('tseco'), float_round),
            'temperatura_ponto_orvalho': round(temp_orvalho, float_round),
            'umidade_relativa': round(umidade_relativa, float_round),
            'temperatura_min': round(data.get('tmin'), float_round),
            'temperatura_max': round(data.get('tmax'), float_round),
            'visibilidade': round(data.get('vis'), float_round),
            'vento': round(data.get('vento'), float_round),
            'pressao': round(data.get('pressao'), float_round),
            'nuvens_baixas': data.get('tipob'),
            'nuvens_medias': data.get('tipom'),
            'nuvens_altas': data.get('tipoa')
        }
        return current_conditions
