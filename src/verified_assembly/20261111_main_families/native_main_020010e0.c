/* Three-word to four-word expand with a guard word (0x020010e0, 52 bytes).
 *
 * Loads three words and stores them plus a guard word, four times: the first
 * three stores use a zero guard and the last one 0x1000.
 *
 * Unknowns: the source record layout and what the 0x1000 guard terminates.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the expander interleaves block loads and stores; C splits it into separate
 * copies and loses the guard scheduling.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_020010e0 (register u32 *src, register u32 *dst)
{
    stmdb sp !, {r4}
    mov r12, #0
    ldmia r0 !, {r2, r3, r4}
    stmia r1 !, {r2, r3, r4, r12}
    ldmia r0 !, {r2, r3, r4}
    stmia r1 !, {r2, r3, r4, r12}
    ldmia r0 !, {r2, r3, r4}
    stmia r1 !, {r2, r3, r4, r12}
    mov r12, #4096
    ldmia r0 !, {r2, r3, r4}
    stmia r1 !, {r2, r3, r4, r12}
    ldmia sp !, {r4}
    bx lr
}
