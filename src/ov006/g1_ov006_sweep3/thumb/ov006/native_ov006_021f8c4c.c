/* ov006 row 0x021f8c4c: 72 bytes.
 *
 * What it does: 29 instructions; 3 call(s) to 0x021ff6d4, 0x021ff6d4, 0x0220490c; no back edge; returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x40 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0x44 -> native_fn_021f8a18+1 (image word 0x021f8a19)
 *   branch +0x08 -> +0x26
 *   branch +0x12 -> +0x3e
 *   test +0x06 cmp r1, #0x0
 *   test +0x10 cmp r0, #0x0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8c4c; the literal pool and
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
extern void native_fn_021f8a18(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f8c4c (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c0d8
    ldrh r1, [r0, #0x2]
    cmp r1, #0x0
    bne ov006_021f8c4c_L26
    ldr r0, [r0, #0x4]
    add r0, #0x59
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f8c4c_L3e
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c0d8
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021f8c4c_L26:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, =native_fn_021f8a18+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c0d8
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
ov006_021f8c4c_L3e:
    pop {r3, pc}
}
