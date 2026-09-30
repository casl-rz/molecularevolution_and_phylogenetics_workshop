import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. Which gene would you investigate?

    Gene X affects a trait in Species A. Species B has related copies.
    Which would you test first, and what evidence is still missing?

    Allow **6 minutes** for the guided experiment, then discuss the decision.
    The species and functions here are hypothetical.
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import networkx as nx
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
    return mo, np, nx, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Follow each candidate back to its last common ancestor with Gene X.
        Was that a species split or a gene duplication? That distinction can
        change which copy we investigate first. It cannot establish function
        on its own.
        """
    ).callout(kind="info", title="What we're testing")
    return


@app.cell(hide_code=True)
def _(mo):
    prediction_input = mo.ui.text_area(
        placeholder="After an early duplication, are all cross-species pairs orthologs?",
        label="Your prediction", rows=2,
    )
    session_step = mo.ui.radio(
        ["Start", "Compare", "Explore"], value="Start",
        label="Session step", inline=True,
    )
    mo.vstack([
        mo.md("## 1. Predict\nCould the most similar copy be a different gene lineage?"),
        prediction_input,
        mo.md(
            "## 2. Try it\nCompare changes duplication events from 0 to 3. "
            "Keep the target on Species B and inspect the relationship matrix "
            "before reading the ranking. You can still move any slider. "
            "Switch to another step and back to reset."
        ),
        session_step,
    ])
    return (session_step,)


@app.cell(hide_code=True)
def _(mo, session_step):
    n_species_slider = mo.ui.slider(3, 10, value=4, step=1, label="Number of species")
    n_duplications_slider = mo.ui.slider(0, 5, value=3 if session_step.value == "Compare" else 0, step=1, label="Gene duplication events")
    functional_divergence_slider = mo.ui.slider(0.0, 1.0, value=0.70, step=0.05, label="Functional divergence after duplication")
    sequence_divergence_slider = mo.ui.slider(0.0, 1.0, value=0.40, step=0.05, label="Sequence divergence rate")
    highlight_species_dropdown = mo.ui.dropdown(
        options=["All species"] + [f"Species {chr(65 + i)}" for i in range(10)],
        value="Species B",
        label="Highlight species",
    )
    seed_slider = mo.ui.slider(1, 100, value=29, step=1, label="Random seed")

    mo.vstack(
        [
            mo.md("### Controls"),
            mo.hstack([n_species_slider, n_duplications_slider], justify="start", gap=3),
            mo.hstack([functional_divergence_slider, sequence_divergence_slider], justify="start", gap=3),
            mo.hstack([highlight_species_dropdown, seed_slider], justify="start", gap=3),
            mo.md(
                r"""
                *`Number of species` sets how many present-day species are in
                the simulated species tree; `gene duplication events` sets how
                many duplications occur somewhere in the gene family's
                history; `functional divergence` is the chance a duplicated
                copy's function drifts away from the original; `sequence
                divergence rate` scales how fast sequences accumulate
                differences over time; `highlight species` visually
                emphasizes one species in the diagrams below and focuses the
                candidate-gene panel on it; `random seed` fixes the randomness
                so a run can be reproduced. If your chosen species letter does
                not exist at the current number of species, all species are
                shown instead.*
                """
            ),
        ]
    )
    return (
        functional_divergence_slider,
        highlight_species_dropdown,
        n_duplications_slider,
        n_species_slider,
        seed_slider,
        sequence_divergence_slider,
    )


@app.cell(hide_code=True)
def _(
    functional_divergence_slider,
    n_duplications_slider,
    n_species_slider,
    np,
    seed_slider,
    sequence_divergence_slider,
):
    def simulate_gene_family(n_species, n_duplications, seq_div_rate, func_div_prob, rng):
        species_names = [chr(65 + i) for i in range(n_species)]
        spec_times = list(np.linspace(0.1, 0.7, max(n_species - 1, 1)))[: n_species - 1]
        dup_times = sorted(rng.uniform(0.05, 0.95, size=n_duplications).tolist())

        node_counter = [0]

        def new_node(parent, node_type, time):
            nid = node_counter[0]
            node_counter[0] += 1
            branch_len = 0.0
            cum_div = 0.0
            functionally_diverged = False
            if parent is not None:
                noise = rng.uniform(0.7, 1.3) if time > parent["time"] else 1.0
                branch_len = (time - parent["time"]) * seq_div_rate * noise
                cum_div = parent["cum_div"] + branch_len
                functionally_diverged = parent["functionally_diverged"]
            node = {
                "id": nid,
                "type": node_type,
                "time": time,
                "parent": parent,
                "children": [],
                "species": parent["species"] if parent is not None else None,
                "branch_len": branch_len,
                "cum_div": cum_div,
                "functionally_diverged": functionally_diverged,
            }
            if parent is not None:
                parent["children"].append(node)
            return node

        root = new_node(None, "root", 0.0)
        active = [root]

        events = [("speciation", t, None) for t in spec_times] + [("duplication", t, None) for t in dup_times]
        events.sort(key=lambda e: e[1])

        species_index = 0
        for ev_type, t, _ in events:
            if ev_type == "speciation":
                peeled_species = species_names[species_index]
                species_index += 1
                new_active = []
                for node in active:
                    if node["species"] is None:
                        event_node = new_node(node, "speciation", t)
                        tip = new_node(event_node, "lineage", t)
                        tip["species"] = peeled_species
                        cont = new_node(event_node, "lineage", t)
                        new_active.append(tip)
                        new_active.append(cont)
                    else:
                        new_active.append(node)
                active = new_active
            else:
                idx = int(rng.integers(len(active)))
                node = active[idx]
                event_node = new_node(node, "duplication", t)
                child1 = new_node(event_node, "lineage", t)
                child2 = new_node(event_node, "lineage", t)
                if rng.random() < func_div_prob:
                    (child1 if rng.random() < 0.5 else child2)["functionally_diverged"] = True
                active = [n for i2, n in enumerate(active) if i2 != idx] + [child1, child2]

        tips = []
        for node in active:
            if node["species"] is None:
                node["species"] = species_names[-1]
            tip = new_node(node, "tip", 1.0)
            tip["final_branch_len"] = tip["branch_len"]
            tip["cum_div_final"] = tip["cum_div"]
            tips.append(tip)

        return root, tips, species_names


    _rng = np.random.default_rng(seed_slider.value)
    gene_tree_root, gene_tips, species_names = simulate_gene_family(
        int(n_species_slider.value),
        int(n_duplications_slider.value),
        sequence_divergence_slider.value,
        functional_divergence_slider.value,
        _rng,
    )
    gene_labels = {}
    _species_counter = {}
    for _tip in gene_tips:
        _sp = _tip["species"]
        _species_counter[_sp] = _species_counter.get(_sp, 0) + 1
        gene_labels[_tip["id"]] = f"{_sp}_g{_species_counter[_sp]}"
    return gene_labels, gene_tips, gene_tree_root, species_names


@app.cell(hide_code=True)
def _(gene_tips, np, plt):
    def get_ancestors_chain(node):
        chain = []
        n = node
        while n is not None:
            chain.append(n)
            n = n["parent"]
        return chain


    def mrca(node_a, node_b):
        chain_b_ids = {id(n) for n in get_ancestors_chain(node_b)}
        for n in get_ancestors_chain(node_a):
            if id(n) in chain_b_ids:
                return n
        return None


    def relationship(node_a, node_b):
        if node_a is node_b:
            return "same gene"
        m = mrca(node_a, node_b)
        if m is None:
            return "unrelated"
        if m["type"] == "speciation":
            return "ortholog"
        if m["type"] == "duplication":
            return "paralog"
        return "unrelated"


    def oldest_duplication_group(node):
        """Color descendants by the copy inherited from the earliest duplication."""
        chain = get_ancestors_chain(node)
        copies = [child["id"] for child, parent in zip(chain, chain[1:])
                  if parent["type"] == "duplication"]
        if not copies:
            return "ND"
        return copies[-1]


    paralog_group = {tip["id"]: oldest_duplication_group(tip) for tip in gene_tips}
    _unique_groups = sorted(set(paralog_group.values()), key=lambda g: (g == "ND", g))
    _group_palette = plt.cm.Set2(np.linspace(0, 1, max(len(_unique_groups), 1)))
    group_color = {g: _group_palette[i] for i, g in enumerate(_unique_groups)}
    if "ND" in group_color:
        group_color["ND"] = np.array([0.55, 0.60, 0.58, 1.0])
    return group_color, mrca, paralog_group, relationship


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Read the result

    Trace a pair to its last shared node. A species split makes that pair
    orthologous; a duplication makes it paralogous. Then compare the candidate
    panel's relationship, similarity and toy confidence tier.

    **Simulated:** events, branch distances and function-change flags.
    **Observed:** the displayed endpoint copies; no empirical sequence is measured.
    **Inferred:** a candidate priority. **Assumed:** a rule that uses relationship,
    a distance-based similarity proxy and simulated function-change flags.

    ### Gene-family tree
    """)
    return


@app.cell(hide_code=True)
def _(
    gene_labels,
    gene_tips,
    gene_tree_root,
    group_color,
    highlight_species_dropdown,
    nx,
    paralog_group,
    plt,
    species_names,
):
    def _all_nodes(root):
        nodes = [root]
        for child in root["children"]:
            nodes.extend(_all_nodes(child))
        return nodes


    _nodes = _all_nodes(gene_tree_root)

    _G = nx.DiGraph()
    for _n in _nodes:
        _G.add_node(_n["id"])
        if _n["parent"] is not None:
            _G.add_edge(_n["parent"]["id"], _n["id"])


    def _layout(root, y_counter=None, positions=None):
        if y_counter is None:
            y_counter = [0]
        if positions is None:
            positions = {}
        if root["children"]:
            child_ys = []
            for child in root["children"]:
                _layout(child, y_counter, positions)
                child_ys.append(positions[child["id"]][1])
            y = sum(child_ys) / len(child_ys)
        else:
            y = y_counter[0]
            y_counter[0] += 1
        positions[root["id"]] = (root["time"], y)
        return positions


    _pos = _layout(gene_tree_root)

    _target_species = None
    if highlight_species_dropdown.value != "All species":
        _candidate = highlight_species_dropdown.value.split()[-1]
        if _candidate in species_names:
            _target_species = _candidate

    _id_to_node = {n["id"]: n for n in _nodes}

    _fig, _ax = plt.subplots(figsize=(9, 0.55 * len(gene_tips) + 1.5))
    nx.draw_networkx_edges(_G, _pos, ax=_ax, edge_color="#546e7a", width=1.5, arrows=False)

    _tip_ids = [t["id"] for t in gene_tips]
    _tip_colors = [group_color[paralog_group[i]] for i in _tip_ids]
    nx.draw_networkx_nodes(_G, _pos, nodelist=_tip_ids, node_color=_tip_colors, node_size=220, ax=_ax, edgecolors="#33402f", linewidths=1)

    _dup_ids = [n["id"] for n in _nodes if n["type"] == "duplication"]
    _spec_ids = [n["id"] for n in _nodes if n["type"] == "speciation"]
    nx.draw_networkx_nodes(_G, _pos, nodelist=_dup_ids, node_color="#e65100", node_shape="s", node_size=140, ax=_ax)
    nx.draw_networkx_nodes(_G, _pos, nodelist=_spec_ids, node_color="#1565c0", node_shape="o", node_size=100, ax=_ax)

    for _tid in _tip_ids:
        _x, _y = _pos[_tid]
        _node = _id_to_node[_tid]
        _weight = "bold" if (_target_species is not None and _node["species"] == _target_species) else "normal"
        _ax.text(_x + 0.02, _y, gene_labels[_tid], va="center", fontsize=10, fontweight=_weight)

    _ax.set_xlabel("Time (root = 0, present day = 1)")
    _ax.set_yticks([])
    _ax.set_xlim(-0.05, 1.35)
    for _spine in ["top", "right", "left"]:
        _ax.spines[_spine].set_visible(False)
    _ax.set_title("Gene family tree: blue circle = speciation, orange square = duplication", fontsize=11, color="#2e5a27")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Colors track the two copy lineages from the earliest duplication.
    Later duplications can create paralogs within one color, so color alone
    does not classify a pair. Use the last shared event and the OR/PA matrix.
    Grey means the lineage has no duplication ancestor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Event timeline
    """)
    return


@app.cell(hide_code=True)
def _(gene_tips, gene_tree_root, plt):
    def _collect_nodes(root):
        nodes = [root]
        for child in root["children"]:
            nodes.extend(_collect_nodes(child))
        return nodes


    _events_sorted = sorted(
        [n for n in _collect_nodes(gene_tree_root) if n["type"] in ("speciation", "duplication")],
        key=lambda n: n["time"],
    )

    _fig, _ax = plt.subplots(figsize=(9, 2.2))
    _ax.axhline(0, color="#546e7a", linewidth=1.5, zorder=1)
    _ax.scatter([0], [0], color="#1b5e20", s=140, zorder=5)
    _ax.text(0, 0.15, "Ancestral gene", ha="center", fontsize=9, color="#1b5e20")

    for _n in _events_sorted:
        if _n["type"] == "duplication":
            _ax.scatter([_n["time"]], [0], color="#e65100", marker="s", s=120, zorder=5)
            _ax.text(_n["time"], 0.15, "Duplication", ha="center", fontsize=9, color="#e65100", rotation=0)
        else:
            _ax.scatter([_n["time"]], [0], color="#1565c0", marker="o", s=100, zorder=5)
            _ax.text(_n["time"], -0.22, "Speciation", ha="center", fontsize=9, color="#1565c0")

    _ax.scatter([1.0] * len(gene_tips), [0] * len(gene_tips), color="#2e7d32", s=60, zorder=5)
    _ax.text(1.0, 0.15, f"{len(gene_tips)} descendant genes (present day)", ha="center", fontsize=9, color="#2e7d32")

    _ax.set_xlim(-0.1, 1.15)
    _ax.set_ylim(-0.5, 0.5)
    _ax.axis("off")
    _ax.set_title("Ancestor -> duplication / speciation events -> descendant genes", fontsize=11, color="#2e5a27")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Reading left to right: the single ancestral gene experiences
    duplication and speciation events in the order they occurred, ending
    in the full set of present-day gene copies shown in the tree above.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Relationships between endpoint copies
    """)
    return


@app.cell(hide_code=True)
def _(gene_labels, gene_tips, np, plt, relationship):
    _tip_labels_ordered = [gene_labels[t["id"]] for t in gene_tips]
    _n_tips = len(gene_tips)
    _rel_matrix = np.empty((_n_tips, _n_tips), dtype=object)
    _rel_code = {"same gene": 0, "ortholog": 1, "paralog": 2, "unrelated": 3}
    _rel_num = np.zeros((_n_tips, _n_tips))

    for _i in range(_n_tips):
        for _j in range(_n_tips):
            _r = relationship(gene_tips[_i], gene_tips[_j])
            _rel_matrix[_i, _j] = _r
            _rel_num[_i, _j] = _rel_code[_r]

    _cmap = plt.cm.colors.ListedColormap(["#cfd8dc", "#a5d6a7", "#ffab91", "#eeeeee"])
    _fig, _ax = plt.subplots(figsize=(0.55 * _n_tips + 2, 0.55 * _n_tips + 2))
    _ax.imshow(_rel_num, cmap=_cmap, vmin=0, vmax=3)
    _ax.set_xticks(range(_n_tips))
    _ax.set_yticks(range(_n_tips))
    _ax.set_xticklabels(_tip_labels_ordered, rotation=45, ha="right")
    _ax.set_yticklabels(_tip_labels_ordered)
    for _i in range(_n_tips):
        for _j in range(_n_tips):
            _label = {"same gene": "-", "ortholog": "OR", "paralog": "PA", "unrelated": "?"}[_rel_matrix[_i, _j]]
            _ax.text(_j, _i, _label, ha="center", va="center", fontsize=8, color="#222")
    _ax.set_title("OR = ortholog, PA = paralog", fontsize=11, color="#2e5a27")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Every pair of present-day gene copies is classified by what kind of
    event their most recent common ancestor represents: a speciation
    (ortholog) or a duplication (paralog). Note that two genes in the
    **same** species can be paralogs of each other if that species
    retained more than one copy from a duplication.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Make a candidate choice

    Suppose Gene X affects Trait Y in Species A. Which copy in the target
    species would you investigate first? A relationship supports a hypothesis;
    it does not establish the trait effect.
    """)
    return


@app.cell(hide_code=True)
def _(
    gene_labels,
    gene_tips,
    highlight_species_dropdown,
    mrca,
    np,
    relationship,
    species_names,
):
    gene_x = min([t for t in gene_tips if t["species"] == species_names[0]], key=lambda t: t["id"])

    _target_species_panel = None
    if highlight_species_dropdown.value != "All species":
        _cand = highlight_species_dropdown.value.split()[-1]
        if _cand in species_names:
            _target_species_panel = _cand

    _candidate_rows = []
    for _tip in gene_tips:
        if _tip is gene_x:
            continue
        if _target_species_panel is not None and _tip["species"] != _target_species_panel:
            continue
        _rel = relationship(gene_x, _tip)
        _m = mrca(gene_x, _tip)
        _patristic = (gene_x["cum_div_final"] - _m["cum_div"]) + (_tip["cum_div_final"] - _m["cum_div"])
        _similarity = float(np.exp(-_patristic))
        _diverged = _tip["functionally_diverged"] or gene_x["functionally_diverged"]
        _time_since_split = 1.0 - _m["time"]

        if _rel == "ortholog" and not _diverged and _similarity > 0.6:
            _confidence = "High"
        elif _rel == "ortholog":
            _confidence = "Medium"
        elif _rel == "paralog" and not _diverged and _time_since_split < 0.3 and _similarity > 0.6:
            _confidence = "Medium"
        else:
            _confidence = "Low"

        _candidate_rows.append(
            {
                "Candidate gene": gene_labels[_tip["id"]],
                "Species": _tip["species"],
                "Relationship to Gene X": _rel,
                "Sequence similarity": round(_similarity, 3),
                "Functionally diverged?": "Yes" if _diverged else "No",
                "Confidence": _confidence,
            }
        )

    _confidence_order = {"High": 0, "Medium": 1, "Low": 2}
    _candidate_rows.sort(key=lambda r: (_confidence_order[r["Confidence"]], -r["Sequence similarity"]))
    candidate_rows = _candidate_rows
    return candidate_rows, gene_x


@app.cell(hide_code=True)
def _(candidate_rows, gene_labels, gene_x, mo, species_names):
    mo.vstack(
        [
            mo.md(
                f"""### Candidate-gene panel

                Reference gene: **{gene_labels[gene_x["id"]]}** in Species {species_names[0]}
                (this is our "Gene X").
                """
            ),
            mo.ui.table(data=candidate_rows, selection=None, pagination=False, show_download=False),
            mo.md(
                "The panel sorts by toy confidence tier, then similarity. "
                "Similarity is exp(-simulated path distance), not measured "
                "percent identity. The function-change flags are known only "
                "because we simulated them; High/Medium/Low are not probabilities."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(gene_tips, gene_tree_root, mo, n_duplications_slider, species_names):
    def _collect_all_nodes(root):
        nodes = [root]
        for child in root["children"]:
            nodes.extend(_collect_all_nodes(child))
        return nodes


    _n_dup_total = int(n_duplications_slider.value)
    _gene_x_species_tips = [t for t in gene_tips if t["species"] == species_names[0]]
    _n_paralogs_in_species_a = len(_gene_x_species_tips) - 1

    if _n_dup_total == 0:
        _case = "Case 1: No Duplication"
        _kind = "success"
        _explain = (
            "There has been no gene duplication in this family's history: every "
            "species has exactly one copy of this gene, and every present-day "
            "gene is an ortholog of every other. There is no copy-selection "
            "ambiguity, but conserved function still needs evidence."
        )
    elif _n_paralogs_in_species_a >= 2:
        _case = "Case 4: Many Paralogs"
        _kind = "danger"
        _explain = (
            f"Species {species_names[0]} itself carries {_n_paralogs_in_species_a + 1} "
            "copies of this gene family. With this many paralogs to choose "
            "from, it is genuinely ambiguous which one best represents "
            "\"the\" gene of interest, and candidate selection in other "
            "species inherits that ambiguity."
        )
    else:
        _dup_times = [
            n["time"] for n in _collect_all_nodes(gene_tree_root)
            if n["type"] == "duplication"
        ]
        _most_recent_dup_time = max(
            _dup_times,
            default=None,
        )
        if min(_dup_times) <= 0.6 < _most_recent_dup_time:
            _case = "Older and newer duplications"
            _kind = "warn"
            _explain = (
                "This family has duplications on both sides of the toy age "
                "cutoff. Trace the specific pair: the newest event alone "
                "cannot describe every candidate's history."
            )
        elif _most_recent_dup_time is not None and _most_recent_dup_time > 0.6:
            _case = "Case 2: Recent Duplication"
            _kind = "warn"
            _explain = (
                "The duplication in this family happened relatively recently. "
                "The resulting copies have not had much time to diverge, so "
                "they may still perform overlapping functions (or one copy may "
                "be starting to specialize — subfunctionalization). Treat "
                "paralogs from a recent duplication with some caution, but they "
                "are not automatically unsafe."
            )
        else:
            _case = "Case 3: Ancient Duplication"
            _kind = "danger"
            _explain = (
                "The duplication in this family happened long ago. Paralogous "
                "copies have had a great deal of time to accumulate independent "
                "functional changes (neofunctionalization or subfunctionalization). "
                "A paralog here — even one with high sequence similarity — carries "
                "real risk of having a different function than Gene X."
            )

    mo.md(
        f"""
        **{_case}.** {_explain}
        """
    ).callout(kind=_kind, title=f"Interpretation: {_case}")
    return


@app.cell(hide_code=True)
def _(mo):
    check_answer = mo.ui.radio(
        ["Every cross-species pair is an ortholog", "Pairs within a copy lineage can be orthologs; pairs across the duplication are paralogs", "Every pair must have the same function"],
        label="A duplication occurs before a species split. Which statement fits?",
    )
    show_explanation = mo.ui.checkbox(label="Show the explanation")
    mo.vstack([mo.md("## 4. Check your reasoning"), check_answer, show_explanation])
    return check_answer, show_explanation


@app.cell(hide_code=True)
def _(check_answer, mo, show_explanation):
    mo.stop(not show_explanation.value)
    _correct = check_answer.value == "Pairs within a copy lineage can be orthologs; pairs across the duplication are paralogs"
    mo.md(
        ("Yes. " if _correct else "Trace each pair's last common ancestor. ")
        + "Species membership is not enough: cross-species pairs can be "
        "paralogs. A later duplication can also leave several target copies "
        "orthologous to the same reference gene."
    ).callout(kind="success" if _correct else "info", title="Explanation")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 5. Take it further

        Select Explore; these challenges are optional.

        **Duplication before speciation.** Set duplication
        events to 1 and try different random seeds until every species has
        two copies of the gene (look at the gene family tree: the duplication
        node, marked with an orange square, should sit to the *left* of every
        speciation node). What does the ortholog/paralog matrix look like in
        this case?

        **Duplication after speciation.** Now find a seed where
        only *one* species ends up with two gene copies, and every other
        species has just one. Where does the duplication node sit relative to
        the speciation nodes this time?

        **When the closest sequence is not the safest
        candidate.** Increase functional divergence and try to find a
        candidate gene with high sequence similarity to Gene X but **Low**
        confidence in the candidate-gene panel (an ancient or functionally
        diverged paralog). Why is sequence similarity alone not enough here?

        **Find all orthologs of a gene.** Use the "highlight
        species" control and the ortholog/paralog matrix to identify every
        gene that is an ortholog (not a paralog) of Gene X. How many did you
        find, and in which species?
        """
    ).callout(kind="info", title="Challenges")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Exercise:** You discovered a disease-resistance gene in **Tomato**.
        Can the same gene function be safely assigned to **Potato**,
        **Pepper**, and **Soybean**?

        Work through it in order:

        1. Is there a single, unambiguous ortholog in each species, or several
           paralogs to choose among?
        2. For each candidate, has any duplication occurred since it diverged
           from the tomato gene — and if so, how long ago?
        3. Does sequence similarity alone support your choice, or does the
           relationship (ortholog vs. paralog) change your confidence?
        4. What evidence would justify a ranking of these candidates?

        (Potato and Pepper are close relatives of Tomato in the same plant
        family; Soybean is a much more distant relative — use that general
        intuition alongside specific evolutionary evidence. Distance between
        species alone does not justify a candidate-confidence ranking.)
        """
    ).callout(kind="neutral", title="Knowledge-Transfer Exercise: Tomato Disease Resistance")
    return


@app.cell(hide_code=True)
def _(mo):
    reflection_input = mo.ui.text_area(
        label="One sentence for a colleague", rows=2,
        placeholder="I would test ___ first because ___; I still need evidence for ___.",
    )
    mo.vstack([
        mo.md("## 6. Put it into words"), reflection_input,
        mo.accordion({
            "One possible explanation": mo.md(
                "I would prioritize a supported ortholog, while checking "
                "additional copies and signs of divergence. I still need "
                "expression, domain, genomic-context and functional evidence "
                "before assigning the trait effect."
            ),
            "Where the model stops": mo.md(
                "Event labels and function-change flags are simulator truth. "
                "Real orthology inference needs a gene tree reconciled with "
                "a species tree, with uncertainty in alignments, models and "
                "sampling. Gene loss, incomplete lineage sorting and horizontal "
                "transfer are not simulated here. The tree has artificial "
                "normalized time, and the confidence cutoffs are teaching rules. "
                "A function-change flag on either path does not measure the "
                "functional difference between a pair of endpoint genes. "
                "Changing duplication count changes random-number consumption, "
                "so the same seed does not preserve every branch distance."
            ),
        }),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What would you do next?

    <div style="text-align:center; padding: 24px; background:#f4f9f4; border:2px solid #2e7d32; border-radius:12px;">
    <span style="font-size:20px; color:#1b5e20; font-weight:700;">
    Use the tree to choose<br>
    what to investigate next.
    </span>
    </div>
    """)
    return


if __name__ == "__main__":
    app.run()
