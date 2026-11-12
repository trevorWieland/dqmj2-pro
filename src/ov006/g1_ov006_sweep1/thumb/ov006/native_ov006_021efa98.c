/* ov006 row 0x021efa98: 212 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1a -> +0x22
 *   branch +0x26 -> +0x2e
 *   branch +0x44 -> +0xae
 *   branch +0x4a -> +0x56
 *   branch +0x4e -> +0x6e
 *   branch +0x52 -> +0x88
 *   branch +0x54 -> +0x9e
 *   branch +0x6c -> +0x9e
 *   branch +0x86 -> +0x9e
 *   back edge +0xac -> +0x46
 *   branch +0xb0 -> +0xb8
 *   branch +0xb6 -> +0xbe
 *   branch +0xc0 -> +0xc8
 *   branch +0xc6 -> +0xcc
 *   test +0x18 cmp r5, #0x0
 *   test +0x24 cmp r0, #0x1
 *   test +0x42 cmp r0, #0x0
 *   test +0x48 cmp r1, #0x1
 *   test +0x4c cmp r1, #0x2
 *   test +0x50 cmp r1, #0x5
 *   test +0xaa cmp r0, #0x0
 *   test +0xae cmp r6, #0x1
 *   test +0xb4 cmp r0, #0x1
 *   test +0xbe cmp r7, #0x1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021efa98; the literal pool and
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

extern void native_fn_021ef858(void);
extern void native_fn_021ef8c8(void);


asm u32 native_ov006_021efa98 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x1c
    str r1, [sp]
    add r1, sp, #0x18
    add r2, sp, #0x14
    bl native_fn_021ef858
    mov r6, #0x0
    add r5, r0, #0x0
    add r7, r6, #0x0
    str r5, [sp, #0x8]
    str r6, [sp, #0x4]
    cmp r5, #0x0
    bne ov006_021efa98_L22
    add sp, #0x1c
    add r0, r6, #0x0
    pop {r4, r5, r6, r7, pc}
ov006_021efa98_L22:
    ldr r0, [sp, #0x18]
    cmp r0, #0x1
    beq ov006_021efa98_L2e
    add sp, #0x1c
    add r0, r6, #0x0
    pop {r4, r5, r6, r7, pc}
ov006_021efa98_L2e:
    ldr r4, [sp, #0x14]
    add r0, r5, #0x0
    add r0, #0x8
    str r0, [sp, #0x8]
    add r0, sp, #0x8
    add r1, r5, r4
    add r2, sp, #0x10
    add r3, sp, #0xc
    bl native_fn_021ef8c8
    cmp r0, #0x0
    beq ov006_021efa98_Lae
ov006_021efa98_L46:
    ldr r1, [sp, #0x10]
    cmp r1, #0x1
    beq ov006_021efa98_L56
    cmp r1, #0x2
    beq ov006_021efa98_L6e
    cmp r1, #0x5
    beq ov006_021efa98_L88
    b ov006_021efa98_L9e
ov006_021efa98_L56:
    ldrh r1, [r0, #0]
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r0, r1
    orr r0, r2
    lsl r0, r0, #0x10
    lsr r6, r0, #0x10
    b ov006_021efa98_L9e
ov006_021efa98_L6e:
    ldrh r1, [r0, #0]
    asr r0, r1, #0x8
    lsl r2, r1, #0x8
    mov r1, #0xff
    lsl r0, r0, #0x18
    lsl r1, r1, #0x8
    lsr r0, r0, #0x18
    and r1, r2
    orr r0, r1
    lsl r0, r0, #0x10
    lsr r0, r0, #0x10
    str r0, [sp, #0x4]
    b ov006_021efa98_L9e
ov006_021efa98_L88:
    ldrh r1, [r0, #0]
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r0, r1
    orr r0, r2
    lsl r0, r0, #0x10
    lsr r7, r0, #0x10
ov006_021efa98_L9e:
    add r0, sp, #0x8
    add r1, r5, r4
    add r2, sp, #0x10
    add r3, sp, #0xc
    bl native_fn_021ef8c8
    cmp r0, #0x0
    bne ov006_021efa98_L46
ov006_021efa98_Lae:
    cmp r6, #0x1
    bne ov006_021efa98_Lb8
    ldr r0, [sp, #0x4]
    cmp r0, #0x1
    beq ov006_021efa98_Lbe
ov006_021efa98_Lb8:
    add sp, #0x1c
    mov r0, #0x0
    pop {r4, r5, r6, r7, pc}
ov006_021efa98_Lbe:
    cmp r7, #0x1
    blt ov006_021efa98_Lc8
    mov r1, #0x1
    ldr r0, [sp]
    b ov006_021efa98_Lcc
ov006_021efa98_Lc8:
    ldr r0, [sp]
    mov r1, #0x0
ov006_021efa98_Lcc:
    str r1, [r0, #0]
    mov r0, #0x1
    add sp, #0x1c
    pop {r4, r5, r6, r7, pc}
}
