/* ov006 row 0x02200974: 84 bytes.
 *
 * What it does: 32 instructions; 5 call(s) to 0x02202f98, 0x02200770, 0x022009b8, +2 more; loops (back edge at +0x1c); returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x48 -> constant 0x0221c15c (image word 0x0221c15c)
 *   pool +0x4c -> native_fn_022009c8+1 (image word 0x022009c9)
 *   pool +0x50 -> native_fn_02200a04+1 (image word 0x02200a05)
 *   branch +0x24 -> +0x44
 *   branch +0x2e -> +0x3c
 *   test +0x22 cmp r0, #0xc0
 *   test +0x2c cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200974; the literal pool and
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

extern void native_fn_02202f98(void);
extern void native_fn_02200770(void);
extern void native_fn_022009c8(void);
extern void native_fn_02204970(void);
extern void native_fn_02200a04(void);


asm u32 native_ov006_02200974 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c15c
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r2, sp, #0x4
    ldr r0, [r0, #0]
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r0, [sp]
    add r0, #0xc
    str r0, [sp]
    bl native_fn_02200770
    ldr r0, [sp]
    cmp r0, #0xc0
    blt ov006_02200974_L44
    ldr r0, =0x0221c15c
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x1e]
    cmp r0, #0x0
    beq ov006_02200974_L3c
    ldr r1, =native_fn_022009c8+1
    add r0, r4, #0x0
    bl native_fn_02204970
    add sp, #0x8
    pop {r4, pc}
ov006_02200974_L3c:
    ldr r1, =native_fn_02200a04+1
    add r0, r4, #0x0
    bl native_fn_02204970
ov006_02200974_L44:
    add sp, #0x8
    pop {r4, pc}
}
