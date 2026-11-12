/* ov006 row 0x021efa10: 94 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021efa10; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0201b208(void);
extern void native_fn_0201b19c(void);


asm u32 native_ov006_021efa10 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    lsl r0, r1, #0x10
    add r4, r3, #0x0
    mov r3, #0x0
    lsr r0, r0, #0x10
    add r7, r2, #0x0
    strb r3, [r5, #0]
    asr r1, r0, #0x8
    lsl r2, r0, #0x8
    mov r0, #0xff
    strb r3, [r5, #0x1]
    lsl r1, r1, #0x18
    lsl r0, r0, #0x8
    strb r3, [r5, #0x2]
    lsr r1, r1, #0x18
    and r2, r0
    orr r1, r2
    strb r3, [r5, #0x3]
    add r2, r4, #0x0
    strh r1, [r5, #0]
    add r2, #0xb
    mov r1, #0x7
    bic r2, r1
    lsl r1, r4, #0x10
    sub r6, r2, #0x4
    lsr r2, r1, #0x10
    asr r1, r2, #0x8
    lsl r1, r1, #0x18
    lsl r2, r2, #0x8
    and r0, r2
    lsr r1, r1, #0x18
    orr r0, r1
    strh r0, [r5, #0x2]
    add r5, r5, #0x4
    add r0, r5, #0x0
    add r1, r3, #0x0
    add r2, r6, #0x0
    blx native_fn_0201b208
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r4, #0x0
    blx native_fn_0201b19c
    add r0, r5, r6
    pop {r3, r4, r5, r6, r7, pc}
}
