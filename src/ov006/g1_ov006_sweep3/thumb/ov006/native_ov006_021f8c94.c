/* ov006 row 0x021f8c94: 88 bytes.
 *
 * What it does: 37 instructions; 3 call(s) to 0x021ff6d4, 0x021ff6d4, 0x0220490c; no back edge; returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x50 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0x54 -> native_fn_021f8a98+1 (image word 0x021f8a99)
 *   branch +0x10 -> +0x1c
 *   branch +0x1a -> +0x36
 *   branch +0x22 -> +0x4e
 *   test +0x0e cmp r1, r0
 *   test +0x18 cmp r0, #0x4
 *   test +0x20 cmp r0, #0x0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8c94; the literal pool and
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

extern void native_fn_021ff6d4(void);
extern void native_fn_021f8a98(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f8c94 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c0d8
    ldr r2, [r0, #0x4]
    ldrh r1, [r0, #0x2]
    add r0, r2, #0x0
    add r0, #0x40
    ldrh r0, [r0, #0]
    cmp r1, r0
    beq ov006_021f8c94_L1c
    add r0, r2, #0x0
    add r0, #0x51
    ldrb r0, [r0, #0]
    cmp r0, #0x4
    bhi ov006_021f8c94_L36
ov006_021f8c94_L1c:
    add r2, #0x59
    ldrb r0, [r2, #0]
    cmp r0, #0x0
    bne ov006_021f8c94_L4e
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c0d8
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021f8c94_L36:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, =native_fn_021f8a98+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c0d8
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
ov006_021f8c94_L4e:
    pop {r3, pc}
}
