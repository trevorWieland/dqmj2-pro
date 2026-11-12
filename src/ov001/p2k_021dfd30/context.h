/* Shared declarations for the ov001 handler/sound packet (ov001-u1).
 *
 * Overlay globals are declared as flat byte arrays and addressed with their
 * measured field offsets. Every symbol name carries its measured address, so the
 * comparison harness resolves relocations without any side table.
 *
 * Reusable mechanism facts for this module (each one cost a failed draft):
 *   - the recorded-flag bitmap at record+0x3ED is byte indexed: flag / 8 picks
 *     the byte and flag % 8 the bit. A /32 draft is four bytes too long, and the
 *     signed-division bias shift (lsr #29 rather than #27) proves the divisor.
 *   - 0x0206c718 takes six arguments: slot five is a literal zero and slot six is
 *     the entry index (9 power-on, 0xC looped, 0x7F/6 selected by the sibling).
 *   - the sound context block at 0x02239c10 keeps the mixer handle at 0x24 and
 *     the two stream slots released by 0x021feb50 at 0x44 and 0x48.
 *   - 0x02239d70 / 0x02239d78 / 0x02239d78 record lanes are addressed as three
 *     separate word bases plus index * 0x0C, not as one base plus offsets.
 *   - the six-slot handler table at 0x02238950 is 4 bytes per slot and the slot
 *     index must be declared *after* the liveness guard for the frame to match.
 *   - 0x02065d88 returns the handle's record; 0x2F is the mode byte and 0x30 the
 *     cap byte that forces the caller's selection to 4.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* 0x02239c10: sound context block. */
extern u8 native_data_ov001_02239c10[];
/* 0x02238950: six-slot handler table, 4 bytes per slot. */
extern u8 native_data_02238950[];

extern void native_fn_0202a498(s32 target);
extern void native_fn_0206c718(s32 handle, s32 bank, s32 arg0, s32 arg1,
                               s32 pad, s32 entry);
extern u8 *native_fn_02065d88(s32 handle);
extern s32 ov001_side_slot_record_021db438();
extern s32 ov001_record_is_active_021db8d0();
extern void native_fn_ov001_0220468c();
extern void native_fn_ov001_022046bc();
extern void native_fn_ov001_0220b738(u8 value);
extern void native_fn_ov001_0220b75c(s32 handle);
extern void native_fn_ov001_0220b780(u8 value);
