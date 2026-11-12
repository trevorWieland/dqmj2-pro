/* ov006 row 0x02203d94: 296 bytes.
 *
 * What it does: 142 instructions; 5 call(s) to 0x0200e070, 0x0200e26c, 0x022038d0, +2 more; loops (back edge at +0x1a); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x124 -> constant 0x0221c18c (image word 0x0221c18c)
 *   branch +0x10 -> +0x16
 *   branch +0x14 -> +0x18
 *   branch +0x36 -> +0x58
 *   branch +0x3c -> +0x58
 *   branch +0x56 -> +0x66
 *   back edge +0x64 -> +0x2c
 *   branch +0xde -> +0xe8
 *   branch +0xf2 -> +0x108
 *   branch +0x10a -> +0x120
 *   test +0x34 cmp r2, #0x1
 *   test +0x3a cmp r2, #0x0
 *   test +0x62 cmp r4, #0x4
 *   test +0xdc cmp r5, #0x0
 *   test +0xf0 cmp r1, #0x28
 *   test +0x108 cmp r1, #0x2f
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203d94; the literal pool and
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

extern void native_fn_0200e070(void);
extern void native_fn_0200e26c(void);
extern void native_fn_022038d0(void);
extern void native_fn_020024bc(void);


asm u32 native_ov006_02203d94 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =0x0221c18c
    ldr r0, [r0, #0x4]
    add r0, #0x38
    ldrb r0, [r0, #0]
    lsl r0, r0, #0x1f
    lsr r0, r0, #0x1f
    beq ov006_02203d94_L16
    mov r7, #0x1
    b ov006_02203d94_L18
ov006_02203d94_L16:
    mov r7, #0x0
ov006_02203d94_L18:
    mov r5, #0x0
    blx native_fn_0200e070
    ldr r6, =0x0221c18c
    add r4, r5, #0x0
    ldr r2, [r6, #0x4]
    ldrh r1, [r2, #0x28]
    strh r1, [r2, #0x2c]
    ldrh r1, [r2, #0x2a]
    strh r1, [r2, #0x2e]
ov006_02203d94_L2c:
    ldr r2, [r6, #0x4]
    lsl r1, r0, #0x3
    add r1, r2, r1
    ldrh r2, [r1, #0x4]
    cmp r2, #0x1
    bne ov006_02203d94_L58
    ldrh r2, [r1, #0x6]
    cmp r2, #0x0
    bne ov006_02203d94_L58
    add r0, sp, #0x0
    mov r5, #0x1
    blx native_fn_0200e26c
    ldr r2, =0x0221c18c
    add r1, sp, #0x0
    ldrh r0, [r1, #0]
    ldr r2, [r2, #0x4]
    ldrh r1, [r1, #0x2]
    add r2, #0x28
    bl native_fn_022038d0
    b ov006_02203d94_L66
ov006_02203d94_L58:
    add r0, r0, #0x4
    mov r1, #0x5
    add r4, r4, #0x1
    blx native_fn_020024bc
    cmp r4, #0x4
    blt ov006_02203d94_L2c
ov006_02203d94_L66:
    ldr r0, =0x0221c18c
    add r3, r5, #0x0
    ldr r2, [r0, #0x4]
    mov r4, #0x2
    add r1, r2, #0x0
    add r1, #0x38
    ldrb r1, [r1, #0]
    eor r3, r7
    add r2, #0x38
    bic r1, r4
    add r4, r5, #0x0
    and r4, r3
    lsl r4, r4, #0x18
    lsr r4, r4, #0x18
    lsl r4, r4, #0x1f
    lsr r4, r4, #0x1e
    orr r1, r4
    strb r1, [r2, #0]
    ldr r2, [r0, #0x4]
    and r3, r7
    add r1, r2, #0x0
    add r1, #0x38
    lsl r3, r3, #0x18
    lsr r3, r3, #0x18
    lsl r3, r3, #0x1f
    ldrb r1, [r1, #0]
    mov r4, #0x8
    lsr r3, r3, #0x1c
    bic r1, r4
    orr r1, r3
    add r2, #0x38
    strb r1, [r2, #0]
    ldr r1, [r0, #0x4]
    add r2, r1, #0x0
    add r2, #0x38
    ldrb r3, [r2, #0]
    mov r2, #0x1
    add r1, #0x38
    bic r3, r2
    mov r2, #0x1
    and r2, r5
    orr r2, r3
    strb r2, [r1, #0]
    ldr r2, [r0, #0x4]
    mov r3, #0x4
    add r1, r2, #0x0
    add r1, #0x38
    ldrb r1, [r1, #0]
    bic r1, r3
    add r3, r2, #0x0
    add r3, #0x38
    ldrb r3, [r3, #0]
    add r2, #0x38
    lsl r3, r3, #0x1e
    lsr r3, r3, #0x1f
    lsl r3, r3, #0x1f
    lsr r3, r3, #0x1d
    orr r1, r3
    strb r1, [r2, #0]
    cmp r5, #0x0
    bne ov006_02203d94_Le8
    mov r1, #0x0
    strb r1, [r0, #0x1]
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_02203d94_Le8:
    ldrb r1, [r0, #0x1]
    add r1, r1, #0x1
    strb r1, [r0, #0x1]
    ldrb r1, [r0, #0x1]
    cmp r1, #0x28
    bne ov006_02203d94_L108
    ldr r2, [r0, #0x4]
    add sp, #0x8
    add r0, r2, #0x0
    add r0, #0x38
    ldrb r1, [r0, #0]
    mov r0, #0x4
    add r2, #0x38
    orr r0, r1
    strb r0, [r2, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_02203d94_L108:
    cmp r1, #0x2f
    bne ov006_02203d94_L120
    ldr r3, [r0, #0x4]
    add r1, r3, #0x0
    add r1, #0x38
    ldrb r2, [r1, #0]
    mov r1, #0x4
    add r3, #0x38
    orr r1, r2
    strb r1, [r3, #0]
    mov r1, #0x28
    strb r1, [r0, #0x1]
ov006_02203d94_L120:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
