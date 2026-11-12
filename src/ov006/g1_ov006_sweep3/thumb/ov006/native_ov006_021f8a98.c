/* ov006 row 0x021f8a98: 104 bytes.
 *
 * What it does: 40 instructions; 11 call(s) to 0x021fe6e8, 0x021f2a4c, 0x020024bc, +8 more; loops (back edge at +0x08); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x64 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   branch +0x1e -> +0x26
 *   test +0x1c cmp r0, #0x4
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8a98; the literal pool and
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
extern void native_fn_021f8998(void);
extern void native_fn_021f8800(void);
extern void native_fn_02002480(void);
extern void native_fn_021fe6d0(void);
extern void native_fn_021fe6d8(void);
extern void native_fn_021f8b3c(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_021f8a98 (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0x0
    bl native_fn_021fe6e8
    bl native_fn_021f2a4c
    ldr r0, =0x0221c0d8
    ldrh r1, [r0, #0x2]
    add r1, r1, #0x4
    strh r1, [r0, #0x2]
    ldrh r0, [r0, #0x2]
    mov r1, #0x1c
    blx native_fn_020024bc
    cmp r0, #0x4
    blt ov006_021f8a98_L26
    bl native_fn_021f8998
    pop {r4, pc}
ov006_021f8a98_L26:
    ldr r1, =0x0221c0d8
    ldrh r2, [r1, #0x2]
    sub r0, r2, r0
    strh r0, [r1, #0x2]
    bl native_fn_021f8800
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
    add r1, r4, #0x0
    bl native_fn_02204974
    pop {r4, pc}
}
