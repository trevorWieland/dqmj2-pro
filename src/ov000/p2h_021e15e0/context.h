/* Shared declarations for the ov000 fixed-point packet (ov000-u1).
 *
 * Overlay globals are declared as flat byte arrays and addressed with their
 * measured field offsets. Every symbol name carries its measured address, so the
 * comparison harness resolves relocations without any side table.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef long long s64;

extern s32 native_fn_0200235c(s32 value, s32 limit);
extern s32 native_fn_0200285c(u8 *out, u8 *state);
