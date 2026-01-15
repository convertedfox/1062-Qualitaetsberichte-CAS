from __future__ import annotations

import streamlit as st

from import_parser import StudyProgramRow, load_latest_import_table


def main() -> None:
    st.set_page_config(
        page_title="Qualitaetsberichte Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.title("Qualitaetsberichte Dashboard")

    data = load_latest_import_table()
    if not data:
        st.warning("Keine Studiengaenge im Import gefunden.")
        return

    study_programs = sorted(row.studiengang for row in data)
    selected = st.sidebar.selectbox("Studiengang", study_programs)
    row = next(item for item in data if item.studiengang == selected)

    st.subheader(row.studiengang)
    st.caption(f"Fachbereich: {row.fachbereich}")

    _render_student_metrics(row)
    _render_profile_sections(row)


def _render_student_metrics(row: StudyProgramRow) -> None:
    st.markdown("### Studierendenzahlen")
    cols = st.columns(2)

    with cols[0]:
        st.markdown("**Studienanfaenger (letzte 4 Jahre)**")
        _render_year_series(row.studienanfaenger)

    with cols[1]:
        st.markdown("**Immatrikulierte Studierende (letzte 4 Jahre)**")
        _render_year_series(row.immatrikulierte)

    metrics = st.columns(4)
    metrics[0].metric("Erfolgsquote", _format_percent(row.erfolgsquote))
    metrics[1].metric("Fachsemester", _format_number(row.fachsemester))
    metrics[2].metric("Berufserfahrung", _format_number(row.berufserfahrung))
    metrics[3].metric("Alter", _format_number(row.alter))

    st.markdown("### Module")
    module_cols = st.columns(2)
    module_cols[0].metric("Durchschnittliche Modulauslastung", _format_number(row.modulauslastung))
    module_cols[1].metric("Anzahl Module", _format_number(row.anzahl_module))


def _render_profile_sections(row: StudyProgramRow) -> None:
    st.markdown("### Profile")
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Vorstudium der Studienanfaenger**")
        _render_profile_table(row.vorstudium_profil)

        st.markdown("**Dozentenherkunft (Lehrveranstaltungsstunden)**")
        _render_profile_table(row.dozenten_herkunft_profil)

    with col_right:
        st.markdown("**Modulbelegung nach Studiengaengen**")
        _render_profile_table(row.module_belegung_nach_sg)

        st.markdown("**Herkunft der Modulteilnehmer**")
        _render_profile_table(row.modulteilnehmer_herkunft)


def _render_year_series(values: dict[str, int | None]) -> None:
    labels = ["-4", "-3", "-2", "-1"]
    series = [values.get(label) for label in labels]
    st.bar_chart(series)
    st.caption(" / ".join(f"{label}: {_format_number(values.get(label))}" for label in labels))


def _render_profile_table(profile: dict[str, float | None]) -> None:
    if not profile:
        st.caption("Keine Daten vorhanden.")
        return
    rows = [{"Kategorie": key, "Wert": _format_number(value)} for key, value in profile.items()]
    st.dataframe(rows, hide_index=True, use_container_width=True)


def _format_number(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _format_percent(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


if __name__ == "__main__":
    main()
