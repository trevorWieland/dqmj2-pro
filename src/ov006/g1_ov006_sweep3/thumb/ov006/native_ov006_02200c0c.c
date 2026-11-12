/* ov006 row 0x02200c0c: 96 bytes.
 *
 * What it does: 42 instructions; 4 call(s) to 0x02014424, 0x02007ff4, 0x02008008, +1 more; loops (back edge at +0x06); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x5c -> constant 0x0221c160 (image word 0x0221c160)
 *   branch +0x0c -> +0x58
 *   test +0x0a cmp r0, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200c0c; the literal pool and
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

extern void native_fn_02014424(void);
extern void native_fn_02007ff4(void);
extern void native_fn_02008008(void);
extern void native_fn_02018640(void);


asm u32 native_ov006_02200c0c (register u32 a0)
{
    push {r3, r4, r5, lr}
    mov r1, #0x1
    add r5, r0, #0x0
    blx native_fn_02014424
    cmp r0, #0x0
    bne ov006_02200c0c_L58
    mov r0, #0x1
    lsl r0, r5
    mvn r0, r0
    lsl r0, r0, #0x10
    lsr r4, r0, #0x10
    blx native_fn_02007ff4
    ldr r1, =0x0221c160
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x2]
    and r2, r4
    strh r2, [r3, #0x2]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x4]
    and r2, r4
    strh r2, [r3, #0x4]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x6]
    and r2, r4
    strh r2, [r3, #0x6]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x8]
    and r2, r4
    strh r2, [r3, #0x8]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0xa]
    and r2, r4
    strh r2, [r3, #0xa]
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0xc]
    and r1, r4
    strh r1, [r2, #0xc]
    blx native_fn_02008008
    add r0, r5, #0x0
    blx native_fn_02018640
ov006_02200c0c_L58:
    pop {r3, r4, r5, pc}
    mov r8, r8
}
