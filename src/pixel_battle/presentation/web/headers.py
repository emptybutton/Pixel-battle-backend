from dataclasses import dataclass
from typing import Annotated, ClassVar, TypeAlias

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


@dataclass(kw_only=True, frozen=True, slots=True)
class AdminKeyHeader:
    _security: ClassVar[HTTPBearer] = HTTPBearer(
        scheme_name="Admin key header",
        description=(
            "Required for administering."
            " Cannot be obtained from the application itself directly."
        ),
        auto_error=False,
    )

    CredentialsOrNone: ClassVar[TypeAlias] = (
        Annotated[HTTPAuthorizationCredentials | None, Depends(_security)]
    )
