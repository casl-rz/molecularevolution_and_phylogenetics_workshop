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

    <nav class="lab-nav" aria-label="Interactive workshop lessons"><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/01_sequences_as_historical_records.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">01 &nbsp; Sequence records</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/02_mutation_substitution_saturation.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">02 &nbsp; Hidden changes</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/03_alignment_to_tree.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">03 &nbsp; Alignment to tree</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/04_methods_disagree.py/wasm?embed=true" target="_blank" rel="noopener noreferrer" aria-current="page">04 &nbsp; Competing trees</a><a href="https://molab.marimo.io/github/casl-rz/molecularevolution_and_phylogenetics_workshop/blob/main/05_orthology_and_gene_family_case.py/wasm?embed=true" target="_blank" rel="noopener noreferrer">05 &nbsp; Gene families</a></nav>
    <section class="lab-hero" aria-label="Lesson 4">
    <div class="lab-eyebrow">Molecular evolution field lab / 04</div>
    <h1>Same data.<br>Different verdicts.</h1><p>Three trees compete under three criteria. Agreement is not proof.</p><div class="lab-orbit" aria-hidden="true"></div>
    </section>
    <div class="lab-meta">5-minute guided experiment &middot; Synthetic data &middot; No typing needed.
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
        The methods ask different questions. Distance uses pairwise
        separations; parsimony counts the minimum changes; likelihood
        evaluates the probability of the data under a model.
        Agreement is useful, but all three can agree on a wrong tree.
        """
    ).callout(kind="info", title="What we're testing")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### What the scores mean

        With exactly four taxa (A, B, C, D), there are only three possible
        unrooted trees, distinguished by which two taxa form a "cherry":

        - **Tree 1**: (A, B) | (C, D)
        - **Tree 2**: (A, C) | (B, D)
        - **Tree 3**: (A, D) | (B, C)

        **Distance-like score** — uses the four-point condition: sum the
        pairwise genetic distances for the two taxon pairs each tree implies
        (e.g., d(A,B) + d(C,D) for Tree 1). The tree with the **smallest** sum
        fits the distances best.

        **Parsimony-like score** — counts the minimum number of character
        changes each tree requires to explain every site (via Fitch's
        algorithm). The tree needing the **fewest** changes is preferred.

        **Likelihood-like score** — asks how probable the observed data are
        under a simple shared-rate substitution model, with branch lengths
        fit to each tree separately. The tree with the **highest** likelihood
        is preferred.

        These three criteria usually agree when the signal is clean. They can
        disagree when the data contain **homoplasy** (independent changes that
        mimic shared ancestry), **rate imbalance** (one lineage evolving much
        faster than the others), or when the likelihood method's assumed
        model does not match how the data were actually generated.
        """
    ).callout(kind="neutral", title="Distance, Parsimony, and Likelihood Scoring")
    return


@app.cell(hide_code=True)
def _(mo):
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Watch\nChanging the likelihood model can change its preferred tree."),
        mo.md(
            "## 2. Try it\nCompare changes only model mismatch from 0 to 1. "
            "The alignment, homoplasy and rate-imbalance settings stay fixed. "
            "You can still move any slider. Switch to another step and back to reset."
        ),
        session_step,
    ])
    return (session_step,)


@app.cell(hide_code=True)
def _(mo, session_step):
    n_sites_slider = mo.ui.slider(5, 150, value=10, step=5, label="Number of simulated sites",
        show_value=True,
    )
    homoplasy_slider = mo.ui.slider(0.0, 1.0, value=0.50, step=0.05, label="Homoplasy level",
        show_value=True,
    )
    rate_imbalance_slider = mo.ui.slider(0.0, 1.0, value=0.20, step=0.05, label="Rate imbalance (randomize taxon D)",
        show_value=True,
    )
    model_mismatch_slider = mo.ui.slider(0.0, 1.0, value=1.0 if session_step.value == "Compare" else 0.0, step=0.05, label="Model mismatch level",
        show_value=True,
    )
    seed_slider = mo.ui.slider(1, 100, value=29, step=1, label="Random seed",
        show_value=True,
    )

    mo.vstack(
        [
            mo.md("### Controls"),
            mo.hstack([n_sites_slider, homoplasy_slider], justify="start", gap=3),
            mo.hstack([rate_imbalance_slider, model_mismatch_slider], justify="start", gap=3),
            mo.hstack([seed_slider], justify="start", gap=3),
            mo.md(
                r"""
                *`Number of simulated sites` sets how much data the methods
                have to work with; `homoplasy level` is the fraction of sites
                that, instead of supporting the true tree, misleadingly
                support one of the two wrong trees; `rate imbalance` is the
                chance taxon D's state gets randomized at a site (simulating a
                fast-evolving lineage); `model mismatch` skews the base
                frequencies assumed by the likelihood method away from the
                frequencies actually used to generate the data; `random seed`
                fixes the randomness so a run can be reproduced. Randomizing
                D can make some columns no longer parsimony-informative.*
                """
            ),
        ]
    )
    return (
        homoplasy_slider,
        model_mismatch_slider,
        n_sites_slider,
        rate_imbalance_slider,
        seed_slider,
    )


@app.cell(hide_code=True)
def _(
    homoplasy_slider,
    n_sites_slider,
    np,
    rate_imbalance_slider,
    seed_slider,
):
    taxa = ["A", "B", "C", "D"]
    bipartitions = {
        "Tree 1": (("A", "B"), ("C", "D")),
        "Tree 2": (("A", "C"), ("B", "D")),
        "Tree 3": (("A", "D"), ("B", "C")),
    }
    true_tree_name = "Tree 1"

    rng = np.random.default_rng(seed_slider.value)
    n_sites = int(n_sites_slider.value)

    data = np.empty((4, n_sites), dtype=int)  # rows: A, B, C, D
    for _j in range(n_sites):
        if rng.random() < homoplasy_slider.value:
            _generating = rng.choice(["Tree 2", "Tree 3"])
        else:
            _generating = true_tree_name

        _cherry1, _cherry2 = bipartitions[_generating]
        _state1, _state2 = rng.choice(4, size=2, replace=False)
        _col = np.empty(4, dtype=int)
        for _i, _name in enumerate(taxa):
            _col[_i] = _state1 if _name in _cherry1 else _state2
        data[:, _j] = _col

    # rate imbalance: taxon D (index 3) sometimes has its state randomized
    _randomize_mask = rng.random(n_sites) < rate_imbalance_slider.value
    data[3, _randomize_mask] = rng.integers(0, 4, size=int(_randomize_mask.sum()))

    obs = {name: data[i] for i, name in enumerate(taxa)}
    return bipartitions, data, n_sites, obs, taxa, true_tree_name


@app.cell(hide_code=True)
def _(bipartitions, np, obs, taxa):
    def _p_distance(a, b):
        return float(np.mean(a != b))


    pairwise = {}
    for _i in range(4):
        for _j in range(4):
            pairwise[(taxa[_i], taxa[_j])] = _p_distance(obs[taxa[_i]], obs[taxa[_j]])

    distance_scores = {}
    for _name, (_c1, _c2) in bipartitions.items():
        distance_scores[_name] = pairwise[(_c1[0], _c1[1])] + pairwise[(_c2[0], _c2[1])]
    return (distance_scores,)


@app.cell(hide_code=True)
def _(bipartitions, data, n_sites, taxa):
    def _fitch_site_cost(col, cherry1, cherry2, idx):
        a, b = col[idx[cherry1[0]]], col[idx[cherry1[1]]]
        c, d = col[idx[cherry2[0]]], col[idx[cherry2[1]]]
        set1 = {a, b} if a != b else {a}
        cost1 = 0 if a == b else 1
        set2 = {c, d} if c != d else {c}
        cost2 = 0 if c == d else 1
        if set1 & set2:
            return cost1 + cost2
        return cost1 + cost2 + 1


    _idx = {name: i for i, name in enumerate(taxa)}
    parsimony_scores = {}
    for _name, (_c1, _c2) in bipartitions.items():
        _total = 0
        for _j in range(n_sites):
            _total += _fitch_site_cost(data[:, _j], _c1, _c2, _idx)
        parsimony_scores[_name] = _total
    return (parsimony_scores,)


@app.cell(hide_code=True)
def _(bipartitions, data, model_mismatch_slider, np, taxa):
    _true_pi = np.full(4, 0.25)
    _mismatch = model_mismatch_slider.value
    _assumed_pi = np.array([1 + 3 * _mismatch, 1 - _mismatch, 1 - _mismatch, 1 - _mismatch])
    _assumed_pi = np.clip(_assumed_pi, 0.02, None)
    _assumed_pi = _assumed_pi / _assumed_pi.sum()

    _beta = 1.0 / (1.0 - np.sum(_assumed_pi ** 2))
    _t_grid = np.linspace(0.02, 2.0, 40)

    _idx_lik = {name: i for i, name in enumerate(taxa)}
    _onehot = {name: np.eye(4)[data[_idx_lik[name]]] for name in taxa}  # (n_sites, 4)


    def _transition_matrix(t):
        decay = np.exp(-_beta * t)
        return decay * np.eye(4) + (1 - decay) * np.outer(np.ones(4), _assumed_pi)


    likelihood_scores = {}
    best_branch_length = {}
    for _name, (_c1, _c2) in bipartitions.items():
        _best_ll = -np.inf
        _best_t = None
        for _t in _t_grid:
            _P = _transition_matrix(_t)
            _partial_kl = (_onehot[_c2[0]] @ _P.T) * (_onehot[_c2[1]] @ _P.T)
            _partial_kl_prop = _partial_kl @ _P.T
            _partial_ij = (_onehot[_c1[0]] @ _P.T) * (_onehot[_c1[1]] @ _P.T)
            _site_lik = (_partial_ij * _partial_kl_prop) @ _assumed_pi
            _total_ll = np.sum(np.log(np.clip(_site_lik, 1e-300, None)))
            if _total_ll > _best_ll:
                _best_ll = _total_ll
                _best_t = _t
        likelihood_scores[_name] = _best_ll
        best_branch_length[_name] = _best_t
    return (likelihood_scores,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Read the result
    Find the lowest distance and parsimony scores and the highest likelihood score. Do the winners match? Compare scores within each method, not across their different scales.

    **Simulated:** the generating split and constructed site patterns. **Observed:** this alignment. **Inferred:** each method's preferred tree. **Assumed:** its scoring rule and, for likelihood, its base frequencies.
    """)
    return


@app.cell(hide_code=True)
def _(bipartitions, plt, true_tree_name):
    def _draw_quartet(ax, cherry1, cherry2, title, highlight=False):
        # simple quartet layout: two cherries joined by an internal edge
        ax.plot([0, 0.4], [1, 0.5], color="#546e7a", linewidth=2)
        ax.plot([0, 0.4], [0, 0.5], color="#546e7a", linewidth=2)
        ax.plot([0.4, 0.5], [0.5, 0.5], color="#546e7a", linewidth=2.5)
        ax.plot([0.5, 0.9], [0.5, 1], color="#546e7a", linewidth=2)
        ax.plot([0.5, 0.9], [0.5, 0], color="#546e7a", linewidth=2)

        # bracket each cherry so the grouping is obvious at a glance, not just from labels
        ax.plot([-0.12, -0.12], [-0.15, 1.15], color="#2e7d32", linewidth=2)
        ax.plot([-0.12, 0.0], [-0.15, -0.15], color="#2e7d32", linewidth=2)
        ax.plot([-0.12, 0.0], [1.15, 1.15], color="#2e7d32", linewidth=2)
        ax.plot([1.02, 1.02], [-0.15, 1.15], color="#c62828", linewidth=2)
        ax.plot([1.02, 0.9], [-0.15, -0.15], color="#c62828", linewidth=2)
        ax.plot([1.02, 0.9], [1.15, 1.15], color="#c62828", linewidth=2)

        ax.text(-0.05, 1, cherry1[0], ha="right", va="center", fontsize=12, color="#1b5e20", fontweight="bold")
        ax.text(-0.05, 0, cherry1[1], ha="right", va="center", fontsize=12, color="#1b5e20", fontweight="bold")
        ax.text(0.95, 1, cherry2[0], ha="left", va="center", fontsize=12, color="#8e0000", fontweight="bold")
        ax.text(0.95, 0, cherry2[1], ha="left", va="center", fontsize=12, color="#8e0000", fontweight="bold")
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.4, 1.4)
        ax.axis("off")
        color = "#2e5a27" if highlight else "#33402f"
        ax.set_title(title, fontsize=11, color=color, fontweight="bold" if highlight else "normal")
        ax.text(
            0.5, -0.35,
            f"cherries: ({cherry1[0]},{cherry1[1]}) | ({cherry2[0]},{cherry2[1]})",
            ha="center", va="center", fontsize=9, color="#546e7a", transform=ax.transData,
        )


    _fig, _axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
    for _ax, (_name, (_c1, _c2)) in zip(_axes, bipartitions.items()):
        _label = _name + (" (generating tree)" if _name == true_tree_name else "")
        _draw_quartet(_ax, _c1, _c2, _label, highlight=(_name == true_tree_name))
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *These are the only three possible unrooted trees for four taxa. Tree 1
    is marked because it is the tree actually used to generate this
    dataset — in a real analysis you would not know this in advance.*
    """)
    return


@app.cell(hide_code=True)
def _(
    bipartitions,
    distance_scores,
    likelihood_scores,
    mo,
    np,
    parsimony_scores,
):
    def rank_scores(scores, lower_is_better):
        sign = 1 if lower_is_better else -1
        return {
            name: 1 + sum(
                sign * other < sign * value and not np.isclose(other, value, rtol=1e-9, atol=1e-9)
                for other in scores.values()
            )
            for name, value in scores.items()
        }

    ranks = {}
    for _method_name, _scores, _lower_is_better in [
        ("Distance-like", distance_scores, True),
        ("Parsimony-like", parsimony_scores, True),
        ("Likelihood-like", likelihood_scores, False),
    ]:
        ranks[_method_name] = rank_scores(_scores, _lower_is_better)

    _score_rows = []
    for _name in bipartitions:
        _score_rows.append(
            {
                "Tree": _name,
                "Distance-like score": round(distance_scores[_name], 3),
                "Parsimony-like score": parsimony_scores[_name],
                "Likelihood-like score": round(likelihood_scores[_name], 2),
                "Distance rank": ranks["Distance-like"][_name],
                "Parsimony rank": ranks["Parsimony-like"][_name],
                "Likelihood rank": ranks["Likelihood-like"][_name],
            }
        )

    mo.vstack(
        [
            mo.md("### Scores and ranks"),
            mo.ui.table(data=_score_rows, selection=None, pagination=False, show_download=False, show_search=False),
            mo.md(
                "*Lower is better for distance-like and parsimony-like scores; "
                "higher (less negative) is better for likelihood. Equal scores "
                "share a rank; a rank is not a confidence probability.*"
            ),
        ]
    )
    return (ranks,)


@app.cell(hide_code=True)
def _(bipartitions, np, plt, ranks):
    method_names = ["Distance-like", "Parsimony-like", "Likelihood-like"]
    tree_names = list(bipartitions.keys())
    _rank_matrix = np.array([[ranks[m][t] for t in tree_names] for m in method_names])

    _fig, _ax = plt.subplots(figsize=(5.4, 3.2))
    _im = _ax.imshow(_rank_matrix, cmap=plt.matplotlib.colors.ListedColormap(["#9bcbb2", "#f1d589", "#f5a28e"]), vmin=1, vmax=3)
    _ax.set_xticks(range(len(tree_names)))
    _ax.set_xticklabels(tree_names)
    _ax.set_yticks(range(len(method_names)))
    _ax.set_yticklabels(method_names)
    for _i in range(len(method_names)):
        for _j in range(len(tree_names)):
            _ax.text(_j, _i, f"rank {_rank_matrix[_i, _j]}", ha="center", va="center", fontsize=10, color="#222")
    _ax.set_title("Each method's preference ranking per tree", fontsize=12, color="#2e5a27")
    _fig.colorbar(_im, ax=_ax, fraction=0.046, pad=0.04, label="Rank (1 = best)")
    _fig.tight_layout()
    _fig
    return (method_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Mint = that method's top choice (rank 1); coral = that method's least
    preferred tree (rank 3). If the same column is green across all three
    rows, the methods agree.*
    """)
    return


@app.cell(hide_code=True)
def _(method_names, metric_card, mo, ranks):
    _top_choices = {m: [t for t, r in ranks[m].items() if r == 1] for m in method_names}
    _has_ties = any(len(choices) > 1 for choices in _top_choices.values())
    _unique_top_choices = {t for choices in _top_choices.values() for t in choices}

    if _has_ties:
        _agreement_level = "Tied scores: inspect the alternatives"
        _agreement_kind = "warn"
    elif len(_unique_top_choices) == 1:
        _agreement_level = "Strong agreement"
        _agreement_kind = "success"
    elif len(_unique_top_choices) == 2:
        _agreement_level = "Moderate disagreement"
        _agreement_kind = "warn"
    else:
        _agreement_level = "Severe disagreement"
        _agreement_kind = "danger"


    _preference_cards = mo.hstack([
        metric_card(method, " + ".join(choices), "All tied best choices are retained",
                    "#0099a8" if method == "Likelihood-like" else "#7a9f36" if method == "Distance-like" else "#ee916e")
        for method, choices in _top_choices.items()
    ], wrap=True, gap=1)
    agreement_level = _agreement_level
    top_choices = _top_choices

    _agreement = mo.md(
        f"""
        **{_agreement_level}**

        Distance: {", ".join(_top_choices["Distance-like"])}.
        Parsimony: {", ".join(_top_choices["Parsimony-like"])}.
        Likelihood: {", ".join(_top_choices["Likelihood-like"])}.
        """
    ).callout(kind=_agreement_kind, title=f"Agreement Check: {_agreement_level}")
    mo.vstack([_preference_cards, _agreement])
    return agreement_level, top_choices


@app.cell(hide_code=True)
def _(agreement_level, mo, top_choices, true_tree_name):
    if agreement_level == "Strong agreement":
        _matches_truth = top_choices["Distance-like"] == [true_tree_name]
        _explain = (
            "All three methods land on the same tree. "
            + (
                "That tree also matches the one actually used to generate the "
                "data — with this much clean signal, the choice of method "
                "did not matter."
                if _matches_truth
                else
                "That tree does NOT match the one actually used to generate "
                "the data — strong agreement between methods does not "
                "guarantee correctness; it only means the methods agree with "
                "each other on this dataset."
            )
        )
        _kind = "success" if _matches_truth else "warn"
    elif agreement_level.startswith("Tied scores"):
        _explain = (
            "At least one method gives several trees the same best score. "
            "There is no unique winner for that method. Keep all tied choices "
            "in the discussion rather than choosing the first row."
        )
        _kind = "warn"
    elif agreement_level == "Moderate disagreement":
        _explain = (
            "Two methods agree with each other, but the third method scores "
            "the trees differently. This usually happens when there is enough "
            "homoplasy or rate imbalance to create a conflicting signal that "
            "one criterion is more sensitive to than the others."
        )
        _kind = "warn"
    else:
        _explain = (
            "All three methods prefer a different tree. This is a sign that "
            "the data contain substantial conflicting signal (homoplasy, rate "
            "imbalance, and/or a poor model fit for the likelihood method) — "
            "there is no dataset-independent way to say which method is "
            "'right' here without additional information."
        )
        _kind = "danger"

    mo.md(
        f"""
        **{agreement_level}.** {_explain}
        """
    ).callout(kind=_kind, title=f"Interpretation: {agreement_level}")
    return


@app.cell(hide_code=True)
def _(mo):
    check_answer = mo.ui.radio(
        ["The tree must be correct", "The methods share a preference, but may share a mistake", "The alignment contains no uncertainty"],
        label="All three methods agree. What follows?",
    )
    show_explanation = mo.ui.checkbox(label="Show the explanation")
    mo.vstack([mo.md("## 4. Quick check"), check_answer, show_explanation])
    return check_answer, show_explanation


@app.cell(hide_code=True)
def _(check_answer, mo, show_explanation):
    mo.stop(not show_explanation.value)
    _correct = check_answer.value == "The methods share a preference, but may share a mistake"
    mo.md(
        ("Yes. " if _correct else "Agreement is a shared preference, not proof. ")
        + "All methods see the same alignment. Misleading patterns can "
        "therefore mislead them together. Compare the winner with the "
        "known generating tree here; real data do not give us that answer."
    ).callout(kind="success" if _correct else "info", title="Explanation")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
        mo.md(
            "## 5. Explore further\nSelect Explore. Change homoplasy while "
            "holding model mismatch fixed. Can the methods agree on a tree "
            "other than Tree 1? Check for ties before calling a winner."
        ),
        mo.md("## 6. Behind the model"),
        mo.accordion({
            "The idea in one sentence": mo.md(
                "Different criteria can favor different explanations of the "
                "same data. I would check alignment, sampling and model fit "
                "before treating a disagreement as a biological result."
            ),
            "Where the model stops": mo.md(
                "These are constructed patterns, not a full branch-by-branch "
                "simulation. D's states are randomized to mimic noisy rate "
                "imbalance. Likelihood uses a shared branch-length grid and "
                "an F81-like model; parsimony uses unweighted Fitch counts. "
                "We compare only three trees, with no bootstrap or posterior support."
            ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
