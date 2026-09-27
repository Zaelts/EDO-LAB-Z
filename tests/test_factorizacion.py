import json
import unittest
from pathlib import Path

from core.factorizacion import EJERCICIOS, LECCIONES, PISTAS


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
        factor_cases = [(path, case) for path, case in zip(case_files, cases) if case.get("topic_id") == "factorizacion"]
        self.assertEqual(len(factor_cases), 7)
        self.assertEqual({case["variant_set"] for _, case in factor_cases}, set(EJERCICIOS))
        for path, case in factor_cases:
            self.assertEqual(case["id"], path.parent.name)
            self.assertEqual(case.get("challenge_count", 3), len(EJERCICIOS[case["variant_set"]]))
            rubric = case["modes"]["evaluative"]["rubric"]
            self.assertEqual(len(rubric), len(EJERCICIOS[case["variant_set"]]))
            self.assertEqual(sum(item["weight"] for item in rubric), 100)
        self.assertEqual(set(LECCIONES), set(EJERCICIOS))
        self.assertEqual(set(PISTAS), set(EJERCICIOS))

    def test_each_method_has_valid_challenges_lessons_and_hints(self):
        for method, exercises in EJERCICIOS.items():
            with self.subTest(method=method):
                self.assertGreaterEqual(len(exercises), 3)
                self.assertEqual(len(PISTAS[method]), len(exercises))
                lesson = LECCIONES[method]
                self.assertTrue(lesson["definition"])
                self.assertTrue(lesson["pattern"])
                self.assertTrue(lesson["recognition"])
                self.assertGreaterEqual(len(lesson["steps"]), 4)
                for index, (prompt, choices, answer, explanation) in enumerate(exercises):
                    self.assertTrue(prompt)
                    self.assertGreaterEqual(len(choices), 3)
                    self.assertGreaterEqual(answer, 0)
                    self.assertLess(answer, len(choices))
                    self.assertTrue(explanation)
                    self.assertTrue(PISTAS[method][index])


if __name__ == "__main__":
    unittest.main()
