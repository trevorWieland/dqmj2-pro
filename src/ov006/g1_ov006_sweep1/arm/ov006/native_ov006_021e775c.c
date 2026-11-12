/* ov006 row 0x021e775c: 200 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc4 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x38 -> +0xb8
 *   branch +0x64 -> +0x7c
 *   branch +0x78 -> +0x84
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmpne r0, #0
 *   test +0x34 cmpne r4, #0
 *   test +0x60 cmp r1, #1
 *   test +0x68 cmp r1, #2
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e775c; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_020470fc(void);
extern void native_fn_02087674(void);
extern void native_fn_02087a48(void);


asm u32 native_ov006_021e775c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r7, r1
    mov r6, r2
    mov r5, r3
    ldr r8, [sp, #0x20]
    bl native_fn_02049ad0
    cmp r0, #0
    ldrne r0, [r0]
    cmpne r0, #0
    ldrne r4, [r0, #0x4]
    cmpne r4, #0
    beq ov006_021e775c_Lb8
    mov r0, r7
    bl native_fn_020470fc
    strh r0, [r4, #108]
    ldr r0, =0x021c9698
    mov r2, r7
    add r1, r4, #60
    bl native_fn_02087674
    ldr r1, [sp, #0x28]
    mov r6, r6, lsl #3
    cmp r1, #1
    beq ov006_021e775c_L7c
    cmp r1, #2
    rsbeq r0, r0, r8, lsl #3
    addeq r0, r0, r0, lsr #31
    addeq r6, r6, r0, asr #1
    b ov006_021e775c_L84
ov006_021e775c_L7c:
    rsb r0, r0, r8, lsl #3
    add r6, r6, r0
ov006_021e775c_L84:
    ldr r0, [sp, #0x24]
    mov r1, r6, lsl #16
    str r0, [sp]
    mov r3, r5, lsl #19
    mov r2, r1, asr #16
    mov r0, r4
    mov r3, r3, asr #16
    mov r1, #0
    str r7, [sp, #0x4]
    bl native_fn_02087a48
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov006_021e775c_Lb8:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
