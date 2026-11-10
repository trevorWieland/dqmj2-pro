/*
 * ov006 packet p4-1 shared context.
 *
 * Overlay 006 owns a small set of globals and runtime helpers. The overlay is
 * linked at a fixed address, so cross-module entry points are declared with
 * their measured address in the name; the comparison harness resolves those
 * names back to the linked address. Field offsets below are measured from the
 * overlay image and are the only layout facts asserted here.
 */
#ifndef OV006_P4_021D7240_CONTEXT_H
#define OV006_P4_021D7240_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* 0x0220e9a0: overlay UI state. 0x04..0x2c form the current mode record. */
extern u8 native_data_ov006_0220e9a0[];
/* 0x0220e9d0: source byte string drained by the glyph queue. */
extern u8 native_data_ov006_0220e9d0[];
/* 0x0220eb04: sprite slots; entry i is a pointer created by 0x02084924. */
extern u8 native_data_ov006_0220eb04[];
/* 0x0220c8a0: draw state; field 4 is the active draw-list handle. */
extern u8 native_data_ov006_0220c8a0[];
/* 0x0220cb98: two-record source table for the hint panel. */
extern u8 native_data_ov006_0220cb98[];
/* 0x021c9698: shared "%..." format string used by the menu text setters. */
extern u8 native_data_021c9698[];
/* 0x020dbc18: glyph halfword table addressed by style + character class. */
extern u8 native_data_020dbc18[];

/* 0x02049ffc releases the slot pointer still held in r0; called both with an
 * explicit slot and (at 0x021d7d28) with the value a helper just returned. */
extern void native_fn_02049ffc();
extern void native_fn_02085284(u8 *record, u32 a, u32 b, u32 c);
extern void native_fn_02046af4(u8 *format, u32 value, u32 width, u32 pad, u8 *text, u32 limit);
extern void native_fn_02087a48(u8 *slot, u32 x, s32 y, u32 attr, u32 draw, u8 *text);
extern void native_fn_02008c58(u32 value, u8 *dst, u32 size);
extern void native_fn_02008be0(u32 value, u8 *dst, u32 size);
extern u8 *native_fn_020449d4(u32 index);
extern u32 native_fn_020470fc(u8 *text);
extern u8 *native_fn_02084924(u32 type, u32 b0, u32 b1, u32 b2, s32 b3, u32 c1, u32 c2, u32 scale, u32 d1, u32 d2);
extern void native_fn_0204861c(s32 x, u32 glyph);
extern void native_fn_0207b460(s32 id, u32 glyph, u8 *name, u8 *text);
extern s32 native_fn_0207c2b8(u8 *record, u8 *text);
extern s32 native_fn_0207c3d8(u8 *record, u8 *text);
extern s32 native_fn_0207c18c(u8 *record, u8 *text);
extern s32 native_fn_0207c1b8(u8 *record, u8 *text);
extern u8 *native_fn_02067748(void);
extern u32 native_fn_0206784c(void);
extern u8 *native_fn_0206442c(void);
extern u32 native_fn_020643fc(u16 id);
extern void native_fn_02067dd4(void);
extern u32 native_fn_02067d54(void);
extern u32 native_fn_02067b48(void);
extern u32 native_fn_02067bd4(s32 index);
extern void native_fn_02067bec(s32 index, u32 value);
extern u32 native_fn_02008e0c(u8 *dst, u8 *src, u32 size);
extern u32 native_fn_02008d78(u8 *dst, u32 value, u32 size);

/* Same-overlay helpers. */
extern void native_fn_ov006_021d77f8(u32 arg);
extern void native_fn_ov006_021d7860(void);
extern void native_fn_ov006_021d79d4(u32 value);
extern void native_fn_ov006_021d79e4(u32 index, u32 a, u32 b, u32 c);
extern void native_fn_ov006_021d79f8(u32 index, u32 a, u32 b, u32 c, s16 d);
extern void native_fn_ov006_021d7ad0(u32 index, u8 *text);
extern void native_fn_ov006_021d7b3c(u32 index, u32 a, u32 b);
extern void native_fn_ov006_021d7d28(u8 *records, s32 count);
extern void native_fn_ov006_021d8288(u32 value);
extern u32 native_fn_ov006_021da9d0(void);
extern void native_fn_ov006_021daaf0(void);

#endif
