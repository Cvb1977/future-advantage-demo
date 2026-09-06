# -*- coding: utf-8 -*-

def get_priority(match_week):
    """
    Prioritet:
    All = højest
    tal = numerisk værdi
    NA = lavest
    """

    value = str(match_week).strip()

    if value.lower() == "all":
        return 9999

    if value.lower() == "na":
        return -1

    try:
        return int(value)
    except ValueError:
        return -1


def select_best(rows):
    """
    Returnerer rækken med højeste prioritet.
    """

    if not rows:
        return None

    return max(
        rows,
        key=lambda row: get_priority(
            row.get("Match_Week", "NA")
        )
    )


def split_country_links(rows):

    highlights = []
    goals = []

    for row in rows:

        content = (
            row.get("Content", "")
               .lower()
               .replace(" ", "")
        )

        if content == "highlights":
            highlights.append(row)

        elif content == "goals":
            goals.append(row)

    best_highlight = select_best(highlights)
    best_goal = select_best(goals)

    used_links = set()

    if best_highlight:
        used_links.add(best_highlight["Link"])

    if best_goal:
        used_links.add(best_goal["Link"])

    other_links = []

    for row in rows:

        if row["Link"] in used_links:
            continue

        other_links.append(row)

    return (
        best_highlight,
        best_goal,
        other_links
    )