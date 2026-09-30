import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. When methods disagree

    Four taxa allow three unrooted trees. We will give the same alignment
    to three scoring methods and ask which tree each one prefers.

    Allow **5 minutes** for the guided experiment. The comparison changes
    an assumption in the likelihood calculation, without changing the data.
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
    prediction_input = mo.ui.text_area(
        placeholder="Can a method change its preferred tree when only its model changes?",
        label="Your prediction", rows=2,
    )
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Predict\nWill the three methods still prefer the same tree?"),
        prediction_input,
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
    n_sites_slider = mo.ui.slider(5, 150, value=10, step=5, label="Number of simulated sites")
    homoplasy_slider = mo.ui.slider(0.0, 1.0, value=0.50, step=0.05, label="Homoplasy level")
    rate_imbalance_slider = mo.ui.slider(0.0, 1.0, value=0.20, step=0.05, label="Rate imbalance (randomize taxon D)")
    model_mismatch_slider = mo.ui.slider(0.0, 1.0, value=1.0 if session_step.value == "Compare" else 0.0, step=0.05, label="Model mismatch level")
    seed_slider = mo.ui.slider(1, 100, value=29, step=1, label="Random seed")

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
            mo.ui.table(data=_score_rows, selection=None, pagination=False, show_download=False),
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
    _im = _ax.imshow(_rank_matrix, cmap="RdYlGn_r", vmin=1, vmax=3)
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
    *Green = that method's top choice (rank 1); red = that method's least
    preferred tree (rank 3). If the same column is green across all three
    rows, the methods agree.*
    """)
    return


@app.cell(hide_code=True)
def _(method_names, mo, ranks):
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

    agreement_level = _agreement_level
    top_choices = _top_choices

    mo.md(
        f"""
        **{_agreement_level}**

        Distance: {", ".join(_top_choices["Distance-like"])}.
        Parsimony: {", ".join(_top_choices["Parsimony-like"])}.
        Likelihood: {", ".join(_top_choices["Likelihood-like"])}.
        """
    ).callout(kind=_agreement_kind, title=f"Agreement Check: {_agreement_level}")
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
    mo.vstack([mo.md("## 4. Check your reasoning"), check_answer, show_explanation])
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
    reflection_input = mo.ui.text_area(
        label="One sentence for a colleague", rows=2,
        placeholder="What would you investigate if methods disagreed on your data?",
    )
    mo.vstack([
        mo.md(
            "## 5. Take it further\nSelect Explore. Change homoplasy while "
            "holding model mismatch fixed. Can the methods agree on a tree "
            "other than Tree 1? Check for ties before calling a winner."
        ),
        mo.md("## 6. Put it into words"), reflection_input,
        mo.accordion({
            "One possible explanation": mo.md(
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
