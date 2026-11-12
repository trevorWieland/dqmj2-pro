/* ov000 row 0x0221cf24: 60 bytes.
 *
 * Decoded shape: 1 call and a loop.
 *
 *   pool +0x34 -> native_data_022461c4 (image word 0x022461c4)
 *   pool +0x38 -> native_data_022461d4 (image word 0x022461d4)
 *   call +0x20 -> native_fn_0221cf84
 *   back edge +0x2c -> +0x18
 *   test +0x0c cmp r0, #0
 *   test +0x28 cmp r0, #0
 *   memory +0x08 ldr r0, [r4, #0xc]
 *   memory +0x1c ldrsb r0, [r0, #-1]
 *   memory +0x24 ldr r0, [r4, #0xc]
 *
 * Why transcribed rather than written as C: drain loop re-reads the depth one instruction earlier (52 vs 60
 * B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221cf24; the literal pool and
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

extern u8 native_data_022461c4[];
extern u8 native_data_022461d4[];
extern void native_fn_0221cf84(void);


asm u32 native_ov000_0221cf24 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =native_data_022461c4
    ldr r0, [r4, #0xc]
    cmp r0, #0
    ldmleia sp!, {r3, r4, r5, pc}
    ldr r5, =native_data_022461d4
ov000_0221cf24_L18:
    add r0, r5, r0
    ldrsb r0, [r0, #-1]
    bl native_fn_0221cf84
    ldr r0, [r4, #0xc]
    cmp r0, #0
    bgt ov000_0221cf24_L18
    ldmia sp!, {r3, r4, r5, pc}
}
