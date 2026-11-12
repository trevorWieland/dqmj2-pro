/* Thirty-two-byte block copy with a word tail (0x02008ca4, 56 bytes).
 *
 * Copies 32 bytes per iteration with an eight-register block move, then the
 * remaining whole words one at a time; both loops test before the body.
 *
 * Unknowns: the buffers and why the bulk move is 32 bytes wide.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the register set (r2-r9) and the two predicated loops are a hand-written
 * copy; mwcc's struct copy uses a narrower set and different rotation.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008ca4 (register u32 *src, register u32 *dst, register u32 span)
{
    stmdb sp !, {r4 - r10}
    add r10, r1, r2
    mov r12, r2, lsr #5
    add r12, r1, r12, lsl #5
native_main_02008ca4_bulk:
    cmp r1, r12
    ldmltia r0 !, {r2 - r9}
    stmltia r1 !, {r2 - r9}
    blt native_main_02008ca4_bulk
native_main_02008ca4_tail:
    cmp r1, r10
    ldmltia r0 !, {r2}
    stmltia r1 !, {r2}
    blt native_main_02008ca4_tail
    ldmia sp !, {r4 - r10}
    bx lr
}
