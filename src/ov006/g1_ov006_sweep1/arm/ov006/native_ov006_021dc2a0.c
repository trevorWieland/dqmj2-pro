/* ov006 row 0x021dc2a0: 280 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x44 -> +0x74
 *   branch +0x60 -> +0x74
 *   branch +0x68 -> +0x9c
 *   branch +0x8c -> +0x9c
 *   branch +0xa0 -> +0x110
 *   branch +0xb4 -> +0xcc
 *   branch +0xbc -> +0xe4
 *   branch +0xc4 -> +0xfc
 *   branch +0xc8 -> +0x110
 *   branch +0xd8 -> +0x110
 *   branch +0xf0 -> +0x110
 *   test +0x40 cmp r0, #4
 *   test +0x5c cmp r0, #6
 *   test +0x64 cmp r4, #1
 *   test +0x88 cmp r0, #7
 *   test +0x90 cmp r4, #0
 *   test +0x9c cmp r6, #0
 *   test +0xb0 cmp r6, #1
 *   test +0xb8 cmp r6, #2
 *   test +0xc0 cmp r6, #3
 *   test +0xcc cmp r0, #1
 *   test +0xd0 cmpne r0, #2
 *   test +0xd4 cmpne r0, #3
 *   test +0xe4 cmp r0, #4
 *   test +0xe8 cmpne r0, #5
 *   test +0xec cmpne r0, #6
 *   test +0xfc cmp r0, #7
 *   test +0x100 cmpne r0, #8
 *   test +0x104 cmpne r0, #9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dc2a0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020449d4(void);
extern void native_fn_02044dc4(void);


asm u32 native_ov006_021dc2a0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r1
    mov r6, r0
    mov r0, r5
    mov r4, r2
    bl native_fn_020449d4
    ldrh r0, [r0, #6]
    mov r0, r0, lsl #19
    movs r0, r0, lsr #19
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #4
    blo ov006_021dc2a0_L74
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #6
    bhi ov006_021dc2a0_L74
    cmp r4, #1
    ble ov006_021dc2a0_L9c
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov006_021dc2a0_L74:
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #7
    blo ov006_021dc2a0_L9c
    cmp r4, #0
    movgt r0, #1
    ldmgtia sp!, {r4, r5, r6, pc}
ov006_021dc2a0_L9c:
    cmp r6, #0
    beq ov006_021dc2a0_L110
    mov r0, r5
    mov r1, r4
    bl native_fn_02044dc4
    cmp r6, #1
    beq ov006_021dc2a0_Lcc
    cmp r6, #2
    beq ov006_021dc2a0_Le4
    cmp r6, #3
    beq ov006_021dc2a0_Lfc
    b ov006_021dc2a0_L110
ov006_021dc2a0_Lcc:
    cmp r0, #1
    cmpne r0, #2
    cmpne r0, #3
    beq ov006_021dc2a0_L110
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov006_021dc2a0_Le4:
    cmp r0, #4
    cmpne r0, #5
    cmpne r0, #6
    beq ov006_021dc2a0_L110
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov006_021dc2a0_Lfc:
    cmp r0, #7
    cmpne r0, #8
    cmpne r0, #9
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
ov006_021dc2a0_L110:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
