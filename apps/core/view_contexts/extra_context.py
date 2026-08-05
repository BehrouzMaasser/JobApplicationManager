from dataclasses import dataclass


@dataclass(frozen=True)
class ExtraContext:

    app_kind: str | None = None
    page_title: str | None = None
