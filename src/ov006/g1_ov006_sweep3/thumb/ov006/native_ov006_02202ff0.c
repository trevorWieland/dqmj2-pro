/* ov006 row 0x02202ff0: 76 bytes.
 *
 * What it does: 33 instructions; 5 call(s) to 0x02008c14, 0x02203034, 0x02008bf8, +2 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x48 -> constant 0x0221c178 (image word 0x0221c178)
 *   branch +0x24 -> +0x44
 *   back edge +0x42 -> +0x26
 *   test +0x22 cmp r7, #0x0
 *   test +0x40 cmp r5, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202ff0; the literal pool and
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

extern void native_fn_02008c14(void);
extern void native_fn_02008bf8(void);
extern void native_fn_02008c28(void);


asm u32 native_ov006_02202ff0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r6, r2, #0x0
    lsl r2, r0, #0x2
    ldr r0, =0x0221c178
    lsl r1, r1, #0x3
    ldr r2, [r0, r2]
    add r0, r2, r1
    ldr r0, [r0, #0x4]
    ldrh r7, [r2, r1]
    add r4, r2, r0
    mov r0, #0x0
    add r1, sp, #0x0
    mov r2, #0x8
    blx native_fn_02008c14
    mov r5, #0x0
    cmp r7, #0x0
    ble ov006_02202ff0_L44
ov006_02202ff0_L26:
    add r0, r4, #0x0
    add r1, sp, #0x0
    mov r2, #0x6
    blx native_fn_02008bf8
    add r0, sp, #0x0
    add r1, r6, #0x0
    mov r2, #0x8
    blx native_fn_02008c28
    add r5, r5, #0x1
    add r4, r4, #0x6
    add r6, #0x8
    cmp r5, r7
    blt ov006_02202ff0_L26
ov006_02202ff0_L44:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
