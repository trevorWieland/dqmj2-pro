/* ov000 row 0x021e7b60: 60 bytes.
 *
 * Decoded shape: 1 call and a loop.
 *
 *   pool +0x38 -> native_data_022351ec (image word 0x022351ec)
 *   call +0x1c -> native_fn_0205e73c
 *   back edge +0x2c -> +0x10
 *   test +0x14 cmp r0, #0
 *   test +0x28 cmp r6, #0x20
 *   memory +0x10 ldr r0, [r4, r6, lsl #2]
 *
 * Why transcribed rather than written as C: AND of the probe results allocates the accumulator late (64 vs
 * 60 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e7b60; the literal pool and
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

extern u8 native_data_022351ec[];
extern void native_fn_0205e73c(void);


asm u32 native_ov000_021e7b60 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r4, =native_data_022351ec
    mov r5, #1
    mov r6, #0
ov000_021e7b60_L10:
    ldr r0, [r4, r6, lsl #2]
    cmp r0, #0
    beq ov000_021e7b60_L24
    bl native_fn_0205e73c
    and r5, r5, r0
ov000_021e7b60_L24:
    add r6, r6, #1
    cmp r6, #0x20
    blt ov000_021e7b60_L10
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
