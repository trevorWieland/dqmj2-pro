/* ov000 row 0x021df220: 180 bytes.
 *
 * What it does: 45 instructions; 3 call(s) to 0x021df3bc, 0x021df3bc, 0x021df3bc; no back edge; returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0xac
 *   branch +0x34 -> +0x50
 *   branch +0x54 -> +0x70
 *   branch +0x74 -> +0xa4
 *   branch +0x84 -> +0xa4
 *   branch +0x94 -> +0xa4
 *   test +0x14 cmp r8, #153
 *   test +0x24 cmp r6, #0
 *   test +0x50 cmp r5, #0
 *   test +0x70 cmp r7, #0
 *   test +0x78 cmp r4, #0
 *   test +0x88 cmp r4, #1
 *   test +0x98 cmp r4, #2
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021df220; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021df3bc(void);


asm u32 native_ov000_021df220 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r5, r3
    cmp r8, #153
    bhs ov000_021df220_Lac
    bl native_fn_021df3bc
    ldrh r0, [r0]
    cmp r6, #0
    mov r0, r0, lsl #29
    mov r0, r0, lsr #29
    and r4, r0, #255
    beq ov000_021df220_L50
    mov r0, r8
    bl native_fn_021df3bc
    ldrh r0, [r0]
    mov r0, r0, lsl #25
    mov r0, r0, lsr #28
    strb r0, [r6]
ov000_021df220_L50:
    cmp r5, #0
    beq ov000_021df220_L70
    mov r0, r8
    bl native_fn_021df3bc
    ldrh r0, [r0]
    mov r0, r0, lsl #21
    mov r0, r0, lsr #28
    strb r0, [r5]
ov000_021df220_L70:
    cmp r7, #0
    beq ov000_021df220_La4
    cmp r4, #0
    moveq r0, #115
    streqb r0, [r7]
    beq ov000_021df220_La4
    cmp r4, #1
    moveq r0, #107
    streqb r0, [r7]
    beq ov000_021df220_La4
    cmp r4, #2
    moveq r0, #119
    streqb r0, [r7]
ov000_021df220_La4:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov000_021df220_Lac:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
