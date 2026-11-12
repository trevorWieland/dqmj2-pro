/* ov006 row 0x02202a80: 164 bytes.
 *
 * What it does: 67 instructions; 12 call(s) to 0x02203114, 0x0200bd04, 0x0200bfe4, +9 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x9c -> constant 0x0221c170 (image word 0x0221c170)
 *   pool +0xa0 -> native_data_0220e8d8 (image word 0x0220e8d8)
 *   branch +0x26 -> +0x2c
 *   branch +0x34 -> +0x38
 *   branch +0x44 -> +0x4c
 *   branch +0x4a -> +0x4e
 *   branch +0x6a -> +0x72
 *   branch +0x7a -> +0x7e
 *   test +0x24 cmp r0, #0x0
 *   test +0x32 cmp r5, #0x0
 *   test +0x42 cmp r0, #0x0
 *   test +0x68 cmp r6, #0x0
 *   test +0x78 cmp r5, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202a80; the literal pool and
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

extern void native_fn_02203114(void);
extern void native_fn_0200bd04(void);
extern void native_fn_0200bfe4(void);
extern void native_fn_02008430(void);
extern u8 native_data_0220e8d8[];
extern void native_fn_02202b48(void);
extern void native_fn_02203c08(void);
extern void native_fn_0200c180(void);
extern void native_fn_0200c02c(void);
extern void native_fn_02008f54(void);
extern void native_fn_02203c20(void);


asm u32 native_ov006_02202a80 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x4c
    add r6, r0, #0x0
    ldr r0, =0x0221c170
    add r5, r1, #0x0
    ldr r0, [r0, #0]
    add r7, r2, #0x0
    add r0, #0x84
    ldr r0, [r0, #0]
    bl native_fn_02203114
    add r0, sp, #0x4
    blx native_fn_0200bd04
    add r0, sp, #0x4
    add r1, r6, #0x0
    blx native_fn_0200bfe4
    cmp r0, #0x0
    bne ov006_02202a80_L2c
    blx native_fn_02008430
ov006_02202a80_L2c:
    ldr r1, [sp, #0x2c]
    ldr r0, [sp, #0x28]
    sub r4, r1, r0
    cmp r5, #0x0
    beq ov006_02202a80_L38
    str r4, [r5, #0]
ov006_02202a80_L38:
    ldr r1, =native_data_0220e8d8
    add r0, r6, #0x0
    mov r2, #0x2
    bl native_fn_02202b48
    cmp r0, #0x0
    beq ov006_02202a80_L4c
    mov r6, #0x3
    mvn r6, r6
    b ov006_02202a80_L4e
ov006_02202a80_L4c:
    add r6, r7, #0x0
ov006_02202a80_L4e:
    add r0, r4, #0x0
    add r1, r6, #0x0
    bl native_fn_02203c08
    add r1, r0, #0x0
    add r0, sp, #0x4
    add r2, r4, #0x0
    str r1, [sp]
    blx native_fn_0200c180
    add r0, sp, #0x4
    blx native_fn_0200c02c
    cmp r6, #0x0
    ble ov006_02202a80_L72
    ldr r0, [sp]
    add sp, #0x4c
    pop {r4, r5, r6, r7, pc}
ov006_02202a80_L72:
    ldr r0, [sp]
    ldr r0, [r0, #0]
    lsr r0, r0, #0x8
    cmp r5, #0x0
    beq ov006_02202a80_L7e
    str r0, [r5, #0]
ov006_02202a80_L7e:
    add r1, r7, #0x0
    bl native_fn_02203c08
    add r4, r0, #0x0
    ldr r0, [sp]
    add r1, r4, #0x0
    blx native_fn_02008f54
    add r0, sp, #0x0
    bl native_fn_02203c20
    add r0, r4, #0x0
    add sp, #0x4c
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
