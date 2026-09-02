#!/usr/bin/env python3
"""Generate the cross-project clay illustration library.

One locked structural recipe (r8-2-grounded-tray, measured from the
Reviso originals) + parametrized accent palettes. Every illustration is
generated ONCE on a seamless white background, then shipped as two
variants: `white` (original) and `transparent` (rembg cutout) — so the
style never diverges between variants.

Model/endpoint: wan2.7-image-pro via the DashScope async
`image-generation/generation` route with `input.messages`. Do NOT route
this model through the image-x skill's generate_image.py (it hits the
legacy text2image endpoint and fails with `InvalidParameter url error`).

Usage:
    python3 scripts/generate_clay_library.py --list
    python3 scripts/generate_clay_library.py --dry-run --group empty
    python3 scripts/generate_clay_library.py --group error --palette terracotta
    python3 scripts/generate_clay_library.py --subject empty/no-search-results --palette ocean
    python3 scripts/generate_clay_library.py --all --palette terracotta --skip-existing

Reads DASHSCOPE_API_KEY from the environment, falling back to
~/.claude/.env. Sequential on purpose — DashScope quota rate-limits
parallel submissions.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import sys
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "out" / "clay-png"
TMP_DIR = pathlib.Path(tempfile.gettempdir()) / "illustration-foundry"
BASE_API = "https://dashscope.aliyuncs.com/api/v1"
MODEL = "wan2.7-image-pro"
SHIP_SIZE = 512
SIZE_BUDGET = 300_000  # bytes per shipped PNG
DOWNSCALE_STEPS = (512, 448, 384)

# Locked structure (never parametrized) ----------------------------------

STRUCTURE = ("soft 3D matte clay render, cute isometric illustration, "
             "one centered composition, pure plain seamless white "
             "background, no gradient, no texture, matte clay material, "
             "smooth rounded shapes, no outlines, soft diffuse studio "
             "lighting, light from upper left, soft elliptical drop "
             "shadow under the subject, precise axonometric projection, "
             "crisp geometric construction, vector-like clarity")

TRAY = ("a large rounded square with medium rounded corners, moderate "
        "corner radius, in clean bright off-white #f9f9f9, clearly "
        "debossed into the white background like a shallow open tray "
        "with visible depth between the tray floor and the white "
        "surface, the subject clearly standing inside the tray resting "
        "directly on the recessed floor, one pronounced soft elliptical "
        "contact shadow cast by the subject onto the tray floor right "
        "beneath it, a strong grounded physical relationship between "
        "the subject on top and the tray below, only the top and left "
        "inner walls softly shadowed with no grey muddy tones, the "
        "panel centered and clearly larger than the subject, two-layer "
        "composition")

AVOID = ("background scene, room, desk, table surface, floor, props, "
         "pencil, bookshelf, text, letters, numbers, words, watermark, "
         "logo, human, person, hand, finger, photorealistic, photo, "
         "outline, sketch, line art, dark background, colored "
         "background, gradient background, busy background, upright "
         "standing panel, floating card held by hand, multiple objects "
         "crowd, muted colors, dull, desaturated, grey muddy recessed "
         "floor, any hue outside the stated palette")

# Parametrized palettes ---------------------------------------------------

PALETTES = {
    "terracotta": {
        "PRIMARY": "vivid orange #ff6b35",
        "HIGHLIGHT": "warm amber #ffa55c",
        "SECONDARY": "soft violet #a984ff",
        "TERTIARY": "pale lavender #e6e6f5",
    },
    "ocean": {
        "PRIMARY": "vivid azure #2f7cf6",
        "HIGHLIGHT": "sky cyan #6cc4f0",
        "SECONDARY": "warm coral #ff8f6b",
        "TERTIARY": "pale mist #e8f1fa",
    },
    "forest": {
        "PRIMARY": "leaf green #3ba55d",
        "HIGHLIGHT": "fresh mint #7fd8a4",
        "SECONDARY": "clay amber #e8a94f",
        "TERTIARY": "pale sage #eaf4ec",
    },
    "sunset": {
        "PRIMARY": "coral pink #f4647c",
        "HIGHLIGHT": "soft peach #ffb38a",
        "SECONDARY": "dusk violet #8d7bf0",
        "TERTIARY": "pale blush #fceef0",
    },
    "gold": {
        "PRIMARY": "marigold #f2a516",
        "HIGHLIGHT": "warm honey #ffd166",
        "SECONDARY": "slate teal #4f8a8b",
        "TERTIARY": "pale cream #fbf3e0",
    },
    "coffee": {
        "PRIMARY": "espresso #6f4e37",
        "HIGHLIGHT": "latte #c8a97e",
        "SECONDARY": "matcha #8fa37a",
        "TERTIARY": "pale cream #f5efe6",
    },
    "minecraft": {
        "PRIMARY": "grass green #5aab47",
        "HIGHLIGHT": "bright grass #8fd662",
        "SECONDARY": "diamond cyan #4ed3c8",
        "TERTIARY": "pale stone #eef0e8",
    },
    "blackpink": {
        "PRIMARY": "hot pink #ff4d8d",
        "HIGHLIGHT": "soft rose #ff9ec2",
        "SECONDARY": "soft graphite #55556b",
        "TERTIARY": "pale blush #fdeff5",
    },
}

# Subject library: group -> state -> template with palette slots ---------
# {PRIMARY} main subject color, {HIGHLIGHT} edge highlights,
# {SECONDARY} accent object, {TERTIARY} pale surfaces/paper.

SUBJECTS = {
    "empty": {
        "empty-list": "an open empty folder in {PRIMARY} with {HIGHLIGHT} edge highlights and its front flap lowered, a single blank white sheet of paper floating gently above it",
        "no-search-results": "a {PRIMARY} blank sheet of paper with {HIGHLIGHT} edge highlights, a large {SECONDARY} magnifying glass hovering over it, the round lens completely empty showing clean {TERTIARY} glass with nothing inside",
        "no-favorites": "a soft clay five-pointed star in {PRIMARY} with {HIGHLIGHT} highlights resting on a small neat stack of {TERTIARY} blank documents, one tiny {SECONDARY} sparkle floating nearby",
        "empty-recycle": "a rounded clay trash bin in {PRIMARY} with {HIGHLIGHT} highlights and its lid tilted half open, completely empty inside, one small crumpled white paper ball resting beside it",
        "empty-inbox": "an empty clay inbox tray in {PRIMARY} with {HIGHLIGHT} edge highlights, clean and bare, one small {SECONDARY} envelope hovering just above it about to arrive",
        "no-notifications": "a clay bell in {PRIMARY} with {HIGHLIGHT} highlights, clapper still, one small {SECONDARY} crescent moon resting beside it suggesting quiet",
        "no-team": "a clay shared folder in {PRIMARY} with a {HIGHLIGHT} tab, two small round people-avatar tokens in {SECONDARY} and {TERTIARY} leaning against it",
        "no-projects": "a closed clay briefcase in {PRIMARY} with {HIGHLIGHT} highlights, one blank {TERTIARY} tag on it, one tiny {SECONDARY} seedling sprout beside it suggesting nothing started yet",
        "no-history": "a clay clock in {PRIMARY} with {HIGHLIGHT} rim and a blank {TERTIARY} face, one {SECONDARY} page curling and drifting away from it",
        "no-uploads": "a clay cloud in {PRIMARY} with {HIGHLIGHT} highlights and an empty upward slot, one blank {TERTIARY} sheet of paper waiting below it",
        "empty-chat": "a large round clay speech bubble in {PRIMARY} with {HIGHLIGHT} highlights, completely empty with a clean {TERTIARY} interior, one small {SECONDARY} plus sign resting beside it",
        "no-bookmarks": "a {TERTIARY} blank page with a {PRIMARY} ribbon bookmark dangling loose off its edge, one tiny {SECONDARY} star beside it",
    },
    "error": {
        "not-found-404": "a {PRIMARY} sheet of paper with {HIGHLIGHT} edge highlights and a large round hole torn through its center, one small {SECONDARY} magnifying glass tilted beside it",
        "server-error-500": "a small stack of clay server blocks in {PRIMARY} with {HIGHLIGHT} indicator dots, the top block toppled sideways, one {SECONDARY} warning triangle chip resting beside it",
        "offline": "a clay cloud in {PRIMARY} with {HIGHLIGHT} highlights and three signal arcs above it, the largest arc broken into two separated pieces",
        "no-permission": "a chunky circular prohibition no-entry sign in {PRIMARY} with {HIGHLIGHT} highlights, a thick ring with a diagonal slash across it standing like a round clay badge, one small {SECONDARY} key lying beside it that clearly does not fit",
        "account-disabled": "a chunky round power-off button badge in {PRIMARY} shaped like the classic power symbol, a thick open ring with a short vertical bar at the top, resting at a slight tilt, one small {SECONDARY} crescent moon lying beside it",
        "session-expired": "a clay hourglass in {PRIMARY} with {HIGHLIGHT} frame and {TERTIARY} glass, all the sand run into the bottom bulb, one small {SECONDARY} clock chip beside it",
        "region-locked": "a clay globe in {PRIMARY} and {TERTIARY} with {HIGHLIGHT} highlights, a chunky {SECONDARY} padlock wrapped around its equator",
        "broken-link": "a chunky clay chain in {PRIMARY} with {HIGHLIGHT} highlights and one link broken open in the middle, one tiny torn {TERTIARY} paper scrap drifting away",
        "rate-limited": "a clay gauge dial in {PRIMARY} with {HIGHLIGHT} rim and a {TERTIARY} face, the needle pinned at the maximum mark, two small {SECONDARY} pause bars standing beside it",
        "maintenance": "a clay wrench crossed with a screwdriver in {PRIMARY} with {HIGHLIGHT} highlights over one {TERTIARY} gear, one small {SECONDARY} traffic cone beside them",
        "payment-failed": "a rounded clay credit card in {PRIMARY} with a {HIGHLIGHT} stripe, tipped over at an angle, one small {SECONDARY} cross-mark coin resting beside it",
        "timeout": "a clay clock in {PRIMARY} with {HIGHLIGHT} rim and {TERTIARY} face, its hands frozen still, one small {SECONDARY} hourglass tipped over beside it",
    },
    "loading": {
        "loading": "a chunky clay progress ring in {PRIMARY} with {HIGHLIGHT} highlights, three quarters complete with the last quarter an open gap, one small {SECONDARY} spark dot traveling along the ring",
        "processing": "two clay gears turning together in {PRIMARY} with {HIGHLIGHT} highlights, one {TERTIARY} document sheet entering from one side",
        "uploading": "a clay cloud in {PRIMARY} with {HIGHLIGHT} highlights, one {TERTIARY} sheet of paper lifted halfway up into it on a chunky {SECONDARY} upward arrow",
        "syncing": "two chunky curved clay arrows in {PRIMARY} chasing each other in a circle with {HIGHLIGHT} edge highlights, one small {SECONDARY} document resting inside the circle",
        "importing": "an open clay box in {PRIMARY} with {HIGHLIGHT} highlights, a neat stack of {TERTIARY} sheets sliding into it",
        "deploying": "a small clay rocket in {PRIMARY} with {HIGHLIGHT} fins sitting on a {TERTIARY} launch pad, one soft {SECONDARY} puff cloud at its base",
    },
    "success": {
        "done": "one big chunky clay checkmark standing upright in {PRIMARY} with {HIGHLIGHT} edge highlights, one tiny {SECONDARY} sparkle floating beside it",
        "saved": "a {PRIMARY} document sheet with {HIGHLIGHT} edge highlights, a chunky {SECONDARY} shield badge with a check resting on its lower corner",
        "published": "a clay paper plane in {PRIMARY} with {HIGHLIGHT} highlights just leaving the tray, one soft {SECONDARY} motion arc behind it",
        "milestone": "a clay flag in {PRIMARY} planted on a small {TERTIARY} hill, one tiny {SECONDARY} confetti dot floating above",
        "all-clear": "a chunky clay shield in {PRIMARY} with {HIGHLIGHT} highlights and a {SECONDARY} check on its face, two tiny sparkles beside it",
        "streak": "a clay flame in {PRIMARY} with {HIGHLIGHT} highlights rising from three small ascending {TERTIARY} steps",
    },
    "onboarding": {
        "welcome": "a clay arch doorway in {PRIMARY} with {HIGHLIGHT} highlights and an open {TERTIARY} doorway, a small {SECONDARY} welcome mat in front of it",
        "get-started": "a chunky clay signpost arrow in {PRIMARY} with {HIGHLIGHT} highlights pointing up and forward, standing on a small {TERTIARY} base",
        "setup": "one large clay gear in {PRIMARY} with {HIGHLIGHT} highlights, one {SECONDARY} slider knob on a {TERTIARY} track beside it",
        "tutorial": "an open clay book in {PRIMARY} cover with blank {TERTIARY} pages, one {SECONDARY} pointer arrow hovering above it",
        "invite-team": "a clay envelope in {PRIMARY} with {HIGHLIGHT} highlights, three small round people-avatar tokens in {SECONDARY} and {TERTIARY} popping out of it",
        "create-first": "a chunky clay plus-sign block in {PRIMARY} with {HIGHLIGHT} highlights standing on a small {TERTIARY} pedestal, one blank sheet waiting below",
    },
    "auth": {
        "sign-in": "a clay arch door in {PRIMARY} with {HIGHLIGHT} highlights and a {TERTIARY} keyhole plate, one {SECONDARY} key hovering toward the lock",
        "sign-up": "a clay identification badge in {PRIMARY} with {HIGHLIGHT} highlights and a blank {TERTIARY} face, one chunky {SECONDARY} plus sign beside it",
        "two-factor": "a chunky clay padlock in {PRIMARY} with {HIGHLIGHT} highlights, a {SECONDARY} shield standing behind it",
        "password-reset": "a clay key in {PRIMARY} with {HIGHLIGHT} highlights, one circular arrow in {SECONDARY} wrapping around the key head",
        "magic-link": "a clay envelope in {PRIMARY} with {HIGHLIGHT} highlights, one chunky {SECONDARY} chain-link charm hanging from it and one tiny sparkle",
    },
    "notifications": {
        "new-message": "a clay envelope in {PRIMARY} with {HIGHLIGHT} highlights, slightly open, one chunky {SECONDARY} notification dot badge on its corner",
        "alert-warning": "a chunky clay warning triangle in {PRIMARY} with {HIGHLIGHT} edge highlights, one small {SECONDARY} lightning bolt beside it",
        "reminder": "a clay bell in {PRIMARY} with {HIGHLIGHT} highlights, one small {SECONDARY} clock chip leaning against it",
        "digest": "a neat stack of three clay sheets in {TERTIARY} bound with a {PRIMARY} ribbon with {HIGHLIGHT} highlights",
        "announcement": "a clay megaphone in {PRIMARY} with {HIGHLIGHT} highlights, one soft {SECONDARY} sound-wave arc leaving its mouth",
    },
    "gamification": {
        "streak-freeze": "a chunky clay flame in {PRIMARY} sealed inside a pale frosty {TERTIARY} ice cube with {HIGHLIGHT} frost highlights, one small {SECONDARY} snowflake beside it",
        "leaderboard-podium": "a three-tier clay podium in {PRIMARY} with {HIGHLIGHT} highlights, the tallest step in the center with one small {SECONDARY} trophy token resting on it",
        "level-up": "a clay arrow curving up and forward in {PRIMARY} with {HIGHLIGHT} highlights over two ascending {TERTIARY} steps, one small {SECONDARY} sparkle bursting above it",
        "achievement-badge": "a round clay medal badge in {PRIMARY} with {HIGHLIGHT} highlights and a {SECONDARY} star on its face, one {TERTIARY} ribbon loop hanging below it",
        "quest": "a clay map scroll unrolled in {PRIMARY} with {HIGHLIGHT} highlights and a dashed dotted path crossing it, one {SECONDARY} flag pin marking the end",
        "treasure-chest": "a clay treasure chest in {PRIMARY} with {HIGHLIGHT} trim and its lid open, a small glow of {SECONDARY} star and coin tokens peeking out",
        "energy-hearts": "three round clay hearts in a row in {PRIMARY} with {HIGHLIGHT} highlights, the rightmost heart chipped with a small corner missing",
        "gem-currency": "one chunky clay gem in {PRIMARY} with {HIGHLIGHT} facet highlights, a small stack of {SECONDARY} coin tokens beside it",
        "daily-goal": "a clay target ring in {PRIMARY} with {TERTIARY} rings and a {SECONDARY} check mark pinned at the bullseye, one small {HIGHLIGHT} sparkle beside it",
        "practice-again": "one chunky circular clay arrow looping in {PRIMARY} with {HIGHLIGHT} highlights, one small {SECONDARY} star resting inside the loop",
    },
    "learning": {
        "lesson-complete": "an open clay book in {PRIMARY} cover with {TERTIARY} pages and a large chunky {SECONDARY} checkmark resting on its page, one tiny {HIGHLIGHT} confetti dot above",
        "lesson-locked": "a small clay book in {PRIMARY} cover closed tight with a chunky {SECONDARY} padlock strapped around its cover",
        "wrong-answer": "a small stack of {TERTIARY} cards with the top card slightly askew and a large chunky {PRIMARY} cross mark leaning against it",
        "flashcards": "a neat small stack of {TERTIARY} flashcards with the top card standing upright and propped forward, one {SECONDARY} spark dot beside it",
        "certificate": "a rolled clay scroll certificate in {PRIMARY} with {HIGHLIGHT} highlights bound by a {SECONDARY} ribbon seal",
        "study-review": "an open clay notebook in {PRIMARY} cover with {TERTIARY} pages, one chunky {SECONDARY} bookmark ribbon dangling from its edge",
    },
    "community": {
        "empty-room": "two small round clay cafe stools in {PRIMARY} with {HIGHLIGHT} highlights facing each other, everything clean and unoccupied, one small {SECONDARY} steaming cup resting between them",
        "open-table": "a small round clay cafe stool in {PRIMARY} with {HIGHLIGHT} highlights and one empty {TERTIARY} stool clearly waiting beside it, one small {SECONDARY} cup with rising steam resting on top",
        "anon-mask": "a smooth rounded clay carnival mask in {PRIMARY} with {HIGHLIGHT} highlights and blank eye holes, resting at a slight tilt",
        "direct-message": "two small clay speech bubbles in {PRIMARY} and {SECONDARY} facing each other with {HIGHLIGHT} highlights, one tiny spark between them",
        "waiting-reply": "a clay speech bubble in {PRIMARY} with three small round {SECONDARY} typing dots inside it, one small {TERTIARY} clock leaning beside it",
        "reported": "a clay flag raised on a short {PRIMARY} pole with {HIGHLIGHT} highlights, one small {SECONDARY} shield chip at its base",
        "blocked": "a clay speech bubble in {PRIMARY} with a chunky {SECONDARY} prohibition slash across it, resting at a slight tilt",
        "content-removed": "a {TERTIARY} sheet of paper dissolving into a few soft drifting pieces, one small {PRIMARY} trash chip beside it",
    },
    "assessment": {
        "blank-exam-paper": "a folded blank clay exam paper in {TERTIARY} with {PRIMARY} edges and {HIGHLIGHT} highlights, a round {SECONDARY} wax seal stamped on its fold, everything blank and pristine",
        "results-sealed": "a clay sealed envelope in {PRIMARY} with {HIGHLIGHT} highlights and a {TERTIARY} inner flap, a round {SECONDARY} wax seal with a star pressed on its fold, kept closed and waiting",
        "proctor-camera": "a soft rounded clay camera in {PRIMARY} with {HIGHLIGHT} highlights and a clean {TERTIARY} lens, one small {SECONDARY} shield token resting beside it",
        "device-check": "a small clay laptop in {PRIMARY} with a blank {TERTIARY} screen and {HIGHLIGHT} highlights, a chunky {SECONDARY} shield with a check mark resting beside it",
        "integrity-shield": "a chunky clay shield in {PRIMARY} with {HIGHLIGHT} highlights and a large {SECONDARY} check mark at its center, standing on a small {TERTIARY} base",
    },
    "billing": {
        "storage-full": "a clay storage box in {PRIMARY} with {HIGHLIGHT} highlights packed to the brim with {TERTIARY} sheets, one last sheet hovering just above it with nowhere to fit, one small {SECONDARY} alert dot floating beside it",
        "upload-limit": "a chunky clay progress bar in {PRIMARY} filled completely to the end with {HIGHLIGHT} highlights, a small {SECONDARY} cloud token at its far end, one blank {TERTIARY} sheet waiting below it",
        "feature-locked": "a round clay button badge in {TERTIARY} with a {SECONDARY} gear on its face, a chunky {PRIMARY} padlock with {HIGHLIGHT} highlights leaning across it",
        "upgrade": "a chunky clay crown in {PRIMARY} with {HIGHLIGHT} highlights and one {SECONDARY} gem dot on its front, rising above two small ascending {TERTIARY} steps",
        "trial-ended": "a perforated clay ticket in {PRIMARY} with {HIGHLIGHT} highlights torn cleanly in half along its perforation, the stub half tilted slightly, one small {SECONDARY} clock chip lying beside it",
        "subscribed": "a chunky clay membership card standing upright in {PRIMARY} with {HIGHLIGHT} highlights and a {SECONDARY} star on its face, one {TERTIARY} check badge resting on its corner, one tiny sparkle",
    },
    "wellness": {
        "journal": "a closed clay notebook in {PRIMARY} with {HIGHLIGHT} highlights and a {SECONDARY} strap around it, one small feather resting on top",
        "mood-checkin": "three round clay mood coins in {PRIMARY} and {SECONDARY} each showing a different simple smiley expression, one {HIGHLIGHT} check dot under the middle one",
        "calm-breathing": "a soft round clay breathing wave circle in {PRIMARY} with gentle {HIGHLIGHT} concentric rings, one tiny {SECONDARY} leaf floating above it",
        "reflection": "a small round clay mirror in {PRIMARY} frame with a clean {TERTIARY} glass, one small {SECONDARY} spark dot on its surface",
        "safe-space": "a small clay house with a round {PRIMARY} door, one soft {SECONDARY} heart resting on its doorstep",
        "session-complete": "a soft clay lotus flower in {PRIMARY} with {HIGHLIGHT} petals resting on a pale {TERTIARY} ripple, one tiny {SECONDARY} sparkle above it",
    },
}


def palette_line(palette: dict[str, str]) -> str:
    return ("vibrant lively colors: "
            f"{palette['PRIMARY']}, {palette['HIGHLIGHT']} highlights, "
            f"{palette['SECONDARY']} accents, {palette['TERTIARY']} "
            "pale surfaces")


def prompt_for(group: str, state: str, palette: str) -> str:
    p = PALETTES[palette]
    subject = SUBJECTS[group][state].format(**p)
    return (f"{STRUCTURE}, {palette_line(p)}, {TRAY}, {subject}. "
            f"Avoid: {AVOID}")


def all_keys() -> list[str]:
    return [f"{g}/{s}" for g, subs in SUBJECTS.items() for s in subs]


def api_key() -> str:
    key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if key:
        return key
    env_file = pathlib.Path(os.path.expanduser("~/.claude/.env"))
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("DASHSCOPE_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
    print("generate_clay_library: DASHSCOPE_API_KEY not set and not "
          "found in ~/.claude/.env", file=sys.stderr)
    raise SystemExit(1)


def submit(text: str, key: str) -> str:
    body = {"model": MODEL,
            "input": {"messages": [{"role": "user",
                                     "content": [{"text": text}]}]},
            "parameters": {"size": "1024*1024", "n": 1}}
    req = urllib.request.Request(
        BASE_API + "/services/aigc/image-generation/generation",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}",
                 "X-DashScope-Async": "enable",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)["output"]["task_id"]


def poll(task_id: str, key: str) -> dict:
    while True:
        req = urllib.request.Request(f"{BASE_API}/tasks/{task_id}",
                                     headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        if data["output"]["task_status"] in ("SUCCEEDED", "FAILED", "UNKNOWN"):
            return data
        time.sleep(4)


def image_url(output: dict) -> str:
    if "results" in output and output["results"]:
        return output["results"][0]["url"]
    return output["choices"][0]["message"]["content"][0]["image"]


def generate(text: str, key: str) -> pathlib.Path:
    task_id = submit(text, key)
    print(f"  task {task_id}", flush=True)
    data = poll(task_id, key)
    if data["output"]["task_status"] != "SUCCEEDED":
        raise RuntimeError(json.dumps(data.get("output", {})))
    tmp = TMP_DIR / f"raw-{task_id}.png"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(
            urllib.request.Request(image_url(data["output"])),
            timeout=120) as resp:
        tmp.write_bytes(resp.read())
    return tmp


def ship_variants(src: pathlib.Path, stem: pathlib.Path) -> dict[str, int]:
    """Resize to ship size, save white + transparent, enforce budget."""
    from PIL import Image

    img = Image.open(src).convert("RGB")
    white_path = stem.with_name(stem.name + ".white.png")
    shipped: dict[str, int] = {}
    size = DOWNSCALE_STEPS[-1]
    for step in DOWNSCALE_STEPS:
        img.resize((step, step), Image.LANCZOS).save(
            white_path, optimize=True)
        size = step
        if white_path.stat().st_size <= SIZE_BUDGET:
            shipped["white"] = white_path.stat().st_size
            break
    if "white" not in shipped:
        raise RuntimeError(f"white variant over budget at "
                           f"{DOWNSCALE_STEPS[-1]}px")
    from rembg import remove
    cut = remove(white_path.read_bytes())
    cut_img = Image.open(io.BytesIO(cut)).convert("RGBA")
    if cut_img.size != (size, size):
        cut_img = cut_img.resize((size, size), Image.LANCZOS)
    trans_path = stem.with_name(stem.name + ".transparent.png")
    cut_img.save(trans_path, optimize=True)
    shipped["transparent"] = trans_path.stat().st_size
    return shipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the cross-project clay illustration "
                    "library with the locked r8-2 recipe.")
    parser.add_argument("--list", action="store_true",
                        help="list all groups/states and palettes")
    parser.add_argument("--dry-run", action="store_true",
                        help="print assembled prompts, call nothing")
    parser.add_argument("--group", help="one group name")
    parser.add_argument("--subject", help="one subject as group/state")
    parser.add_argument("--palette", default="terracotta",
                        choices=sorted(PALETTES))
    parser.add_argument("--all", action="store_true",
                        help="every subject for --palette")
    parser.add_argument("--skip-existing", action="store_true",
                        help="skip subjects whose shipped files exist")
    args = parser.parse_args()

    if args.list:
        for group, subs in SUBJECTS.items():
            print(f"{group} ({len(subs)}): {', '.join(subs)}")
        print(f"\npalettes: {', '.join(PALETTES)}")
        print(f"total subjects: {len(all_keys())}")
        return 0

    if args.subject:
        keys = [args.subject]
        if keys[0] not in all_keys():
            print(f"unknown subject {keys[0]}", file=sys.stderr)
            return 1
    elif args.group:
        if args.group not in SUBJECTS:
            print(f"unknown group {args.group}", file=sys.stderr)
            return 1
        keys = [f"{args.group}/{s}" for s in SUBJECTS[args.group]]
    elif args.all:
        keys = all_keys()
    else:
        parser.print_help()
        return 1

    if args.dry_run:
        for key in keys:
            group, state = key.split("/")
            print(f"=== {key} [{args.palette}] ===\n"
                  f"{prompt_for(group, state, args.palette)}\n")
        return 0

    key = api_key()
    failed: list[str] = []
    for item in keys:
        group, state = item.split("/")
        dest_dir = OUT_DIR / args.palette
        dest_dir.mkdir(parents=True, exist_ok=True)
        stem = dest_dir / f"{group}-{state}"
        if args.skip_existing and all(
                stem.with_name(f"{group}-{state}.{v}.png").exists()
                for v in ("white", "transparent")):
            print(f"=== {item} [{args.palette}] === exists, skipped",
                  flush=True)
            continue
        print(f"=== {item} [{args.palette}] ===", flush=True)
        src = None
        for attempt in range(1, 4):
            try:
                src = generate(prompt_for(group, state, args.palette), key)
                break
            except Exception as exc:
                print(f"  attempt {attempt} failed: {exc}", flush=True)
                if attempt < 3:
                    time.sleep(6)
        if src is None:
            failed.append(item)
            continue
        try:
            shipped = ship_variants(src, stem)
        except Exception as exc:
            print(f"  ERROR shipping {item}: {exc}", file=sys.stderr)
            failed.append(item)
            continue
        for variant, nbytes in shipped.items():
            print(f"  saved {stem.name}.{variant}.png {nbytes}B", flush=True)
    if failed:
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
