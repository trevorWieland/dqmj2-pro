/* Shared declarations for the ov006 BLX packet (batch 10).
 *
 * BLX-lane verdict and the two rules this row proved:
 *   - the callee mode for R_ARM_THM_CALL is measured from the image word, so a
 *     lx site is an ordinary BLX-immediate call, not a toolchain blocker
 *     (ops/thumb_branch.py, pinned by public_tools/test_thumb_branches.py).
 *   - a global read as *native_data_<addr> compiles to TWO dereferences when the
 *     symbol is declared as a pointer; declare it as the scalar it is
 *     (xtern u32 native_data_<addr>;) to get the single measured load.
 */

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0221c144: block whose first word is the frame base for 0x021feb34. */
extern u32 native_data_ov006_0221c144;

extern s32 native_fn_02012b28(u8 *table, u32 offset);
extern void native_fn_02005d50(u32 mode);
extern void native_fn_02005d20();
