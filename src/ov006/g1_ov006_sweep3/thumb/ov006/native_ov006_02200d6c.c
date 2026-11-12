/* ov006 row 0x02200d6c: 132 bytes.
 *
 * What it does: 59 instructions; 6 call(s) to 0x022010e0, 0x02007ff4, 0x02008008, +3 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x80 -> constant 0x0221c160 (image word 0x0221c160)
 *   branch +0x18 -> +0x72
 *   branch +0x1e -> +0x72
 *   branch +0x24 -> +0x6c
 *   branch +0x6a -> +0x72
 *   back edge +0x7a -> +0x0e
 *   test +0x16 tst r2, r1
 *   test +0x1c tst r2, r1
 *   test +0x22 tst r0, r1
 *   test +0x78 cmp r4, #0x10
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200d6c; the literal pool and
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

extern void native_fn_022010e0(void);
extern void native_fn_02007ff4(void);
extern void native_fn_02008008(void);
extern void native_fn_02018640(void);
extern void native_fn_02200cec(void);


asm u32 native_ov006_02200d6c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r0, #0x3
    bl native_fn_022010e0
    mov r4, #0x1
    ldr r6, =0x0221c160
    add r7, r4, #0x0
ov006_02200d6c_Le:
    ldr r0, [r6, #0]
    add r1, r7, #0x0
    ldrh r2, [r0, #0x2]
    lsl r1, r4
    tst r2, r1
    beq ov006_02200d6c_L72
    ldrh r2, [r0, #0x4]
    tst r2, r1
    bne ov006_02200d6c_L72
    ldrh r0, [r0, #0x6]
    tst r0, r1
    bne ov006_02200d6c_L6c
    mvn r0, r1
    lsl r0, r0, #0x10
    lsr r5, r0, #0x10
    blx native_fn_02007ff4
    ldr r1, [r6, #0]
    ldrh r2, [r1, #0x2]
    and r2, r5
    strh r2, [r1, #0x2]
    ldr r1, [r6, #0]
    ldrh r2, [r1, #0x4]
    and r2, r5
    strh r2, [r1, #0x4]
    ldr r1, [r6, #0]
    ldrh r2, [r1, #0x6]
    and r2, r5
    strh r2, [r1, #0x6]
    ldr r1, [r6, #0]
    ldrh r2, [r1, #0x8]
    and r2, r5
    strh r2, [r1, #0x8]
    ldr r1, [r6, #0]
    ldrh r2, [r1, #0xa]
    and r2, r5
    strh r2, [r1, #0xa]
    ldr r1, [r6, #0]
    ldrh r2, [r1, #0xc]
    and r2, r5
    strh r2, [r1, #0xc]
    blx native_fn_02008008
    add r0, r4, #0x0
    blx native_fn_02018640
    b ov006_02200d6c_L72
ov006_02200d6c_L6c:
    add r0, r4, #0x0
    bl native_fn_02200cec
ov006_02200d6c_L72:
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    lsr r4, r0, #0x10
    cmp r4, #0x10
    blo ov006_02200d6c_Le
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
