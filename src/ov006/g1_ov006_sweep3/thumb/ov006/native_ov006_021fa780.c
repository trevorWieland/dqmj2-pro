/* ov006 row 0x021fa780: 80 bytes.
 *
 * What it does: 34 instructions; 4 call(s) to 0x021fedc8, 0x021fedd8, 0x021fedec, +1 more; no back edge; returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x4c -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   branch +0x10 -> +0x48
 *   branch +0x14 -> +0x2a
 *   branch +0x20 -> +0x26
 *   branch +0x24 -> +0x38
 *   branch +0x28 -> +0x38
 *   test +0x0e cmp r1, r4
 *   test +0x12 cmp r4, #0x0
 *   test +0x1e cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fa780; the literal pool and
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

extern void native_fn_021fedc8(void);
extern void native_fn_021fedd8(void);
extern void native_fn_021fedec(void);
extern void native_fn_021fabe4(void);


asm u32 native_ov006_021fa780 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r4, r0, #0x0
    bl native_fn_021fedc8
    add r1, r0, #0x0
    add r1, #0xf5
    ldrb r1, [r1, #0]
    cmp r1, r4
    beq ov006_021fa780_L48
    cmp r4, #0x0
    beq ov006_021fa780_L2a
    ldr r0, =0x0221c0ec
    ldr r0, [r0, #0x8]
    add r0, #0x43
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021fa780_L26
    mov r5, #0x1
    b ov006_021fa780_L38
ov006_021fa780_L26:
    mov r5, #0x0
    b ov006_021fa780_L38
ov006_021fa780_L2a:
    add r0, #0xf6
    ldrb r1, [r0, #0]
    ldr r0, =0x0221c0ec
    mov r5, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x43
    strb r1, [r0, #0]
ov006_021fa780_L38:
    add r0, r4, #0x0
    bl native_fn_021fedd8
    add r0, r5, #0x0
    bl native_fn_021fedec
    bl native_fn_021fabe4
ov006_021fa780_L48:
    pop {r3, r4, r5, pc}
    mov r8, r8
}
