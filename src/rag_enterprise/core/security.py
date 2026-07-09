from dataclasses import dataclass

from rag_enterprise.services.rbac import Principal


@dataclass(frozen=True)
class TokenClaims:
    sub: str
    roles: list[str]
    groups: list[str]


def claims_to_principal(claims: TokenClaims) -> Principal:
    return Principal(user_id=claims.sub, roles=claims.roles, groups=claims.groups)
