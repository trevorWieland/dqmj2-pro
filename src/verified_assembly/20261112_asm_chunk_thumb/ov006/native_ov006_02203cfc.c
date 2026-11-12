/* ov006 row 0x02203cfc: 152 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x84 -> constant 0x04000130 (image word 0x04000130)
 *   pool +0x88 -> constant 0x0221c18c (image word 0x0221c18c)
 *   pool +0x8c -> constant 0x027fffa8 (image word 0x027fffa8)
 *   pool +0x90 -> constant 0x0221c194 (image word 0x0221c194)
 *   pool +0x94 -> constant 0x00002fff (image word 0x00002fff)
 *   branch +0x4a -> +0x52
 *   branch +0x50 -> +0x78
 *   branch +0x5c -> +0x68
 *   branch +0x66 -> +0x78
 *   branch +0x6a -> +0x78
 *   back edge +0x7e -> +0x3e
 *   test +0x48 tst r2, r3
 *   test +0x5a cmp r2, #0x28
 *   test +0x68 cmp r2, #0x2f
 *   test +0x7c cmp r5, #0xe
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203cfc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 13 of 152 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_ov006_02203cfc (register u32 a0)
{
    push {r4, r5, r6, r7}
    ldr r0, =0x04000130
    ldr r1, =0x0221c18c
    ldrh r3, [r0, #0]
    ldr r0, =0x027fffa8
    ldr r2, [r1, #0x4]
    ldrh r0, [r0, #0]
    ldr r6, =0x0221c194
    mov r5, #0x0
    orr r3, r0
    ldr r0, =0x00002fff
    mov r4, #0x1
    eor r3, r0
    and r0, r3
    lsl r0, r0, #0x10
    ldrh r3, [r2, #0x30]
    lsr r0, r0, #0x10
    eor r3, r0
    and r3, r0
    strh r3, [r2, #0x32]
    ldrh r3, [r2, #0x30]
    add r2, r0, #0x0
    eor r2, r3
    and r3, r2
    ldr r2, [r1, #0x4]
    strh r3, [r2, #0x36]
    ldr r2, [r1, #0x4]
    strh r0, [r2, #0x30]
    ldr r3, [r1, #0x4]
    ldrh r2, [r3, #0x32]
    strh r2, [r3, #0x34]
ov006_02203cfc_L3e:
    add r2, r4, #0x0
    lsl r2, r5
    lsl r2, r2, #0x10
    lsr r3, r2, #0x10
    add r2, r0, #0x0
    tst r2, r3
    bne ov006_02203cfc_L52
    mov r2, #0x0
    strb r2, [r6, #0]
    b ov006_02203cfc_L78
ov006_02203cfc_L52:
    ldrb r2, [r6, #0]
    add r2, r2, #0x1
    strb r2, [r6, #0]
    ldrb r2, [r6, #0]
    cmp r2, #0x28
    bne ov006_02203cfc_L68
    ldr r2, [r1, #0x4]
    ldrh r7, [r2, #0x34]
    orr r3, r7
    strh r3, [r2, #0x34]
    b ov006_02203cfc_L78
ov006_02203cfc_L68:
    cmp r2, #0x2f
    bne ov006_02203cfc_L78
    ldr r2, [r1, #0x4]
    ldrh r7, [r2, #0x34]
    orr r3, r7
    strh r3, [r2, #0x34]
    mov r2, #0x28
    strb r2, [r6, #0]
ov006_02203cfc_L78:
    add r5, r5, #0x1
    add r6, r6, #0x1
    cmp r5, #0xe
    blt ov006_02203cfc_L3e
    pop {r4, r5, r6, r7}
    bx lr
}
