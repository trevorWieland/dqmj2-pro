typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long uptr;
int native_main_0201d800(const u8 *first, const u8 *second) {
    const u8 *left = first;
    const u8 *right = second;
    u32 alignment, a, b, test;
    a = *left;
    b = *right;
    if (a - b) return a - b;
    if ((alignment = ((uptr)left & 3)) != ((uptr)right & 3)) goto byte_compare;
    if (alignment) {
        if (a == 0) return 0;
        for (alignment = 3 - alignment; alignment; alignment--) {
            a = *++left;
            b = *++right;
            if (a - b) return a - b;
            if (a == 0) return 0;
        }
        ++left;
        ++right;
    }
    a = *(const u32 *)left;
    b = *(const u32 *)right;
    test = (a + 0xFEFEFEFFu) & ~a;
    if (test & 0x80808080u) goto adjust;
    while (a == b) {
        left += 4;
        right += 4;
        a = *(const u32 *)left;
        b = *(const u32 *)right;
        test = a + 0xFEFEFEFFu;
        if (test & 0x80808080u) goto adjust;
    }
    --left;
    --right;
    goto byte_compare;
adjust:
    a = *left;
    b = *right;
    if (a - b) return a - b;
byte_compare:
    if (a == 0) return 0;
    do {
        a = *++left;
        b = *++right;
        if (a - b) return a - b;
    } while (a);
    return 0;
}
