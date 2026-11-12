/* ov006 row 0x021f98d0: 100 bytes.
 *
 * What it does: 46 instructions; 4 call(s) to 0x02008e0c, 0x021f9908, 0x0201f274, +1 more; loops (back edge at +0x2a); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x60 -> constant 0x0221c0e4 (image word 0x0221c0e4)
 *   branch +0x18 -> +0x24
 *   branch +0x1c -> +0x24
 *   branch +0x3c -> +0x48
 *   back edge +0x46 -> +0x38
 *   branch +0x50 -> +0x58
 *   test +0x16 cmp r0, #0x0
 *   test +0x1a cmp r0, #0x20
 *   test +0x3a cmp r1, #0x0
 *   test +0x44 cmp r2, #0x3
 *   test +0x4e cmp r0, r4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f98d0; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_0201f274(void);


asm u32 native_ov006_021f98d0 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x4
    add r4, r0, #0x0
    ldr r0, =0x0221c0e4
    ldr r0, [r0, #0]
    ldrb r1, [r0, #0x14]
    add r2, r0, #0x0
    add r2, #0x8
    lsl r0, r1, #0x1
    add r1, r1, r0
    ldrb r0, [r2, r1]
    cmp r0, #0x0
    beq ov006_021f98d0_L24
    cmp r0, #0x20
    beq ov006_021f98d0_L24
    add sp, #0x4
    mov r0, #0x1
    pop {r3, r4, pc}
ov006_021f98d0_L24:
    add r0, r2, r1
    add r1, sp, #0x0
    mov r2, #0x3
    blx native_fn_02008e0c
    mov r2, #0x0
    add r0, sp, #0x0
    strb r2, [r0, #0x3]
    add r3, sp, #0x0
    mov r0, #0x20
ov006_021f98d0_L38:
    ldrb r1, [r3, #0]
    cmp r1, #0x0
    bne ov006_021f98d0_L48
    add r2, r2, #0x1
    strb r0, [r3, #0]
    add r3, r3, #0x1
    cmp r2, #0x3
    blt ov006_021f98d0_L38
ov006_021f98d0_L48:
    add r0, sp, #0x0
    blx native_fn_0201f274
    cmp r0, r4
    blt ov006_021f98d0_L58
    add sp, #0x4
    mov r0, #0x1
    pop {r3, r4, pc}
ov006_021f98d0_L58:
    mov r0, #0x0
    add sp, #0x4
    pop {r3, r4, pc}
    mov r8, r8
}
