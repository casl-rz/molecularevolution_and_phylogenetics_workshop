import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. From alignment to tree

    We know the tree because we made it. Now hide that history and try to
    recover its groupings from the sequences. Will a longer sequence help?

    Allow **5 minutes** for the guided experiment. Compare the tip names in
    each group, rather than the orientation of the two drawings.
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.spatial.distance import squareform
    from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

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
    return dendrogram, linkage, mo, np, plt, squareform


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        More bases can mean more useful patterns, but some patterns conflict
        and some do not resolve the grouping at all. We will compare a
        20-base alignment with a 500-base alignment from the same tree.
        The estimated tree is a hypothesis, even when it matches our toy truth.
        """
    ).callout(kind="info", title="What we're testing")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Terms you can come back to": mo.md(r"""
    **Parsimony-informative sites:** at
    least two different states are each shared by at least two taxa. Every
    site in the alignment below falls into one of three categories:

    ```
    Taxon:      T1  T2  T3  T4  T5
    Constant:    A   A   A   A   A    <- no variation to resolve a split
    Uninformative: A   A   A   A   G  <- only T5 differs; a difference unique
                                          to one taxon can't group anyone
    Informative:  A   A   G   G   A  <- T3 and T4 share G, everyone else
                                          shares A: this site is evidence
                                          that T3 and T4 form a group
    ```

    "Uninformative" here means no grouping signal under parsimony.
    Constant and singleton sites can still help estimate rates and
    branch lengths in likelihood analyses. Informative patterns can
    also be misleading if changes occurred independently.

    **Topology:** the branching pattern of the tree: which taxa are
    grouped together, and in what nested order. Two trees can have very
    different branch lengths but the same topology, or the same-looking
    shape but different topologies once you check which tips are actually
    grouped.

    **Branch lengths:** the amount of evolutionary change (here,
    genetic distance) accumulated along each edge of the tree. Long
    branches mean more accumulated substitutions, not necessarily more
    elapsed time.

    **Rooted vs. unrooted trees:** a rooted tree specifies a direction of
    time (an ancestor at the root, descendants at the tips). An unrooted
    tree shows only how taxa are grouped and how much change separates
    them, with no implied direction — you would need extra information
    (like an outgroup) to root it.
    """)})
    return


@app.cell(hide_code=True)
def _(mo):
    prediction_input = mo.ui.text_area(
        placeholder="Will 500 bases recover more of the known groupings?",
        label="Your prediction", rows=2,
    )
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Predict\nWould more sequence help, and what might it fail to fix?"),
        prediction_input,
        mo.md(
            "## 2. Try it\nCompare changes sequence length from 20 to 500 bases. "
            "Taxa, rates, correction and seed stay fixed. You can still move "
            "any slider. Switch to another step and back to reset."
        ),
        session_step,
    ])
    return (session_step,)


@app.cell(hide_code=True)
def _(mo, session_step):
    n_taxa_slider = mo.ui.slider(4, 10, value=4, step=1, label="Number of taxa")
    seq_length_slider = mo.ui.slider(20, 1000, value=500 if session_step.value == "Compare" else 20, step=10, label="Sequence length (bp)")
    mutation_rate_slider = mo.ui.slider(0.001, 0.200, value=0.005, step=0.001, label="Mutation rate (per site, per branch-length unit)")
    rate_het_slider = mo.ui.slider(0.0, 2.0, value=0.0, step=0.1, label="Rate heterogeneity across sites")
    distance_correction_dropdown = mo.ui.dropdown(
        options=["Raw p-distance", "Jukes-Cantor-like"], value="Raw p-distance", label="Distance correction"
    )
    rooting_dropdown = mo.ui.dropdown(
        options=["Rooted", "Unrooted"], value="Rooted", label="Root label (display only)"
    )
    seed_slider = mo.ui.slider(1, 100, value=1, step=1, label="Random seed")

    mo.vstack(
        [
            mo.md("### Controls"),
            mo.hstack([n_taxa_slider, seq_length_slider], justify="start", gap=3),
            mo.hstack([mutation_rate_slider, rate_het_slider], justify="start", gap=3),
            mo.hstack([distance_correction_dropdown, rooting_dropdown], justify="start", gap=3),
            mo.hstack([seed_slider], justify="start", gap=3),
            mo.md(
                r"""
                *`Number of taxa` sets how many tips the tree has; `sequence
                length` sets how many sites are simulated; `mutation rate`
                controls how fast substitutions accumulate along each branch;
                `rate heterogeneity` makes some sites mutate much faster than
                others when increased above 0 (uniform rates); `distance
                correction` chooses how observed differences are converted
                into a genetic distance before building the inferred tree;
                `root label` hides or shows the root annotation, without
                changing the UPGMA estimate;
                `random seed` fixes the randomness so a run can be
                reproduced.*
                """
            ),
        ]
    )
    return (
        distance_correction_dropdown,
        mutation_rate_slider,
        n_taxa_slider,
        rate_het_slider,
        rooting_dropdown,
        seed_slider,
        seq_length_slider,
    )


@app.cell(hide_code=True)
def _(n_taxa_slider, np, seed_slider):
    def build_random_tree(n_tips, rng, min_branch=2.0, max_branch=20.0):
        """Build a random rooted binary tree on n_tips leaves via random joining."""
        active = [{"name": f"T{i + 1}", "children": [], "branch": None} for i in range(n_tips)]
        counter = n_tips
        while len(active) > 1:
            i, j = rng.choice(len(active), size=2, replace=False)
            a, b = active[i], active[j]
            a["branch"] = float(rng.uniform(min_branch, max_branch))
            b["branch"] = float(rng.uniform(min_branch, max_branch))
            parent = {"name": f"N{counter}", "children": [a, b], "branch": None}
            counter += 1
            active = [x for k, x in enumerate(active) if k not in (i, j)] + [parent]
        root = active[0]
        root["branch"] = 0.0
        return root


    def tip_names(node):
        if not node["children"]:
            return [node["name"]]
        names = []
        for child in node["children"]:
            names.extend(tip_names(child))
        return names


    def collect_clades(node, clades=None):
        """Collect the set of tip names under every internal node (non-trivial clades)."""
        if clades is None:
            clades = []
        if node["children"]:
            names = frozenset(tip_names(node))
            if 1 < len(names) < len(tip_names(root_node)):
                clades.append(names)
            for child in node["children"]:
                collect_clades(child, clades)
        return clades


    _rng_tree = np.random.default_rng(seed_slider.value)
    root_node = build_random_tree(int(n_taxa_slider.value), _rng_tree)
    taxa_names = tip_names(root_node)
    true_clades = collect_clades(root_node)
    return root_node, taxa_names, true_clades


@app.cell(hide_code=True)
def _(
    mutation_rate_slider,
    np,
    rate_het_slider,
    root_node,
    seed_slider,
    seq_length_slider,
    taxa_names,
):
    def simulate_sequences(root, n_sites, base_rate, het_strength, rng):
        bases = np.array(list("ACGT"))

        # rate heterogeneity: gamma-distributed per-site rate multipliers, mean 1
        alpha = 1.0 / (het_strength + 0.05)
        rate_multiplier = rng.gamma(shape=alpha, scale=1.0 / alpha, size=n_sites)
        site_rate = base_rate * rate_multiplier

        ancestral_idx = rng.integers(0, 4, size=n_sites)
        sequences = {}

        def evolve(node, current_idx):
            if node["children"]:
                for child in node["children"]:
                    lam = site_rate * child["branch"]
                    n_hits = rng.poisson(lam)
                    child_idx = current_idx.copy()
                    max_hits = int(n_hits.max()) if n_hits.size else 0
                    for k in range(max_hits):
                        still = n_hits > k
                        if not still.any():
                            break
                        idx_sites = np.where(still)[0]
                        offsets = rng.integers(1, 4, size=len(idx_sites))
                        child_idx[idx_sites] = (child_idx[idx_sites] + offsets) % 4
                    evolve(child, child_idx)
            else:
                sequences[node["name"]] = "".join(bases[current_idx])

        evolve(root, ancestral_idx)
        return sequences, rate_multiplier


    _rng_seq = np.random.default_rng(seed_slider.value + 1000)
    n_sites = int(seq_length_slider.value)
    sequences, site_rate_multiplier = simulate_sequences(
        root_node, n_sites, mutation_rate_slider.value, rate_het_slider.value, _rng_seq
    )
    sequence_matrix = np.array([[c for c in sequences[name]] for name in taxa_names])
    return n_sites, sequence_matrix


@app.cell(hide_code=True)
def _(np, sequence_matrix):
    def classify_sites(matrix):
        """Return per-site status: 'constant', 'uninformative', or 'informative'."""
        n_taxa_local, n_sites_local = matrix.shape
        status = np.empty(n_sites_local, dtype=object)
        for j in range(n_sites_local):
            col = matrix[:, j]
            vals, counts = np.unique(col, return_counts=True)
            if len(vals) == 1:
                status[j] = "constant"
            elif np.sum(counts >= 2) >= 2:
                status[j] = "informative"
            else:
                status[j] = "uninformative"
        return status


    site_status = classify_sites(sequence_matrix)
    n_constant = int((site_status == "constant").sum())
    n_uninformative = int((site_status == "uninformative").sum())
    n_informative = int((site_status == "informative").sum())
    return n_constant, n_informative, n_uninformative, site_status


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Read the result
    Look for an A/A/G/G-style column in the alignment; a short alignment may not contain one. Then compare the named groups in the known and estimated trees. Do they agree?

    **Simulated:** tree, ancestor and branch changes. **Observed:** aligned endpoint bases. **Inferred:** distances and the UPGMA tree. **Assumed:** the positions correspond, the distance model is suitable, and UPGMA's clock-like structure is useful.
    """)
    return


@app.cell(hide_code=True)
def _(mo, n_sites, sequence_matrix, site_status, taxa_names):
    def _colorize_char(v, status):
        styles = {
            "constant": "color:#78909c;",
            "uninformative": "background:#fff3cd;color:#8a6500;font-weight:600;border-radius:3px;padding:0 1px;",
            "informative": "background:#a5d6a7;color:#1b5e20;font-weight:700;border-radius:3px;padding:0 1px;",
        }
        return f'<span style="{styles[status]}">{v}</span>'


    _preview_len = min(80, n_sites)
    _rows_html = []
    for _i, _name in enumerate(taxa_names):
        _spans = []
        for _j in range(_preview_len):
            _spans.append(_colorize_char(sequence_matrix[_i, _j], site_status[_j]))
        _rows_html.append(f"{_name:<6}" + "".join(_spans))

    _pre_style = (
        "font-family: \'Fira Code\', \'Courier New\', monospace; font-size:12px; "
        "line-height:1.9; background:#f4f9f4; padding:14px; border-radius:10px; "
        "border:1px solid #c8e6c9; overflow-x:auto; white-space:pre;"
    )

    mo.vstack(
        [
            mo.md("## Multiple Sequence Alignment"),
            mo.md(
                f"""<pre style="{_pre_style}">""" + "\n".join(_rows_html) + """</pre>"""
            ),
            mo.md(
                f"""
                *Showing the first {_preview_len} of {n_sites} sites.*

                - **Plain grey** — *constant*: every taxon has the same base;
                  no variation to resolve a split under parsimony.
                - **Amber highlight** — *variable but uninformative*: the base
                  varies, but only one taxon (or every taxon) has a unique
                  state, so no grouping of two or more taxa is supported.
                - **Green highlight (bold)** — *parsimony-informative*: at
                  least two different bases are each shared by at least two
                  taxa, so this site provides evidence for grouping some taxa
                  together.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(distance_correction_dropdown, np, sequence_matrix):
    def compute_distance_matrix(matrix, correction):
        n_taxa_local = matrix.shape[0]
        p_dist = np.zeros((n_taxa_local, n_taxa_local))
        for i in range(n_taxa_local):
            for j in range(n_taxa_local):
                p_dist[i, j] = np.mean(matrix[i] != matrix[j])

        if correction == "Jukes-Cantor-like":
            p_capped = np.minimum(p_dist, 0.7499)
            dist = -3 / 4 * np.log(1 - 4 / 3 * p_capped)
        else:
            dist = p_dist
        return dist


    distance_matrix = compute_distance_matrix(sequence_matrix, distance_correction_dropdown.value)
    return (distance_matrix,)


@app.cell(hide_code=True)
def _(distance_correction_dropdown, distance_matrix, plt, taxa_names):
    _fig, _ax = plt.subplots(figsize=(5.2, 4.4))
    _im = _ax.imshow(distance_matrix, cmap="YlOrRd")
    _ax.set_xticks(range(len(taxa_names)))
    _ax.set_yticks(range(len(taxa_names)))
    _ax.set_xticklabels(taxa_names, rotation=45, ha="right")
    _ax.set_yticklabels(taxa_names)
    for _i in range(len(taxa_names)):
        for _j in range(len(taxa_names)):
            _ax.text(_j, _i, f"{distance_matrix[_i, _j]:.2f}", ha="center", va="center", fontsize=8, color="#33402f")
    _ax.set_title(f"Distance matrix ({distance_correction_dropdown.value})", fontsize=12, color="#2e5a27")
    _fig.colorbar(_im, ax=_ax, fraction=0.046, pad=0.04)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(plt, root_node, rooting_dropdown, taxa_names):
    def _layout_tree(node, depth=0.0, y_counter=None, positions=None):
        if y_counter is None:
            y_counter = [0]
        if positions is None:
            positions = {}
        if node["children"]:
            child_ys = []
            for child in node["children"]:
                _layout_tree(child, depth + child["branch"], y_counter, positions)
                child_ys.append(positions[id(child)][1])
            y = sum(child_ys) / len(child_ys)
        else:
            y = y_counter[0]
            y_counter[0] += 1
        positions[id(node)] = (depth, y)
        return positions


    def _draw_tree(ax, node, positions, is_root_display=True):
        x, y = positions[id(node)]
        if node["children"]:
            for child in node["children"]:
                cx, cy = positions[id(child)]
                ax.plot([x, x], [y, cy], color="#546e7a", linewidth=1.5)
                ax.plot([x, cx], [cy, cy], color="#546e7a", linewidth=1.5)
                _draw_tree(ax, child, positions, is_root_display=False)
        else:
            ax.text(x + 0.02 * x_span[0], y, node["name"], va="center", fontsize=10)


    _positions = _layout_tree(root_node)
    x_span = [max(p[0] for p in _positions.values()) or 1.0]

    _fig, _ax = plt.subplots(figsize=(6.0, 0.5 * len(taxa_names) + 1.2))
    _draw_tree(_ax, root_node, _positions)
    if rooting_dropdown.value == "Rooted":
        _root_x, _root_y = _positions[id(root_node)]
        _ax.scatter([_root_x], [_root_y], color="#1b5e20", s=60, zorder=5)
        _ax.set_title("True tree (rooted)", fontsize=12, color="#2e5a27")
    else:
        _ax.set_title("True tree (topology and branch lengths only, root arbitrary)", fontsize=12, color="#2e5a27")
    _ax.set_xlabel("Accumulated simulation branch length")
    _ax.set_yticks([])
    for _spine in ["top", "right", "left"]:
        _ax.spines[_spine].set_visible(False)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *This is the tree actually used to simulate the sequences — the ground
    truth we are trying to recover. Horizontal distance represents
    accumulated simulation branch units. Expected substitutions per site
    also depend on the rate; these are not calibrated calendar times.*
    """)
    return


@app.cell(hide_code=True)
def _(
    dendrogram,
    distance_matrix,
    linkage,
    plt,
    rooting_dropdown,
    squareform,
    taxa_names,
):
    _condensed = squareform(distance_matrix, checks=False)
    linkage_matrix = linkage(_condensed, method="average")

    _fig, _ax = plt.subplots(figsize=(6.0, 0.5 * len(taxa_names) + 1.5))
    _dendro = dendrogram(linkage_matrix, labels=taxa_names, ax=_ax, color_threshold=0, above_threshold_color="#546e7a")
    if rooting_dropdown.value == "Rooted":
        _ax.set_title("Inferred tree (UPGMA, rooted)", fontsize=12, color="#2e5a27")
    else:
        _ax.set_title("Inferred tree (UPGMA topology and branch lengths only)", fontsize=12, color="#2e5a27")
    _ax.set_ylabel("Genetic distance")
    _fig.tight_layout()
    _fig
    return (linkage_matrix,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *This tree is built only from the distance matrix above, using UPGMA
    (a simple average-linkage clustering method) — it has no access to the
    true tree. Compare its groupings to the true tree: matching branching
    patterns mean the inference recovered the true relationships from the
    sequence data alone.*
    """)
    return


@app.cell(hide_code=True)
def _(n_sites, sequence_matrix, site_status, taxa_names, true_clades):
    def clade_supported_by_site(clade_names, col, name_to_idx):
        idx_in = [name_to_idx[n] for n in clade_names]
        idx_out = [name_to_idx[n] for n in taxa_names if n not in clade_names]
        vals_in = set(col[idx_in])
        if len(vals_in) != 1:
            return False
        shared_val = next(iter(vals_in))
        vals_out = set(col[idx_out]) if idx_out else set()
        return shared_val not in vals_out


    _name_to_idx = {name: i for i, name in enumerate(taxa_names)}
    clade_support_counts = {}
    for _clade in true_clades:
        _count = 0
        for _j in range(n_sites):
            if site_status[_j] != "informative":
                continue
            if clade_supported_by_site(_clade, sequence_matrix[:, _j], _name_to_idx):
                _count += 1
        clade_support_counts[_clade] = _count
    return (clade_support_counts,)


@app.cell(hide_code=True)
def _(
    clade_support_counts,
    mo,
    n_constant,
    n_informative,
    n_sites,
    n_uninformative,
    taxa_names,
):
    _summary_rows = [
        {"Quantity": "Taxa", "Value": len(taxa_names)},
        {"Quantity": "Sites simulated", "Value": n_sites},
        {"Quantity": "Constant sites", "Value": n_constant},
        {"Quantity": "Variable but uninformative sites", "Value": n_uninformative},
        {"Quantity": "Parsimony-informative sites", "Value": n_informative},
    ]

    _clade_rows = [
        {"Clade (taxa)": ", ".join(sorted(clade)), "Informative sites supporting it": count}
        for clade, count in sorted(clade_support_counts.items(), key=lambda kv: -kv[1])
    ]

    mo.vstack(
        [
            mo.md("## Informative-Site Summary"),
            mo.ui.table(data=_summary_rows, selection=None, pagination=False, show_download=False),
            mo.md("### Sites Supporting Each True Clade"),
            mo.ui.table(data=_clade_rows, selection=None, pagination=False, show_download=False),
        ]
    )
    return


@app.cell(hide_code=True)
def _(clade_support_counts, linkage_matrix, mo, taxa_names, true_clades):
    def linkage_clades(Z, labels):
        n = len(labels)
        clusters = {i: frozenset([labels[i]]) for i in range(n)}
        clades = []
        for i in range(Z.shape[0]):
            a, b = int(Z[i, 0]), int(Z[i, 1])
            members = clusters[a] | clusters[b]
            clusters[n + i] = members
            if 1 < len(members) < n:
                clades.append(members)
        return clades


    _inferred_clades = linkage_clades(linkage_matrix, taxa_names)
    _recovered = [c for c in true_clades if c in _inferred_clades]
    _n_recovered = len(_recovered)
    _n_true_clades = len(true_clades)
    _unsupported_clades = [c for c, count in clade_support_counts.items() if count == 0]

    if _n_true_clades == 0:
        _level = "Too few taxa to assess"
        _kind = "neutral"
        _explain = "With this few taxa there are no non-trivial clades to recover."
    elif _n_recovered == _n_true_clades and not _unsupported_clades:
        _level = "Topology fully recovered"
        _kind = "success"
        _explain = (
            "Every true clade has at least one informative site behind it, and "
            "the inferred tree reproduces all of them. With this much signal, "
            "the distance method had enough information to get the branching "
            "pattern right."
        )
    elif _n_recovered == _n_true_clades:
        _level = "Topology recovered, but signal is thin"
        _kind = "warn"
        _explain = (
            "The inferred tree happens to match the true topology, but at "
            "least one true clade has no informative sites supporting it — "
            "that agreement could easily break with a different random seed "
            "or a shorter sequence."
        )
    else:
        _level = "Topology partially incorrect"
        _kind = "danger"
        _explain = (
            f"Only {_n_recovered} of {_n_true_clades} true clades were "
            "recovered by the inferred tree. Clades with zero informative "
            "sites behind them are missing that particular kind of shared "
            "pattern. Other sites still inform distances; UPGMA's clock "
            "assumption can also distort the grouping. This table alone "
            "does not diagnose why a clade was missed."
        )

    mo.md(
        f"""
        **{_level}** — {_n_recovered} of {_n_true_clades} true clades recovered;
        {len(_unsupported_clades)} true clade(s) have zero supporting
        informative sites.

        {_explain}
        """
    ).callout(kind=_kind, title=f"Interpretation: {_level}")
    return


@app.cell(hide_code=True)
def _(mo):
    check_answer = mo.ui.radio(
        ["A A A A", "A A A G", "A A G G"],
        label="For taxa A, B, C and D, which column supports AB | CD under parsimony?",
    )
    show_explanation = mo.ui.checkbox(label="Show the explanation")
    mo.vstack([mo.md("## 4. Check your reasoning"), check_answer, show_explanation])
    return check_answer, show_explanation


@app.cell(hide_code=True)
def _(check_answer, mo, show_explanation):
    mo.stop(not show_explanation.value)
    _correct = check_answer.value == "A A G G"
    mo.md(
        ("Yes. " if _correct else "Choose A A G G. ")
        + "Two taxa share A and two share G. That supports a split, "
        "but does not prove it: independent changes can create the same "
        "pattern. Constant and singleton sites still matter to other methods."
    ).callout(kind="success" if _correct else "info", title="Explanation")
    return


@app.cell(hide_code=True)
def _(mo):
    reflection_input = mo.ui.text_area(
        label="One sentence for a colleague", rows=2,
        placeholder="Why is the estimated tree a hypothesis rather than an observation?",
    )
    mo.vstack([
        mo.md(
            "## 5. Take it further\nSelect Explore. Shorten the sequence again "
            "and inspect the supporting-site counts. Then change the seed. "
            "Does the same length always recover the same groupings?"
        ),
        mo.md("## 6. Put it into words"), reflection_input,
        mo.accordion({
            "One possible explanation": mo.md(
                "The sequences are the endpoint data. The tree is our estimate "
                "from those patterns, using a chosen distance and method. More "
                "signal can help, but it cannot repair every wrong assumption."
            ),
            "Where the model stops": mo.md(
                "UPGMA imposes a clock-like structure; the randomly generated "
                "tree need not satisfy that assumption. Root hiding changes "
                "labels only. Supporting-site counts are not bootstrap support. "
                "The positions are already aligned in this substitution-only "
                "simulation; real alignments can be uncertain. Even a heterogeneity "
                "setting of zero retains some gamma-distributed rate variation."
            ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
