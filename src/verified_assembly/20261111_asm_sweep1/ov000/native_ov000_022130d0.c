/* ov000 row 0x022130d0: 60 bytes.
 *
 * Decoded shape: 1 call and a loop.
 *
 *   pool +0x38 -> native_data_02243e3c (image word 0x02243e3c)
 *   call +0x14 -> native_fn_02212f80
 *   back edge +0x2c -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x24 cmp r4, #0x10
 *
 * Why transcribed rather than written as C: record-pointer walk allocates the count across the call (64 vs
 * 60 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022130d0; the literal pool and
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

extern u8 native_data_02243e3c[];
extern void native_fn_02212f80(void);


asm u32 native_ov000_022130d0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, #0
    ldr r6, =native_data_02243e3c
    mov r4, r5
ov000_022130d0_L10:
    mov r0, r6
    bl native_fn_02212f80
    cmp r0, #0
    add r4, r4, #1
    addne r5, r5, #1
    cmp r4, #0x10
    add r6, r6, #0x10c
    blt ov000_022130d0_L10
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
