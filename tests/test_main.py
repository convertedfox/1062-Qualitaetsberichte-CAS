from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main
from import_parser import StudyProgramRow


def make_row(
    *,
    studiengang: str,
    fachbereich: str,
    studienanfaenger: dict[str, int | None] | None = None,
    immatrikulierte: dict[str, int | None] | None = None,
    vorstudium_profil: dict[str, float | None] | None = None,
    erfolgsquote: float | None = None,
    fachsemester: float | None = None,
    berufserfahrung: float | None = None,
    alter: float | None = None,
    dozenten_herkunft_profil: dict[str, float | None] | None = None,
    module_belegung_nach_sg: dict[str, float | None] | None = None,
    modulteilnehmer_herkunft: dict[str, float | None] | None = None,
    modulauslastung: float | None = None,
) -> StudyProgramRow:
    return StudyProgramRow(
        studiengang=studiengang,
        fachbereich=fachbereich,
        studienanfaenger=studienanfaenger or {"-4": None, "-3": None, "-2": None, "-1": None},
        immatrikulierte=immatrikulierte or {"-4": None, "-3": None, "-2": None, "-1": None},
        vorstudium_profil=vorstudium_profil or {},
        erfolgsquote=erfolgsquote,
        fachsemester=fachsemester,
        berufserfahrung=berufserfahrung,
        alter=alter,
        dozenten_herkunft_profil=dozenten_herkunft_profil or {},
        module_belegung_nach_sg=module_belegung_nach_sg or {},
        modulteilnehmer_herkunft=modulteilnehmer_herkunft or {},
        modulauslastung=modulauslastung,
    )


def test_normalize_selection_keeps_cas() -> None:
    result = main._normalize_selection(
        {"Technik": ["Informatik"]},
        {"Informatik": "Technik"},
        "cas",
        None,
    )

    assert result == ("cas", main.CAS_OVERVIEW_LABEL)


def test_normalize_selection_falls_back_to_cas_for_invalid_values() -> None:
    result = main._normalize_selection(
        {"Technik": ["Informatik"]},
        {"Informatik": "Technik"},
        "program",
        "Unbekannt",
    )

    assert result == ("cas", main.CAS_OVERVIEW_LABEL)


def test_sum_year_series_handles_missing_values() -> None:
    rows = [
        make_row(
            studiengang="A",
            fachbereich="Technik",
            studienanfaenger={"-4": 1, "-3": None, "-2": 3, "-1": 4},
        ),
        make_row(
            studiengang="B",
            fachbereich="Technik",
            studienanfaenger={"-4": 2, "-3": 5, "-2": None, "-1": None},
        ),
    ]

    result = main._sum_year_series(rows, "studienanfaenger")

    assert result == {"-4": 3, "-3": 5, "-2": 3, "-1": 4}


def test_average_metric_ignores_missing_values() -> None:
    rows = [
        make_row(studiengang="A", fachbereich="Technik", erfolgsquote=0.8),
        make_row(studiengang="B", fachbereich="Technik", erfolgsquote=None),
        make_row(studiengang="C", fachbereich="Technik", erfolgsquote=1.0),
    ]

    result = main._average_metric(rows, "erfolgsquote")

    assert result == 0.9


def test_aggregate_profiles_sums_categories() -> None:
    rows = [
        make_row(
            studiengang="A",
            fachbereich="Technik",
            vorstudium_profil={"DHBW": 2.0, "Uni": None},
        ),
        make_row(
            studiengang="B",
            fachbereich="Technik",
            vorstudium_profil={"DHBW": 1.0, "Uni": 4.0},
        ),
    ]

    result = main._aggregate_profiles(rows, "vorstudium_profil")

    assert result == {"DHBW": 3.0, "Uni": 4.0}


def test_render_selected_view_renders_cas_overview(monkeypatch) -> None:
    rows = [
        make_row(studiengang="Informatik", fachbereich="Technik"),
        make_row(studiengang="MBA", fachbereich="Wirtschaft"),
    ]
    calls: dict[str, tuple[object, ...]] = {}

    def capture_overview(
        overview_rows: list[StudyProgramRow],
        import_year: int | None,
        title: str,
        subtitle: str,
    ) -> None:
        calls["overview"] = (overview_rows, import_year, title, subtitle)

    monkeypatch.setattr(main, "_render_overview", capture_overview)
    main._render_selected_view(rows, "cas", main.CAS_OVERVIEW_LABEL, 2026)

    assert calls["overview"] == (
        rows,
        2026,
        "Gesamtübersicht DHBW CAS",
        main.CAS_OVERVIEW_LABEL,
    )
