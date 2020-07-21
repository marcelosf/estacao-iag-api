import numpy as np


class Normalize:
    def ep(self, temperature):
        exp = np.exp((17.62 * temperature)/(temperature + 243.12))
        resp = 1.0044 * 6.112 * exp
        return resp

    def trans_p(self, p_mmhg, tbar):
        p0 = p_mmhg * (1.0-0.000163 * tbar)
        p_hpa = (p0 - 1.3) * 1013.25/760.0
        return p_hpa

    def rh_tw(self, dry, wet, p_hpa):
        e = self.ep(wet) - p_hpa * (dry - wet) * 0.000653 * (1.0 + (0.000944 * wet))
        es = self.ep(dry)
        rh = (e / es) * 100
        return rh