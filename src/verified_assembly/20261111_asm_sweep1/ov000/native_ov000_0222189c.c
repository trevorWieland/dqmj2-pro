/* ov000 row 0x0222189c: 56 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x34 -> native_data_02246428 (image word 0x02246428)
 *   pool +0x34 -> native_data_02246428 (image word 0x02246428)
 *   call +0x1c -> native_fn_0203cf9c
 *   test +0x0c cmp r1, #0
 *   memory +0x08 ldr r1, [r0]
 *   memory +0x28 str r1, [r0]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: same handle allocation (2-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222189c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_02246428[];
extern void native_fn_0203cf9c(void);


asm u32 native_ov000_0222189c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_02246428
    ldr r1, [r0]
    cmp r1, #0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    mov r0, #1
    bl native_fn_0203cf9c
    ldr r0, =native_data_02246428
    mov r1, #0
    str r1, [r0]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
