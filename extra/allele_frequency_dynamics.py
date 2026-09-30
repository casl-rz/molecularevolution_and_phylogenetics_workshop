import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Allele Frequency Dynamics

    ### Mutation, Selection, Drift, and Migration in a Plant Population

    Imagine a wildflower population segregating for a flower-color gene:
    a "P" allele that produces purple pigment, and a "w" allele that does
    not (white flowers). The frequency of these two alleles in the
    population does not stay fixed — it is pushed around by four
    evolutionary forces at once: new mutations, natural selection (say,
    pollinators visiting purple flowers more often), random chance in who
    survives and reproduces (genetic drift), and seeds or pollen arriving
    from other populations (migration). This notebook lets you tune the
    strength of each force and watch how the allele frequency responds.
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
        ## Learning Objective

        By the end of this notebook, you should understand that:

        - Allele frequencies change over time under the combined influence of
          **mutation**, **natural selection**, **genetic drift**, and
          **migration**.
        - These forces can reinforce or oppose one another, and their relative
          strength depends on population size and the magnitude of selection.
        - In small populations, chance (drift) can overwhelm selection, so even
          a beneficial allele is not guaranteed to spread — and a single
          individual joining the population can shift its frequency
          noticeably.
        """
    ).callout(kind="info", title="Learning Objective")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Four Forces Acting on Allele Frequency

        **Mutation** — new "P" or "w" alleles arise by chance when DNA is
        copied. Mutation alone changes allele frequency very slowly, but it is
        the ultimate source of the variation the other three forces act on.

        **Natural selection** — if purple flowers attract more pollinators and
        set more seed, the "P" allele has a survival/reproduction advantage
        captured by a selection coefficient, *s*. Positive *s* favors "P";
        negative *s* favors "w".

        **Genetic drift** — each generation, only a finite number of
        individuals survive and reproduce. Which alleles get passed on is
        partly a matter of chance, especially in small populations. Drift can
        push an allele to fixation or loss even without any fitness
        difference.

        **Migration (gene flow)** — seeds or pollen arriving from a
        neighboring population, or a single plant transplanted in, carry
        alleles at a different frequency, pulling the local population's
        frequency toward the source population's.

        This notebook models a single two-allele locus in a population of
        diploid individuals, using a standard population-genetics simulation
        (a Wright-Fisher model) that applies all four forces each generation.
        """
    ).callout(kind="neutral", title="Mutation, Selection, Drift, and Migration")
    return


@app.cell(hide_code=True)
def _(mo):
    prediction_input = mo.ui.text_area(
        placeholder="Type your prediction here (optional)...",
        label="Your answer",
        rows=2,
    )

    mo.vstack(
        [
            mo.md(
                r"""
                ## Make a Prediction

                **If the purple allele gives a real reproductive advantage, but
                the population is very small, will natural selection reliably
                carry it to fixation?**

                Jot down a guess before you experiment with the sliders below.
                """
            ),
            prediction_input,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pop_size_slider = mo.ui.slider(
        5, 1000, value=100, step=5, label="Population size (diploid individuals)"
    )
    initial_freq_slider = mo.ui.slider(
        0.01, 0.99, value=0.50, step=0.01, label="Initial frequency of the purple (P) allele"
    )
    mutation_rate_slider = mo.ui.slider(
        0.0, 0.02, value=0.001, step=0.0005, label="Mutation rate (per generation, both directions)"
    )
    selection_coeff_slider = mo.ui.slider(
        -0.5, 0.5, value=0.05, step=0.01, label="Selection coefficient for P (s)"
    )
    migration_rate_slider = mo.ui.slider(
        0.0, 0.5, value=0.02, step=0.01, label="Migration rate (fraction of alleles from outside each generation)"
    )
    source_freq_slider = mo.ui.slider(
        0.0, 1.0, value=0.90, step=0.05, label="Allele frequency in the source (migrant) population"
    )
    n_generations_slider = mo.ui.slider(
        10, 500, value=150, step=10, label="Number of generations"
    )
    seed_slider = mo.ui.slider(
        1, 100, value=1, step=1, label="Random seed"
    )

    mo.vstack(
        [
            mo.md("## Interactive Controls"),
            mo.hstack([pop_size_slider, initial_freq_slider], justify="start", gap=3),
            mo.hstack([mutation_rate_slider, selection_coeff_slider], justify="start", gap=3),
            mo.hstack([migration_rate_slider, source_freq_slider], justify="start", gap=3),
            mo.hstack([n_generations_slider, seed_slider], justify="start", gap=3),
            mo.md(
                r"""
                *`Population size` sets how many individuals (and therefore how
                strong genetic drift is); `initial frequency` sets the starting
                share of the purple allele; `mutation rate` is the chance either
                allele mutates into the other each generation; `selection
                coefficient` is the reproductive advantage (positive) or
                disadvantage (negative) of the purple allele; `migration rate`
                is the fraction of the next generation's alleles that come from
                outside, at the `source population frequency`; `generations` is
                how long the simulation runs; `random seed` fixes the
                randomness so a run can be reproduced.*
                """
            ),
        ]
    )
    return (
        initial_freq_slider,
        migration_rate_slider,
        mutation_rate_slider,
        n_generations_slider,
        pop_size_slider,
        seed_slider,
        selection_coeff_slider,
        source_freq_slider,
    )


@app.cell(hide_code=True)
def _(
    initial_freq_slider,
    migration_rate_slider,
    mutation_rate_slider,
    n_generations_slider,
    np,
    pop_size_slider,
    seed_slider,
    selection_coeff_slider,
    source_freq_slider,
):
    n_replicates = 30
    N = int(pop_size_slider.value)
    p0 = initial_freq_slider.value
    mu = mutation_rate_slider.value
    s = selection_coeff_slider.value
    m = migration_rate_slider.value
    p_source = source_freq_slider.value
    n_gens = int(n_generations_slider.value)

    rng = np.random.default_rng(seed_slider.value)

    freq_history = np.empty((n_replicates, n_gens + 1))
    freq_history[:, 0] = p0
    p = np.full(n_replicates, p0)

    for _g in range(1, n_gens + 1):
        # natural selection (viability selection, P allele fitness 1+s vs w fitness 1)
        p_sel = (p * (1 + s)) / (p * (1 + s) + (1 - p))
        p_sel = np.clip(p_sel, 0.0, 1.0)
        # mutation (symmetric, both directions)
        p_mut = p_sel * (1 - mu) + (1 - p_sel) * mu
        # migration (gene flow from an external source population)
        p_mig = (1 - m) * p_mut + m * p_source
        p_mig = np.clip(p_mig, 0.0, 1.0)
        # genetic drift: finite-population sampling of the next generation
        counts = rng.binomial(2 * N, p_mig)
        p = counts / (2 * N)
        freq_history[:, _g] = p

    final_freqs = freq_history[:, -1]
    n_fixed = int((final_freqs >= 1.0).sum())
    n_lost = int((final_freqs <= 0.0).sum())
    n_segregating = n_replicates - n_fixed - n_lost
    return (
        N,
        final_freqs,
        freq_history,
        m,
        n_fixed,
        n_gens,
        n_lost,
        n_replicates,
        n_segregating,
        p0,
        p_source,
        s,
    )


@app.cell(hide_code=True)
def _(N, freq_history, n_gens, n_replicates, np, plt):
    _fig, _ax = plt.subplots(figsize=(6.2, 3.8))
    _generations = np.arange(n_gens + 1)

    for _i in range(n_replicates):
        _ax.plot(_generations, freq_history[_i], color="#2e7d32", alpha=0.18, linewidth=1)

    _ax.plot(_generations, freq_history.mean(axis=0), color="#1b5e20", linewidth=2.5, label="Mean across replicates")
    _ax.axhline(1.0, color="#8d6e63", linestyle=":", linewidth=1)
    _ax.axhline(0.0, color="#8d6e63", linestyle=":", linewidth=1)
    _ax.set_xlabel("Generation")
    _ax.set_ylabel("Frequency of the P (purple) allele")
    _ax.set_ylim(-0.03, 1.03)
    _ax.set_title(f"{n_replicates} replicate populations of size {N}", fontsize=12, color="#2e5a27")
    _ax.legend(loc="best", frameon=False, fontsize=9)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Each thin line is one independent replicate population evolving under
    the same rates. The bold line is the average trajectory. The spread
    between the thin lines is genetic drift at work — the smaller the
    population, the wider that spread will be.*
    """)
    return


@app.cell(hide_code=True)
def _(final_freqs, n_gens, np, plt):
    _fig, _ax = plt.subplots(figsize=(6.2, 3.4))
    _ax.hist(final_freqs, bins=np.linspace(0, 1, 21), color="#66bb6a", edgecolor="white")
    _ax.axvline(final_freqs.mean(), color="#1b5e20", linestyle="--", linewidth=2, label="Mean final frequency")
    _ax.set_xlabel("Final frequency of the P allele")
    _ax.set_ylabel("Number of replicate populations")
    _ax.set_title(f"Outcome after {n_gens} generations", fontsize=12, color="#2e5a27")
    _ax.legend(loc="upper center", frameon=False, fontsize=9)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo, n_fixed, n_gens, n_lost, n_replicates, n_segregating):
    mo.md(
        f"""
        *Of {n_replicates} replicate populations, **{n_fixed}** ended fixed for
        the P allele, **{n_lost}** ended with P lost entirely, and
        **{n_segregating}** were still segregating at generation {n_gens}. A
        tall single bar near 0 or 1 suggests one force (often drift or strong
        selection) dominated; a spread-out histogram suggests the forces are
        more evenly balanced.*
        """
    )
    return


@app.cell(hide_code=True)
def _(N, np, p0, plt):
    _N_range = np.unique(np.round(np.geomspace(5, 1000, 40)).astype(int))
    _p_before = p0
    # a single migrant individual is heterozygous (Pw), contributing one P and one w allele copy
    _delta_p = (( _p_before * 2 * _N_range + 1) / (2 * _N_range + 2)) - _p_before

    _fig, _ax = plt.subplots(figsize=(6.2, 3.6))
    _ax.plot(_N_range, _delta_p, color="#e65100", linewidth=2.5)
    _ax.scatter([N], [(( _p_before * 2 * N + 1) / (2 * N + 2)) - _p_before], color="#e65100", zorder=5, s=90)
    _ax.set_xscale("log")
    _ax.set_xlabel("Population size (individuals, log scale)")
    _ax.set_ylabel("Change in allele frequency from one migrant")
    _ax.set_title("A single individual matters more in small populations", fontsize=12, color="#2e5a27")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *This shows the immediate shift in allele frequency caused by a single
    heterozygous migrant individual joining a population of a given size
    (holding the starting frequency at the initial value above). The
    highlighted point is your current population size. In a population of
    10, one individual can shift the frequency by several percentage
    points; in a population of 1,000, the same individual barely registers
    — this is why drift (and the impact of any one individual) is strongest
    in small populations.*
    """)
    return


@app.cell(hide_code=True)
def _(
    N,
    final_freqs,
    mo,
    n_fixed,
    n_gens,
    n_lost,
    n_replicates,
    n_segregating,
    p0,
    s,
):
    _summary_rows = [
        {"Quantity": "Population size (N)", "Value": N},
        {"Quantity": "Generations simulated", "Value": n_gens},
        {"Quantity": "Replicate populations", "Value": n_replicates},
        {"Quantity": "Starting P-allele frequency", "Value": round(p0, 3)},
        {"Quantity": "Mean final P-allele frequency", "Value": round(float(final_freqs.mean()), 3)},
        {"Quantity": "Replicates fixed for P", "Value": n_fixed},
        {"Quantity": "Replicates with P lost", "Value": n_lost},
        {"Quantity": "Replicates still segregating", "Value": n_segregating},
        {"Quantity": "N x s (selection vs. drift scale)", "Value": round(N * s, 2)},
    ]

    mo.vstack(
        [
            mo.md("## Summary Table"),
            mo.ui.table(data=_summary_rows, selection=None, pagination=False, show_download=False),
        ]
    )
    return


@app.cell(hide_code=True)
def _(N, final_freqs, m, mo, n_replicates, p_source, s):
    _Ns = N * s

    if abs(_Ns) > 4:
        _level = "Selection-dominated"
        _kind = "success" if s > 0 else "danger"
        _explain = (
            "The population is large enough, and/or selection strong enough, "
            "that selection reliably overpowers drift: the P allele should "
            "trend toward fixation if s is positive, or toward loss if s is "
            "negative, fairly consistently across replicates."
        )
    elif m > 0.1 and abs(p_source - float(final_freqs.mean())) < 0.3:
        _level = "Migration-dominated"
        _kind = "info"
        _explain = (
            "Gene flow from the source population is strong enough to pull "
            "the local allele frequency toward the source frequency, largely "
            "overriding local selection and drift."
        )
    else:
        _level = "Drift-dominated"
        _kind = "warn"
        _explain = (
            "With this population size and selection strength, N x s is small: "
            "genetic drift is strong enough to move the allele frequency around "
            "unpredictably, even against the direction selection favors. "
            "Outcomes vary a lot from one replicate population to the next."
        )

    mo.md(
        f"""
        **{_level}** — N x s = {_Ns:.2f}. Across {n_replicates} replicates,
        outcomes ranged from {final_freqs.min():.2f} to {final_freqs.max():.2f}.

        {_explain}
        """
    ).callout(kind=_kind, title=f"Interpretation: {_level}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Try it:** Set a positive selection coefficient (say, s = 0.05) and
        compare a small population (N = 10) to a large one (N = 1000), keeping
        everything else the same. In how many replicates does the P allele
        actually reach fixation in each case? Then try increasing the migration
        rate with a source frequency far from your initial frequency — how
        quickly does the local population converge toward the source?
        """
    ).callout(kind="info", title="Challenge")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        This is a **simplified single-locus, two-allele model**, not a full
        population-genetics simulation. In particular:

        - Only one gene with two alleles is modeled — no linkage, epistasis, or
          polygenic traits.
        - Selection acts through a single fitness coefficient with no
          dominance, environment interaction, or frequency dependence.
        - Migration follows a simple one-way "island" model with a fixed
          source frequency, not a network of exchanging populations.
        - Generations are discrete and non-overlapping (a Wright-Fisher
          assumption), and population size is held constant over time.
        - Real plant populations also have seed banks, spatial structure, and
          variable mating systems (e.g., self-fertilization) that are not
          represented here.

        Real evolutionary genetics studies use more detailed models and
        empirical data to account for these factors.
        """
    ).callout(kind="warn", title="Limitations of This Model")
    return


if __name__ == "__main__":
    app.run()
