/* ov006 row 0x02200aa8: 176 bytes.
 *
 * What it does: 73 instructions; 7 call(s) to 0x02008218, 0x02008e0c, 0x02017f64, +4 more; loops (back edge at +0x0a); returns through pop {r3, r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa0 -> constant 0x0221c160 (image word 0x0221c160)
 *   pool +0xa4 -> constant 0x00010040 (image word 0x00010040)
 *   pool +0xa8 -> constant 0x0001b140 (image word 0x0001b140)
 *   pool +0xac -> native_fn_02200ef4+1 (image word 0x02200ef5)
 *   back edge +0x5e -> +0x54
 *   branch +0x80 -> +0x86
 *   test +0x7e cmp r0, #0x0
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200aa8; the literal pool and
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

extern void native_fn_02008218(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02017f64(void);
extern void native_fn_02008430(void);
extern void native_fn_020181b8(void);
extern void native_fn_02200ef4(void);
extern void native_fn_02014324(void);
extern void native_fn_022010e0(void);


asm u32 native_ov006_02200aa8 (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0x7c
    add r5, r0, #0x0
    add r0, sp, #0x28
    add r4, r1, #0x0
    blx native_fn_02008218
    add r2, sp, #0x4
    ldrb r0, [r2, #0xe]
    mov r1, #0xf
    bic r0, r1
    add r1, sp, #0x28
    ldrb r3, [r1, #0x1]
    mov r1, #0xf
    and r1, r3
    orr r0, r1
    strb r0, [r2, #0xe]
    ldrh r3, [r2, #0x3e]
    add r0, sp, #0x2c
    add r1, sp, #0x14
    strb r3, [r2, #0xf]
    lsl r2, r3, #0x1
    blx native_fn_02008e0c
    add r1, sp, #0x4
    ldrb r2, [r1, #0xe]
    mov r0, #0xf0
    mov r3, #0x7
    bic r2, r0
    strb r2, [r1, #0xe]
    add r0, sp, #0x4
    mov r1, #0x0
    strh r1, [r0, #0]
    strh r1, [r0, #0x2]
    strh r1, [r0, #0x4]
    strh r1, [r0, #0x6]
    strh r1, [r0, #0x8]
    strh r1, [r0, #0xa]
    strh r1, [r0, #0xc]
    ldr r1, =0x0221c160
    ldr r1, [r1, #0]
    add r6, r1, #0x0
ov006_02200aa8_L54:
    ldrh r2, [r0, #0]
    add r0, r0, #0x2
    strh r2, [r6, #0]
    add r6, r6, #0x2
    sub r3, r3, #0x1
    bne ov006_02200aa8_L54
    ldr r0, =0x00010040
    add r3, r4, #0x0
    add r2, r1, r0
    ldr r0, =0x0001b140
    str r2, [r1, r0]
    mov r1, #0x2
    str r1, [sp]
    ldr r1, =0x0221c160
    add r2, r5, #0x0
    ldr r1, [r1, #0]
    ldr r0, [r1, r0]
    add r1, sp, #0x10
    add r1, #0x2
    blx native_fn_02017f64
    cmp r0, #0x0
    beq ov006_02200aa8_L86
    blx native_fn_02008430
ov006_02200aa8_L86:
    mov r0, #0x1
    lsl r0, r0, #0x8
    mov r1, #0x1
    blx native_fn_020181b8
    ldr r0, =native_fn_02200ef4+1
    blx native_fn_02014324
    mov r0, #0x1
    bl native_fn_022010e0
    add sp, #0x7c
    pop {r3, r4, r5, r6, pc}
}
