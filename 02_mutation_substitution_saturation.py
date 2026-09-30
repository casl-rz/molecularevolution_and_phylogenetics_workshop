import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Mutation, substitution and saturation

    A site can change and then change again. Sometimes it even returns to
    its starting base. The endpoint comparison misses those earlier events.

    Allow **4 minutes** for the guided experiment. We will compare the event
    record with what a sequence comparison can see.
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
        We will lengthen one branch without changing its rate. Count all
        simulated changes, then count the sites that differ at the end.
        Are those still measuring the same thing?
        """
    ).callout(kind="info", title="What we're testing")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        A new A-to-G change in one copy is a **mutation**. If A and G coexist
        in a population, that site is **polymorphic**. If G replaces A in the
        lineage, the replacement is a **substitution**. The new variant can
        also disappear; fixation is not its inevitable next step.

        This notebook skips the population stage and simulates
        substitution-like events directly. Differences between sampled
        individuals can include polymorphism, so a mismatch alone does not
        prove that a change became fixed.
        """
    ).callout(kind="neutral", title="Before we start")
    return


@app.cell(hide_code=True)
def _(mo):
    prediction_input = mo.ui.text_area(
        label="Your prediction", rows=2,
        placeholder="Can the final bases reveal every earlier change?",
    )
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Predict\nWhat happens to the gap between events and mismatches on a longer branch?"),
        prediction_input,
        mo.md(
            "## 2. Try it\nCompare changes branch length from 5 to 200 generations. "
            "Rate, bias, conserved fraction and seed stay fixed. You can still "
            "move any slider. Switch to another step and back to reset."
        ),
        session_step,
    ])
    return (session_step,)


@app.cell(hide_code=True)
def _(mo, session_step):
    mutation_rate_slider = mo.ui.slider(
        0.001, 0.300, value=0.020, step=0.001, label="Mutation rate (per site, per generation)"
    )
    branch_length_slider = mo.ui.slider(
        1, 500, value=200 if session_step.value == "Compare" else 5, step=1, label="Branch length (generations)"
    )
    ts_tv_slider = mo.ui.slider(
        0.5, 10.0, value=2.0, step=0.1, label="Transition/transversion bias"
    )
    conserved_fraction_slider = mo.ui.slider(
        0.0, 0.95, value=0.30, step=0.05, label="Conserved site fraction"
    )
    seed_slider = mo.ui.slider(
        1, 100, value=7, step=1, label="Random seed"
    )

    mo.vstack(
        [
            mo.md("### Controls"),
            mo.hstack([mutation_rate_slider, branch_length_slider], justify="start", gap=3),
            mo.hstack([ts_tv_slider, conserved_fraction_slider], justify="start", gap=3),
            mo.hstack([seed_slider], justify="start", gap=3),
            mo.md(
                r"""
                *`Mutation rate` sets how often a site attempts to mutate each
                generation; `branch length` sets how many generations the
                lineage has evolved for; `transition/transversion bias` makes
                mutations between similar bases (A/G or C/T) more likely than
                others when it is above 1; `conserved site fraction` marks a
                portion of sites as slowly changing, with a
                rate reduced to 5% of the base rate; this is not a population
                model of selection. `Random seed`
                fixes the randomness so a run can be reproduced.*
                """
            ),
        ]
    )
    return (
        branch_length_slider,
        conserved_fraction_slider,
        mutation_rate_slider,
        seed_slider,
        ts_tv_slider,
    )


@app.cell(hide_code=True)
def _(
    branch_length_slider,
    conserved_fraction_slider,
    mutation_rate_slider,
    np,
    seed_slider,
    ts_tv_slider,
):
    n_sites = 200
    bases = np.array(list("ACGT"))

    # transition partner for each base index (A<->G, C<->T)
    _transition_partner = np.array([2, 3, 0, 1])
    # the two transversion options for each base index
    _transversion_options = np.array([
        [1, 3],  # A -> C, T
        [0, 2],  # C -> A, G
        [1, 3],  # G -> C, T
        [0, 2],  # T -> A, G
    ])

    rng = np.random.default_rng(seed_slider.value)

    conserved_mask = rng.random(n_sites) < conserved_fraction_slider.value
    site_rate = np.where(conserved_mask, mutation_rate_slider.value * 0.05, mutation_rate_slider.value)

    ancestor_idx = rng.integers(0, 4, size=n_sites)
    current_idx = ancestor_idx.copy()
    hit_count = np.zeros(n_sites, dtype=int)

    kappa = ts_tv_slider.value
    p_transition = kappa / (kappa + 2)

    n_generations = int(branch_length_slider.value)
    for _ in range(n_generations):
        mutate_mask = rng.random(n_sites) < site_rate
        n_mut = int(mutate_mask.sum())
        if n_mut == 0:
            continue
        idx_mut = np.where(mutate_mask)[0]
        draws = rng.random(n_mut)
        is_transition = draws < p_transition

        new_bases = np.empty(n_mut, dtype=int)
        cur_at_mut = current_idx[idx_mut]
        new_bases[is_transition] = _transition_partner[cur_at_mut[is_transition]]

        n_transversion = int((~is_transition).sum())
        if n_transversion > 0:
            choice = rng.integers(0, 2, size=n_transversion)
            opts = _transversion_options[cur_at_mut[~is_transition]]
            new_bases[~is_transition] = opts[np.arange(n_transversion), choice]

        current_idx[idx_mut] = new_bases
        hit_count[idx_mut] += 1

    ancestor_seq = "".join(bases[ancestor_idx])
    descendant_seq = "".join(bases[current_idx])

    observed_diff_mask = current_idx != ancestor_idx
    n_true_substitutions = int(hit_count.sum())
    n_observed_differences = int(observed_diff_mask.sum())
    multi_hit_mask = hit_count >= 2
    n_multi_hit_sites = int(multi_hit_mask.sum())
    return (
        conserved_mask,
        hit_count,
        n_multi_hit_sites,
        n_observed_differences,
        n_sites,
        n_true_substitutions,
        observed_diff_mask,
    )


@app.cell(hide_code=True)
def _(mo, n_multi_hit_sites, n_observed_differences, n_true_substitutions):
    mo.vstack([
        mo.md(
            "## 3. Read the result\nCompare the event total with the number of "
            "differing sites. Then find a repeatedly hit site with no visible "
            "difference in the two strips below."
        ),
        mo.hstack([
            mo.stat(value=str(n_true_substitutions), label="Simulated events", bordered=True),
            mo.stat(value=str(n_observed_differences), label="Visible mismatches", bordered=True),
            mo.stat(value=str(n_multi_hit_sites), label="Sites hit more than once", bordered=True),
        ]),
        mo.md(
            "**Simulated:** every event and the ancestral bases. **Observed:** "
            "endpoint mismatches. **Inferred:** how incomplete that comparison "
            "is. **Assumed:** independent sites and two rate classes."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(conserved_mask, hit_count, n_sites, np, observed_diff_mask, plt):
    _rng_jitter = np.random.default_rng(0)
    _x_jitter = hit_count + _rng_jitter.uniform(-0.15, 0.15, size=n_sites)
    _y_jitter = observed_diff_mask.astype(float) + _rng_jitter.uniform(-0.06, 0.06, size=n_sites)

    _fig, _ax = plt.subplots(figsize=(5.8, 3.8))
    _ax.scatter(
        _x_jitter[~conserved_mask], _y_jitter[~conserved_mask],
        color="#2e7d32", alpha=0.55, s=28, label="Variable sites",
    )
    _ax.scatter(
        _x_jitter[conserved_mask], _y_jitter[conserved_mask],
        color="#8d6e63", alpha=0.55, s=28, label="Conserved sites",
    )
    _ax.set_xlabel("True number of substitutions at a site")
    _ax.set_ylabel("Observed as different from ancestor")
    _ax.set_yticks([0, 1])
    _ax.set_yticklabels(["No", "Yes"])
    _ax.set_title("Each point is one site: true hits vs. observable difference", fontsize=12, color="#2e5a27")
    _ax.legend(loc="center right", frameon=False, fontsize=9)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Each point is a single site. Points at x = 1 that read "Yes" are simple,
    visible substitutions. Points further to the right that still read "No"
    are sites that mutated multiple times but happened to land back on the
    ancestral base — their history is real, but it is invisible when you
    only compare the two sequences you have today.*
    """)
    return


@app.cell(hide_code=True)
def _(hit_count, np, observed_diff_mask, plt):
    _fig, (_ax1, _ax2) = plt.subplots(
        2, 1, figsize=(9, 2.6), sharex=True, gridspec_kw={"height_ratios": [3, 1.2]}
    )
    _im = _ax1.imshow(
        hit_count[np.newaxis, :], aspect="auto", cmap="YlOrRd",
        vmin=0, vmax=max(3, int(hit_count.max())),
    )
    _ax1.set_yticks([])
    _ax1.set_title("True substitution events per site (darker = struck more times)", fontsize=11)
    _fig.colorbar(_im, ax=_ax1, orientation="vertical", fraction=0.03, pad=0.02)

    _ax2.imshow(observed_diff_mask[np.newaxis, :].astype(int), aspect="auto", cmap="Greens", vmin=0, vmax=1)
    _ax2.set_yticks([])
    _ax2.set_xlabel("Site position along the sequence")
    _ax2.set_title("Observed difference from ancestor (green = yes)", fontsize=10)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo, n_multi_hit_sites, n_sites):
    mo.md(
        f"""
        *Out of {n_sites} sites, **{n_multi_hit_sites}** were struck by two or
        more substitutions. Compare the top row (true history) to the bottom
        row (what a sequence comparison would actually show) — darker patches
        in the top row that don't line up with a green patch below are hidden
        history.*
        """
    )
    return


@app.cell(hide_code=True)
def _(
    branch_length_slider,
    conserved_mask,
    hit_count,
    mutation_rate_slider,
    np,
    observed_diff_mask,
    plt,
    ts_tv_slider,
):
    _g = np.arange(501)
    _rates = np.where(conserved_mask, mutation_rate_slider.value * 0.05, mutation_rate_slider.value)
    _true_per_site = _rates.mean() * _g
    _observed_frac = expected_mismatches(_rates[:, None], _g, ts_tv_slider.value).mean(axis=0)

    _true_now = float(hit_count.mean())
    _observed_now = float(observed_diff_mask.mean())

    _fig, _ax = plt.subplots(figsize=(5.8, 3.8))
    _ax.plot(_g, _true_per_site, color="#546e7a", linewidth=2, linestyle="--", label="Expected events / site")
    _ax.plot(_g, _observed_frac, color="#2e7d32", linewidth=2.5, label="Expected endpoint mismatches / site")
    _ax.scatter([branch_length_slider.value], [_true_now], color="#546e7a", zorder=5, s=70)
    _ax.scatter([branch_length_slider.value], [_observed_now], color="#e65100", zorder=5, s=90, label="This simulation")
    _ax.set_xlabel("Branch length (generations)")
    _ax.set_ylabel("Events or mismatches per site")
    _ax.set_title("Observed differences plateau while true changes keep climbing", fontsize=12, color="#2e5a27")
    _ax.legend(loc="upper left", frameon=False, fontsize=9)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both curves are expectations under the process used in this notebook,
    including transition bias and the actual mix of slow and fast sites.
    The points are this run's counts. The event record keeps growing;
    the endpoint comparison can only say whether each site differs.
    """)
    return


@app.cell(hide_code=True)
def _(
    hit_count,
    mo,
    n_multi_hit_sites,
    n_observed_differences,
    n_sites,
    n_true_substitutions,
):
    _hit_bins = ["0 hits", "1 hit", "2 hits", "3+ hits"]
    _hit_values = [
        int((hit_count == 0).sum()),
        int((hit_count == 1).sum()),
        int((hit_count == 2).sum()),
        int((hit_count >= 3).sum()),
    ]

    _summary_rows = [
        {"Quantity": "Sites simulated", "Value": n_sites},
        {"Quantity": "True substitution events (total)", "Value": n_true_substitutions},
        {"Quantity": "Observed differing sites", "Value": n_observed_differences},
        {"Quantity": "Sites hit 2+ times (multi-hit)", "Value": n_multi_hit_sites},
        {"Quantity": "Sites: 0 hits", "Value": _hit_values[0]},
        {"Quantity": "Sites: 1 hit", "Value": _hit_values[1]},
        {"Quantity": "Sites: 2 hits", "Value": _hit_values[2]},
        {"Quantity": "Sites: 3+ hits", "Value": _hit_values[3]},
    ]

    mo.vstack(
        [
            mo.md("### Counts for this run"),
            mo.ui.table(data=_summary_rows, selection=None, pagination=False, show_download=False),
        ]
    )
    return


@app.cell(hide_code=True)
def _(hit_count, mo, observed_diff_mask):
    _mean_true = float(hit_count.mean())

    if _mean_true < 0.2:
        _level = "Early divergence"
        _kind = "success"
        _explain = (
            "Most sites have not been hit. Visible mismatches are still "
            "close to the event count in this run."
        )
    elif _mean_true < 1.5:
        _level = "Intermediate divergence"
        _kind = "warn"
        _explain = (
            "Some sites have changed repeatedly. The event count and the "
            "mismatch count are starting to separate."
        )
    else:
        _level = "Saturation"
        _kind = "danger"
        _explain = (
            "Many sites have changed repeatedly; some returned exactly to "
            "the ancestral base. The endpoint comparison misses that history. "
            "This label is a teaching shorthand, not a universal saturation threshold."
        )

    mo.md(
        f"""
        **{_level}:** on average {_mean_true:.2f} simulated events per site,
        but only {observed_diff_mask.mean():.2f} observed differences per site.

        {_explain}
        """
    ).callout(kind=_kind, title=f"Interpretation: {_level}")
    return


@app.function(hide_code=True)
def expected_mismatches(rate, generations, bias):
    # Diagonal of the discrete four-state transition matrix raised to g.
    a = 1 - 4 * rate / (bias + 2)
    b = 1 - 2 * rate * (bias + 1) / (bias + 2)
    return 0.75 - 0.25 * a**generations - 0.5 * b**generations


@app.cell(hide_code=True)
def _(mo):
    check_answer = mo.ui.radio(
        ["No change is possible", "One or more changes may be hidden", "Exactly two changes occurred"],
        label="A site starts as A and ends as A. What does that tell us?",
    )
    show_explanation = mo.ui.checkbox(label="Show the explanation")
    mo.vstack([mo.md("## 4. Check your reasoning"), check_answer, show_explanation])
    return check_answer, show_explanation


@app.cell(hide_code=True)
def _(check_answer, mo, show_explanation):
    mo.stop(not show_explanation.value)
    _correct = check_answer.value == "One or more changes may be hidden"
    mo.md(
        ("Yes. " if _correct else "Matching endpoints can hide earlier changes. ")
        + "The site could have stayed A, or followed A -> G -> A, or a "
        "longer path. The endpoints do not count those events."
    ).callout(kind="success" if _correct else "info", title="Explanation")
    return


@app.cell(hide_code=True)
def _(mo):
    reflection_input = mo.ui.text_area(
        label="One sentence for a colleague", rows=2,
        placeholder="Why can a sequence comparison underestimate historical change?",
    )
    mo.vstack([
        mo.md(
            "## 5. Take it further\nSelect Explore and lengthen the branch to "
            "500 generations. Leave the rate fixed. How far apart do the two "
            "counts get? Then change the conserved-site fraction and compare "
            "how quickly the mismatch curve rises."
        ),
        mo.md("## 6. Put it into words"), reflection_input,
        mo.accordion({
            "One possible explanation": mo.md(
                "A mismatch records the final state, not the number of times "
                "the site changed. Repeated changes can overwrite one another."
            ),
            "Where the model stops": mo.md(
                "There is no population, drift or fixation here. Slow sites "
                "have 5% of the fast-site rate, which stands in for constraint "
                "without simulating fitness. Sites are independent, with no "
                "indels or sequence context. The stage labels are toy thresholds."
            ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
