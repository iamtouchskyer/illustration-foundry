"""Per-group flat icon geometry modules.

Each module exposes ``ICONS: dict[str, callable]`` mapping subject name
to a function ``(palette) -> list[El]``. The build script asserts this
package covers the clay catalog exactly (fail-closed parity).
"""

from __future__ import annotations

from . import (assessment, auth, billing, clubs, community, empty, error,
               gamification, learning, loading, notifications,
               onboarding, success, wellness)

GROUPS: dict[str, dict] = {
    "empty": empty.ICONS,
    "error": error.ICONS,
    "loading": loading.ICONS,
    "success": success.ICONS,
    "onboarding": onboarding.ICONS,
    "auth": auth.ICONS,
    "notifications": notifications.ICONS,
    "gamification": gamification.ICONS,
    "learning": learning.ICONS,
    "community": community.ICONS,
    "assessment": assessment.ICONS,
    "billing": billing.ICONS,
    "wellness": wellness.ICONS,
    "clubs": clubs.ICONS,
}
