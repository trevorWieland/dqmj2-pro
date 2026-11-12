/* Display-control word pair writer, five pairs (0x020010b8, 40 bytes).
 *
 * The same alternating 0x1000 / 0 writer as 0x02000ce8 with five two-word
 * block stores and no trailing field write.
 *
 * Unknowns: the hardware window and why this variant stores one pair more.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; as 0x02000ce8: the C form uses single stores and a different constant order.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_020010b8 (register u32 *window)
{
    mov r2, #4096
    mov r3, #0
    stmia r0 !, {r2, r3}
    mov r1, #0
    stmia r0 !, {r1, r3}
    stmia r0 !, {r2, r3}
    stmia r0 !, {r1, r3}
    stmia r0 !, {r2, r3}
    stmia r0 !, {r1, r3}
    bx lr
}
