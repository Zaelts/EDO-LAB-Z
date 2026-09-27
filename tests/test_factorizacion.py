import json
import unittest
from pathlib import Path

from core.factorizacion import EJERCICIOS


ROOT = Path(__file__).resolve().parents[1]


class FactorizationCurriculumTest(unittest.TestCase):
    def test_factorization_topic_has_seven_cases_and_matching_exercise_sets(self):
        with (ROOT / "casos" / "curriculo.json").open(encoding="utf-8") as file:
            curriculum = json.load(file)
        subject = next(
            subject
            for area in curriculum["areas"]
            for subject in area["subjects"]
            if subject["id"] == "matematica_basica"
        )
        topic = next(topic for topic in subject["topics"] if topic["id"] == "factorizacion")
        self.assertEqual(topic["status"], "available")

        case_files = sorted((ROOT / "casos").glob("caso_*/caso.json"))
        cases = [json.loads(path.read_text(encoding="utf-8")) for path in case_files]
        cases = [case for case in cases if case.get("topic_id") == "factorizacion"]
        self.assertEqual(len(cases), 7)
        self.assertEqual({case["variant_set"] for case in cases}, set(EJERCICIOS))

    def test_each_method_has_three_valid_factorization_challenges(self):
        for method, exercises in EJERCICIOS.items():
            with self.subTest(method=method):
                self.assertEqual(len(exercises), 3)
                for prompt, choices, answer, explanation in exercises:
                    self.assertTrue(prompt)
                    self.assertGreaterEqual(len(choices), 3)
                    self.assertGreaterEqual(answer, 0)
                    self.assertLess(answer, len(choices))
                    self.assertTrue(explanation)


if __name__ == "__main__":
    unittest.main()
