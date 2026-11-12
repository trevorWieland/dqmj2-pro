/* ov006 row 0x02201130: 128 bytes.
 *
 * What it does: 58 instructions; 4 call(s) to 0x02007ff4, 0x02008008, 0x02008e0c, +1 more; loops (back edge at +0x06); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> constant 0x0221c160 (image word 0x0221c160)
 *   branch +0x1c -> +0x28
 *   branch +0x3e -> +0x46
 *   branch +0x4a -> +0x52
 *   branch +0x56 -> +0x5e
 *   branch +0x62 -> +0x6a
 *   branch +0x6e -> +0x76
 *   test +0x1a tst r1, r5
 *   test +0x3c tst r1, r5
 *   test +0x48 tst r1, r5
 *   test +0x54 tst r1, r5
 *   test +0x60 tst r1, r5
 *   test +0x6c tst r0, r5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02201130; the literal pool and
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

extern void native_fn_02007ff4(void);
extern void native_fn_02008008(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov006_02201130 (register u32 a0)
{
    push {r3, r4, r5, lr}
    sub sp, #0x10
    add r5, r0, #0x0
    blx native_fn_02007ff4
    mov r1, #0x1
    lsl r1, r5
    lsl r1, r1, #0x10
    lsr r5, r1, #0x10
    ldr r1, =0x0221c160
    add r4, r0, #0x0
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0x2]
    tst r1, r5
    bne ov006_02201130_L28
    blx native_fn_02008008
    add sp, #0x10
    mov r0, #0x0
    pop {r3, r4, r5, pc}
ov006_02201130_L28:
    add r0, r2, #0x0
    add r1, sp, #0x0
    mov r2, #0xe
    blx native_fn_02008e0c
    add r0, r4, #0x0
    blx native_fn_02008008
    add r0, sp, #0x0
    ldrh r1, [r0, #0x4]
    tst r1, r5
    beq ov006_02201130_L46
    add sp, #0x10
    mov r0, #0x2
    pop {r3, r4, r5, pc}
ov006_02201130_L46:
    ldrh r1, [r0, #0x6]
    tst r1, r5
    beq ov006_02201130_L52
    add sp, #0x10
    mov r0, #0x3
    pop {r3, r4, r5, pc}
ov006_02201130_L52:
    ldrh r1, [r0, #0x8]
    tst r1, r5
    beq ov006_02201130_L5e
    add sp, #0x10
    mov r0, #0x4
    pop {r3, r4, r5, pc}
ov006_02201130_L5e:
    ldrh r1, [r0, #0xa]
    tst r1, r5
    beq ov006_02201130_L6a
    add sp, #0x10
    mov r0, #0x5
    pop {r3, r4, r5, pc}
ov006_02201130_L6a:
    ldrh r0, [r0, #0xc]
    tst r0, r5
    beq ov006_02201130_L76
    add sp, #0x10
    mov r0, #0x6
    pop {r3, r4, r5, pc}
ov006_02201130_L76:
    mov r0, #0x1
    add sp, #0x10
    pop {r3, r4, r5, pc}
}
