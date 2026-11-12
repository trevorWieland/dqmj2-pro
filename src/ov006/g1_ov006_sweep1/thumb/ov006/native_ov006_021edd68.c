/* ov006 row 0x021edd68: 140 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> native_data_0220d450 (image word 0x0220d450)
 *   branch +0x34 -> +0x58
 *   branch +0x44 -> +0x56
 *   back edge +0x5e -> +0x2e
 *   branch +0x6e -> +0x76
 *   branch +0x78 -> +0x80
 *   test +0x32 tst r3, r7
 *   test +0x42 tst r3, r7
 *   test +0x5c cmp r0, #0xc
 *   test +0x6c cmp r0, #0x1
 *   test +0x76 cmp r0, #0x2
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021edd68; the literal pool and
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

extern void native_fn_02008bf8(void);
extern u8 native_data_0220d450[];


asm u32 native_ov006_021edd68 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    ldrh r0, [r5, #0xa]
    add r4, r1, #0x0
    add r1, r4, #0x4
    str r0, [r4, #0]
    add r0, r5, #0x0
    add r0, #0xc
    mov r2, #0x20
    blx native_fn_02008bf8
    ldrh r0, [r5, #0x36]
    add r1, r4, #0x0
    add r1, #0x30
    str r0, [r4, #0x24]
    add r0, r5, #0x4
    mov r2, #0x6
    blx native_fn_02008bf8
    mov r1, #0x0
    ldr r2, =native_data_0220d450
    add r0, r1, #0x0
    mov r6, #0x80
ov006_021edd68_L2e:
    ldrh r7, [r5, #0x30]
    ldrh r3, [r2, #0]
    tst r3, r7
    beq ov006_021edd68_L58
    ldrb r7, [r2, #0x2]
    add r3, r4, r1
    add r3, #0x3c
    strb r7, [r3, #0]
    ldrh r7, [r5, #0x2e]
    ldrh r3, [r2, #0]
    tst r3, r7
    beq ov006_021edd68_L56
    add r3, r4, r1
    add r3, #0x3c
    ldrb r3, [r3, #0]
    add r7, r3, #0x0
    add r3, r4, r1
    orr r7, r6
    add r3, #0x3c
    strb r7, [r3, #0]
ov006_021edd68_L56:
    add r1, r1, #0x1
ov006_021edd68_L58:
    add r0, r0, #0x1
    add r2, r2, #0x4
    cmp r0, #0xc
    blt ov006_021edd68_L2e
    str r1, [r4, #0x38]
    ldrh r0, [r5, #0x32]
    str r0, [r4, #0x4c]
    ldrh r1, [r5, #0x2c]
    mov r0, #0x3
    and r0, r1
    cmp r0, #0x1
    bne ov006_021edd68_L76
    mov r0, #0x1
    str r0, [r4, #0x50]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021edd68_L76:
    cmp r0, #0x2
    bne ov006_021edd68_L80
    mov r0, #0x2
    str r0, [r4, #0x50]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021edd68_L80:
    mov r0, #0x0
    str r0, [r4, #0x50]
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
