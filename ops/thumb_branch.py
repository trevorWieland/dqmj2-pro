"""Mode-aware Thumb ``BL`` / ``BLX`` immediate expansion for authors.

The measured image says whether a call site is a Thumb ``BL`` or an ARM
``BLX`` immediate, and an author comparing bytes has to reproduce that exactly.
Two details are easy to get wrong and cost a round each, so they are encoded here
once:

1. **The branch base differs.** ``BL`` is relative to ``PC + 4``; ``BLX`` is
   relative to ``Align(PC + 4, 4)``. Using ``PC + 4`` for both shifts every BLX
   site by the alignment difference.
2. **The ARM/Thumb marker is in the second halfword.** The discriminating bit is
   bit 12: a ``BLX`` immediate clears it (``11 J1 0 J2 imm10L 0``), a ``BL`` sets
   it (``11 J1 1 J2 imm11``). The commonly quoted ``0xE800`` is only the pattern
   when ``J1`` is set; a BLX with ``J1 == 0`` is ``0xC8xx``, so testing
   ``(second & 0xF800) == 0xE800`` misclassifies it as a ``BL``. Test
   ``(second & 0xD000) == 0xC000`` instead. Reading the first halfword instead
   silently yields ``BL`` for every site (both forms start ``0xF000``-ish).

The compiler's relocation addend already carries the ``-4`` PC bias for a plain
call (``R_ARM_THM_CALL`` with addend ``-4``), so the delta is computed relative to
that base without adding another bias.

``public_tools/repo_build.py`` has the same rule inline; this module exists so an
author can call it directly instead of copying that code. It does not import or
modify ``repo_build``.

Usage
-----
    from thumb_branch import expand, marker_mode, encode

    words = expand(image, offset, site, target)          # mode read from the image
    words = encode(site, target, arm=True)               # mode given explicitly
"""

THM_CALL = 10
THM_JUMP24 = 30
BLX_MARKER = 0xE800
BL_MARKER = 0xF800
# Bit 15:14 == 11 and bit 12 == 0 identifies every BLX-immediate regardless of J1/J2.
BLX_MASK = 0xD000
BLX_VALUE = 0xC000


def is_blx(second):
    """True when a second halfword encodes a BLX immediate (bit 12 clear)."""
    return (second & BLX_MASK) == BLX_VALUE


def marker_mode(image, offset):
    """Mode of the callee, from the measured instruction at ``offset``.

    ``image`` is the module image, ``offset`` the site's offset into it. Returns
    ``'arm'`` for a ``BLX`` immediate and ``'thumb'`` for a ``BL``.
    """
    second = int.from_bytes(image[offset + 2:offset + 4], 'little')
    return 'arm' if is_blx(second) else 'thumb'


def encode(site, target, addend=-4, arm=False, mode=None):
    """Encode one Thumb-2 ``BL`` (``arm=False``) or ``BLX`` (``arm=True``).

    ``mode`` is an explicit ``'arm'``/``'thumb'`` override; when given it wins
    over ``arm``. Callers that resolved the target from project evidence pass
    ``mode`` and never infer the mode from the placeholder halfword the
    compiler emitted.

    Returns the two instruction halfwords, ``(first, second)``.
    """
    if mode is not None:
        if mode not in ('arm', 'thumb'):
            raise ValueError(f'unknown branch target mode: {mode!r}')
        arm = mode == 'arm'
    base = ((site + 4) & ~3) if arm else (site + 4)
    delta = target + addend + 4 - base
    sign = (delta >> 24) & 1
    i1 = (delta >> 23) & 1
    i2 = (delta >> 22) & 1
    j1 = (i1 ^ sign) ^ 1
    j2 = (i2 ^ sign) ^ 1
    first = 0xF000 | (sign << 10) | ((delta >> 12) & 0x3FF)
    second = (BLX_MARKER if arm else BL_MARKER) | (j1 << 13) | (j2 << 11) | ((delta >> 1) & 0x7FF)
    return first, second


def expand(image, offset, site, target, addend=-4):
    """Encode using the mode the measured image records at the site."""
    return encode(site, target, addend, arm=(marker_mode(image, offset) == 'arm'))
