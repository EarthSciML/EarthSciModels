"""
Unit tests for tools/esm_to_docs.py.

Run locally with: pytest tools/esm_to_docs_test.py
Or without pytest: python -m unittest tools/esm_to_docs_test.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import esm_to_docs as mod  # noqa: E402


class AstToLatexPrimitivesTest(unittest.TestCase):
    """One test per op from the spec-required set: + - * / ^ exp log10 sin cos."""

    def test_integer_literal(self):
        self.assertEqual(mod.ast_to_latex(42), "42")

    def test_float_literal(self):
        self.assertEqual(mod.ast_to_latex(1.5), "1.5")

    def test_scientific_literal(self):
        # repr(1e-5) == '1e-05' on CPython 3.11
        out = mod.ast_to_latex(1e-5)
        self.assertIn(r"\times 10^{-5}", out)

    def test_variable_plain(self):
        self.assertEqual(mod.ast_to_latex("T"), "T")

    def test_variable_with_subscript(self):
        self.assertEqual(mod.ast_to_latex("p_sat"), "p_{sat}")

    def test_variable_multi_underscore_uses_thinspace(self):
        # Subsequent underscores become LaTeX thin spaces so the variable name
        # survives both Markdown backslash-escaping and KaTeX subscript parsing.
        self.assertEqual(mod.ast_to_latex("T_Dv_ref"), r"T_{Dv\,ref}")

    def test_plus_binary(self):
        node = {"op": "+", "args": ["a", "b"]}
        self.assertEqual(mod.ast_to_latex(node), "a + b")

    def test_plus_nary(self):
        node = {"op": "+", "args": ["a", "b", "c"]}
        self.assertEqual(mod.ast_to_latex(node), "a + b + c")

    def test_minus_binary(self):
        node = {"op": "-", "args": ["a", "b"]}
        self.assertEqual(mod.ast_to_latex(node), "a - b")

    def test_minus_unary(self):
        node = {"op": "-", "args": ["a"]}
        self.assertEqual(mod.ast_to_latex(node), "-a")

    def test_times_binary(self):
        node = {"op": "*", "args": ["a", "b"]}
        self.assertEqual(mod.ast_to_latex(node), r"a \cdot b")

    def test_times_nary(self):
        node = {"op": "*", "args": ["a", "b", "c"]}
        self.assertEqual(mod.ast_to_latex(node), r"a \cdot b \cdot c")

    def test_divide_renders_as_frac(self):
        node = {"op": "/", "args": ["a", "b"]}
        self.assertEqual(mod.ast_to_latex(node), r"\frac{a}{b}")

    def test_power(self):
        node = {"op": "^", "args": ["x", 2]}
        self.assertEqual(mod.ast_to_latex(node), "x^{2}")

    def test_exp(self):
        node = {"op": "exp", "args": ["x"]}
        self.assertEqual(mod.ast_to_latex(node), "e^{x}")

    def test_log10(self):
        node = {"op": "log10", "args": ["x"]}
        self.assertEqual(mod.ast_to_latex(node), r"\log_{10}\left(x\right)")

    def test_sin(self):
        node = {"op": "sin", "args": ["x"]}
        self.assertEqual(mod.ast_to_latex(node), r"\sin\left(x\right)")

    def test_cos(self):
        node = {"op": "cos", "args": ["x"]}
        self.assertEqual(mod.ast_to_latex(node), r"\cos\left(x\right)")

    def test_no_backslash_bang_in_output(self):
        # Guard against reintroducing ``\!``: Goldmark would strip the backslash
        # because ``!`` is a Markdown-escape punctuation character, leaving KaTeX
        # with a bare ``!`` that it cannot parse.
        nodes = [
            {"op": "log10", "args": ["x"]},
            {"op": "sin", "args": ["x"]},
            {"op": "exp", "args": [{"op": "log10", "args": ["y"]}]},
        ]
        for n in nodes:
            self.assertNotIn(r"\!", mod.ast_to_latex(n))


class AstToLatexPrecedenceTest(unittest.TestCase):
    """Exercises precedence/parenthesization across nested ops."""

    def test_sum_inside_product_is_parenthesized(self):
        # (a + b) * c
        node = {"op": "*", "args": [{"op": "+", "args": ["a", "b"]}, "c"]}
        out = mod.ast_to_latex(node)
        self.assertEqual(out, r"\left(a + b\right) \cdot c")

    def test_product_inside_sum_is_not_parenthesized(self):
        # a + b*c
        node = {"op": "+", "args": ["a", {"op": "*", "args": ["b", "c"]}]}
        out = mod.ast_to_latex(node)
        self.assertEqual(out, r"a + b \cdot c")

    def test_quotient_in_product_is_unambiguous(self):
        # a * (b/c) — frac is self-delimiting, no parens needed.
        node = {"op": "*", "args": ["a", {"op": "/", "args": ["b", "c"]}]}
        out = mod.ast_to_latex(node)
        self.assertEqual(out, r"a \cdot \frac{b}{c}")

    def test_sum_inside_fraction_has_no_parens(self):
        # (a+b) / c — frac braces isolate the numerator, so no \left( \right).
        node = {"op": "/", "args": [{"op": "+", "args": ["a", "b"]}, "c"]}
        out = mod.ast_to_latex(node)
        self.assertEqual(out, r"\frac{a + b}{c}")

    def test_power_of_fraction(self):
        node = {"op": "^", "args": [{"op": "/", "args": ["a", "b"]}, 2]}
        self.assertEqual(mod.ast_to_latex(node), r"\frac{a}{b}^{2}")


class AstToLatexRealFixturesTest(unittest.TestCase):
    """Exercises deeply-nested reaction rates and observed bindings taken from real .esm files."""

    # Copied from components/aerosol/radiative_forcing/cloud_albedo.esm.
    # γ = 2 / (√3 * (1 + (-1)·g))
    CLOUD_ALBEDO_GAMMA = {
        "op": "/",
        "args": [
            2,
            {
                "op": "*",
                "args": [
                    1.7320508075688772,
                    {
                        "op": "+",
                        "args": [
                            1,
                            {"op": "*", "args": [-1, "g"]},
                        ],
                    },
                ],
            },
        ],
    }

    # Copied from components/gaschem/superfast.esm reaction R1:
    # rate = (1023.4 * P * exp(-940/T)) / (8314000 * T)
    SUPERFAST_R1_RATE = {
        "args": [
            {
                "args": [
                    1023.4,
                    "P",
                    {"args": [{"args": [-940, "T"], "op": "/"}], "op": "exp"},
                ],
                "op": "*",
            },
            {"args": [8314000, "T"], "op": "*"},
        ],
        "op": "/",
    }

    def test_cloud_albedo_gamma_renders(self):
        out = mod.ast_to_latex(self.CLOUD_ALBEDO_GAMMA)
        # Must produce valid LaTeX for KaTeX/MathJax.
        self.assertIn(r"\frac{2}{", out)
        self.assertIn(r"1.7320508075688772 \cdot", out)
        # The "1 + (-1)*g" subterm must appear in the denominator as a sum.
        self.assertIn("1 + ", out)
        self.assertIn("g", out)

    def test_superfast_r1_rate_renders_as_frac(self):
        out = mod.ast_to_latex(self.SUPERFAST_R1_RATE)
        # Top-level is a division → \frac{...}{...}
        self.assertTrue(out.startswith(r"\frac{"), f"expected top-level \\frac, got: {out[:40]}")
        # Must contain the exp(-940/T) term.
        self.assertIn(r"e^{\frac{-940}{T}}", out)
        # Denominator must contain 8314000 \cdot T.
        self.assertIn(r"8314000 \cdot T", out)

    def test_latex_has_balanced_braces(self):
        # A deeply-nested real fixture must still produce balanced {} braces.
        out = mod.ast_to_latex(self.SUPERFAST_R1_RATE)
        self.assertEqual(out.count("{"), out.count("}"), f"unbalanced braces in: {out}")

    def test_latex_has_balanced_left_right(self):
        out = mod.ast_to_latex(self.CLOUD_ALBEDO_GAMMA)
        self.assertEqual(
            out.count(r"\left("),
            out.count(r"\right)"),
            f"unbalanced \\left/\\right in: {out}",
        )


class VarnameFormatTest(unittest.TestCase):
    def test_greek_unicode_passthrough(self):
        # KaTeX/MathJax render unicode Greek directly; we don't convert to \tau etc.
        self.assertEqual(mod._fmt_varname("τ_c"), "τ_{c}")

    def test_no_underscore_returns_as_is(self):
        self.assertEqual(mod._fmt_varname("R_c"), "R_{c}")
        self.assertEqual(mod._fmt_varname("CO2"), "CO2")


class ComponentEntryDerivedFieldsTest(unittest.TestCase):
    def test_domain_and_slug_from_path(self):
        entry = mod.ComponentEntry(
            section="models",
            name="DropletGrowth",
            body={},
            esm_path=Path("components/aerosol/cloud_physics/droplet_growth.esm"),
            esm_version="1.0.0",
            file_metadata={},
        )
        self.assertEqual(entry.domain, "aerosol")
        self.assertEqual(entry.subdomain, "cloud_physics")
        self.assertEqual(entry.type_label, "model")
        self.assertEqual(entry.slug, "aerosol/cloud_physics/dropletgrowth")

    def test_flat_domain_no_subdomain(self):
        entry = mod.ComponentEntry(
            section="reaction_systems",
            name="SuperFast",
            body={},
            esm_path=Path("components/gaschem/superfast.esm"),
            esm_version="1.0.0",
            file_metadata={},
        )
        self.assertEqual(entry.domain, "gaschem")
        self.assertEqual(entry.subdomain, "")
        self.assertEqual(entry.type_label, "reaction_system")
        self.assertEqual(entry.slug, "gaschem/superfast")


class DataSourcePageTest(unittest.TestCase):
    """`data_sources` is the esm 1.0.0 spelling of 0.x's `data_loaders`.

    A source is pure I/O and exposes no variables (esm-spec §8), so its page
    carries the I/O descriptor; the fields it feeds are documented on the
    consuming model as parameters with a `data` update.
    """

    def _entry(self) -> mod.ComponentEntry:
        return mod.ComponentEntry(
            section="data_sources",
            name="GEOSFP_A1",
            body={
                "kind": "grid",
                "source": {"url_template": "s3://gcgrid/GEOS_0.25x0.3125/{date:%Y/%m}/a1.nc"},
                "temporal": {"file_period": "P1D", "frequency": "PT1H"},
            },
            esm_path=Path("components/earthsci_data/geosfp_a1.esm"),
            esm_version="1.0.0",
            file_metadata={},
        )

    def test_type_label_is_data_source(self):
        self.assertEqual(self._entry().type_label, "data_source")

    def test_page_renders_io_descriptor(self):
        md = mod.render_markdown(self._entry())
        self.assertIn("## Data source", md)
        self.assertIn("`grid`", md)
        self.assertIn("s3://gcgrid/", md)
        self.assertIn("`P1D`", md)

    def test_section_absent_for_models(self):
        entry = mod.ComponentEntry(
            section="models",
            name="Foo",
            body={"kind": "grid", "variables": {"x": {"type": "parameter"}}},
            esm_path=Path("components/toy/foo.esm"),
            esm_version="1.0.0",
            file_metadata={},
        )
        self.assertNotIn("## Data source", mod.render_markdown(entry))


class ParseEsmTest(unittest.TestCase):
    def test_parse_data_source_file(self):
        body = {
            "esm": "1.0.0",
            "metadata": {"name": "X"},
            "data_sources": {
                "geosfp_a1": {
                    "kind": "grid",
                    "source": {"url_template": "s3://bucket/{date:%Y%m%d}.nc"},
                }
            },
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root / "components" / "earthsci_data" / "geosfp_a1.esm"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(body), encoding="utf-8")
            entries = mod.parse_esm(p, root)
            self.assertEqual([e.section for e in entries], ["data_sources"])
            self.assertEqual(entries[0].type_label, "data_source")

    def test_parse_model_file(self):
        body = {
            "esm": "1.0.0",
            "metadata": {"name": "X", "tags": ["a", "b"]},
            "models": {
                "Foo": {
                    "description": "a foo",
                    "variables": {
                        "x": {"type": "parameter", "units": "1", "default": 1.0},
                    },
                }
            },
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root / "components" / "mydomain" / "foo.esm"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(body), encoding="utf-8")
            entries = mod.parse_esm(p, root)
            self.assertEqual(len(entries), 1)
            e = entries[0]
            self.assertEqual(e.name, "Foo")
            self.assertEqual(e.section, "models")
            self.assertEqual(e.domain, "mydomain")
            self.assertEqual(e.esm_version, "1.0.0")


class RenderMarkdownTest(unittest.TestCase):
    """End-to-end smoke test: ensure frontmatter + required sections appear."""

    def _make_entry(self) -> mod.ComponentEntry:
        return mod.ComponentEntry(
            section="models",
            name="Foo",
            body={
                "description": "A toy component.",
                "reference": {"citation": "Smith 2020", "doi": "10.1/abc"},
                # esm 1.0.0 declares only `unknown` and `parameter`: `y` is
                # observed and `z` an ODE state purely by virtue of the
                # equations below (esm-spec §6.3.1).
                "variables": {
                    "x": {"type": "parameter", "units": "1", "default": 1.0, "description": "a param"},
                    "y": {"type": "unknown", "units": "1", "description": "y = 2x"},
                    "z": {"type": "unknown", "units": "1", "description": "a state"},
                },
                "equations": [
                    {"lhs": "y", "rhs": {"op": "*", "args": [2, "x"]}},
                    {"lhs": {"op": "D", "args": ["z"], "wrt": "t"}, "rhs": "y"},
                ],
                "tests": [{"id": "t1", "description": "sanity", "assertions": [1, 2]}],
                "analyses": [
                    {
                        "id": "e1",
                        "description": "a toy run",
                        "time_span": {"start": 0, "end": 10},
                    }
                ],
            },
            esm_path=Path("components/toy/foo.esm"),
            esm_version="1.0.0",
            file_metadata={"name": "Foo", "tags": ["toy"]},
        )

    def test_frontmatter_contains_required_keys(self):
        md = mod.render_markdown(self._make_entry())
        self.assertTrue(md.startswith("---\n"))
        head, _, _ = md[4:].partition("\n---\n")
        self.assertIn('title: "Foo"', head)
        self.assertIn('domain: "toy"', head)
        self.assertIn('component_type: "model"', head)
        self.assertIn('esm_version: "1.0.0"', head)
        self.assertIn("tags: [", head)

    def test_body_contains_all_sections(self):
        md = mod.render_markdown(self._make_entry())
        for section in (
            "## Description",
            "## Reference",
            "## Variables",
            "## Parameters",
            "## Observed",
            "## Observed expressions",
            "## Equations",
            "## Analyses",
            "## Raw .esm",
        ):
            self.assertIn(section, md, f"missing section: {section}")

    def test_derived_classification_places_each_variable(self):
        # The declared type is `unknown` for both y and z; only the equations
        # say which is observed and which is a state (esm-spec §6.3.1).
        md = mod.render_markdown(self._make_entry())
        variables_tbl = md.split("## Variables", 1)[1].split("## Parameters", 1)[0]
        self.assertIn("`z`", variables_tbl)
        self.assertNotIn("`y`", variables_tbl)
        observed_tbl = md.split("## Observed\n", 1)[1].split("## Observed expressions", 1)[0]
        self.assertIn("`y`", observed_tbl)
        self.assertNotIn("`z`", observed_tbl)

    def test_observed_definition_not_duplicated_in_equations(self):
        # `y ~ 2x` is rendered once, under Observed expressions; the Equations
        # section carries only the remaining (ODE) row.
        md = mod.render_markdown(self._make_entry())
        equations = md.split("## Equations", 1)[1].split("\n## ", 1)[0]
        self.assertIn(r"\mathrm{D}\left(z\right)", equations)
        self.assertNotIn(r"2 \cdot x", equations)
        self.assertIn(r"y = 2 \cdot x", md.split("## Observed expressions", 1)[1])

    def test_variable_with_an_undefined_type_is_still_rendered(self):
        # `"type": "variable"` is in no version's enum, so classification
        # accounts for it nowhere. Filtering the tables by the classified sets
        # alone would drop it from the page silently.
        entry = self._make_entry()
        entry.body["variables"]["w"] = {"type": "variable", "description": "stray"}
        md = mod.render_markdown(entry)
        variables_tbl = md.split("## Variables", 1)[1].split("## Parameters", 1)[0]
        self.assertIn("`w`", variables_tbl)

    def test_analysis_renders_id_and_time_span(self):
        md = mod.render_markdown(self._make_entry())
        analyses = md.split("## Analyses", 1)[1].split("\n## ", 1)[0]
        self.assertIn("### e1", analyses)
        self.assertIn("a toy run", analyses)
        self.assertIn("**Time span:** 0 → 10", analyses)

    def test_tests_section_not_rendered(self):
        # Tests are dev-only; they must not appear on user-facing pages.
        md = mod.render_markdown(self._make_entry())
        self.assertNotIn("## Tests", md)

    def test_equation_renders_as_display_math(self):
        md = mod.render_markdown(self._make_entry())
        # `$$` fences with the rendered RHS should be present.
        self.assertIn("$$", md)
        self.assertIn(r"2 \cdot x", md)


class ExpressionTemplatesSectionTest(unittest.TestCase):
    """Render expression_templates as a documented section on the component page."""

    def _entry_with_templates(self) -> mod.ComponentEntry:
        return mod.ComponentEntry(
            section="reaction_systems",
            name="HasTemplates",
            body={
                "description": "rxn system with templates",
                "expression_templates": {
                    "arrhenius_M": {
                        "params": ["A", "B"],
                        "body": {
                            "op": "*",
                            "args": [
                                "A",
                                {"op": "exp", "args": [{"op": "/", "args": ["B", "T"]}]},
                                "num_density",
                            ],
                        },
                    },
                    "scaled_M": {
                        "params": ["A"],
                        "body": {"op": "*", "args": ["A", "num_density"]},
                    },
                },
                "species": {"O3": {"units": "mol/m^3"}},
            },
            esm_path=Path("components/gaschem/has_templates.esm"),
            esm_version="1.0.0",
            file_metadata={},
        )

    def _entry_without_templates(self) -> mod.ComponentEntry:
        return mod.ComponentEntry(
            section="reaction_systems",
            name="NoTemplates",
            body={
                "description": "rxn system without templates",
                "species": {"O3": {"units": "mol/m^3"}},
            },
            esm_path=Path("components/gaschem/no_templates.esm"),
            esm_version="1.0.0",
            file_metadata={},
        )

    def test_section_emitted_when_templates_present(self):
        md = mod.render_markdown(self._entry_with_templates())
        self.assertIn("## Expression Templates", md)
        self.assertIn("arrhenius_M", md)
        self.assertIn("scaled_M", md)

    def test_template_body_renders_as_latex(self):
        md = mod.render_markdown(self._entry_with_templates())
        # The arrhenius_M body A * exp(B/T) * num_density renders through ast_to_latex.
        self.assertIn(r"A \cdot e^{\frac{B}{T}} \cdot num", md)
        # The scaled_M body A * num_density renders likewise.
        self.assertIn(r"A \cdot num", md)

    def test_template_params_listed(self):
        md = mod.render_markdown(self._entry_with_templates())
        # Both A and B should appear as backtick-fenced params for arrhenius_M.
        self.assertIn("**Parameters:**", md)
        self.assertIn("`A`", md)
        self.assertIn("`B`", md)

    def test_no_section_when_templates_absent(self):
        md = mod.render_markdown(self._entry_without_templates())
        self.assertNotIn("Expression Templates", md)

    def test_no_section_when_templates_empty(self):
        entry = self._entry_without_templates()
        entry.body["expression_templates"] = {}
        md = mod.render_markdown(entry)
        self.assertNotIn("Expression Templates", md)


class BuildIndexTest(unittest.TestCase):
    def test_index_record_shape(self):
        entry = mod.ComponentEntry(
            section="reaction_systems",
            name="SuperFast",
            body={"description": "s", "reference": {"doi": "10.1/x"}},
            esm_path=Path("components/gaschem/superfast.esm"),
            esm_version="1.0.0",
            file_metadata={"tags": ["photochem"]},
        )
        idx = mod.build_index([entry])
        self.assertEqual(idx["count"], 1)
        rec = idx["components"][0]
        self.assertEqual(rec["name"], "SuperFast")
        self.assertEqual(rec["domain"], "gaschem")
        self.assertEqual(rec["type"], "reaction_system")
        self.assertIn("photochem", rec["tags"])
        self.assertEqual(rec["reference"], "10.1/x")


class SlugCollisionTest(unittest.TestCase):
    """Two components on one slug means one page is silently overwritten."""

    def _entry(self, section: str, name: str, path: str) -> mod.ComponentEntry:
        return mod.ComponentEntry(
            section=section,
            name=name,
            body={},
            esm_path=Path(path),
            esm_version="1.0.0",
            file_metadata={},
        )

    def test_no_collision_reports_nothing(self):
        entries = [
            self._entry("models", "CEDS", "components/earthsci_data/ceds.esm"),
            self._entry("data_sources", "CEDS_BC", "components/earthsci_data/ceds.esm"),
        ]
        self.assertEqual(mod._warn_slug_collisions(entries), [])

    def test_same_registry_key_in_two_files_is_reported(self):
        entries = [
            self._entry("data_sources", "CEDS_BC", "components/earthsci_data/ceds.esm"),
            self._entry(
                "data_sources", "CEDS_BC", "components/earthsci_data/ceds_bc_loader.esm"
            ),
        ]
        self.assertEqual(
            mod._warn_slug_collisions(entries), ["earthsci_data/ceds_bc"]
        )


class IntegrationRunTest(unittest.TestCase):
    """Runs the full pipeline against a tiny synthetic repo."""

    def test_run_generates_pages_and_index(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "components" / "toy").mkdir(parents=True)
            (root / "components" / "toy" / "a.esm").write_text(
                json.dumps(
                    {
                        "esm": "1.0.0",
                        "metadata": {"name": "A"},
                        "models": {
                            "A": {
                                "description": "a",
                                "variables": {"x": {"type": "parameter", "units": "1"}},
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            content = root / "docs" / "content"
            data = root / "docs" / "data"
            rc = mod.run(root, content, data)
            self.assertEqual(rc, 0)
            page = content / "components" / "toy" / "a" / "index.md"
            self.assertTrue(page.exists(), f"expected {page} to exist")
            idx = json.loads((data / "components-index.json").read_text())
            self.assertEqual(idx["count"], 1)


if __name__ == "__main__":
    unittest.main()
