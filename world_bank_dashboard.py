# /// script
# requires-python = ">=3.15"
# dependencies = [
#     "marimo>=0.25.2",
# ]
# ///
import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    import pingouin as pg

    return alt, mo, pd, pg


@app.cell
def _(pd):
    base_url = "https://docs.google.com/spreadsheets/d/"
    doc_id = "1YY5iwL8J53umfHMNhJd1m-MbRPtRpX65oyxhq1KjzuI/"
    doc_format = "export?format=csv"

    url = base_url + doc_id + doc_format

    df_raw = pd.read_csv(url)
    return (df_raw,)


@app.cell
def _(df_raw):
    columns = df_raw.columns
    return


@app.cell
def _(mo):
    ###Entirly by AI
    mo.Html("""
    <div style="
        background-color: #D6EAF8;
        color: #183B56;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 12px;
    ">
        <h1 style="font-size: 23px; font-weight: bold; margin: 0 0 7px 0;">
            Group 9 — Digital Freedom and Democratic Accountability
        </h1>
        <p style="font-size: 13px; font-weight: bold; margin: 0;">
            Members: Sushanth Santosh Tambe · Vrundavati Patel · Shakti Murugan
        </p>
    </div>

    <div style="
        display: grid;
        grid-template-columns: 0.8fr 1.2fr;
        gap: 10px;
        color: #183B56;
    ">

        <div style="
            background: #EAF2F8;
            padding: 13px;
            border-radius: 10px;
        ">
            <h3 style="font-size: 16px; font-weight: bold; margin: 0 0 7px;">
                Why this claim?
            </h3>
            <p style="font-size: 13px; margin: 0;">
                We investigate whether freedom of expression and public
                participation are associated with stronger democratic accountability.
            </p>
        </div>

        <div style="
            background: #EAF2F8;
            padding: 13px;
            border-radius: 10px;
        ">
            <h3 style="font-size: 16px; font-weight: bold; margin: 0 0 7px;">
                Why these indicators?
            </h3>
            <p style="font-size: 13px; margin: 0;">
                Voice and Accountability represents citizens' ability to express
                opinions and participate in governance. Internet access, GDP per
                capita, Rule of Law and Control of Corruption provide complementary comparisons.
            </p>
        </div>

        <div style="
            background: #EAF2F8;
            padding: 13px;
            border-radius: 10px;
        ">
            <h3 style="font-size: 16px; font-weight: bold; margin: 0 0 7px;">
                Countries
            </h3>
            <p style="font-size: 13px; margin: 0;">
                Brazil, Germany, India, South Africa and South Korea.
            </p>
        </div>

        <div style="
            background: #EAF2F8;
            padding: 13px;
            border-radius: 10px;
        ">
            <h3 style="font-size: 16px; font-weight: bold; margin: 0 0 7px;">
                Period
            </h3>
            <p style="font-size: 13px; margin: 0;">
                2000–2020 (including both years).
            </p>
        </div>

    </div>
    """)
    return


@app.cell
def _(df_raw, pd):
    selected_countries = [
        "Brazil",
        "Germany",
        "India",
        "South Africa",
        "Korea, Rep.",
    ]

    main_indicator = "voice_and_accountability_estimate"

    comparison_indicator_options = {
        "Individuals using the internet (%)": "individuals_using_internet%",
        "GDP per capita (US$)": "gdp_per_capita",
        "Rule of law (estimate)": "rule_of_law_estimate",
        "Control of corruption (estimate)": "control_of_corruption_estimate",
    }

    required_raw_cols = [
        "country",
        "date",
        main_indicator,
        "individuals_using_internet%",
        "GDP_current_US",
        "population",
        "rule_of_law_estimate",
        "control_of_corruption_estimate",
    ]

    _df = df_raw.copy()
    _df["country"] = _df["country"].astype(str).str.strip()

    # Extract 4-digit year from strings like "1960-01-01" and filter to 2000-2020
    _df["year"] = pd.to_numeric(
        _df["date"].astype(str).str.extract(r"(\d{4})")[0],
        errors="coerce",
    )
    _df = _df[_df["year"].between(2000, 2020, inclusive="both")].copy()
    _df = _df[_df["country"].isin(selected_countries)].copy()

    # Strip thousands commas before converting numeric columns
    for _col in [
        main_indicator,
        "individuals_using_internet%",
        "GDP_current_US",
        "population",
        "rule_of_law_estimate",
        "control_of_corruption_estimate",
    ]:
        if _col in _df.columns:
            _cleaned_str = _df[_col].astype(str).str.replace(",", "", regex=False).str.strip()
            _df[_col] = pd.to_numeric(_cleaned_str, errors="coerce")

    # Calculate GDP per capita = GDP / population
    _df["gdp_per_capita"] = _df["GDP_current_US"] / _df["population"]

    # Clean country display labels (e.g., "Korea, Rep." -> "South Korea")
    _name_map = {"Korea, Rep.": "South Korea"}
    _df["country"] = _df["country"].replace(_name_map)

    keep_cols = [
        "country",
        "year",
        main_indicator,
        "individuals_using_internet%",
        "gdp_per_capita",
        "rule_of_law_estimate",
        "control_of_corruption_estimate",
    ]
    df_clean = (
        _df[[c for c in keep_cols if c in _df.columns]]
        .sort_values(["country", "year"])
        .reset_index(drop=True)
    )
    return comparison_indicator_options, df_clean, main_indicator


@app.cell
def _(comparison_indicator_options, mo):
    indicator_dropdown = mo.ui.dropdown(
        options=comparison_indicator_options,
        value="Individuals using the internet (%)",
        label="Compare with",
    )
    year_slider = mo.ui.range_slider(
        start=2000,
        stop=2020,
        step=1,
        value=[2000, 2020],
        label="Period",
    )
    indicatorUI = mo.hstack([indicator_dropdown, year_slider], justify="start", gap=2)
    return indicatorUI, indicator_dropdown, year_slider


@app.cell
def _(df_clean, indicator_dropdown, year_slider):
    _start_yr, _end_yr = year_slider.value
    _x_col = indicator_dropdown.value
    _x_label = next(
        (k for k, v in {
            "Individuals using the internet (%)": "individuals_using_internet%",
            "GDP per capita (US$)": "gdp_per_capita",
            "Rule of law (estimate)": "rule_of_law_estimate",
            "Control of corruption (estimate)": "control_of_corruption_estimate",
        }.items() if v == _x_col),
        _x_col,
    )

    df_filtered = df_clean[
        df_clean["year"].between(_start_yr, _end_yr, inclusive="both")
    ].copy()
    return (df_filtered,)


@app.cell
def _(
    alt,
    comparison_indicator_options,
    df_filtered,
    indicator_dropdown,
    main_indicator,
):
    _x_col = indicator_dropdown.value
    _x_label = next(
        (k for k, v in comparison_indicator_options.items() if v == _x_col),
        _x_col,
    )
    _y_label = "Voice and accountability (estimate)"

    _plot_df = df_filtered[["country", "year", _x_col, main_indicator]].dropna()

    _points = (
        alt.Chart(_plot_df)
        .mark_circle(size=65, opacity=0.85)
        .encode(
            x=alt.X(f"{_x_col}:Q", title=_x_label),
            y=alt.Y(f"{main_indicator}:Q", title=_y_label),
            color=alt.Color("country:N", title="Country"),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip(f"{_x_col}:Q", title=_x_label, format=",.2f"),
                alt.Tooltip(f"{main_indicator}:Q", title=_y_label, format=".2f"),
            ],
        )
    )

    _trend_lines = (
        alt.Chart(_plot_df)
        .transform_regression(
            _x_col,
            main_indicator,
            groupby=["country"],
        )
        .mark_line(size=2)
        .encode(
            x=alt.X(f"{_x_col}:Q"),
            y=alt.Y(f"{main_indicator}:Q"),
            color=alt.Color("country:N", title="Country"),
        )
    )

    scatter_chart = (
        (_points + _trend_lines)
        .properties(
            width=460,
            height=300,
            title=f"{_y_label} vs. {_x_label}",
        )
    )
    return (scatter_chart,)


@app.cell
def _(
    alt,
    comparison_indicator_options,
    df_filtered,
    indicator_dropdown,
    main_indicator,
    mo,
):
    ##Over Tab: Partiall from AI
    comparison_label = next(
        (label for label, column in comparison_indicator_options.items()
         if column == indicator_dropdown.value),
        indicator_dropdown.value
    )

    over_time_tab = mo.hstack([
        alt.Chart(df_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(
                f"{main_indicator}:Q",
                title="Voice and Accountability (estimate)"
            ),
            color=alt.Color("country:N", title="Country"),
            tooltip=["country:N", "year:O"]
        )
        .properties(
            width=460,
            height=220,
            title="Voice and Accountability over Time"
        ),

        alt.Chart(df_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(
                f"{indicator_dropdown.value}:Q",
                title=comparison_label
            ),
            color=alt.Color("country:N", title="Country"),
            tooltip=["country:N", "year:O"]
        )
        .properties(
            width=460,
            height=220,
            title=f"{comparison_label} over Time"
        )
    ], gap=2)
    return (over_time_tab,)


@app.cell
def _(alt, df_filtered, indicator_dropdown, main_indicator):
    #Distibution tab: Partially form AI:
    main_distribution_chart = (
        alt.Chart(df_filtered.dropna(subset=[main_indicator]))
        .mark_bar(opacity=0.7)
        .encode(
            x=alt.X(
                f"{main_indicator}:Q",
                bin=alt.Bin(maxbins=20),
                title="Voice and Accountability (estimate)"
            ),
            y=alt.Y("count():Q", title="Number of observations"),
            color=alt.Color("country:N", title="Country"),
            tooltip=[
                "country:N",
                alt.Tooltip("count():Q", title="Count")
            ]
        )
        .properties(
            width=460,
            height=220,
            title="Distribution of Voice and Accountability by Country"
        )
    )

    comparison_distribution_chart = (
        alt.Chart(
            df_filtered.dropna(subset=[indicator_dropdown.value])
        )
        .mark_bar(opacity=0.7)
        .encode(
            x=alt.X(
                f"{indicator_dropdown.value}:Q",
                bin=alt.Bin(maxbins=20),
                title=indicator_dropdown.selected_key
            ),
            y=alt.Y("count():Q", title="Number of observations"),
            color=alt.Color("country:N", title="Country"),
            tooltip=[
                "country:N",
                alt.Tooltip("count():Q", title="Count")
            ]
        )
        .properties(
            width=460,
            height=220,
            title=f"Distribution of {indicator_dropdown.selected_key} by Country"
        )
    )
    return comparison_distribution_chart, main_distribution_chart


@app.cell
def _(df_filtered, indicator_dropdown, main_indicator, pd, pg):
    #Correlation analysis by Shakti murugan

    comparison_col = indicator_dropdown.value

    correlation_rows = []

    for country in sorted(df_filtered["country"].dropna().unique()):

        country_df = df_filtered[
            df_filtered["country"] == country
        ][[comparison_col, main_indicator]].dropna()

        n = len(country_df)

        # Check sample size
        if n < 5:
            correlation_rows.append({
                "Country": country,
                "n": n,
                "r": None,
                "p-value": None,
                "95% CI": "Not available",
                "Strength": "Not calculated",
                "Status": "Insufficient data"
            })
            continue

        x = country_df[comparison_col]
        y = country_df[main_indicator]

        # Check for constant values
        if x.nunique() < 2 or y.nunique() < 2:
            correlation_rows.append({
                "Country": country,
                "n": n,
                "r": None,
                "p-value": None,
                "95% CI": "Not available",
                "Strength": "Not calculated",
                "Status": "Constant values"
            })
            continue

        # Calculate Spearman correlation
        result = pg.corr(
            x=x,
            y=y,
            method="spearman"
        )

        r = float(result.loc["spearman", "r"])
        p = float(result.loc["spearman", "p_val"])
        ci = result.loc["spearman", "CI95"]

        ci_text = (
            f"[{ci[0]:.2f}, {ci[1]:.2f}]"
            if ci is not None and len(ci) == 2
            else "Not available"
        )

        # Interpret correlation strength
        abs_r = abs(r)

        if abs_r < 0.1:
            strength = "Negligible"
        elif abs_r < 0.3:
            strength = "Small"
        elif abs_r < 0.5:
            strength = "Moderate"
        else:
            strength = "Large"

        correlation_rows.append({
            "Country": country,
            "n": n,
            "r": round(r, 3),
            "p-value": round(p, 4),
            "95% CI": ci_text,
            "Strength": strength,
            "Status": (
                "Significant"
                if p < 0.05
                else "Not significant"
            )
        })

    correlation_results = pd.DataFrame(correlation_rows)
    return (correlation_results,)


@app.cell
def _(correlation_results, mo):
    #Display the correlation table- by shakti murugan

    correlation_table = mo.vstack([
        mo.md("### Country-wise correlation results"),
        mo.md(
            "Method: **Spearman rank correlation** | "
            "Significance level: **5%**"
        ),
        correlation_results
    ])
    return (correlation_table,)


@app.cell
def _(mo):
    # Compact statistical method explanation

    correlation_method_explanation = mo.md(
        "**Method: Spearman rank correlation.** "
        "We use Spearman because it measures monotonic relationships "
        "without requiring a linear relationship and is less sensitive "
        "to extreme values than Pearson correlation."
    )
    return (correlation_method_explanation,)


@app.cell
def _(correlation_results, mo):
    #generating the final verdict- by shakti murugan

    valid_results = correlation_results[
        correlation_results["r"].notna()
        & correlation_results["p-value"].notna()
    ]

    total = len(valid_results)

    if total == 0:

        verdict_text = (
            "There is insufficient data to draw a conclusion "
            "for the selected indicator and period."
        )

    else:

        positive = (valid_results["r"] > 0).sum()
        negative = (valid_results["r"] < 0).sum()

        significant = (
            valid_results["p-value"] < 0.05
        ).sum()

        significant_positive = (
            (valid_results["r"] > 0)
            & (valid_results["p-value"] < 0.05)
        ).sum()

        significant_negative = (
            (valid_results["r"] < 0)
            & (valid_results["p-value"] < 0.05)
        ).sum()

        if significant_positive > total / 2:
            conclusion = "supports the expected positive association"

        elif significant_negative > total / 2:
            conclusion = "contradicts the expected positive association"

        else:
            conclusion = "provides mixed evidence"

        verdict_text = (
            f"For {positive} of {total} valid countries, "
            f"the relationship is positive, while {negative} "
            f"show a negative relationship. "
            f"{significant} of {total} countries have statistically "
            f"significant correlations at the 5% level, including "
            f"{significant_positive} significantly positive and "
            f"{significant_negative} significantly negative results. "
            f"Overall, the evidence {conclusion}. "
            f"However, shared trends over time and other factors "
            f"may explain these relationships; correlation does "
            f"not prove causation."
        )

    verdict = mo.callout(
        verdict_text,
        kind="info"
    )
    return (verdict,)


@app.cell
def _(mo):
    # Group Contributions tab

    contributions_tab = mo.md ("""
    # Group 9 — Contributions

    ### Sushanth Santosh Tambe
    - Performed data cleaning and preparation.
    - Created the Claim Check scatterplot.

    ### Vrundavati Patel
    - Created the Distribution charts and Over Time graphs.
    - Arranged and designed the dashboard layout, including the group title, claim rationale, indicator rationale, country selection, and “How to Use” section.

    ### Shakti Murugan
    - Conducted country-wise Spearman correlation analysis to evaluate relationships between the selected indicators.
    - Developed the correlation results table, including correlation coefficients, p-values, confidence intervals, and significance levels.
    - Performed advanced statistical analysis comparing long-term relationships with year-to-year changes.
    - Created comparative visualisations and statistical interpretations to identify differences in correlation patterns across countries.
    - Developed the overall statistical verdict and explained the choice of Spearman correlation.
    - Integrated the additional analysis into the interactive dashboard.

    """)
    return (contributions_tab,)


@app.cell
def _(
    advanced_analysis_tab,
    comparison_distribution_chart,
    contributions_tab,
    correlation_method_explanation,
    correlation_table,
    indicatorUI,
    main_distribution_chart,
    mo,
    over_time_tab,
    scatter_chart,
    verdict,
):
    # Dashboard integration — by Shakti Murugan

    # 1. Short usage instruction
    how_to_use = mo.md(
        "**How to use:** Select an indicator and adjust the "
        "period to explore relationships across countries."
    )

    # 2. Over Time instruction
    over_time_instruction = mo.md(
        "**How to read:** Track how both indicators change "
        "over time for each country."
    )

    # 3. Distribution instruction
    distribution_instruction = mo.md(
        "**How to read:** Compare the spread of indicator "
        "values across the five countries."
    )

    # 4. Expandable additional analysis
    additional_analysis = mo.accordion({

        "Additional Analysis: Long-term vs Annual Relationship":
            mo.vstack([

                advanced_analysis_tab,

                mo.md("""
                ### Interpretation

                - Long-term correlation measures the association
                  between the original indicator values.

                - Annual-change correlation measures the association
                  between changes in consecutive years.

                - Same direction means both correlations have
                  the same sign.

                - Opposite direction means their signs differ.

                Annual-change results should be interpreted
                cautiously because they contain fewer observations.
                """),

                correlation_method_explanation

            ], gap=2)

    })

    # 5. Main Claim Check tab
    claim_check_tab = mo.vstack([

        mo.hstack([
            scatter_chart,
            correlation_table
        ], gap=2),

        verdict,

        additional_analysis

    ], gap=2)

    # 6. Distribution tab
    distribution_view = mo.vstack([

        distribution_instruction,

        mo.hstack([
            main_distribution_chart,
            comparison_distribution_chart
        ], gap=2)

    ], gap=2)

    # 7. Over Time tab
    over_time_view = mo.vstack([

        over_time_instruction,

        over_time_tab

    ], gap=2)

    # 8. Main navigation tabs
    dashboard_tabs = mo.ui.tabs({

        "Claim Check": claim_check_tab,

        "Over Time": over_time_view,

        "Distributions": distribution_view,

        "Group Contributions": contributions_tab

    })

    # 9. Final dashboard
    final_dashboard = mo.vstack([

        how_to_use,

        indicatorUI,

        dashboard_tabs

    ], gap=2)

    final_dashboard
    return


@app.cell
def _(df_filtered, indicator_dropdown, main_indicator, pd, pg):
    _change_rows = []
    _comparison_col = indicator_dropdown.value

    # Analyse each country separately
    for _country in sorted(df_filtered["country"].dropna().unique()):

        # Select and sort the required data
        _country_data = (
            df_filtered[
                df_filtered["country"] == _country
            ][["year", _comparison_col, main_indicator]]
            .dropna()
            .sort_values("year")
            .copy()
        )

        # Calculate year-to-year changes
        _country_data["year_gap"] = (
            _country_data["year"].diff()
        )

        _country_data["x_change"] = (
            _country_data[_comparison_col].diff()
        )

        _country_data["y_change"] = (
            _country_data[main_indicator].diff()
        )

        # Keep only consecutive-year changes
        _change_data = _country_data.loc[
            _country_data["year_gap"] == 1,
            ["x_change", "y_change"]
        ].dropna()

        _n = len(_change_data)

        # Check minimum observations
        if _n < 5:
            _change_rows.append({
                "Country": _country,
                "Change n": _n,
                "Change r": None,
                "Change p": None,
                "Interpretation": "Insufficient data"
            })
            continue

        # Check for constant annual changes
        if (
            _change_data["x_change"].nunique() < 2
            or _change_data["y_change"].nunique() < 2
        ):
            _change_rows.append({
                "Country": _country,
                "Change n": _n,
                "Change r": None,
                "Change p": None,
                "Interpretation": "Constant changes"
            })
            continue

        # Calculate Spearman correlation
        _corr_result = pg.corr(
            x=_change_data["x_change"],
            y=_change_data["y_change"],
            method="spearman"
        )

        _r = float(_corr_result.loc["spearman", "r"])
        _p = float(_corr_result.loc["spearman", "p_val"])

        # Interpret direction and strength
        if abs(_r) < 0.1:
            _strength = "Negligible"
        elif abs(_r) < 0.3:
            _strength = "Small"
        elif abs(_r) < 0.5:
            _strength = "Moderate"
        else:
            _strength = "Large"

        if _r > 0:
            _direction = "Positive"
        elif _r < 0:
            _direction = "Negative"
        else:
            _direction = "No association"

        _significance = (
            "Significant" if _p < 0.05
            else "Not significant"
        )

        _change_rows.append({
            "Country": _country,
            "Change n": _n,
            "Change r": round(_r, 3),
            "Change p": round(_p, 4),
            "Interpretation": (
                f"{_strength} {_direction.lower()} "
                f"({ _significance.lower()})"
            )
        })

    # Final results table
    change_correlation_results = pd.DataFrame(_change_rows)
    return (change_correlation_results,)


@app.cell
def _(change_correlation_results, correlation_results, mo, pd):
    _comparison = correlation_results[
        ["Country", "n", "r", "p-value"]
    ].merge(
        change_correlation_results[
            ["Country", "Change n", "Change r", "Change p"]
        ],
        on="Country",
        how="left"
    )

    _comparison = _comparison.rename(columns={
        "r": "Long-term r",
        "p-value": "Long-term p",
        "Change r": "Annual change r",
        "Change p": "Annual change p"
    })

    _comparison["Relationship pattern"] = (
        _comparison.apply(
            lambda row:
                "Same direction"
                if pd.notna(row["Long-term r"])
                and pd.notna(row["Annual change r"])
                and row["Long-term r"] * row["Annual change r"] > 0
                else "Different direction"
                if pd.notna(row["Long-term r"])
                and pd.notna(row["Annual change r"])
                else "Insufficient data",
            axis=1
        )
    )

    _comparison_view = mo.vstack([
        mo.md("### Long-term vs year-to-year comparison"),
        mo.md(
            "Comparing the relationship between indicator levels "
            "with the relationship between consecutive annual changes."
        ),
        _comparison
    ])
    return


@app.cell
def _(alt, change_correlation_results, correlation_results, mo, pd):
    # 1. Combine long-term and annual-change results

    _comparison = correlation_results[
        ["Country", "n", "r", "p-value"]
    ].merge(
        change_correlation_results[
            ["Country", "Change n", "Change r", "Change p"]
        ],
        on="Country",
        how="left"
    )

    # 2. Compare relationship directions

    def _get_pattern(row):

        level = row["r"]
        annual = row["Change r"]

        if pd.isna(level) or pd.isna(annual):
            return "Insufficient data"

        if abs(level) < 0.1 or abs(annual) < 0.1:
            return "Near zero"

        return (
            "Same direction"
            if level * annual > 0
            else "Opposite direction"
        )

    _comparison["Pattern"] = _comparison.apply(
        _get_pattern,
        axis=1
    )

    # 3. Compact results table

    _display = _comparison[
        [
            "Country",
            "n",
            "r",
            "Change n",
            "Change r",
            "Change p",
            "Pattern"
        ]
    ].rename(columns={
        "n": "Level n",
        "r": "Level r",
        "Change n": "Annual n",
        "Change r": "Annual r",
        "Change p": "Annual p"
    }).copy()

    _display = _display.round({
        "Level r": 3,
        "Annual r": 3,
        "Annual p": 4
    })

    # 4. Prepare chart data

    _plot_data = _comparison.melt(
        id_vars=["Country"],
        value_vars=["r", "Change r"],
        var_name="Analysis",
        value_name="Correlation"
    ).dropna()

    _plot_data["Analysis"] = _plot_data["Analysis"].replace({
        "r": "Long-term",
        "Change r": "Year-to-year"
    })

    # 5. Grouped bar chart

    _bars = alt.Chart(_plot_data).mark_bar().encode(
        x=alt.X("Country:N", title="Country"),
        xOffset="Analysis:N",
        y=alt.Y(
            "Correlation:Q",
            title="Spearman correlation",
            scale=alt.Scale(domain=[-1, 1])
        ),
        color=alt.Color(
            "Analysis:N",
            title="Analysis"
        ),
        tooltip=[
            "Country:N",
            "Analysis:N",
            alt.Tooltip("Correlation:Q", format=".3f")
        ]
    )

    # 6. Zero-reference line

    _zero_data = pd.DataFrame({"zero": [0]})

    _zero_line = alt.Chart(_zero_data).mark_rule(
        color="black",
        strokeDash=[6, 4],
        strokeWidth=2
    ).encode(
        y=alt.Y(
            "zero:Q",
            scale=alt.Scale(domain=[-1, 1])
        )
    )

    _comparison_chart = alt.layer(
        _bars,
        _zero_line
    ).properties(
        width=500,
        height=240,
        title="Long-term vs Year-to-year Correlation"
    )

    # 7. Dynamic analytical insight

    _valid = _comparison.dropna(
        subset=["r", "Change r"]
    )

    _same = (
        _valid["r"] * _valid["Change r"] > 0
    ).sum()

    _opposite = (
        _valid["r"] * _valid["Change r"] < 0
    ).sum()

    _annual_significant = (
        _comparison["Change p"] < 0.05
    ).sum()

    _long_significant = (
        _comparison["p-value"] < 0.05
    ).sum()

    _count = len(_valid)

    if _count == 0:
        _insight = "Insufficient data for comparison."

    else:
        _insight = (
            f"{_same} of {_count} countries show the same "
            f"direction, while {_opposite} show opposite "
            f"directions. Statistically significant results: "
            f"{_long_significant} long-term and "
            f"{_annual_significant} year-to-year. "
            "Correlation does not establish causation."
        )

    # 8. Dynamic sample-size explanation

    _level_n = _comparison["n"].dropna()
    _annual_n = _comparison["Change n"].dropna()

    _level_range = (
        f"{int(_level_n.min())}–{int(_level_n.max())}"
        if len(_level_n) else "N/A"
    )

    _annual_range = (
        f"{int(_annual_n.min())}–{int(_annual_n.max())}"
        if len(_annual_n) else "N/A"
    )

    _sample_note = (
        f"Sample size: long-term n = {_level_range}; "
        f"year-to-year n = {_annual_range}. "
        "Annual changes require valid observations in "
        "two consecutive years."
    )
    # 9. Compact Advanced Analysis section

    advanced_analysis_tab = mo.vstack([

        mo.md(
            "**Additional analysis: Long-term vs annual relationship**"
        ),

        mo.vstack([
            _display,
            _comparison_chart
        ], gap=2),

        mo.callout(
            _insight,
            kind="info"
        ),

        mo.md(f"<small>{_sample_note}</small>")

    ], gap=2)
    return (advanced_analysis_tab,)


if __name__ == "__main__":
    app.run()
