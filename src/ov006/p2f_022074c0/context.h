/* Shared declarations for the ov006 flow packet (ov006-u1).
 *
 * Overlay globals are declared as flat byte arrays and addressed with their
 * measured field offsets, matching the shape the accepted ov006 sources use.
 * Every symbol name carries its measured address, so the comparison harness
 * resolves relocations without any side table.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* 0x0220bc24: decoder table indexed by the stream word. */
extern u8 native_data_ov006_0220bc24[];
/* 0x0221c27c: stream word holding the decoder index at 0x08. */
extern u8 native_data_ov006_0221c27c[];
/* 0x0221c2c0 / 0x0221c308 / 0x0221c350: resource queues retired per frame. */
extern u8 native_data_ov006_0221c2c0[];
extern u8 native_data_ov006_0221c308[];
extern u8 native_data_ov006_0221c350[];
/* 0x0220d108 / 0x02218d70: sound state words; 0x08 is the pending id. */
extern u8 native_data_ov006_0220d108[];
extern u8 native_data_ov006_02218d70[];
/* 0x02207db8 / 0x02207da0: sound block headers. */
extern u8 native_data_ov006_02207db8[];
extern u8 native_data_ov006_02207da0[];

extern void native_fn_0205f9e4(u8 *queue);
extern void native_fn_02008d78(u8 *dst, u32 value, u32 size);
extern s32 native_fn_020baf04(u8 *params);
extern void native_fn_ov006_021e3cd4();
extern void native_fn_ov006_021e3cd8();
extern void native_fn_ov006_021e3f28(u32 id);
extern s32 native_fn_ov006_021e5870(u32 size, u8 *state, u32 params_size, s32 mixer);
extern u32 native_fn_ov006_021e65a4();
extern void native_fn_ov006_021e7a60(u32 channel, s32 value);
extern void native_fn_ov006_021e7d98(u32 value);
extern void native_fn_ov006_021e7e28();
extern void native_fn_ov006_021e7e78(u32 value);
extern void native_fn_ov006_021e9148(u8 *block, u32 value);
