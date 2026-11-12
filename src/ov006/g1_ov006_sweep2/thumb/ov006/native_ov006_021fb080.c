/* ov006 row 0x021fb080: 348 bytes.
 *
 * What it does: Writes one block of 5 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x150 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x154 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x158 -> constant 0x01ff0000 (image word 0x01ff0000)
 *   branch +0x28 -> +0x54
 *   branch +0x2e -> +0x36
 *   branch +0x34 -> +0x3a
 *   back edge +0x8c -> +0x5a
 *   branch +0x98 -> +0xd2
 *   branch +0xd0 -> +0xe2
 *   branch +0xea -> +0x12c
 *   branch +0xee -> +0x12c
 *   branch +0x12a -> +0x140
 *   test +0x26 cmp r0, #0x0
 *   test +0x2c cmp r0, #0x0
 *   test +0x8a cmp r6, #0x5
 *   test +0x96 cmp r0, #0x2
 *   test +0xe8 cmp r0, #0x2
 *   test +0xec cmp r0, #0x6
 *   0 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb080; the literal pool and
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

extern void native_fn_02002480(void);
extern void native_fn_020024bc(void);


asm u32 native_ov006_021fb080 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    ldr r0, =0x0221c0ec
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_02002480
    str r0, [sp, #0x4]
    ldr r0, =0x0221c0ec
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_020024bc
    mov r1, #0x34
    sub r0, r1, r0
    str r0, [sp]
    ldr r0, =0x0221c0ec
    ldr r2, [r0, #0x8]
    ldr r0, [r2, #0x34]
    cmp r0, #0x0
    beq ov006_021fb080_L54
    ldr r0, [sp, #0x4]
    cmp r0, #0x0
    bne ov006_021fb080_L36
    mov r0, #0x26
    str r0, [sp, #0xc]
    b ov006_021fb080_L3a
ov006_021fb080_L36:
    add r1, #0xcc
    str r1, [sp, #0xc]
ov006_021fb080_L3a:
    ldr r1, [r2, #0x34]
    ldr r0, [sp, #0xc]
    ldr r3, [r1, #0]
    ldr r2, =0xfe00ff00
    lsl r0, r0, #0x17
    and r3, r2
    ldr r2, [sp]
    lsr r0, r0, #0x7
    lsl r2, r2, #0x18
    lsr r2, r2, #0x18
    orr r2, r3
    orr r0, r2
    str r0, [r1, #0]
ov006_021fb080_L54:
    mov r6, #0x0
    ldr r3, [sp]
    add r4, r6, #0x0
ov006_021fb080_L5a:
    ldr r0, =0x0221c0ec
    add r6, r6, #0x1
    ldr r0, [r0, #0x8]
    add r0, r0, r4
    ldr r2, [r0, #0x18]
    ldr r0, =0x01ff0000
    ldr r5, [r2, #0]
    add r4, r4, #0x4
    and r0, r5
    lsr r1, r0, #0x10
    lsl r0, r5, #0x18
    lsr r0, r0, #0x18
    mov r12, r0
    lsl r0, r1, #0x17
    lsr r7, r0, #0x7
    ldr r5, [r2, #0]
    ldr r0, =0xfe00ff00
    and r0, r5
    lsl r5, r3, #0x18
    lsr r5, r5, #0x18
    orr r0, r5
    orr r0, r7
    add r3, #0x1d
    str r0, [r2, #0]
    cmp r6, #0x5
    blt ov006_021fb080_L5a
    mov r0, r12
    str r0, [sp, #0x8]
    ldr r0, [sp, #0x4]
    str r1, [sp, #0xc]
    cmp r0, #0x2
    bgt ov006_021fb080_Ld2
    ldr r0, =0x0221c0ec
    mov r4, #0x2
    ldr r0, [r0, #0x8]
    ldr r2, [r0, #0x2c]
    ldr r0, =0x01ff0000
    ldr r1, [r2, #0]
    and r0, r1
    lsr r3, r0, #0x10
    lsl r0, r1, #0x18
    lsr r0, r0, #0x18
    str r0, [sp, #0x8]
    lsl r0, r3, #0x17
    str r3, [sp, #0xc]
    lsr r1, r0, #0x7
    ldr r3, [r2, #0]
    ldr r0, =0xfe00ff00
    and r0, r3
    ldr r3, [sp, #0x4]
    sub r4, r4, r3
    mov r3, #0x1d
    add r5, r4, #0x0
    mul r5, r3
    ldr r3, [sp]
    add r3, r3, r5
    lsl r3, r3, #0x18
    lsr r3, r3, #0x18
    orr r0, r3
    b ov006_021fb080_Le2
ov006_021fb080_Ld2:
    ldr r0, =0x0221c0ec
    ldr r0, [r0, #0x8]
    ldr r2, [r0, #0x2c]
    ldr r0, =0xfe00ff00
    ldr r1, [r2, #0]
    and r1, r0
    mov r0, #0x1
    lsl r0, r0, #0x18
ov006_021fb080_Le2:
    orr r0, r1
    str r0, [r2, #0]
    ldr r0, [sp, #0x4]
    cmp r0, #0x2
    blt ov006_021fb080_L12c
    cmp r0, #0x6
    bgt ov006_021fb080_L12c
    ldr r0, =0x0221c0ec
    mov r4, #0x6
    ldr r0, [r0, #0x8]
    ldr r2, [r0, #0x30]
    ldr r0, =0x01ff0000
    ldr r1, [r2, #0]
    and r0, r1
    lsr r3, r0, #0x10
    lsl r0, r1, #0x18
    lsr r0, r0, #0x18
    str r0, [sp, #0x8]
    lsl r0, r3, #0x17
    str r3, [sp, #0xc]
    lsr r1, r0, #0x7
    ldr r3, [r2, #0]
    ldr r0, =0xfe00ff00
    and r0, r3
    ldr r3, [sp, #0x4]
    sub r4, r4, r3
    mov r3, #0x1d
    add r5, r4, #0x0
    mul r5, r3
    ldr r3, [sp]
    add r3, r3, r5
    lsl r3, r3, #0x18
    lsr r3, r3, #0x18
    orr r0, r3
    orr r0, r1
    str r0, [r2, #0]
    b ov006_021fb080_L140
ov006_021fb080_L12c:
    ldr r0, =0x0221c0ec
    ldr r0, [r0, #0x8]
    ldr r2, [r0, #0x30]
    ldr r0, =0xfe00ff00
    ldr r1, [r2, #0]
    and r1, r0
    mov r0, #0x1
    lsl r0, r0, #0x18
    orr r0, r1
    str r0, [r2, #0]
ov006_021fb080_L140:
    ldr r0, =0x0221c0ec
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x44
    strb r1, [r0, #0]
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
