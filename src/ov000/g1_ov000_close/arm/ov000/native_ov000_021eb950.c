/* ov000 row 0x021eb950: 152 bytes.
 *
 * What it does: 35 instructions; 3 call(s) to 0x020633b0, 0x021ec2a0, 0x021eb9b8; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> constant 0x02236980 (image word 0x02236980)
 *   pool +0x90 -> constant 0x0098967f (image word 0x0098967f)
 *   pool +0x94 -> constant 0x000f423f (image word 0x000f423f)
 *   branch +0x18 -> +0x64
 *   branch +0x20 -> +0x30
 *   branch +0x28 -> +0x4c
 *   branch +0x2c -> +0x64
 *   branch +0x48 -> +0x64
 *   back edge +0x84 -> +0x68
 *   test +0x14 cmp r1, #0
 *   test +0x1c cmp r1, #1
 *   test +0x24 cmp r1, #2
 *   test +0x34 cmp r1, #0
 *   test +0x40 cmpne r1, r0
 *   test +0x50 cmp r1, #0
 *   test +0x5c cmpne r1, r0
 *   test +0x80 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021eb950; the literal pool and
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

extern void native_fn_020633b0(void);
extern void native_fn_021ec2a0(void);


asm u32 native_ov000_021eb950 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_020633b0
    ldr r1, =0x02236980
    mov r4, #1
    ldrsb r1, [r1, #32]
    cmp r1, #0
    beq ov000_021eb950_L64
    cmp r1, #1
    beq ov000_021eb950_L30
    cmp r1, #2
    beq ov000_021eb950_L4c
    b ov000_021eb950_L64
ov000_021eb950_L30:
    ldr r1, [r0, #0x14]
    cmp r1, #0
    ldrne r1, [r0, #0x18]
    ldrne r0, =0x0098967f
    cmpne r1, r0
    moveq r4, #3
    b ov000_021eb950_L64
ov000_021eb950_L4c:
    ldr r1, [r0, #0x18]
    cmp r1, #0
    ldrne r1, [r0, #0x14]
    ldrne r0, =0x000f423f
    cmpne r1, r0
    moveq r4, #3
ov000_021eb950_L64:
    mov r5, #0
ov000_021eb950_L68:
    mov r0, r5
    mov r1, r4
    bl native_fn_021ec2a0
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #3
    blt ov000_021eb950_L68
    ldmia sp!, {r3, r4, r5, pc}
}
