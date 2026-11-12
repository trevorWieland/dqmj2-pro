/* ov006 row 0x021f746c: 132 bytes.
 *
 * What it does: 50 instructions; 10 call(s) to 0x021f5554, 0x022034dc, 0x021f74f0, +7 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x78 -> constant 0x0221c0c4 (image word 0x0221c0c4)
 *   pool +0x7c -> native_fn_021f76e8+1 (image word 0x021f76e9)
 *   pool +0x80 -> native_fn_021f7540+1 (image word 0x021f7541)
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f746c; the literal pool and
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

extern void native_fn_021f5554(void);
extern void native_fn_022034dc(void);
extern void native_fn_021f74f0(void);
extern void native_fn_02008be0(void);
extern void native_fn_02008bf8(void);
extern void native_fn_022037c0(void);
extern void native_fn_022038ac(void);
extern void native_fn_021f76e8(void);
extern void native_fn_021f5538(void);
extern void native_fn_02200344(void);
extern void native_fn_021f7540(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021f746c (register u32 a0)
{
    push {r3, r4, r5, lr}
    sub sp, #0x28
    bl native_fn_021f5554
    add r5, r0, #0x0
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_022034dc
    add r4, r0, #0x0
    ldr r0, =0x0221c0c4
    mov r1, #0x0
    strb r1, [r0, #0x1]
    strb r1, [r0, #0]
    bl native_fn_021f74f0
    mov r0, #0x0
    add r1, sp, #0x10
    mov r2, #0x16
    blx native_fn_02008be0
    ldrb r2, [r5, #0x1]
    add r0, r5, #0x2
    add r1, sp, #0x10
    lsl r2, r2, #0x1
    blx native_fn_02008bf8
    mov r0, #0x1c
    str r0, [sp]
    mov r0, #0x2
    str r0, [sp, #0x4]
    mov r0, #0x12
    lsl r0, r0, #0x6
    str r0, [sp, #0x8]
    add r0, sp, #0x10
    str r0, [sp, #0xc]
    add r0, r4, #0x0
    mov r1, #0x8
    mov r2, #0x35
    mov r3, #0xf0
    bl native_fn_022037c0
    add r0, r4, #0x0
    bl native_fn_022038ac
    ldr r0, =native_fn_021f76e8+1
    bl native_fn_021f5538
    mov r1, #0x4
    mov r2, #0x0
    mov r0, #0x1d
    sub r3, r1, #0x5
    str r2, [sp]
    bl native_fn_02200344
    ldr r0, =native_fn_021f7540+1
    bl ov006_main_loop_set_callback_021f52cc
    add sp, #0x28
    pop {r3, r4, r5, pc}
}
