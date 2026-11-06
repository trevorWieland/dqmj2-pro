typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long uptr;
u8 *native_main_0201d6b8(u8 *destination, const u8 *source) {
    u8 *out;
    const u8 *in;
    u32 word, test, alignment;
    in = source;
    out = destination;
    if ((alignment = ((uptr)in & 3)) != ((uptr)out & 3)) goto byte_copy;
    if (alignment) {
        if ((*out = *in) == 0) return destination;
        for (alignment = 3 - alignment; alignment; alignment--) {
            if ((*++out = *++in) == 0) return destination;
        }
        ++out;
        ++in;
    }
    word = *(const u32 *)in;
    test = word + 0xFEFEFEFFu;
    test &= ~word;
    test &= 0x80808080u;
    if (test) goto byte_copy;
    out -= 4;
    do {
        out += 4;
        *(u32 *)out = word;
        in += 4;
        word = *(const u32 *)in;
        test = word + 0xFEFEFEFFu;
    test &= ~word;
        test &= 0x80808080u;
        if (test) goto adjust;
    } while (1);
adjust:
    out += 4;
byte_copy:
    if ((*out = *in) == 0) return destination;
    do {
        if ((*++out = *++in) == 0) return destination;
    } while (1);
    return destination;
}
