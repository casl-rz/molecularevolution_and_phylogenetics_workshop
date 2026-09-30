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
    mo.Html(r"""
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

    <nav class="lab-nav" aria-label="Interactive workshop lessons"><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/01_sequences_as_historical_records.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">01 &nbsp; Sequence records</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/02_mutation_substitution_saturation.py/wasm?embed=true" target="_blank" rel="noopener noreferrer" aria-current="page">02 &nbsp; Hidden changes</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/03_alignment_to_tree.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">03 &nbsp; Alignment to tree</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/04_methods_disagree.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">04 &nbsp; Competing trees</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/05_orthology_and_gene_family_case.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">05 &nbsp; Gene families</a></nav>
    <section class="lab-hero" aria-label="Lesson 2">
    <div class="lab-eyebrow">Molecular evolution field lab / 02</div>
    <h1>The endpoint is<br>not the whole story.</h1><p>Count every event, then compare what remains visible in the final bases.</p><div class="lab-orbit" aria-hidden="true"></div>
    </section>
    <div class="lab-meta">4-minute guided experiment &middot; Synthetic data &middot; No typing needed.
    Lesson links open the browser-only WebAssembly apps in new tabs.</div>
    """)
    return


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
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Watch\nLonger branches can hide more history behind the same endpoints."),
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
        0.001, 0.300, value=0.020, step=0.001, label="Mutation rate (per site, per generation)",
        show_value=True,
    )
    branch_length_slider = mo.ui.slider(
        1, 500, value=200 if session_step.value == "Compare" else 5, step=1, label="Branch length (generations)",
        show_value=True,
    )
    ts_tv_slider = mo.ui.slider(
        0.5, 10.0, value=2.0, step=0.1, label="Transition/transversion bias",
        show_value=True,
    )
    conserved_fraction_slider = mo.ui.slider(
        0.0, 0.95, value=0.30, step=0.05, label="Conserved site fraction",
        show_value=True,
    )
    seed_slider = mo.ui.slider(
        1, 100, value=7, step=1, label="Random seed",
        show_value=True,
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
def _(
    hit_count,
    metric_card,
    mo,
    n_multi_hit_sites,
    n_observed_differences,
    n_true_substitutions,
    observed_diff_mask,
):

    _hidden = int(((hit_count >= 2) & ~observed_diff_mask).sum())
    mo.vstack([
        mo.md("## 3. Read the result\nCompare the event record with the endpoint mismatches. The coral H tiles below expose history that the final comparison misses."),
        mo.hstack([
            metric_card("Simulated events", n_true_substitutions, "Every change is recorded", "#ee916e"),
            metric_card("Visible mismatches", n_observed_differences, "Only the final states are compared", "#0099a8"),
            metric_card("Hidden repeat-hit sites", _hidden, f"Within {n_multi_hit_sites} repeatedly hit sites", "#7a9f36"),
        ], wrap=True, gap=1),
        mo.md("**Simulated:** every event and ancestral base. **Observed:** endpoint mismatches. **Inferred:** how incomplete that comparison is. **Assumed:** independent sites and two rate classes."),
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
def _(hit_count, mo, observed_diff_mask):

    _tiles = []
    for _position, (_hits, _different) in enumerate(zip(hit_count, observed_diff_mask)):
        _hidden = _hits >= 2 and not _different
        _color = "#f5a28e" if _hidden else "#d9ec91" if _different else "#dce6de"
        _label = f"{_hits}H" if _hidden else str(_hits)
        _tiles.append(
            f'<span class="lab-site" style="background:{_color}" '
            f'title="Site {_position + 1}: {_hits} events; endpoint '
            f'{"different" if _different else "matching"}">{_label}</span>'
        )
    mo.Html(
        '<section class="lab-surface"><h3>The hidden-history atlas</h3>'
        '<div class="lab-legend"><b style="background:#f5a28e">H: hidden repeat changes</b>'
        '<b style="background:#d9ec91">Visible mismatch</b><b style="background:#dce6de">Matching endpoints</b></div>'
        '<div class="lab-scroll"><div class="lab-history">' + "".join(_tiles) + '</div></div>'
        '<p class="lab-metric-detail">Every tile is one simulated site; its number counts events. '
        'Coral H tiles changed repeatedly but end on the ancestral base. Read left to right, '
        'wrapping every 20 sites. Hover for the position.</p></section>'
    )
    return


@app.cell(hide_code=True)
def _(mo, n_multi_hit_sites, n_sites):
    mo.md(
        f"""
        *Out of {n_sites} sites, **{n_multi_hit_sites}** were struck by two or
        more substitutions. The atlas labels hidden repeat-hit sites with H. Their event counts
        are greater than zero, even though the endpoints match.*
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
            mo.ui.table(data=_summary_rows, selection=None, pagination=False, show_download=False, show_search=False),
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
    mo.vstack([mo.md("## 4. Quick check"), check_answer, show_explanation])
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
    mo.vstack([
        mo.md(
            "## 5. Explore further\nSelect Explore and lengthen the branch to "
            "500 generations. Leave the rate fixed. How far apart do the two "
            "counts get? Then change the conserved-site fraction and compare "
            "how quickly the mismatch curve rises."
        ),
        mo.md("## 6. Behind the model"),
        mo.accordion({
            "The idea in one sentence": mo.md(
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
