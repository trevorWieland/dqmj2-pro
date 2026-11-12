/* ov006 row 0x021f8a18: 128 bytes.
 *
 * What it does: 52 instructions; 12 call(s) to 0x021fe6e8, 0x021f2a4c, 0x021f8a30, +9 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   branch +0x12 -> +0x18
 *   branch +0x16 -> +0x1a
 *   branch +0x2a -> +0x32
 *   branch +0x32 -> +0x42
 *   branch +0x48 -> +0x7a
 *   test +0x10 cmp r1, #0x4
 *   test +0x28 cmp r4, #0x18
 *   test +0x46 cmp r4, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8a18; the literal pool and
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

extern void native_fn_021fe6e8(void);
extern void native_fn_021f2a4c(void);
extern void native_fn_020024bc(void);
extern void native_fn_021f8800(void);
extern void native_fn_021f8998(void);
extern void native_fn_02002480(void);
extern void native_fn_021fe6d0(void);
extern void native_fn_021fe6d8(void);
extern void native_fn_021f8b3c(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_021f8a18 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r0, #0x0
    bl native_fn_021fe6e8
    bl native_fn_021f2a4c
    ldr r0, =0x0221c0d8
    ldrh r1, [r0, #0x2]
    cmp r1, #0x4
    bls ov006_021f8a18_L18
    sub r1, r1, #0x4
    b ov006_021f8a18_L1a
ov006_021f8a18_L18:
    mov r1, #0x0
ov006_021f8a18_L1a:
    strh r1, [r0, #0x2]
    ldr r0, =0x0221c0d8
    mov r1, #0x1c
    ldrh r0, [r0, #0x2]
    blx native_fn_020024bc
    add r4, r0, #0x0
    cmp r4, #0x18
    bne ov006_021f8a18_L32
    bl native_fn_021f8800
    pop {r3, r4, r5, pc}
ov006_021f8a18_L32:
    ble ov006_021f8a18_L42
    ldr r1, =0x0221c0d8
    mov r0, #0x1c
    ldrh r2, [r1, #0x2]
    sub r0, r0, r4
    mov r4, #0x0
    add r0, r2, r0
    strh r0, [r1, #0x2]
ov006_021f8a18_L42:
    bl native_fn_021f8998
    cmp r4, #0x0
    bne ov006_021f8a18_L7a
    ldr r0, =0x0221c0d8
    ldr r2, [r0, #0x4]
    ldrh r1, [r0, #0x2]
    add r0, r2, #0x0
    add r0, #0x53
    ldrb r0, [r0, #0]
    add r2, #0x40
    mul r0, r1
    ldrh r1, [r2, #0]
    blx native_fn_02002480
    bl native_fn_021fe6d0
    bl native_fn_021fe6d8
    bl native_fn_021f8b3c
    ldr r1, =0x0221c0d8
    mov r0, #0x0
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
    add r1, r5, #0x0
    bl native_fn_02204974
ov006_021f8a18_L7a:
    pop {r3, r4, r5, pc}
}
