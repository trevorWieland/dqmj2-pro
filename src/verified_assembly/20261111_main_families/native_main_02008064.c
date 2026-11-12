/* Countdown delay loop (0x02008064, 12 bytes).
 *
 * Subtracts four from the argument until the unsigned borrow, i.e. spins for
 * arg / 4 iterations; nothing is read or written, so the loop is a delay.
 *
 * Unknowns: the delay's consumer and whether the step of four is a timing unit.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the same loop in C has no side effects and is deleted.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008064 (register u32 count)
{
native_main_02008064_loop:
    subs r0, r0, #4
    bhs native_main_02008064_loop
    bx lr
}
