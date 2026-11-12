/* ov006 row 0x0220342c: 144 bytes.
 *
 * What it does: 66 instructions; 4 call(s) to 0x02203114, 0x02204484, 0x020364dc, +1 more; loops (back edge at +0x16); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x8c -> constant 0x0221c184 (image word 0x0221c184)
 *   branch +0x48 -> +0x50
 *   branch +0x4e -> +0x54
 *   test +0x44 cmp r7, #0x1
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220342c; the literal pool and
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
extern void native_fn_02204484(void);
extern void native_fn_020364dc(void);
extern void native_fn_02036348(void);


asm u32 native_ov006_0220342c (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    add r7, r0, #0x0
    ldr r0, =0x0221c184
    str r3, [sp, #0x4]
    add r5, r1, #0x0
    ldr r1, [r0, #0]
    mov r0, #0x67
    lsl r0, r0, #0x4
    ldr r0, [r1, r0]
    add r6, r2, #0x0
    bl native_fn_02203114
    add r4, r0, #0x0
    add r0, #0x2e
    strb r5, [r0, #0]
    add r0, r4, #0x0
    add r0, #0x2f
    strb r6, [r0, #0]
    add r1, r5, #0x0
    ldr r2, [sp, #0x4]
    add r0, r7, #0x0
    mul r1, r6
    add r3, sp, #0x8
    bl native_fn_02204484
    str r0, [r4, #0x28]
    ldr r0, [sp, #0x8]
    add r1, r6, #0x0
    strh r0, [r4, #0x2c]
    add r0, r5, #0x0
    blx native_fn_020364dc
    ldr r1, [sp, #0x20]
    cmp r7, #0x1
    str r0, [r1, #0]
    bne ov006_0220342c_L50
    mov r1, #0x66
    lsl r1, r1, #0x14
    b ov006_0220342c_L54
ov006_0220342c_L50:
    mov r1, #0x19
    lsl r1, r1, #0x16
ov006_0220342c_L54:
    ldr r0, [sp, #0x8]
    add r3, r6, #0x0
    lsl r2, r0, #0x7
    mov r0, #0x4
    str r0, [sp]
    add r1, r1, r2
    add r0, r4, #0x0
    add r2, r5, #0x0
    blx native_fn_02036348
    ldr r2, [r4, #0x14]
    add r0, r4, #0x0
    ldr r2, [r2, #0x4]
    mov r1, #0x0
    blx r2
    ldr r0, =0x0221c184
    ldr r1, [r0, #0]
    ldr r0, [sp, #0x24]
    str r4, [r4, #0x18]
    lsl r0, r0, #0x3
    add r0, r1, r0
    str r0, [r4, #0x1c]
    mov r0, #0x1
    str r0, [r4, #0x20]
    str r0, [r4, #0x24]
    add r0, r4, #0x0
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
