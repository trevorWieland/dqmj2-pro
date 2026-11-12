/* ov006 row 0x021f058c: 440 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1b4 -> constant 0xa6a6a6a6 (image word 0xa6a6a6a6)
 *   branch +0x16 -> +0x1e
 *   branch +0x1c -> +0x24
 *   branch +0x2a -> +0x32
 *   back edge +0x5a -> +0x50
 *   branch +0x6c -> +0x70
 *   branch +0x6e -> +0x18c
 *   back edge +0xa4 -> +0x9a
 *   back edge +0x182 -> +0x178
 *   back edge +0x18a -> +0x8e
 *   branch +0x194 -> +0x198
 *   back edge +0x196 -> +0x66
 *   back edge +0x1aa -> +0x19c
 *   test +0x14 tst r1, r0
 *   test +0x1a tst r0, r2
 *   test +0x28 cmp r0, #0x2
 *   test +0x6a cmp r0, #0x1
 *   test +0x188 cmp r4, r0
 *   test +0x192 cmp r0, #0x6
 *   0 block transfer(s), 28 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f058c; the literal pool and
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

extern void native_fn_021f0944(void);
extern void native_fn_0201b19c(void);
extern void native_fn_02026124(void);
extern void native_fn_021f0d8c(void);
extern void native_fn_021f08fc(void);


asm u32 native_ov006_021f058c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x1a8
    str r0, [sp]
    ldr r0, =0xa6a6a6a6
    add r4, r2, #0x0
    add r5, r1, #0x0
    str r0, [sp, #0x48]
    str r0, [sp, #0x4c]
    mov r0, #0x7
    add r1, r4, #0x0
    tst r1, r0
    bne ov006_021f058c_L1e
    ldr r2, [sp, #0x1c0]
    tst r0, r2
    beq ov006_021f058c_L24
ov006_021f058c_L1e:
    add sp, #0x1a8
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f058c_L24:
    lsr r0, r4, #0x3
    str r0, [sp, #0x14]
    cmp r0, #0x2
    bge ov006_021f058c_L32
    add sp, #0x1a8
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f058c_L32:
    add r0, sp, #0x68
    add r1, r3, #0x0
    lsl r2, r2, #0x3
    bl native_fn_021f0944
    str r0, [sp, #0x1c]
    ldr r0, [sp]
    add r1, r5, #0x0
    add r0, #0x8
    add r2, r4, #0x0
    blx native_fn_0201b19c
    add r3, sp, #0x58
    add r2, sp, #0x48
    mov r1, #0x8
ov006_021f058c_L50:
    ldrb r0, [r2, #0]
    add r2, r2, #0x1
    strb r0, [r3, #0]
    add r3, r3, #0x1
    sub r1, r1, #0x1
    bne ov006_021f058c_L50
    mov r0, #0x0
    str r0, [sp, #0x20]
    ldr r0, [sp, #0x14]
    asr r0, r0, #0x1f
    str r0, [sp, #0x18]
ov006_021f058c_L66:
    ldr r0, [sp, #0x14]
    mov r4, #0x1
    cmp r0, #0x1
    bge ov006_021f058c_L70
    b ov006_021f058c_L18c
ov006_021f058c_L70:
    ldr r2, [sp, #0x20]
    ldr r1, [sp, #0x18]
    asr r3, r2, #0x1f
    blx native_fn_02026124
    str r0, [sp, #0xc]
    mov r0, #0x0
    str r1, [sp, #0x8]
    str r0, [sp, #0x28]
    mov r0, #0x0
    mov r1, #0x0
    str r0, [sp, #0x30]
    add r0, r1, #0x0
    orr r0, r1
    str r0, [sp, #0x40]
ov006_021f058c_L8e:
    ldr r0, [sp]
    lsl r1, r4, #0x3
    add r5, r0, r1
    add r3, r5, #0x0
    add r2, sp, #0x60
    mov r1, #0x8
ov006_021f058c_L9a:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021f058c_L9a
    add r2, sp, #0x58
    ldr r1, [sp, #0x1c]
    add r0, sp, #0x68
    add r3, r2, #0x0
    bl native_fn_021f0d8c
    ldr r0, [sp, #0xc]
    asr r1, r4, #0x1f
    add r3, r4, r0
    ldr r0, [sp, #0x8]
    adc r1, r0
    mov r0, #0xff
    lsl r0, r0, #0x18
    and r0, r1
    lsr r0, r0, #0x18
    str r0, [sp, #0x24]
    mov r0, #0xff
    lsl r0, r0, #0x10
    and r0, r1
    lsr r0, r0, #0x8
    str r0, [sp, #0x2c]
    mov r0, #0xff
    lsl r0, r0, #0x8
    mov r2, #0x0
    and r0, r1
    and r2, r3
    lsl r6, r0, #0x8
    lsr r2, r2, #0x18
    str r2, [sp, #0x34]
    orr r2, r6
    lsr r0, r0, #0x18
    str r2, [sp, #0x34]
    str r0, [sp, #0x38]
    mov r0, #0xff
    mov r2, #0x0
    and r0, r1
    and r2, r3
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
    and r0, r3
    lsr r6, r0, #0x18
    lsl r0, r0, #0x8
    mov r12, r0
    mov r0, #0x0
    and r1, r0
    mov r0, #0xff
    lsl r0, r0, #0x10
    lsl r2, r2, #0x8
    and r0, r3
    orr r2, r6
    lsr r6, r0, #0x8
    lsl r7, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x18
    and r0, r3
    orr r1, r6
    lsl r6, r0, #0x18
    mov r0, #0xff
    lsl r0, r0, #0x8
    and r0, r3
    lsl r0, r0, #0x8
    orr r0, r6
    orr r1, r0
    ldr r0, [sp, #0x40]
    add r3, r7, #0x0
    orr r3, r0
    mov r0, r12
    orr r1, r2
    add r2, r0, #0x0
    ldr r0, [sp, #0x3c]
    orr r2, r3
    orr r1, r0
    ldr r0, [sp, #0x44]
    orr r2, r0
    ldr r0, [sp, #0x38]
    orr r1, r0
    ldr r0, [sp, #0x34]
    orr r2, r0
    ldr r0, [sp, #0x30]
    orr r1, r0
    ldr r0, [sp, #0x2c]
    orr r2, r0
    ldr r0, [sp, #0x28]
    orr r1, r0
    ldr r0, [sp, #0x24]
    str r1, [sp, #0x54]
    orr r0, r2
    str r0, [sp, #0x50]
    add r0, sp, #0x58
    add r1, sp, #0x50
    add r2, r0, #0x0
    bl native_fn_021f08fc
    add r2, sp, #0x60
    mov r1, #0x8
ov006_021f058c_L178:
    ldrb r0, [r2, #0]
    add r2, r2, #0x1
    strb r0, [r5, #0]
    add r5, r5, #0x1
    sub r1, r1, #0x1
    bne ov006_021f058c_L178
    ldr r0, [sp, #0x14]
    add r4, r4, #0x1
    cmp r4, r0
    ble ov006_021f058c_L8e
ov006_021f058c_L18c:
    ldr r0, [sp, #0x20]
    add r0, r0, #0x1
    str r0, [sp, #0x20]
    cmp r0, #0x6
    bge ov006_021f058c_L198
    b ov006_021f058c_L66
ov006_021f058c_L198:
    add r3, sp, #0x58
    mov r2, #0x8
ov006_021f058c_L19c:
    ldrb r1, [r3, #0]
    ldr r0, [sp]
    add r3, r3, #0x1
    strb r1, [r0, #0]
    add r0, r0, #0x1
    str r0, [sp]
    sub r2, r2, #0x1
    bne ov006_021f058c_L19c
    mov r0, #0x1
    add sp, #0x1a8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
