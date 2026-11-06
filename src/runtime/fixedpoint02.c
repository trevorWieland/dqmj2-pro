typedef int s32;
typedef long long s64;
extern void native_fn_02008d28(const s32 *, s32 *);
void native_main_020019b0(const s32 *s, s32 *d, s32 x, s32 y, s32 z) {
    if (s != d) native_fn_02008d28(s, d);
    d[12] = s[12] + (s32)(((s64)x * s[0] + (s64)y * s[4] + (s64)z * s[8]) >> 12);
    d[13] = s[13] + (s32)(((s64)x * s[1] + (s64)y * s[5] + (s64)z * s[9]) >> 12);
    d[14] = s[14] + (s32)(((s64)x * s[2] + (s64)y * s[6] + (s64)z * s[10]) >> 12);
    d[15] = s[15] + (s32)(((s64)x * s[3] + (s64)y * s[7] + (s64)z * s[11]) >> 12);
}
