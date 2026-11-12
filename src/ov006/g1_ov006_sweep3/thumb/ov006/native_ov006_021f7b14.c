/* ov006 row 0x021f7b14: 136 bytes.
 *
 * What it does: 50 instructions; 12 call(s) to 0x021f7b9c, 0x021f7bc0, 0x021f7bc4, +9 more; loops (back edge at +0x0e); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> constant 0x0221c0cc (image word 0x0221c0cc)
 *   pool +0x80 -> native_fn_021f7d48+1 (image word 0x021f7d49)
 *   pool +0x84 -> native_fn_021f7d10+1 (image word 0x021f7d11)
 *   branch +0x14 -> +0x7a
 *   branch +0x18 -> +0x20
 *   branch +0x1c -> +0x3e
 *   branch +0x26 -> +0x7a
 *   branch +0x44 -> +0x7a
 *   test +0x12 cmp r0, #0x0
 *   test +0x16 cmp r0, #0x1
 *   test +0x1a cmp r0, #0x2
 *   test +0x24 cmp r1, #0x0
 *   test +0x42 cmp r0, #0x0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f7b14; the literal pool and
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

extern void native_fn_021f7b9c(void);
extern void native_fn_021f7bc0(void);
extern void native_fn_021f7bc4(void);
extern void native_fn_021f4ef4(void);
extern void native_fn_0220498c(void);
extern void native_fn_021f7d48(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021ff718(void);
extern void native_fn_02200344(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021f23f4(void);
extern void native_fn_021f7d10(void);


asm u32 native_ov006_021f7b14 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f7b9c
    bl native_fn_021f7bc0
    bl native_fn_021f7bc4
    bl native_fn_021f4ef4
    cmp r0, #0x0
    beq ov006_021f7b14_L7a
    cmp r0, #0x1
    beq ov006_021f7b14_L20
    cmp r0, #0x2
    beq ov006_021f7b14_L3e
    pop {r3, pc}
ov006_021f7b14_L20:
    ldr r2, =0x0221c0cc
    ldr r1, [r2, #0x4]
    cmp r1, #0x0
    beq ov006_021f7b14_L7a
    mov r0, #0x1
    strb r0, [r2, #0]
    bl native_fn_0220498c
    ldr r0, =0x0221c0cc
    mov r1, #0x0
    str r1, [r0, #0x4]
    ldr r0, =native_fn_021f7d48+1
    bl native_fn_021f52cc
    pop {r3, pc}
ov006_021f7b14_L3e:
    ldr r0, =0x0221c0cc
    ldr r0, [r0, #0x4]
    cmp r0, #0x0
    beq ov006_021f7b14_L7a
    bl native_fn_021ff718
    mov r1, #0x1
    mov r0, #0x0
    str r0, [sp]
    mov r0, #0xc
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    mov r0, #0x9
    bl native_fn_021ff6d4
    bl native_fn_021f23f4
    ldr r1, =0x0221c0cc
    mov r0, #0x1
    ldr r1, [r1, #0x4]
    bl native_fn_0220498c
    ldr r0, =0x0221c0cc
    mov r1, #0x0
    str r1, [r0, #0x4]
    ldr r0, =native_fn_021f7d10+1
    bl native_fn_021f52cc
ov006_021f7b14_L7a:
    pop {r3, pc}
}
