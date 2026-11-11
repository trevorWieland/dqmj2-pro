/* 0x02047c68 (main, ARM, 216 B) -- alt-family string builder.

   The counterpart of native_main_02047d50 over the same two line buffers
   (native_data_020facd8[2], each { s32 count; u16 text[64]; }), using the alt family
   slot [0]. `count` is the text-root index and the overflow guard, here at 512.

   For caller kinds 1 and 2 it decodes the current resource text (the pointer stored at
   native_data_020da93c) into the line buffer, then appends a root text and returns the
   buffer base for the caller to concatenate into its own cursor. Unlike the text
   builder, the root group depends on the flag: group 3 when flag != 0, group 2 when it
   is zero, both table 0 index count.

   native_02047e20 is the shared emitter: (destination halfwords, source bytes, kind,
   value) -> halfwords written. native_0203cfe0 is the constant hook the image calls and
   drops.

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

u32 native_main_02047c68(u32 kind, u32 flag, u32 value)
{
    s32 count = native_data_020facd8[0].count;
    u8 written = 0;
    u16 *buffer = native_data_020facd8[0].text;
    u8 *p;
    u16 *dest;

    if (count < 512) {
        native_fn_0203cfe0(kind, flag, value);
        if (kind == 1) {
            written += native_fn_02047e20(buffer, native_data_020da93c, kind, value);
        } else if (kind == 2) {
            written += native_fn_02047e20(buffer, native_data_020da93c, kind, value);
        }
        dest = native_data_020facd8[0].text + written;
        if (flag != 0) {
            p = native_fn_0205dc70(3, 0, (u16)count);
        } else {
            p = native_fn_0205dc70(2, 0, (u16)count);
        }
        native_fn_02047e20(dest, p, kind, value);
    }
    return (u32)native_data_020facd8[0].text;
}
