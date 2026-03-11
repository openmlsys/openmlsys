"""Convert LaTeX math notation to Typst math notation within markdown content.

This module provides a best-effort converter for the LaTeX math subset used in
the OpenMLSys textbook.  It is **not** a general-purpose LaTeX→Typst transpiler;
only the commands that actually appear in the zh_chapters are handled.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Brace-matching helper
# ---------------------------------------------------------------------------

def _find_brace_group(s: str, pos: int) -> tuple[str, int] | None:
    """Return ``(content, end_pos)`` for the ``{…}`` group starting at *pos*.

    Skips leading whitespace.  Returns ``None`` when no opening brace is found
    or braces are unbalanced.
    """
    while pos < len(s) and s[pos] in " \t":
        pos += 1
    if pos >= len(s) or s[pos] != "{":
        return None
    depth = 0
    start = pos + 1
    for i in range(pos, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return (s[start:i], i + 1)
    return None


# ---------------------------------------------------------------------------
# Command tables
# ---------------------------------------------------------------------------

# Commands whose Typst name equals the LaTeX name (just drop the backslash).
SIMPLE_COMMANDS: set[str] = {
    # Greek
    "alpha", "beta", "gamma", "delta", "Delta",
    "epsilon", "zeta", "eta", "theta", "Theta",
    "iota", "kappa", "lambda", "Lambda",
    "mu", "nu", "xi", "Xi",
    "pi", "Pi", "rho",
    "sigma", "Sigma", "tau",
    "upsilon", "Upsilon",
    "phi", "Phi", "chi", "psi", "Psi",
    "omega", "Omega",
    # Operators / relations
    "times", "partial", "nabla", "in",
    "top", "prime",
    "forall", "exists", "approx", "equiv",
    "subset", "supset",
    # Big operators / functions
    "log", "ln", "exp", "sin", "cos", "tan",
    "min", "max", "lim", "sum",
    "det", "dim", "ker", "inf", "sup",
}

# Commands that map to a *different* Typst identifier.
RENAMED_COMMANDS: dict[str, str] = {
    "cdot": "dot.c",
    "cdots": "dots.c",
    "ldots": "dots",
    "dots": "dots",
    "to": "->",
    "rightarrow": "->",
    "leftarrow": "<-",
    "Rightarrow": "=>",
    "rightsquigarrow": "arrow.r.squiggly",
    "leq": "<=",
    "geq": ">=",
    "prod": "product",
    "notag": "",
    "quad": "quad",
    "qquad": "wide",
    "label": "",       # consumed by :eqlabel: already
    "sim": "tilde.op",
    "infty": "infinity",
    "neq": "eq.not",
    "ast": "ast.op",
    "vdots": "dots.v",
    "ddots": "dots.down",
    "lVert": "||",
    "rVert": "||",
    "vert": "|",
    "lvert": "|",
    "rvert": "|",
    "mid": "|",
    "cap": "inter",
    "cup": "union",
    "le": "<=",
    "ge": ">=",
    "odot": "dot.o",
    "oplus": "plus.circle",
    "otimes": "times.circle",
}

# \cmd{arg} → typst_func(arg)
ONE_ARG_COMMANDS: dict[str, str] = {
    "boldsymbol": "bold",
    "mathcal": "cal",
    "mathbf": "bold",
    "mathbb": "bb",
    "hat": "hat",
    "bar": "overline",
    "dot": "dot",
    "tilde": "tilde",
    "sqrt": "sqrt",
    "overline": "overline",
    "pmb": "bold",
    "textbf": "bold",
    "textit": "italic",
    "bm": "bold",
}

# \cmd{arg1}{arg2} → typst_func(arg1, arg2)
TWO_ARG_COMMANDS: dict[str, str] = {
    "frac": "frac",
    "binom": "binom",
}

# Delimiter-sizing commands to strip (the delimiter char after them is kept).
_SIZING_COMMANDS: set[str] = {
    "left", "right", "bigg", "Bigg", "big", "Big", "biggl", "biggr",
}

# ---------------------------------------------------------------------------
# Core single-pass converter
# ---------------------------------------------------------------------------

def _last_char(out: list[str]) -> str:
    """Return the last non-empty character in the output buffer, or ``""``."""
    for part in reversed(out):
        if part:
            return part[-1]
    return ""


def _emit(out: list[str], text: str) -> None:
    """Append *text* to *out*, adding a space separator when needed.

    In Typst math, consecutive letters form a multi-letter identifier which
    will error if unknown.  Similarly, letter→digit transitions form tokens
    like ``W1``.  This helper inserts spaces to prevent such merging, matching
    LaTeX math semantics where adjacent characters are separate symbols.
    """
    if not text:
        out.append(text)
        return
    lc = _last_char(out)
    fc = text[0]
    if lc and (
        # letter→letter  (e.g. "ou" → "o u")
        (lc.isalpha() and fc.isalpha())
        # letter→digit   (e.g. "W1" → "W 1")
        or (lc.isalpha() and fc.isdigit())
        # digit→letter   (e.g. "2x" → "2 x")
        or (lc.isdigit() and fc.isalpha())
        # )→letter/digit (e.g. "bold(X)y" → "bold(X) y")
        or (lc == ")" and (fc.isalpha() or fc.isdigit()))
    ):
        out.append(" ")
    out.append(text)


def _convert(s: str) -> str:
    """Convert a single LaTeX math expression to Typst math."""
    out: list[str] = []
    i = 0
    n = len(s)

    while i < n:
        ch = s[i]

        # ---- backslash commands ----
        if ch == "\\" and i + 1 < n:
            nxt = s[i + 1]

            # Double backslash: either markdown-escaped bracket or line-break
            if nxt == "\\":
                # \\{ \\} \\[ \\] \\( \\) → markdown-escaped LaTeX delimiters
                if i + 2 < n and s[i + 2] in "{}[]()":
                    out.append(s[i + 2])
                    i += 3
                    continue
                out.append(" \\\n")
                i += 2
                continue

            # Escaped characters: \{  \}  \[  \]  \(  \)  \,  \;  \!  \   \.
            if nxt in "{}[]()":
                out.append(nxt)
                i += 2
                continue
            if nxt == ",":
                out.append("thin ")     # thin space
                i += 2
                continue
            if nxt == ";":
                out.append("med ")      # medium space
                i += 2
                continue
            if nxt == "!":
                out.append("")          # negative thin space → ignore
                i += 2
                continue
            if nxt == " ":
                out.append(" ")
                i += 2
                continue
            if nxt == "\n":
                out.append(" ")
                i += 2
                continue

            # Try to match an alphabetic command name
            m = re.match(r"[a-zA-Z]+", s[i + 1:])
            if not m:
                # Bare backslash before non-alpha → keep the char after
                out.append(nxt)
                i += 2
                continue

            cmd = m.group()
            after = i + 1 + m.end()

            # -- environments --
            if cmd == "begin":
                g = _find_brace_group(s, after)
                if g:
                    env_name, env_pos = g
                    end_marker = f"\\end{{{env_name}}}"
                    end_idx = s.find(end_marker, env_pos)
                    if end_idx != -1:
                        body = s[env_pos:end_idx]
                        i = end_idx + len(end_marker)
                        _emit(out, _convert_environment(env_name, body))
                        continue
                # Fallthrough: couldn't parse, skip \begin
                i = after
                continue

            if cmd == "end":
                # Stray \end (shouldn't happen if \begin matched)
                g = _find_brace_group(s, after)
                i = g[1] if g else after
                continue

            # -- special multi-arg commands --
            if cmd == "underset":
                # \underset{below}{base} → attach(base, b: below)
                g1 = _find_brace_group(s, after)
                if g1:
                    below, p1 = g1
                    g2 = _find_brace_group(s, p1)
                    if g2:
                        base, p2 = g2
                        _emit(out, f"attach({_convert(base)}, b: {_convert(below)})")
                        i = p2
                        continue

            if cmd == "overset":
                # \overset{above}{base} → attach(base, t: above)
                g1 = _find_brace_group(s, after)
                if g1:
                    above, p1 = g1
                    g2 = _find_brace_group(s, p1)
                    if g2:
                        base, p2 = g2
                        _emit(out, f"attach({_convert(base)}, t: {_convert(above)})")
                        i = p2
                        continue

            if cmd == "operatorname":
                # \operatorname{name} → op("name")
                g = _find_brace_group(s, after)
                if g:
                    name, pos = g
                    _emit(out, f'op("{name}")')
                    i = pos
                    continue

            if cmd == "tag":
                # \tag{n} → visual equation number
                g = _find_brace_group(s, after)
                if g:
                    content, pos = g
                    _emit(out, f'quad upright("({content})")')
                    i = pos
                    continue

            if cmd == "eqref":
                # \eqref{name} → show label name as fallback
                g = _find_brace_group(s, after)
                if g:
                    content, pos = g
                    _emit(out, f'upright("({content})")')
                    i = pos
                    continue

            if cmd in ("mathrm", "text"):
                # \mathrm{text} → upright("text") — treat as text, not math
                g = _find_brace_group(s, after)
                if g:
                    content, pos = g
                    stripped = content.strip()
                    if stripped:
                        _emit(out, f'upright("{stripped}")')
                    # else: empty mathrm (spacing hack) → drop
                    i = pos
                    continue

            # -- two-arg commands --
            if cmd in TWO_ARG_COMMANDS:
                g1 = _find_brace_group(s, after)
                if g1:
                    c1, p1 = g1
                    g2 = _find_brace_group(s, p1)
                    if g2:
                        c2, p2 = g2
                        func = TWO_ARG_COMMANDS[cmd]
                        _emit(out, f"{func}({_convert(c1)}, {_convert(c2)})")
                        i = p2
                        continue
                # Fallthrough
                _emit(out, cmd)
                i = after
                continue

            # -- one-arg commands --
            if cmd in ONE_ARG_COMMANDS:
                g = _find_brace_group(s, after)
                if g:
                    content, pos = g
                    func = ONE_ARG_COMMANDS[cmd]
                    _emit(out, f"{func}({_convert(content)})")
                    i = pos
                    continue
                # Fallthrough: no brace group → just emit the typst name
                _emit(out, ONE_ARG_COMMANDS[cmd])
                i = after
                continue

            # -- \rm (applies upright to the rest of the current scope) --
            if cmd == "rm":
                raw_rest = s[after:]
                leading = len(raw_rest) - len(raw_rest.lstrip())
                rest = raw_rest.lstrip()
                # Grab one "word"
                wm = re.match(r"[A-Za-z0-9]+", rest)
                if wm:
                    word = wm.group()
                    _emit(out, f"upright({word})")
                    i = after + leading + len(word)
                    continue
                _emit(out, "upright")
                i = after
                continue

            # -- delimiter sizing --
            if cmd in _SIZING_COMMANDS:
                # Skip the command; keep whatever delimiter follows.
                i = after
                continue

            # -- simple (same name) --
            if cmd in SIMPLE_COMMANDS:
                _emit(out, cmd)
                # Also add right-side space when next char would merge
                if after < n and (s[after].isalnum() or s[after] == "\\"):
                    out.append(" ")
                i = after
                continue

            # -- renamed --
            if cmd in RENAMED_COMMANDS:
                repl = RENAMED_COMMANDS[cmd]
                if repl:
                    _emit(out, repl)
                    if after < n and s[after].isalnum():
                        out.append(" ")
                # If repl is empty the command is silently dropped.
                # For \label{...} consume the brace group too.
                if cmd == "label":
                    g = _find_brace_group(s, after)
                    if g:
                        i = g[1]
                        continue
                i = after
                continue

            # -- unknown command → emit name without backslash --
            _emit(out, cmd)
            if after < n and s[after].isalnum():
                out.append(" ")
            i = after
            continue

        # ---- brace groups (not consumed by a command) ----
        if ch == "{":
            g = _find_brace_group(s, i)
            if g:
                content, end = g
                # Check if preceded by ^ or _ → superscript/subscript grouping
                if out and out[-1] and out[-1][-1] in "^_":
                    out.append(f"({_convert(content)})")
                    i = end
                    continue
                # Check for {\rm ...} pattern
                rm_m = re.match(r"\\rm\s+", content)
                if rm_m:
                    inner = content[rm_m.end():]
                    _emit(out, f"upright({_convert(inner)})")
                    i = end
                    continue
                # Otherwise, just emit the converted content (braces act as
                # invisible grouping in LaTeX — no Typst equivalent needed
                # in most contexts).
                _emit(out, _convert(content))
                i = end
                continue
            # Unmatched brace — emit as-is
            out.append(ch)
            i += 1
            continue

        # ---- everything else (digits, letters, operators, whitespace) ----
        # Use _emit so consecutive raw letters get spaces inserted,
        # matching LaTeX math semantics where adjacent letters are
        # separate variables (e.g. "out" → "o u t" in Typst).
        _emit(out, ch)
        i += 1

    result = "".join(out)
    # Typst math requires a base before ^ or _; add an invisible base
    # when the expression starts with a script marker (e.g. $^2$).
    if result and result.lstrip() and result.lstrip()[0] in "^_":
        result = '""' + result.lstrip()
    return result


# ---------------------------------------------------------------------------
# Environment converters
# ---------------------------------------------------------------------------

def _convert_environment(name: str, body: str) -> str:
    """Convert a ``\\begin{name}…\\end{name}`` block to Typst."""
    if name in ("matrix", "bmatrix", "pmatrix", "vmatrix"):
        return _convert_matrix_env(name, body)
    if name == "cases":
        return _convert_cases_env(body)
    if name in ("aligned", "split"):
        # Just unwrap — Typst math handles & alignment and \ line-breaks.
        converted = _convert(body)
        return converted
    if name == "figure":
        # Not real math; pass through as-is.
        return f"\\begin{{{name}}}{body}\\end{{{name}}}"
    # Unknown environment — pass through converted content
    return _convert(body)


def _convert_matrix_env(name: str, body: str) -> str:
    """Convert matrix/bmatrix/pmatrix/vmatrix to ``mat(…)``."""
    delim_map = {
        "matrix": "",
        "bmatrix": '"["',
        "pmatrix": '"("',
        "vmatrix": '"|"',
    }
    # Split rows on \\, columns on &
    rows: list[str] = []
    for row_text in re.split(r"\\\\", body):
        row_text = row_text.strip()
        if not row_text:
            continue
        cells = [_convert(c.strip()) for c in row_text.split("&")]
        rows.append(", ".join(cells))

    inner = "; ".join(rows)
    delim = delim_map.get(name, "")
    if delim:
        return f"mat(delim: {delim}, {inner})"
    return f"mat({inner})"


def _convert_cases_env(body: str) -> str:
    """Convert cases environment to ``cases(…)``."""
    branches: list[str] = []
    for branch_text in re.split(r"\\\\", body):
        branch_text = branch_text.strip()
        if not branch_text:
            continue
        branches.append(_convert(branch_text))
    return "cases(" + ", ".join(branches) + ")"


# ---------------------------------------------------------------------------
# Markdown-level math-span detection
# ---------------------------------------------------------------------------

_FENCE_RE = re.compile(r"^(`{3,}|~{3,})", re.MULTILINE)


def _iter_math_spans(content: str):
    """Yield ``(start, end, is_display)`` for every math span.

    Skips spans inside fenced code blocks and inline code.
    """
    n = len(content)
    i = 0
    in_fence: str | None = None  # fence marker when inside a code block

    while i < n:
        # Track fenced code blocks
        if content[i] == "`" or content[i] == "~":
            m = _FENCE_RE.match(content, i)
            if m and (i == 0 or content[i - 1] == "\n"):
                marker = m.group(1)
                if in_fence is None:
                    in_fence = marker[0]  # opening
                    i = content.index("\n", i) + 1 if "\n" in content[i:] else n
                    continue
                elif marker[0] == in_fence:
                    in_fence = None       # closing
                    i = m.end()
                    continue

        if in_fence:
            i += 1
            continue

        # Skip inline code
        if content[i] == "`":
            end_tick = content.find("`", i + 1)
            if end_tick != -1:
                i = end_tick + 1
                continue

        # Display math $$...$$
        if content[i:i + 2] == "$$":
            start = i
            close = content.find("$$", i + 2)
            if close != -1:
                yield (start + 2, close, True)
                i = close + 2
                continue

        # Inline math $...$
        if content[i] == "$":
            start = i
            # Find closing $ — any next $ closes the span (even if followed
            # by another $, which starts a NEW span).
            j = i + 1
            while j < n:
                if content[j] == "$":
                    if j > i + 1:  # non-empty
                        yield (start + 1, j, False)
                    j += 1
                    break
                if content[j] == "\n" and not content[i + 1:j].strip():
                    break  # empty line → not math
                j += 1
            i = j
            continue

        i += 1


_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")


def convert_latex_math_to_typst(content: str) -> str:
    """Replace LaTeX math with Typst math throughout *content* (markdown)."""
    spans = list(_iter_math_spans(content))
    if not spans:
        return content

    parts: list[str] = []
    prev = 0
    for start, end, is_display in spans:
        delim = "$$" if is_display else "$"
        delim_len = len(delim)
        delim_start = start - delim_len

        latex = content[start:end]

        # Spans containing CJK characters are almost certainly mismatched $.
        # Strip the $ delimiters and emit the raw text.
        if _CJK_RE.search(latex):
            parts.append(content[prev:delim_start])
            parts.append(latex)  # emit without $ delimiters
            prev = end + delim_len
            continue

        parts.append(content[prev:delim_start])
        converted = _convert(latex)
        # Strip leading/trailing whitespace from inline math so that
        # ``$ text$`` (space after opening $) never occurs — CommonMark
        # and mdbook-typst-math treat that as non-math.
        if not is_display:
            converted = converted.strip()
        parts.append(f"{delim}{converted}{delim}")

        prev = end + delim_len

    parts.append(content[prev:])
    return "".join(parts)
