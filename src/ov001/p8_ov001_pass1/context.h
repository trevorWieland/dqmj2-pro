/* Shared declarations for the ov001 straight-line leaf packet (ov001-p8).
 *
 * Every overlay global is declared as a flat byte block and addressed with its
 * measured field offsets; the trailing eight hex digits of every name are the
 * measured overlay address, so the comparison harness resolves the relocation
 * without a side table.  The module base is 0x021d7240 and the overlay image is
 * uncompressed in the extract (compressed in the ROM), so an address minus the
 * base indexes the compared image directly.
 *
 * Mechanism notes measured while authoring this packet (each one is a fact read
 * from the image, not an inference):
 *   - 0x0223d904 is a table of 12-byte records; the element size is proved by the
 *     `mov #12 / mla` stride and the byte slot index by `lsl #2`.
 *   - 0x02238d1c and 0x02238d2e are two parallel 6-byte-record tables 0x12 apart.
 *   - 0x02242998 and 0x02242ba0 hold a mode word at +8 and a mode byte at +2.
 *   - 0x02249828 holds a pointer at +4 that indexes a 100-byte-stride table from
 *     record 0 / offset 1.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* 0x02239c10: sound/interrupt context block. */
extern u8 native_data_ov001_02239c10[];
/* 0x0223d904: table of 12-byte records. */
extern u8 native_data_ov001_0223d904[];
/* 0x02238d1c and 0x02238d2e: the two 6-byte-record tables. */
extern u8 native_data_ov001_02238d1c[];
extern u8 native_data_ov001_02238d2e[];
/* 0x02242998: state block whose word at +8 is the live mode. */
extern u8 native_data_ov001_02242998[];
/* 0x02242ba0: state block whose byte at +2 is the live mode. */
extern u8 native_data_ov001_02242ba0[];
/* 0x02249828: block holding a byte-table pointer at +4. */
extern u8 native_data_ov001_02249828[];
/* 0x02239ca4 and 0x02239c9c: two tables of 16-byte records / bytes. */
extern u8 native_data_ov001_02239ca4[];
extern u8 native_data_ov001_02239c9c[];
/* 0x02239d70, 0x02239d74, 0x02239d78: three 12-byte-stride lane tables. */
extern u8 native_data_ov001_02239d70[];
extern u8 native_data_ov001_02239d74[];
extern u8 native_data_ov001_02239d78[];
/* 0x020d3fe0: main-module table of 4-byte entries whose first field is s16. */
extern u8 native_data_020d3fe0[];
/* 0x02235534: first 20-byte mixer slot of the 0x02235530 block. */
extern u8 native_data_ov001_02235534[];
/* 0x02238ad0: availability record; +3 is the published code byte. */
extern u8 native_data_ov001_02238ad0[];
/* 0x0222ed28: link-ready flag block. */
extern u8 native_data_ov001_0222ed28[];
/* 0x022497e8: pending-state record; +1 is the published code byte. */
extern u8 native_data_ov001_022497e8[];
/* 0x0223e118: two-byte mirror block (state byte at 0, mirror at 1). */
extern u8 native_data_ov001_0223e118[];
/* 0x0223a030: base of the 3-word comparison table at +0x208. */
extern u8 native_data_ov001_0223a030[];
/* 0x0222e060: three halfword fields feeding the audio request structs. */
extern u8 native_data_ov001_0222e060[];
/* 0x02238d58: single word slot for the registered handler. */
extern u8 native_data_ov001_02238d58[];
/* 0x0222ec84: session-open byte. */
extern u8 native_data_ov001_0222ec84[];
/* 0x02238d7c: session record; +0x27 is the released marker. */
extern u8 native_data_ov001_02238d7c[];

/* Two halfwords passed by address to the platform audio helper. */
typedef struct {
    u16 lo;
    s16 hi;
} Pair_ov001_p8;

/* Platform services in the main module. */
extern void native_fn_0202871c(void *slot, s32 a, s32 b, s32 c);
extern void native_fn_020287ac(void *slot, s32 a, s32 b, s32 c);
extern s32 native_fn_0204446c(void);
extern s32 native_fn_02044424(s32 unit);
extern void native_fn_0204b53c(s32 slot, void *pair);
extern void native_fn_0203cf9c(s32 handle);

/* Overlay services. */
extern void native_fn_ov001_022028c8(s32 value);
extern void native_fn_ov001_0220459c(s32 payload, s32 mask);
extern s32 native_fn_ov001_021db578(s32 flag);
extern s32 native_fn_ov001_021dc108(u8 *object);
extern u8 *native_fn_ov001_021f1a44(void);
extern s32 native_fn_ov001_02218a54(u32 a, u32 b, u32 c, s32 d, s32 e);
extern s32 native_fn_ov001_02218b54(u32 value, u32 command, s32 mode);
extern s32 native_fn_ov001_0222be7c(void);
extern s32 native_fn_ov001_021dbd8c(u8 *record);
extern s32 native_fn_ov001_021dbe5c(u8 *record);
extern void native_fn_ov001_021f14a4(void);
