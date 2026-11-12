/* ov000 row 0x022187b8: 72 bytes.
 *
 * What it does: Mode dispatch: for modes 0 and 2 clears the halfwords at
 * block+0x38/+0x3a, otherwise copies two record bytes there.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x44 -> native_data_02245e54 (image word 0x02245e54)
 *   pool +0x44 -> native_data_02245e54 (image word 0x02245e54)
 *   call +0x04 -> native_fn_02066c3c
 *   test +0x0c cmp r1, #0
 *   test +0x10 cmpne r1, #2
 *   memory +0x08 ldrb r1, [r0]
 *   memory +0x20 strh r1, [r0, #0x38]
 *   memory +0x24 strh r1, [r0, #0x3a]
 *   memory +0x2c ldrb r2, [r0, #1]
 *   memory +0x34 strh r2, [r1, #0x38]
 *   memory +0x38 ldrb r0, [r0, #2]
 *   memory +0x3c strh r0, [r1, #0x3a]
 *   4 store instruction(s)
 *
 * Why transcribed rather than written as C: frame byte tests if-converted instead of the image branch (C 64
 * B vs image 72 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022187b8; the literal pool and
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

extern u8 native_data_02245e54[];
extern void native_fn_02066c3c(void);


asm u32 native_ov000_022187b8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02066c3c
    ldrb r1, [r0]
    cmp r1, #0
    cmpne r1, #2
    bne ov000_022187b8_L2c
    ldr r0, =native_data_02245e54
    mov r1, #0
    strh r1, [r0, #0x38]
    strh r1, [r0, #0x3a]
    ldmia sp!, {r3, pc}
ov000_022187b8_L2c:
    ldrb r2, [r0, #1]
    ldr r1, =native_data_02245e54
    strh r2, [r1, #0x38]
    ldrb r0, [r0, #2]
    strh r0, [r1, #0x3a]
    ldmia sp!, {r3, pc}
}
