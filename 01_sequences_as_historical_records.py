import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Sequences as historical records

    Two lineages inherit the same gene fragment. After they split, their
    sequences change separately. How much can their differences tell us?

    Allow **4 minutes** for the guided experiment. The extra controls and
    follow-up question are there if you want to explore afterwards.
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#c8d6c8",
            "axes.labelcolor": "#33402f",
            "text.color": "#33402f",
            "xtick.color": "#5c6b57",
            "ytick.color": "#5c6b57",
            "figure.facecolor": "#fbfefb",
        }
    )
    return mo, np, plt


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
    prediction_input = mo.ui.text_area(
        label="Your prediction", rows=2,
        placeholder="If the rate doubles, what happens to the differences?",
    )
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Predict\nWill twice the rate produce exactly twice the differences?"),
        prediction_input,
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
        0.000, 0.200, value=_rate, step=0.005, label="Mutation rate (per site, per unit time)"
    )
    seq_length_slider = mo.ui.slider(
        20, 300, value=200, step=10, label="Sequence length (bp)"
    )
    evo_time_slider = mo.ui.slider(
        1, 100, value=5, step=1, label="Evolutionary time (arbitrary units)"
    )
    seed_slider = mo.ui.slider(
        1, 100, value=42, step=1, label="Random seed"
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
        ], selection=None, pagination=False, show_download=False),
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
def _(ancestor_seq, descendant_a_seq, descendant_b_seq, mo):
    def _colorize(seq, ref):
        spans = []
        for base, ref_base in zip(seq, ref):
            color = "#e74c3c" if base != ref_base else "#1b5e20"
            spans.append(f'<span style="color:{color}">{base}</span>')
        return "".join(spans)


    _pre_style = (
        "font-family: \'Fira Code\', \'Courier New\', monospace; font-size:13px; "
        "line-height:1.8; background:#f4f9f4; padding:14px; border-radius:10px; "
        "border:1px solid #c8e6c9; overflow-x:auto; white-space:pre;"
    )

    mo.vstack(
        [
            mo.md("### Ancestor and descendants"),
            mo.md(
                f"""<pre style="{_pre_style}">"""
                f"""Ancestor          {ancestor_seq}
    Descendant A      {_colorize(descendant_a_seq, ancestor_seq)}
    Descendant B      {_colorize(descendant_b_seq, ancestor_seq)}</pre>"""
            ),
            mo.md(
                "*Red bases mark positions that mutated relative to the ancestor. "
                "Green bases are unchanged.*"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, n_differences, n_sites, pct_divergence):
    mo.vstack(
        [
            mo.md("### Observed differences"),
            mo.hstack(
                [
                    mo.stat(
                        value=str(n_differences),
                        label="Differing sites (A vs B)",
                        caption=f"out of {n_sites} total",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{pct_divergence:.1f}%",
                        label="Percentage divergence",
                        caption="differences / sequence length",
                        bordered=True,
                    ),
                ],
                gap=3,
            ),
        ]
    )
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
    mo.vstack([mo.md("## 4. Check your reasoning"), check_answer, show_explanation])
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
    reflection_input = mo.ui.text_area(
        label="One sentence for a colleague", rows=2,
        placeholder="Why can't we turn percent difference straight into a date?",
    )
    mo.vstack([
        mo.md(
            "## 5. Take it further\nKeep the rate and time fixed, then change "
            "the seed. Does the exact percentage stay the same? Try a shorter "
            "sequence too. Which result would you trust more, and why?"
        ),
        mo.md("## 6. Put it into words"),
        reflection_input,
        mo.accordion({
            "One possible explanation": mo.md(
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
