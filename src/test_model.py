import Model
import os
import sys
import unittest
from time import perf_counter

SAMPLES = [
    os.path.join(os.path.dirname(__file__), "..", "samples", "sample_tiny.json"),
    os.path.join(os.path.dirname(__file__), "..", "samples", "sample_small.json"),
    os.path.join(os.path.dirname(__file__), "..", "samples", "sample_100k_lines.json"),
    #os.path.join(os.path.dirname(__file__), "..", "samples", "sample_3m_lines.json"),  # too large to fit in the limit of github
]


class ModelTest(unittest.TestCase):
    def test_load_data(self):
        for sample in SAMPLES:
            start = perf_counter()
            mdl = Model.Model()
            mdl.load_data(sample, disable_cache=True)
            print(
                f"test_load_data:[{sample[-25:]}](no cache): {perf_counter() - start} seconds",
                file=sys.stderr,
            )
            del mdl

            mdl1 = Model.Model()
            mdl1.load_data(sample, disable_cache=False)
            del mdl1

            start = perf_counter()
            mdl2 = Model.Model()
            mdl2.load_data(sample, disable_cache=False)
            print(
                f"test_load_data:[{sample[-25:]}](cache): {perf_counter() - start} seconds",
                file=sys.stderr,
            )
            del mdl2

    def test_view_by_country(self):
        mdl = Model.Model()
        mdl.load_data(SAMPLES[1])

        doc_id = "120111003737-ff0d62c2f9e64064b73f058095e4f081"
        start = perf_counter()
        df = mdl.view_by_country(doc_id)
        df_count = df["visitor_country"].value_counts()
        print(
            f"test_view_by_country:[{SAMPLES[1][-25:]}]({doc_id[-10:]}): {perf_counter() - start} seconds"
        )
        expected = {"US": 30}
        nb = 0
        for i in df_count.index:
            self.assertIn(i, expected.keys())
            self.assertEqual(df_count[i], expected[i])
            nb += 1
        self.assertEqual(nb, len(expected))

        doc_id = "140103105022-d0c7d706a1df5106cf88686fb67092ed"
        start = perf_counter()
        df = mdl.view_by_country(doc_id)
        df_count = df["visitor_country"].value_counts()
        print(
            f"test_view_by_country:[{SAMPLES[1][-25:]}]({doc_id[-10:]}): {perf_counter() - start} seconds"
        )
        expected = {"MA": 6}
        nb = 0
        for i in df_count.index:
            self.assertIn(i, expected.keys())
            self.assertEqual(df_count[i], expected[i])
            nb += 1
        self.assertEqual(nb, len(expected))

    def test_view_by_continent(self):
        mdl = Model.Model()
        mdl.load_data(SAMPLES[1])

        doc_id = "120111003737-ff0d62c2f9e64064b73f058095e4f081"
        start = perf_counter()
        df = mdl.view_by_continent(doc_id)
        df_count = df["continent"].value_counts()
        print(
            f"test_view_by_continent:[{SAMPLES[1][-25:]}]({doc_id[-10:]}): {perf_counter() - start} seconds"
        )
        expected = {"NA": 30}
        nb = 0
        for i in df_count.index:
            self.assertIn(i, expected.keys())
            self.assertEqual(df_count[i], expected[i])
            nb += 1
        self.assertEqual(nb, len(expected))

        doc_id = "140103105022-d0c7d706a1df5106cf88686fb67092ed"
        start = perf_counter()
        df = mdl.view_by_continent(doc_id)
        df_count = df["continent"].value_counts()
        print(
            f"test_view_by_continent:[{SAMPLES[1][-25:]}]({doc_id[-10:]}): {perf_counter() - start} seconds"
        )
        expected = {"AF": 6}
        nb = 0
        for i in df_count.index:
            self.assertIn(i, expected.keys())
            self.assertEqual(df_count[i], expected[i])
            nb += 1
        self.assertEqual(nb, len(expected))

    def test_view_by_browser(self):
        mdl = Model.Model()
        mdl.load_data(SAMPLES[1])

        start = perf_counter()
        df = mdl.view_by_browser("all")
        df_count = df["browser"].value_counts()
        print(
            f"test_view_by_browser:[{SAMPLES[1][-25:]}]: {perf_counter() - start} seconds"
        )
        expected = {
            "Mozilla": 10127,
            "Opera": 107,
            "Dalvik": 5,
            "UCWEB": 1,
        }
        nb = 0
        for i in df_count.index:
            self.assertIn(i, expected.keys())
            self.assertEqual(df_count[i], expected[i])
            nb += 1
        self.assertEqual(nb, len(expected))

    def test_reader_profile(self):
        mdl = Model.Model()
        mdl.load_data(SAMPLES[1])

        start = perf_counter()
        df = mdl.reader_profile()
        print(
            f"test_reader_profile:[{SAMPLES[1][-25:]}]: {perf_counter() - start} seconds"
        )
        expected = {
            "03820df02b49ec97": 82744.0,
            "035e2506c961152b": 82167.0,
            "040e6f3aef98911f": 30869.0,
            "02491671b0b21648": 16573.0,
            "0466893bc40bb280": 13009.0,
            "02db215d574d3cfe": 12049.0,
            "03d4a5da87818090": 8015.0,
            "02d0408ff60c2f46": 5636.0,
            "0508626e498eee5d": 3072.0,
            "017bb7e3f878977d": 1648.0,
        }
        nb = 0
        for i, i_value in zip(df.index, df["event_readtime"]):
            self.assertIn(i, expected.keys())
            self.assertEqual(i_value, expected[i])
            nb += 1
        self.assertEqual(nb, len(expected))

    def test_also_likes_default(self):
        mdl = Model.Model()
        mdl.load_data(SAMPLES[1])
        doc_id = "120111003737-ff0d62c2f9e64064b73f058095e4f081"
        user_id = "b417fd6f88d6516d"
        start = perf_counter()
        lst, _ = mdl.also_likes_default(doc_id, user_id)
        print(
            f"test_also_likes_default:[{SAMPLES[1][-25:]}] d:[{doc_id[-10:]}]u:[{user_id[-10:]}]: {perf_counter() - start} seconds"
        )
        expected = []
        self.assertEqual(lst, expected)
        del mdl

        mdl = Model.Model()
        mdl.load_data(SAMPLES[3])
        doc_id = "121109150636-bdf13c63b3964e1494a82f6c144024e2"
        user_id = "d9c9f5e099ac4746"
        start = perf_counter()
        lst, _ = mdl.also_likes(doc_id, user_id, Model.Model.sort_show_weight)
        print(
            f"test_also_likes_default:[{SAMPLES[3][-25:]}] d:[{doc_id[-10:]}]u:[{user_id[-10:]}]: {perf_counter() - start} seconds"
        )
        expected = {
            "130121141937-243485ed0f9644ea8f54791e08297226": 1,
            "130516043301-2137d0ab4a87495dbe6f510bd3ed4aa5": 1,
        }
        nb = 0
        for i_doc, i_value in lst:
            self.assertIn(i_doc, expected.keys())
            self.assertEqual(i_value, expected[i_doc])
            nb += 1
        self.assertEqual(nb, len(expected))

    def test_crash(self):
        mdl = Model.Model()
        try:
            _ = mdl.reader_profile()
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == "__main__":
    _ = unittest.main()
