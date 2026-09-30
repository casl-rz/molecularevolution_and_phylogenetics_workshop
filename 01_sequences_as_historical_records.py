# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.24.2",
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    lab_styles = r"""
    <style>
    .lab-nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px;font:600 13px 'Trebuchet MS',sans-serif}
    .lab-nav a{padding:10px 15px;border:1px solid #c7d7d1;border-radius:24px;color:#16483e;text-decoration:none;background:#f4f8f5}
    .lab-nav a[aria-current=page]{background:#143b33;color:#e2f7a7;border-color:#143b33}
    .lab-nav a:hover{background:#dceebd;color:#163b33}
    .lab-nav a:focus-visible{outline:3px solid #008b9d;outline-offset:3px}
    .lab-hero{position:relative;overflow:hidden;padding:32px 38px;border-radius:24px;background:#123b33;color:#f6f9ee;margin-bottom:20px}
    .lab-hero h1{font:normal clamp(30px,4vw,52px)/1.06 Georgia,serif;margin:16px 0;color:#f6f9ee!important;max-width:76%}
    .lab-hero p{font:17px/1.6 'Trebuchet MS',sans-serif;max-width:78%;margin:0;color:#d4e7dc}
    .lab-eyebrow{font:700 11px 'Trebuchet MS',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#ddf59d}
    .lab-orbit{position:absolute;width:160px;height:160px;right:-15px;top:35px;border:1px solid #517567;border-radius:50%}
    .lab-orbit:before,.lab-orbit:after{content:"";position:absolute;border:1px solid #517567;border-radius:50%;inset:22px}
    .lab-orbit:after{inset:46px;background:#dff48d}
    .lab-meta{font:12px 'Trebuchet MS',sans-serif;color:#587267;margin:12px 2px}
    .lab-metric{border:1px solid #d0dfd7;border-top:5px solid var(--accent);border-radius:16px;padding:20px 22px;background:#f5f8f2;min-width:190px;height:100%;box-sizing:border-box}
    .lab-metric-label{font:700 11px 'Trebuchet MS',sans-serif;letter-spacing:.09em;text-transform:uppercase;color:#426355}
    .lab-metric-value{font:normal 36px/1.2 Georgia,serif;color:#123b33;margin:10px 0}
    .lab-metric-detail{font:13px/1.5 'Trebuchet MS',sans-serif;color:#4f695e}
    .lab-surface{padding:24px;border:1px solid #d0dfd7;border-radius:20px;background:#f5f8f2;color:#163b33;margin:12px 0}
    .lab-surface h3{font:normal 24px Georgia,serif;margin:0 0 16px;color:#163b33}
    .lab-dna{display:grid;grid-template-columns:repeat(50,minmax(12px,1fr));gap:3px;min-width:760px;margin:12px 0 22px}
    .lab-base{display:grid;place-items:center;border-radius:3px;font:700 12px/22px monospace;color:#14372e}
    .lab-base.changed{outline:2px solid #193e35;outline-offset:-2px}
    .lab-scroll{overflow-x:auto}
    .lab-legend{display:flex;flex-wrap:wrap;gap:14px;font:13px 'Trebuchet MS',sans-serif;color:#365b4c;margin:14px 0}
    .lab-legend b{padding:4px 9px;border-radius:5px;color:#17372f}
    .lab-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
    .lab-history{display:grid;grid-template-columns:repeat(20,minmax(24px,1fr));gap:5px;min-width:650px}
    .lab-site{display:grid;place-items:center;font:700 13px/28px monospace;border-radius:5px;color:#153a31}
    .lab-alignment{display:grid;gap:3px;min-width:max-content}
    .lab-candidate{padding:22px;border:1px solid #c8dad0;border-top:5px solid var(--accent);border-radius:16px;background:#f5f8f2}
    .lab-candidate h3{margin:8px 0;font:normal 32px Georgia,serif;color:#133c33}
    .lab-tag{font:700 11px 'Trebuchet MS',sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#346352}
    .lab-track{height:10px;background:#dbe6dc;border-radius:10px;overflow:hidden;margin:10px 0 16px}
    .lab-track span{display:block;height:100%;background:var(--accent)}
    @media(max-width:600px){.lab-hero{padding:25px}.lab-hero h1,.lab-hero p{max-width:100%}.lab-orbit{display:none}.lab-metric{min-width:150px}}
    @media(prefers-reduced-motion:no-preference){.lab-hero{animation:lab-enter .45s ease-out}@keyframes lab-enter{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}}
    </style>
    """
    mo.Html(lab_styles + r"""

    <nav class="lab-nav" aria-label="Interactive workshop lessons"><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/01_sequences_as_historical_records.py/wasm?embed=true" target="_blank" rel="noopener noreferrer" aria-current="page">01 &nbsp; Sequence records</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/02_mutation_substitution_saturation.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">02 &nbsp; Hidden changes</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/03_alignment_to_tree.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">03 &nbsp; Alignment to tree</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/04_methods_disagree.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">04 &nbsp; Competing trees</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/05_orthology_and_gene_family_case.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">05 &nbsp; Gene families</a></nav>
    <section class="lab-hero" aria-label="Lesson 1">
    <div class="lab-eyebrow">Molecular evolution field lab / 01</div>
    <h1>Read the history<br>in a sequence.</h1><p>Two descendants. One ancestor. Change the rate and watch the records diverge.</p><div class="lab-orbit" aria-hidden="true"></div>
    </section>
    <div class="lab-meta">4-minute guided experiment &middot; Synthetic data &middot; No typing needed.
    Lesson links open the browser-only WebAssembly apps in new tabs.</div>
    """)
    return (lab_styles,)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from html import escape
    import numpy as np
    import matplotlib.pyplot as plt


    def metric_card(label, value, detail, accent="#0099a8"):
        return mo.Html(
            f'<div class="lab-metric" style="--accent:{accent}">'
            f'<div class="lab-metric-label">{escape(str(label))}</div>'
            f'<div class="lab-metric-value">{escape(str(value))}</div>'
            f'<div class="lab-metric-detail">{escape(str(detail))}</div></div>'
        )

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#d0dfd7",
            "axes.labelcolor": "#33402f",
            "text.color": "#33402f",
            "xtick.color": "#5c6b57",
            "ytick.color": "#5c6b57",
            "figure.facecolor": "#f5f8f2",
            "axes.facecolor": "#f5f8f2",
            "grid.color": "#d5e2d9",
            "grid.alpha": 0.65,
            "figure.dpi": 120,
        }
    )
    return metric_card, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We will hold time fixed and change the rate. If the sequences become
        more different, that cannot be because more time has passed.
        Similarity is a clue about ancestry, but it is not a date.
        """
    ).callout(kind="info", title="What we're testing")
    return


@app.cell(hide_code=True)
def _(mo):
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Watch\nTwice the rate need not produce exactly twice the differences."),
        mo.md(
            "## 2. Try it\nStart gives you the first run. Compare doubles only "
            "the rate, keeping time, length and seed fixed. You can still move "
            "any slider. To reset, switch to another step and back."
        ),
        session_step,
    ])
    return (session_step,)


@app.cell(hide_code=True)
def _(mo, session_step):
    _rate = 0.010 if session_step.value == "Compare" else 0.005
    mutation_rate_slider = mo.ui.slider(
        0.000, 0.200, value=_rate, step=0.005, label="Mutation rate (per site, per unit time)",
        show_value=True,
    )
    seq_length_slider = mo.ui.slider(
        20, 300, value=200, step=10, label="Sequence length (bp)",
        show_value=True,
    )
    evo_time_slider = mo.ui.slider(
        1, 100, value=5, step=1, label="Evolutionary time (arbitrary units)",
        show_value=True,
    )
    seed_slider = mo.ui.slider(
        1, 100, value=42, step=1, label="Random seed",
        show_value=True,
    )

    mo.vstack(
        [
            mo.md("### Controls"),
            mo.hstack([mutation_rate_slider, seq_length_slider], justify="start", gap=3),
            mo.hstack([evo_time_slider, seed_slider], justify="start", gap=3),
            mo.md(
                r"""
                *`Mutation rate` sets how often a site changes per unit of time;
                `sequence length` sets how many sites are simulated; `evolutionary
                time` sets how long the two lineages have been diverging; and
                `random seed` fixes the randomness so a run can be reproduced.*
                """
            ),
        ]
    )
    return (
        evo_time_slider,
        mutation_rate_slider,
        seed_slider,
        seq_length_slider,
    )


@app.cell(hide_code=True)
def _(np):
    def simulate_descendants(n_sites, rate, time, seed):
        bases = np.array(list("ACGT"))
        ancestor = np.random.default_rng(seed).integers(0, 4, size=n_sites)
        rng_a = np.random.default_rng(seed * 2)
        rng_b = np.random.default_rng(seed * 2 + 1)
        probability = 1 - np.exp(-rate * time)
        mask_a = rng_a.random(n_sites) < probability
        mask_b = rng_b.random(n_sites) < probability
        descendant_a = np.where(mask_a, (ancestor + rng_a.integers(1, 4, size=n_sites)) % 4, ancestor)
        descendant_b = np.where(mask_b, (ancestor + rng_b.integers(1, 4, size=n_sites)) % 4, ancestor)
        differences = int((descendant_a != descendant_b).sum())
        return (
            "".join(bases[ancestor]), "".join(bases[descendant_a]),
            "".join(bases[descendant_b]), mask_a, mask_b, differences,
        )

    def expected_divergence(rate, time):
        probability = 1 - np.exp(-rate * time)
        return 2 * probability - 4 * probability**2 / 3

    return expected_divergence, simulate_descendants


@app.cell(hide_code=True)
def _(
    evo_time_slider,
    mutation_rate_slider,
    seed_slider,
    seq_length_slider,
    simulate_descendants,
):
    n_sites = seq_length_slider.value
    ancestor_seq, descendant_a_seq, descendant_b_seq, mask_a, mask_b, n_differences = simulate_descendants(
        n_sites, mutation_rate_slider.value, evo_time_slider.value, seed_slider.value,
    )
    pct_divergence = 100 * n_differences / n_sites
    return (
        ancestor_seq,
        descendant_a_seq,
        descendant_b_seq,
        mask_a,
        mask_b,
        n_differences,
        n_sites,
        pct_divergence,
    )


@app.cell(hide_code=True)
def _(
    evo_time_slider,
    mo,
    mutation_rate_slider,
    n_differences,
    seed_slider,
    seq_length_slider,
    simulate_descendants,
):
    _start = simulate_descendants(200, 0.005, 5, 42)[-1]
    mo.vstack([
        mo.md(
            "## 3. Read the result\nLook at the highlighted bases and the "
            "difference count. Did the count double, or just increase?"
        ),
        mo.ui.table([
            {"Run": "Guided start", "Rate": 0.005, "Time": 5, "Sites": 200, "Seed": 42, "Differing sites": _start},
            {"Run": "Current settings", "Rate": mutation_rate_slider.value, "Time": evo_time_slider.value,
             "Sites": seq_length_slider.value, "Seed": seed_slider.value, "Differing sites": n_differences},
        ], selection=None, pagination=False, show_download=False, show_search=False),
        mo.md(
            "The first row stays fixed. Compare is a controlled experiment; "
            "if you change other sliders, check which columns changed too.\n\n"
            "**Simulated:** ancestry and branch changes. **Observed:** the endpoint "
            "bases and mismatches. **Inferred:** what similarity suggests about "
            "history. **Assumed:** equal rates and one change at most per site per branch."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(ancestor_seq, descendant_a_seq, descendant_b_seq, lab_styles, mo):

    _palette = {"A": "#d9ec91", "C": "#79cbd7", "G": "#8dc4a6", "T": "#f5a28e"}
    _rows = []
    for _name, _sequence in [
        ("Ancestor", ancestor_seq), ("Descendant A", descendant_a_seq), ("Descendant B", descendant_b_seq)
    ]:
        _tiles = "".join(
            f'<span class="lab-base{" changed" if base != ancestor_seq[position] else ""}" '
            f'style="background:{_palette[base]}" title="Site {position + 1}: {base}; '
            f'ancestor {ancestor_seq[position]}">{base}</span>'
            for position, base in enumerate(_sequence)
        )
        _rows.append(f'<div class="lab-tag">{_name}</div><div class="lab-dna">{_tiles}</div>')
    _legend = "".join(f'<b style="background:{color}">{base}</b>' for base, color in _palette.items())
    _all_sites = mo.Html(
        lab_styles + '<section class="lab-surface"><h3>The sequence records</h3>'
        '<div class="lab-legend">' + _legend + '<span>Dark frame = changed from ancestor</span></div>'
        '<div class="lab-scroll">' + "".join(_rows) + '</div>'
        '<div class="lab-metric-detail">Read left to right, wrapping every 50 sites. '
        'Hover over a tile for its exact position.</div></section>'
    )
    _mismatches = []
    for _position, (_a, _b) in enumerate(zip(descendant_a_seq, descendant_b_seq)):
        if _a != _b:
            _mismatches.append(
                f'<div class="lab-candidate" style="--accent:#ee916e"><div class="lab-tag">Site {_position + 1}</div>'
                f'<h3>{_a} / {_b}</h3><div class="lab-metric-detail">Ancestor: {ancestor_seq[_position]}</div></div>'
            )
    _different_sites = mo.Html(
        lab_styles + (
            '<div class="lab-grid">' + "".join(_mismatches) + '</div>'
            if _mismatches else '<div class="lab-surface">No endpoint mismatches in this run.</div>'
        )
    )
    mo.ui.tabs({"All sites": _all_sites, "Endpoint mismatches": _different_sites})
    return


@app.cell(hide_code=True)
def _(
    evo_time_slider,
    expected_divergence,
    metric_card,
    mo,
    mutation_rate_slider,
    n_differences,
    n_sites,
    pct_divergence,
):

    mo.hstack([
        metric_card("Visible mismatches", n_differences, f"Across {n_sites} endpoint sites", "#ee916e"),
        metric_card("Observed divergence", f"{pct_divergence:.1f}%", "One random realization", "#0099a8"),
        metric_card("Expected divergence", f"{100 * expected_divergence(mutation_rate_slider.value, evo_time_slider.value):.1f}%",
                    "Mean under this one-change toy process", "#7a9f36"),
    ], wrap=True, gap=1)
    return


@app.cell(hide_code=True)
def _(evo_time_slider, mask_a, mask_b, plt):
    _fig, _ax = plt.subplots(figsize=(5.8, 3.8))

    _ax.plot([0, 1], [0, 1], color="#2e7d32", linewidth=3, solid_capstyle="round")
    _ax.plot([0, 1], [0, -1], color="#a1662f", linewidth=3, solid_capstyle="round")
    _ax.scatter([0], [0], color="#1b5e20", s=160, zorder=5, edgecolor="white", linewidth=1.5)
    _ax.scatter([1, 1], [1, -1], color=["#2e7d32", "#a1662f"], s=120, zorder=5, edgecolor="white", linewidth=1.5)

    _ax.text(-0.08, 0, "Common ancestor", ha="right", va="center", fontsize=11, fontweight="bold")
    _ax.text(1.08, 1, f"Descendant A\n{int(mask_a.sum())} mutations", ha="left", va="center", fontsize=11, color="#2e7d32")
    _ax.text(1.08, -1, f"Descendant B\n{int(mask_b.sum())} mutations", ha="left", va="center", fontsize=11, color="#a1662f")

    _ax.set_xlim(-0.7, 2.3)
    _ax.set_ylim(-1.7, 1.7)
    _ax.axis("off")
    _ax.set_title(f"Two lineages diverging over {evo_time_slider.value} time units", fontsize=12.5, color="#2e5a27")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *This diagram shows the two descendant lineages as branches from a single
    common ancestor. Longer branches, or more time, give mutations more
    opportunity to accumulate — the mutation count on each branch shows how
    many sites changed along that particular lineage.*
    """)
    return


@app.cell(hide_code=True)
def _(
    evo_time_slider,
    expected_divergence,
    mutation_rate_slider,
    np,
    pct_divergence,
    plt,
):
    _t = np.linspace(0, 100, 300)
    _expected_pct = 100 * expected_divergence(mutation_rate_slider.value, _t)

    _fig, _ax = plt.subplots(figsize=(5.8, 3.8))
    _ax.fill_between(_t, _expected_pct, color="#a5d6a7", alpha=0.25)
    _ax.plot(_t, _expected_pct, color="#2e7d32", linewidth=2.5, label="Expectation for this toy model")
    _ax.scatter(
        [evo_time_slider.value], [pct_divergence],
        color="#e65100", zorder=5, s=90, edgecolor="white", linewidth=1.5, label="This simulation",
    )
    _ax.set_xlabel("Evolutionary time")
    _ax.set_ylabel("% divergence between descendants")
    _ax.set_title("Time and rate affect expected endpoint differences", fontsize=12.5, color="#2e5a27")
    _ax.set_ylim(0, 85)
    _ax.legend(loc="lower right", frameon=False, fontsize=9)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The line is the expectation for the same one-change-per-branch model
    used above. The point is one random sample, so it need not sit on the line.

    At high rates this toy behaves oddly: the curve can turn down, because
    each branch can change a site only once. That is a limit of this model,
    not a biological prediction. Notebook 2 allows repeated changes.
    """)
    return


@app.cell(hide_code=True)
def _(mo, pct_divergence):
    mo.md(
        f"""
        {pct_divergence:.1f}% of sites differ in this run. That percentage
        depends on rate, time and the random realization. It does not tell
        us whether these are cultivars, species, or genes with the same function.
        """
    ).callout(kind="info", title="What can we say?")
    return


@app.cell(hide_code=True)
def _(mo):
    check_answer = mo.ui.radio(
        ["More time must have passed", "Rate, time and chance can each affect the differences", "Matching sequences prove no change occurred"],
        label="Two sequences are more different. What can you conclude?",
    )
    show_explanation = mo.ui.checkbox(label="Show the explanation")
    mo.vstack([mo.md("## 4. Quick check"), check_answer, show_explanation])
    return check_answer, show_explanation


@app.cell(hide_code=True)
def _(check_answer, mo, show_explanation):
    mo.stop(not show_explanation.value)
    _correct = check_answer.value == "Rate, time and chance can each affect the differences"
    mo.md(
        ("Yes. " if _correct else "Choose the statement about rate, time and chance. ")
        + "Raw difference is not a clock. In our comparison, time stayed "
        "fixed while the rate changed; random sampling also affected the count."
    ).callout(kind="success" if _correct else "info", title="Explanation")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
        mo.md(
            "## 5. Explore further\nKeep the rate and time fixed, then change "
            "the seed. Does the exact percentage stay the same? Try a shorter "
            "sequence too. Which result would you trust more, and why?"
        ),
        mo.md("## 6. Behind the model"),
        mo.accordion({
            "The idea in one sentence": mo.md(
                "Sequences retain traces of shared ancestry, but differences "
                "reflect both time and rate. A short sequence also leaves more "
                "room for chance."
            ),
            "Where the model stops": mo.md(
                "The ancestor is known because we made it. Each site can change "
                "at most once on each branch; selection, indels, recombination "
                "and rate variation are absent. The apparent high-rate downturn "
                "belongs to this toy model. These are hypothetical sequences, "
                "not a measured crop comparison."
            ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
