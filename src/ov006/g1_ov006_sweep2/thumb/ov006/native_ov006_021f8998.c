/* ov006 row 0x021f8998: 128 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x78 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0x7c -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   branch +0x1a -> +0x1e
 *   branch +0x22 -> +0x6a
 *   back edge +0x68 -> +0x28
 *   test +0x18 cmp r1, #0x5
 *   test +0x20 cmp r1, #0x0
 *   test +0x66 cmp r2, r1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8998; the literal pool and
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

extern void native_fn_020024bc(void);


asm u32 native_ov006_021f8998 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0221c0d8
    mov r1, #0x1c
    ldrh r0, [r0, #0x2]
    blx native_fn_020024bc
    mov r1, #0x36
    sub r0, r1, r0
    ldr r1, =0x0221c0d8
    ldr r1, [r1, #0x4]
    add r1, #0x51
    ldrb r1, [r1, #0]
    cmp r1, #0x5
    ble ov006_021f8998_L1e
    mov r1, #0x5
ov006_021f8998_L1e:
    mov r2, #0x0
    cmp r1, #0x0
    ble ov006_021f8998_L6a
    ldr r4, =0x0221c0d8
    add r3, r2, #0x0
ov006_021f8998_L28:
    ldr r5, [r4, #0x4]
    add r2, r2, #0x1
    add r5, r5, r3
    ldr r6, [r5, #0x10]
    ldr r5, =0xfe00ff00
    ldr r7, [r6, #0]
    and r5, r7
    sub r7, r0, #0x2
    lsl r7, r7, #0x18
    lsr r7, r7, #0x18
    orr r7, r5
    mov r5, #0xb3
    lsl r5, r5, #0x10
    orr r5, r7
    str r5, [r6, #0]
    ldr r5, [r4, #0x4]
    add r5, r5, r3
    ldr r6, [r5, #0x24]
    ldr r5, =0xfe00ff00
    ldr r7, [r6, #0]
    add r3, r3, #0x4
    and r5, r7
    add r7, r0, #0x1
    lsl r7, r7, #0x18
    lsr r7, r7, #0x18
    orr r7, r5
    mov r5, #0xd2
    lsl r5, r5, #0x10
    orr r5, r7
    str r5, [r6, #0]
    add r0, #0x1c
    cmp r2, r1
    blt ov006_021f8998_L28
ov006_021f8998_L6a:
    ldr r0, =0x0221c0d8
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x56
    strb r1, [r0, #0]
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
