/* ov006 row 0x021f0744: 440 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1b4 -> constant 0xa6a6a6a6 (image word 0xa6a6a6a6)
 *   branch +0x1a -> +0x22
 *   branch +0x20 -> +0x28
 *   branch +0x30 -> +0x38
 *   back edge +0x54 -> +0x4a
 *   branch +0x72 -> +0x76
 *   branch +0x74 -> +0x190
 *   back edge +0x16c -> +0x162
 *   back edge +0x188 -> +0x17e
 *   back edge +0x18e -> +0x94
 *   branch +0x196 -> +0x19a
 *   back edge +0x198 -> +0x6c
 *   branch +0x1a6 -> +0x1ac
 *   test +0x18 tst r1, r0
 *   test +0x1e tst r0, r2
 *   test +0x2e cmp r0, #0x2
 *   test +0x70 cmp r0, #0x0
 *   test +0x18c cmp r4, #0x0
 *   test +0x1a4 cmp r0, #0x0
 *   0 block transfer(s), 26 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f0744; the literal pool and
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

extern void native_fn_021f0bfc(void);
extern void native_fn_0201b19c(void);
extern void native_fn_02026124(void);
extern void native_fn_021f08fc(void);
extern void native_fn_021f1148(void);
extern void native_fn_0201b248(void);


asm u32 native_ov006_021f0744 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x1a8
    str r0, [sp]
    mov r0, #0x1
    str r0, [sp, #0x1c]
    ldr r0, =0xa6a6a6a6
    add r4, r2, #0x0
    add r5, r1, #0x0
    str r0, [sp, #0x48]
    str r0, [sp, #0x4c]
    mov r0, #0x7
    add r1, r4, #0x0
    tst r1, r0
    bne ov006_021f0744_L22
    ldr r2, [sp, #0x1c0]
    tst r0, r2
    beq ov006_021f0744_L28
ov006_021f0744_L22:
    add sp, #0x1a8
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f0744_L28:
    sub r0, r4, #0x1
    lsr r0, r0, #0x3
    str r0, [sp, #0x14]
    cmp r0, #0x2
    bge ov006_021f0744_L38
    add sp, #0x1a8
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f0744_L38:
    add r0, sp, #0x68
    add r1, r3, #0x0
    lsl r2, r2, #0x3
    bl native_fn_021f0bfc
    str r0, [sp, #0x20]
    add r3, sp, #0x58
    add r2, r5, #0x0
    mov r1, #0x8
ov006_021f0744_L4a:
    ldrb r0, [r2, #0]
    add r2, r2, #0x1
    strb r0, [r3, #0]
    add r3, r3, #0x1
    sub r1, r1, #0x1
    bne ov006_021f0744_L4a
    add r5, #0x8
    ldr r0, [sp]
    add r1, r5, #0x0
    sub r2, r4, #0x1
    blx native_fn_0201b19c
    mov r0, #0x5
    str r0, [sp, #0x24]
    ldr r0, [sp, #0x14]
    asr r0, r0, #0x1f
    str r0, [sp, #0x18]
ov006_021f0744_L6c:
    ldr r4, [sp, #0x14]
    add r0, r4, #0x0
    cmp r0, #0x0
    bgt ov006_021f0744_L76
    b ov006_021f0744_L190
ov006_021f0744_L76:
    ldr r2, [sp, #0x24]
    ldr r1, [sp, #0x18]
    asr r3, r2, #0x1f
    blx native_fn_02026124
    str r0, [sp, #0xc]
    mov r0, #0x0
    str r1, [sp, #0x8]
    str r0, [sp, #0x2c]
    mov r0, #0x0
    mov r1, #0x0
    str r0, [sp, #0x34]
    add r0, r1, #0x0
    orr r0, r1
    str r0, [sp, #0x40]
ov006_021f0744_L94:
    ldr r0, [sp, #0xc]
    asr r1, r4, #0x1f
    add r5, r4, r0
    ldr r0, [sp, #0x8]
    adc r1, r0
    mov r0, #0xff
    lsl r0, r0, #0x18
    and r0, r1
    lsr r0, r0, #0x18
    str r0, [sp, #0x28]
    mov r0, #0xff
    lsl r0, r0, #0x10
    and r0, r1
    lsr r0, r0, #0x8
    str r0, [sp, #0x30]
    mov r0, #0xff
    lsl r0, r0, #0x8
    add r2, r1, #0x0
    and r2, r0
    mov r0, #0x0
    add r3, r5, #0x0
    and r3, r0
    lsl r0, r2, #0x8
    lsr r3, r3, #0x18
    orr r3, r0
    lsr r0, r2, #0x18
    str r0, [sp, #0x38]
    mov r0, #0xff
    mov r2, #0x0
    and r0, r1
    and r2, r5
    lsl r6, r0, #0x18
    lsr r2, r2, #0x8
    str r2, [sp, #0x44]
    orr r2, r6
    lsr r0, r0, #0x8
    str r2, [sp, #0x44]
    str r0, [sp, #0x3c]
    mov r0, #0x0
    add r2, r1, #0x0
    and r2, r0
    mov r0, #0xff
    lsl r0, r0, #0x18
    and r0, r5
    lsr r6, r0, #0x18
    lsl r0, r0, #0x8
    mov r12, r0
    mov r0, #0x0
    and r1, r0
    mov r0, #0xff
    lsl r0, r0, #0x10
    lsl r2, r2, #0x8
    and r0, r5
    orr r2, r6
    lsr r6, r0, #0x8
    lsl r7, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x18
    and r0, r5
    orr r1, r6
    lsl r6, r0, #0x18
    mov r0, #0xff
    lsl r0, r0, #0x8
    and r0, r5
    lsl r0, r0, #0x8
    orr r0, r6
    orr r1, r0
    ldr r0, [sp, #0x40]
    add r5, r7, #0x0
    orr r5, r0
    mov r0, r12
    orr r1, r2
    add r2, r0, #0x0
    ldr r0, [sp, #0x3c]
    orr r2, r5
    orr r1, r0
    ldr r0, [sp, #0x44]
    orr r2, r0
    ldr r0, [sp, #0x38]
    orr r2, r3
    orr r1, r0
    ldr r0, [sp, #0x34]
    orr r1, r0
    ldr r0, [sp, #0x30]
    orr r2, r0
    ldr r0, [sp, #0x2c]
    orr r1, r0
    ldr r0, [sp, #0x28]
    str r1, [sp, #0x54]
    orr r0, r2
    str r0, [sp, #0x50]
    add r0, sp, #0x58
    add r1, sp, #0x50
    add r2, r0, #0x0
    bl native_fn_021f08fc
    sub r0, r4, #0x1
    lsl r1, r0, #0x3
    ldr r0, [sp]
    add r2, sp, #0x60
    add r5, r0, r1
    add r3, r5, #0x0
    mov r1, #0x8
ov006_021f0744_L162:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f0744_L162
    add r2, sp, #0x58
    ldr r1, [sp, #0x20]
    add r0, sp, #0x68
    add r3, r2, #0x0
    bl native_fn_021f1148
    add r2, sp, #0x60
    mov r1, #0x8
ov006_021f0744_L17e:
    ldrb r0, [r2, #0]
    add r2, r2, #0x1
    strb r0, [r5, #0]
    add r5, r5, #0x1
    sub r1, r1, #0x1
    bne ov006_021f0744_L17e
    sub r4, r4, #0x1
    cmp r4, #0x0
    bgt ov006_021f0744_L94
ov006_021f0744_L190:
    ldr r0, [sp, #0x24]
    sub r0, r0, #0x1
    str r0, [sp, #0x24]
    bmi ov006_021f0744_L19a
    b ov006_021f0744_L6c
ov006_021f0744_L19a:
    add r0, sp, #0x48
    add r1, sp, #0x58
    mov r2, #0x8
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_021f0744_L1ac
    mov r0, #0x0
    str r0, [sp, #0x1c]
ov006_021f0744_L1ac:
    ldr r0, [sp, #0x1c]
    add sp, #0x1a8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
