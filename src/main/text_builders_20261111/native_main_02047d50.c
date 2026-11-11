/* 0x02047d50 (main, ARM, 208 B) -- text-family string builder.

   Two line buffers sit back to back as native_data_020facd8[2], each
   { s32 count; u16 text[64]; }: [0] is the alt family, [1] the text family. `count` is
   both the text-root index and the overflow guard -- at 255 or more the builder only
   returns the buffer base.

   Otherwise it decodes the current resource text (the pointer stored at
   native_data_020da93c) into the line buffer for caller kinds 1 and 2, appends the root
   text native_text_roots[4][0][count], and returns the buffer base so the caller can
   concatenate it into its own cursor.

   native_02047e20 is the shared emitter: (destination halfwords, source bytes, kind,
   value) -> halfwords written. native_0203cfe0 is the constant hook the image calls and
   drops. `p` is left unset on the flag != 0 path because the image passes that
   register through uninitialised as well.

   Reproduces under the pinned 2.0/base (p001) and under the src/main rule (2.0/sp1p5,
   p002). The declaration order below is what produces the image's r4/r5/r6/r7
   assignment, so keep it. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

typedef struct {
    s32 count;
    u16 text[64];
} TextLine;

extern TextLine native_data_020facd8[2];
extern u8 *native_data_020da93c;
extern u32 native_fn_0203cfe0(u32, u32, u32);
extern u32 native_fn_02047e20(u16 *, const u8 *, u32, u32);
extern u8 *native_fn_0205dc70(u32, u32, u32);

u32 native_main_02047d50(u32 kind, u32 flag, u32 value)
{
    u8 *p;
    s32 count = native_data_020facd8[1].count;
    u8 written = 0;
    u16 *buffer = native_data_020facd8[1].text;
    u16 *dest;

    if (count < 255) {
        native_fn_0203cfe0(kind, flag, value);
        if (kind == 1) {
            written += native_fn_02047e20(buffer, native_data_020da93c, kind, value);
        } else if (kind == 2) {
            written += native_fn_02047e20(buffer, native_data_020da93c, kind, value);
        }
        dest = native_data_020facd8[1].text + written;
        if (flag == 0) {
            p = native_fn_0205dc70(4, 0, (u16)count);
        }
        native_fn_02047e20(dest, p, kind, value);
    }
    return (u32)native_data_020facd8[1].text;
}
