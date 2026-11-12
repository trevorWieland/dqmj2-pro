/* Guarded field write into the 0x021c72a0 block (0x02083de8, 32 bytes).
 *
 * Rejects a value whose low five bits are set, otherwise stores it at
 * 0x021c72a0 + 0x1c and reports success. The guard survives as a
 * predicated early return; the store stays unconditional on the fall-through
 * path because the value in r0 is the value being stored.
 *
 * Unknowns: what the block describes and why the caller must pass a 32-byte
 * aligned value.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the naive C form compiles four bytes shorter: mwcc folds both returns into
 * one epilogue and predicates the body (ldreq / streq / moveq / bx).
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;
extern u8 native_data_021c72a0[];


asm u32 native_main_02083de8 (register u32 value)
{
    tst r0, #0x1f
    movne r0, #0
    bxne lr
    ldr r1, =native_data_021c72a0
    str r0, [r1, #0x1c]
    mov r0, #1
    bx lr
}
