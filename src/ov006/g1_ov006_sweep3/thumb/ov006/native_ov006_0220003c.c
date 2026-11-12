/* ov006 row 0x0220003c: 92 bytes.
 *
 * What it does: 37 instructions; 5 call(s) to 0x02200194, 0x02200098, 0x021fff6c, +2 more; loops (back edge at +0x42); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x54 -> constant 0x0221c158 (image word 0x0221c158)
 *   pool +0x58 -> constant 0x00001b94 (image word 0x00001b94)
 *   branch +0x06 -> +0x52
 *   branch +0x12 -> +0x20
 *   branch +0x18 -> +0x52
 *   branch +0x24 -> +0x52
 *   branch +0x2a -> +0x48
 *   branch +0x2e -> +0x4e
 *   branch +0x36 -> +0x3e
 *   branch +0x3c -> +0x42
 *   test +0x04 cmp r1, #0x0
 *   test +0x10 cmp r3, #0x0
 *   test +0x16 cmp r0, #0x2
 *   test +0x22 cmp r3, #0x26
 *   test +0x28 cmp r3, #0x4
 *   test +0x2c cmp r3, #0x5
 *   test +0x34 cmp r1, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220003c; the literal pool and
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

extern void native_fn_02200194(void);
extern void native_fn_02200098(void);
extern void native_fn_021fff6c(void);
extern void native_fn_02008430(void);


asm u32 native_ov006_0220003c (register u32 a0)
{
    push {r3, lr}
    ldrh r1, [r0, #0x2]
    cmp r1, #0x0
    bne ov006_0220003c_L52
    ldr r1, =0x0221c158
    ldr r2, =0x00001b94
    ldr r1, [r1, #0]
    ldrb r3, [r1, r2]
    cmp r3, #0x0
    beq ov006_0220003c_L20
    ldrh r0, [r0, #0]
    cmp r0, #0x2
    bne ov006_0220003c_L52
    mov r0, #0x2
    strb r0, [r1, r2]
    pop {r3, pc}
ov006_0220003c_L20:
    ldrh r3, [r0, #0]
    cmp r3, #0x26
    bne ov006_0220003c_L52
    ldrh r3, [r0, #0x8]
    cmp r3, #0x4
    beq ov006_0220003c_L48
    cmp r3, #0x5
    bne ov006_0220003c_L4e
    add r2, r2, #0x2
    ldrb r1, [r1, r2]
    cmp r1, #0x0
    beq ov006_0220003c_L3e
    bl native_fn_02200194
    b ov006_0220003c_L42
ov006_0220003c_L3e:
    bl native_fn_02200098
ov006_0220003c_L42:
    bl native_fn_021fff6c
    pop {r3, pc}
ov006_0220003c_L48:
    bl native_fn_021fff6c
    pop {r3, pc}
ov006_0220003c_L4e:
    blx native_fn_02008430
ov006_0220003c_L52:
    pop {r3, pc}
}
