/* Shared declarations for the ov001 bitmap packet (ov001-u1).
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

/* 0x02239c10: sound context block; 0x24 is the handle the mixer is set from. */
extern u8 native_data_ov001_02239c10[];

extern s32 ov001_record_is_active_021db8d0();
extern void native_fn_0206c718(s32 handle, s32 bank, s32 arg0, s32 arg1,
                               s32 pad, s32 entry);
