/* ov006 row 0x02202b84: 152 bytes.
 *
 * What it does: 67 instructions; 8 call(s) to 0x02203c08, 0x022030a4, 0x02204238, +5 more; loops (back edge at +0x90); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x94 -> constant 0x0221c174 (image word 0x0221c174)
 *   back edge +0x90 -> +0x18
 *   test +0x8e cmp r6, #0x2
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202b84; the literal pool and
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

extern void native_fn_02203c08(void);
extern void native_fn_022030a4(void);
extern void native_fn_02204238(void);
extern void native_fn_022043e0(void);
extern void native_fn_022042b8(void);
extern void native_fn_022042ac(void);


asm u32 native_ov006_02202b84 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r0, #0x45
    lsl r0, r0, #0x4
    mov r1, #0x4
    bl native_fn_02203c08
    ldr r4, =0x0221c174
    mov r6, #0x0
    mov r7, #0x8a
    str r0, [r4, #0]
    add r5, r6, #0x0
    lsl r7, r7, #0x2
ov006_02202b84_L18:
    ldr r1, [r4, #0]
    mov r0, #0x20
    add r1, r1, r5
    mov r2, #0x10
    bl native_fn_022030a4
    ldr r1, [r4, #0]
    add r2, r1, r5
    mov r1, #0x89
    lsl r1, r1, #0x2
    str r0, [r2, r1]
    bl native_fn_02204238
    ldr r1, [r4, #0]
    add r2, r1, r5
    mov r1, #0x22
    lsl r1, r1, #0x4
    str r0, [r2, r1]
    add r0, r6, #0x0
    mov r1, #0x40
    bl native_fn_022043e0
    ldr r1, [r4, #0]
    add r2, r1, r5
    mov r1, #0x82
    lsl r1, r1, #0x2
    str r0, [r2, r1]
    add r0, r6, #0x0
    mov r1, #0x7f
    bl native_fn_022043e0
    ldr r1, [r4, #0]
    add r0, #0x8
    add r2, r1, r5
    mov r1, #0x86
    lsl r1, r1, #0x2
    str r0, [r2, r1]
    ldr r0, [r4, #0]
    mov r2, #0x2
    add r1, r0, r5
    mov r0, #0x22
    lsl r0, r0, #0x4
    ldr r0, [r1, r0]
    lsl r2, r2, #0x8
    add r1, r1, r2
    bl native_fn_022042b8
    ldr r0, [r4, #0]
    mov r2, #0x21
    add r1, r0, r5
    mov r0, #0x22
    lsl r0, r0, #0x4
    ldr r0, [r1, r0]
    lsl r2, r2, #0x4
    add r1, r1, r2
    bl native_fn_022042ac
    add r6, r6, #0x1
    add r5, r5, r7
    cmp r6, #0x2
    blt ov006_02202b84_L18
    pop {r3, r4, r5, r6, r7, pc}
}
