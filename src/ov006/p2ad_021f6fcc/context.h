/* Shared declarations for the ov006 live-range packet (batch 14).
 *
 * Found by ops/form_search.py. The row's residual was a live-range question (where
 * the helper's result lives), and the search space contained the answer: a switch
 * over the call expression with an explicit `default: return;`, so the "neither"
 * path falls out before the shared tail call.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0221c0b8: flag set when the second mode is taken. */
extern u8 native_data_ov006_0221c0b8;
/* 0x021f2390: returns the mode to dispatch on (0, 1 or neither). */
extern s32 native_fn_ov006_021f2390(void);
/* 0x021ff6d4: applies the mode. */
extern void native_fn_ov006_021ff6d4(s32 mode);
/* 0x021f52cc: runs the follow-up callback. */
extern void native_fn_ov006_021f52cc(void (*callback)(void));
