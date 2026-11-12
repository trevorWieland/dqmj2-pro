/* Display-control word pair writer (0x02000ce8, 36 bytes).
 *
 * Writes 0x1000 into the word at +0x20 and then alternates 0x1000 / 0 through
 * four two-word block stores, ending 11 words past the argument.
 *
 * Unknowns: which hardware window the argument points at and what 0x1000 selects.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the mixed constant/zero block stores are a hand-written initialiser; the C
 * form lowers to single str instructions.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02000ce8 (register u32 *window)
{
    mov r2, #4096
    str r2, [r0, #0x20]
    mov r3, #0
    stmia r0 !, {r2, r3}
    mov r1, #0
    stmia r0 !, {r1, r3}
    stmia r0 !, {r2, r3}
    stmia r0 !, {r1, r3}
    bx lr
}
