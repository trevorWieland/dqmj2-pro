/* ov000 row 0x022260a8: 68 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x3c -> native_data_022468b8 (image word 0x022468b8)
 *   pool +0x40 -> native_data_02246aa8 (image word 0x02246aa8)
 *   pool +0x3c -> native_data_022468b8 (image word 0x022468b8)
 *   call +0x28 -> native_fn_02224b84
 *   test +0x10 cmp r0, #0x1b
 *   test +0x1c cmp r0, #0
 *   memory +0x0c ldrsb r0, [r0, #0x18]
 *   memory +0x18 ldrb r0, [r1, #0x193]
 *   memory +0x30 str r0, [r1, #0x14]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: condition block loads one literal later than the image (23-byte
 * diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022260a8; the literal pool and
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

extern u8 native_data_022468b8[];
extern u8 native_data_02246aa8[];
extern void native_fn_02224b84(void);


asm u32 native_ov000_022260a8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_022468b8
    ldr r1, =native_data_02246aa8
    ldrsb r0, [r0, #0x18]
    cmp r0, #0x1b
    bne ov000_022260a8_L34
    ldrb r0, [r1, #0x193]
    cmp r0, #0
    beq ov000_022260a8_L34
    mov r0, #0
    bl native_fn_02224b84
    ldr r1, =native_data_022468b8
    str r0, [r1, #0x14]
ov000_022260a8_L34:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
