import math
import unittest

from core.exactas import DATA
from core.limites import figura as figura_limite, figura_bilateral_interactiva
from core.limites_avanzados import thermal_figure


def partial(function, x, y, axis, step=1e-5):
    if axis == 0:
        return (function(x + step, y) - function(x - step, y)) / (2 * step)
    return (function(x, y + step) - function(x, y - step)) / (2 * step)


class ExactEquationsTest(unittest.TestCase):
    def test_each_model_reconstructs_both_components_and_initial_level(self):
        for name, model in DATA.items():
            with self.subTest(name=name):
                x, y = model["point"]
                self.assertAlmostEqual(model["potential"](x, y), model["level"])
                for x, y in [(0.4, 0.7), (1.3, 2.1), (2.5, 1.2)]:
                    self.assertTrue(math.isclose(partial(model["potential"], x, y, 0), model["M"](x, y), abs_tol=1e-7))
                    self.assertTrue(math.isclose(partial(model["potential"], x, y, 1), model["N"](x, y), abs_tol=1e-7))
                    self.assertTrue(math.isclose(partial(model["M"], x, y, 1), partial(model["N"], x, y, 0), abs_tol=1e-7))

    def test_bilateral_examples_have_correct_endpoints(self):
        fig = figura_bilateral_interactiva(4, 5)
        self.assertEqual(fig.data[2].y[0], 4)
        self.assertEqual(fig.data[3].y[0], 5)
        self.assertEqual(fig.data[2].marker.line.color, "#fff176")
        self.assertEqual(fig.data[3].marker.line.color, "#fff176")

    def test_open_and_filled_points_match_function_definitions(self):
        hole = figura_limite().data[2]
        self.assertEqual((hole.x[0], hole.y[0]), (2, 4))
        self.assertEqual(hole.marker.symbol, "circle")
        self.assertEqual(hole.marker.color, "#06111a")
        self.assertEqual(hole.marker.line.color, "#fff176")
        thermal = thermal_figure()
        self.assertEqual((thermal.data[2].x[0], thermal.data[2].y[0]), (5, 40))
        self.assertEqual((thermal.data[3].x[0], thermal.data[3].y[0]), (5, 46))
        self.assertNotEqual(thermal.data[3].marker.color, thermal.data[2].marker.color)


if __name__ == "__main__":
    unittest.main()
