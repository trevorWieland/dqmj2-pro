/* Shared declarations for the ov006 live-range family (batch 15).
 *
 * Completes the family whose first member (0x021F6FCC) was recovered in #143 with
 * ops/form_search.py. The winning shape is the switch with an explicit
 * `default: return;` for members whose cases share a tail call, and per-case
 * `return` for the members whose cases each end with their own tail call.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0221c114 / 0x0221c12c: flags set when the second mode is taken. */
extern u8 native_data_ov006_0221c114[];
extern u8 native_data_ov006_0221c12c[];

/* 0x021f2390: returns the mode to dispatch on. */
extern s32 native_fn_ov006_021f2390(void);
/* 0x021ff6d4: applies the mode. */
extern void native_fn_ov006_021ff6d4(s32 mode);
/* 0x021f52cc: runs the follow-up callback. */
extern void native_fn_ov006_021f52cc(void (*callback)(void));
/* 0x021f5dcc / 0x021fd62c: second-mode work. */
extern void native_fn_ov006_021f5dcc(void);
extern void native_fn_ov006_021fd62c(void);
/* 0x02200344: five-argument effect used by the 72-byte member. */
extern void native_fn_02200344(s32 a, s32 b, s32 c, s32 d, s32 e);
extern void native_fn_021f23f4(void);
