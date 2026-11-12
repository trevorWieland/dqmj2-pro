/* ov006 row 0x02200e30: 148 bytes.
 *
 * What it does: 66 instructions; 7 call(s) to 0x02014424, 0x02007ff4, 0x02008008, +4 more; loops (back edge at +0x1a); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x90 -> constant 0x0221c160 (image word 0x0221c160)
 *   branch +0x14 -> +0x70
 *   branch +0x20 -> +0x68
 *   branch +0x66 -> +0x70
 *   back edge +0x78 -> +0x08
 *   branch +0x7c -> +0x86
 *   test +0x12 tst r0, r5
 *   test +0x1e cmp r0, #0x0
 *   test +0x76 cmp r4, #0x10
 *   test +0x7a cmp r7, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200e30; the literal pool and
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
extern void native_fn_022010e0(void);


asm u32 native_ov006_02200e30 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r6, =0x0221c160
    mov r7, #0x0
    mov r4, #0x1
ov006_02200e30_L8:
    mov r0, #0x1
    add r5, r0, #0x0
    ldr r0, [r6, #0]
    lsl r5, r4
    ldrh r0, [r0, #0xa]
    tst r0, r5
    beq ov006_02200e30_L70
    add r0, r4, #0x0
    mov r1, #0x3
    blx native_fn_02014424
    cmp r0, #0x0
    bne ov006_02200e30_L68
    mvn r0, r5
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
    b ov006_02200e30_L70
ov006_02200e30_L68:
    add r0, r7, #0x0
    orr r0, r5
    lsl r0, r0, #0x10
    lsr r7, r0, #0x10
ov006_02200e30_L70:
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    lsr r4, r0, #0x10
    cmp r4, #0x10
    blo ov006_02200e30_L8
    cmp r7, #0x0
    bne ov006_02200e30_L86
    mov r0, #0x7
    bl native_fn_022010e0
    pop {r3, r4, r5, r6, r7, pc}
ov006_02200e30_L86:
    mov r0, #0x4
    bl native_fn_022010e0
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
