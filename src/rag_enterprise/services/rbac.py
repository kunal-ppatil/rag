from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    user_id: str
    roles: list[str]
    groups: list[str]


def build_vector_filter(principal: Principal) -> dict[str, object]:
    return {"allowed_groups": {"$in": principal.groups}}
