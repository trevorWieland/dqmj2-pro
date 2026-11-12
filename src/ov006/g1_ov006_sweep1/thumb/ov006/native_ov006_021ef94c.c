/* ov006 row 0x021ef94c: 194 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x3e -> +0x50
 *   branch +0x4e -> +0x58
 *   branch +0x98 -> +0xa4
 *   back edge +0xa2 -> +0x9a
 *   test +0x3c cmp r3, #0x0
 *   test +0x96 cmp r6, r4
 *   test +0xa0 cmp r1, r4
 *   0 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef94c; the literal pool and
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

extern void native_fn_021f058c(void);
extern void native_fn_0201b19c(void);


asm u32 native_ov006_021ef94c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r7, r3, #0x0
    add r6, r0, #0x0
    add r0, r7, #0x0
    sub r0, #0x8
    str r1, [sp, #0x4]
    lsl r0, r0, #0x10
    add r1, r2, #0x0
    mov r5, #0x0
    strb r5, [r1, #0]
    lsr r0, r0, #0x10
    strb r5, [r1, #0x1]
    asr r2, r0, #0x8
    strb r5, [r1, #0x2]
    lsl r2, r2, #0x18
    strb r5, [r1, #0x3]
    lsr r3, r2, #0x18
    lsl r2, r0, #0x8
    mov r0, #0xff
    strb r5, [r1, #0x4]
    lsl r0, r0, #0x8
    strb r5, [r1, #0x5]
    and r0, r2
    strb r5, [r1, #0x6]
    orr r0, r3
    strb r5, [r1, #0x7]
    ldr r3, [sp, #0x20]
    add r4, r6, #0x0
    strh r0, [r1, #0]
    cmp r3, #0x0
    beq ov006_021ef94c_L50
    mov r0, #0x10
    str r0, [sp]
    add r0, r6, #0x6
    add r2, r7, #0x0
    bl native_fn_021f058c
    add r7, #0x8
    b ov006_021ef94c_L58
ov006_021ef94c_L50:
    add r0, r6, #0x6
    add r2, r7, #0x0
    blx native_fn_0201b19c
ov006_021ef94c_L58:
    mov r0, #0x0
    strb r0, [r6, #0]
    strb r0, [r6, #0x1]
    strb r0, [r6, #0x2]
    strb r0, [r6, #0x3]
    strb r0, [r6, #0x4]
    strb r0, [r6, #0x5]
    ldr r0, [sp, #0x4]
    lsl r0, r0, #0x10
    lsr r1, r0, #0x10
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r1, r0
    orr r1, r2
    strh r1, [r6, #0]
    lsl r1, r7, #0x10
    lsr r2, r1, #0x10
    asr r1, r2, #0x8
    lsl r1, r1, #0x18
    lsl r2, r2, #0x8
    lsr r1, r1, #0x18
    and r0, r2
    orr r0, r1
    strh r0, [r6, #0x2]
    add r0, r4, #0x6
    add r4, r0, r7
    add r1, r6, #0x0
    cmp r6, r4
    bhs ov006_021ef94c_La4
ov006_021ef94c_L9a:
    ldrb r0, [r1, #0]
    add r1, r1, #0x1
    add r5, r5, r0
    cmp r1, r4
    blo ov006_021ef94c_L9a
ov006_021ef94c_La4:
    lsl r0, r5, #0x10
    lsr r1, r0, #0x10
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r0, r1
    orr r0, r2
    strh r0, [r4, #0]
    add r0, r4, #0x2
    sub r0, r0, r6
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
