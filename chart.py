import altair as alt


def get_chart(data, plano):
    hover = alt.selection_single(
        fields=["Data"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=f'Evolução das cotas - {plano}')
        .mark_line()
        .encode(
            x="Data",
            y="cota",
            color="Perfil",
            strokeDash="Perfil",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Data",
            y="cota",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Data", title="Data"),
                alt.Tooltip("cota", title="cota"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()