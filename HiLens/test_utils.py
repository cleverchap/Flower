from unittest import TestCase
from HiLens.utils import process_predict_result
import numpy as np


class Test(TestCase):
    def test_process_predict_result(self):
        outputs = np.array([0.5996094, -2.8203125, -2.1113281, 3.0820312, -2.375], dtype="float32").tolist()
        assert process_predict_result(outputs, None) == 3

    def test_process_predict_result2(self):
        outputs = np.array([0.5996094, -2.8203125, -2.1113281, 0.0820312, -2.375], dtype="float32").tolist()
        assert process_predict_result(outputs, None) == 0
