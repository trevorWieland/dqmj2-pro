/* ov006 row 0x022047d4: 160 bytes.
 *
 * What it does: 69 instructions; 8 call(s) to 0x02203c08, 0x02203c08, 0x022030a4, +5 more; loops (back edge at +0x06); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x98 -> constant 0x0221c1e8 (image word 0x0221c1e8)
 *   pool +0x9c -> native_data_0220bb68 (image word 0x0220bb68)
 *   back edge +0x92 -> +0x14
 *   test +0x90 cmp r7, #0x2
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022047d4; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data_0220bb68[];
extern void native_fn_022030a4(void);
extern void native_fn_02203088(void);
extern void native_fn_02204238(void);
extern void native_fn_022042b8(void);
extern void native_fn_022042ac(void);


asm u32 native_ov006_022047d4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r0, #0x80
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r6, =0x0221c1e8
    mov r7, #0x0
    ldr r4, =native_data_0220bb68
    str r0, [r6, #0]
    add r5, r7, #0x0
ov006_022047d4_L14:
    ldr r0, [r6, #0]
    ldrb r1, [r4, #0]
    add r0, r0, r5
    str r1, [r0, #0x34]
    ldrb r1, [r4, #0]
    mov r0, #0x14
    mul r0, r1
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, [r6, #0]
    mov r2, #0x14
    add r1, r1, r5
    str r0, [r1, #0x3c]
    ldr r1, [r6, #0]
    ldrb r0, [r4, #0]
    add r1, r1, r5
    ldr r1, [r1, #0x3c]
    bl native_fn_022030a4
    ldr r1, [r6, #0]
    str r0, [r1, r5]
    ldrb r0, [r4, #0]
    bl native_fn_02203088
    ldr r1, [r6, #0]
    add r1, r1, r5
    str r0, [r1, #0x4]
    bl native_fn_02204238
    ldr r1, [r6, #0]
    add r1, r1, r5
    str r0, [r1, #0x8]
    ldr r0, [r6, #0]
    add r1, r0, r5
    mov r0, #0x0
    strb r0, [r1, #0x1c]
    ldr r0, [r6, #0]
    add r1, r0, r5
    add r1, #0x30
    mov r0, #0xff
    strb r0, [r1, #0]
    ldr r0, [r6, #0]
    add r1, r0, r5
    ldr r0, [r1, #0x8]
    add r1, #0xc
    bl native_fn_022042b8
    ldr r0, [r6, #0]
    add r1, r0, r5
    ldr r0, [r1, #0x8]
    add r1, #0x20
    bl native_fn_022042ac
    ldr r0, [r6, #0]
    add r7, r7, #0x1
    add r1, r0, r5
    add r1, #0x38
    mov r0, #0x1
    strb r0, [r1, #0]
    add r4, r4, #0x1
    add r5, #0x40
    cmp r7, #0x2
    blt ov006_022047d4_L14
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
