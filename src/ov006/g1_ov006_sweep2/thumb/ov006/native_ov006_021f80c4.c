/* ov006 row 0x021f80c4: 240 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xdc -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0xe0 -> native_data_0220b654 (image word 0x0220b654)
 *   pool +0xe4 -> constant 0x000003ff (image word 0x000003ff)
 *   pool +0xe8 -> native_data_0220b658 (image word 0x0220b658)
 *   pool +0xec -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   branch +0x0c -> +0x10
 *   branch +0x14 -> +0x3e
 *   back edge +0x3c -> +0x1a
 *   back edge +0x6c -> +0x44
 *   back edge +0x9c -> +0x74
 *   branch +0xa2 -> +0xd8
 *   back edge +0xd6 -> +0xac
 *   test +0x0a cmp r6, #0x5
 *   test +0x12 cmp r6, #0x0
 *   test +0x3a cmp r4, r6
 *   test +0x6a cmp r7, #0x3
 *   test +0x9a cmp r7, #0x4
 *   test +0xa0 cmp r6, #0x0
 *   test +0xd4 cmp r4, r6
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f80c4; the literal pool and
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

extern void native_fn_0220303c(void);
extern u8 native_data_0220b654[];
extern void native_fn_02202ff0(void);
extern u8 native_data_0220b658[];


asm u32 native_ov006_021f80c4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0221c0d8
    ldr r0, [r0, #0x4]
    add r0, #0x51
    ldrb r6, [r0, #0]
    cmp r6, #0x5
    ble ov006_021f80c4_L10
    mov r6, #0x5
ov006_021f80c4_L10:
    mov r4, #0x0
    cmp r6, #0x0
    ble ov006_021f80c4_L3e
    ldr r7, =0x0221c0d8
    add r5, r4, #0x0
ov006_021f80c4_L1a:
    mov r0, #0x0
    mov r1, #0x2e
    bl native_fn_0220303c
    ldr r1, [r7, #0x4]
    add r1, r1, r5
    str r0, [r1, #0x10]
    mov r0, #0x0
    mov r1, #0x18
    bl native_fn_0220303c
    ldr r1, [r7, #0x4]
    add r4, r4, #0x1
    add r1, r1, r5
    str r0, [r1, #0x24]
    add r5, r5, #0x4
    cmp r4, r6
    blt ov006_021f80c4_L1a
ov006_021f80c4_L3e:
    mov r7, #0x0
    ldr r4, =native_data_0220b654
    add r5, r7, #0x0
ov006_021f80c4_L44:
    ldr r2, =0x0221c0d8
    ldrb r1, [r4, #0]
    ldr r2, [r2, #0x4]
    mov r0, #0x0
    ldr r2, [r2, #0x10]
    bl native_fn_02202ff0
    ldr r0, =0x0221c0d8
    add r7, r7, #0x1
    ldr r0, [r0, #0x4]
    add r4, r4, #0x1
    ldr r1, [r0, #0x10]
    add r0, r0, r5
    ldrh r2, [r1, #0x4]
    ldr r1, =0x000003ff
    add r0, #0x42
    and r1, r2
    add r5, r5, #0x2
    strh r1, [r0, #0]
    cmp r7, #0x3
    blo ov006_021f80c4_L44
    mov r7, #0x0
    ldr r4, =native_data_0220b658
    add r5, r7, #0x0
ov006_021f80c4_L74:
    ldr r2, =0x0221c0d8
    ldrb r1, [r4, #0]
    ldr r2, [r2, #0x4]
    mov r0, #0x0
    ldr r2, [r2, #0x24]
    bl native_fn_02202ff0
    ldr r0, =0x0221c0d8
    add r7, r7, #0x1
    ldr r0, [r0, #0x4]
    add r4, r4, #0x1
    ldr r1, [r0, #0x24]
    add r0, r0, r5
    ldrh r2, [r1, #0x4]
    ldr r1, =0x000003ff
    add r0, #0x48
    and r1, r2
    add r5, r5, #0x2
    strh r1, [r0, #0]
    cmp r7, #0x4
    blo ov006_021f80c4_L74
    mov r4, #0x0
    cmp r6, #0x0
    ble ov006_021f80c4_Ld8
    mov r0, #0x3
    ldr r1, =0x0221c0d8
    add r3, r4, #0x0
    lsl r0, r0, #0xa
ov006_021f80c4_Lac:
    ldr r2, [r1, #0x4]
    ldr r5, =0xfffff3ff
    add r2, r2, r3
    ldr r2, [r2, #0x10]
    add r4, r4, #0x1
    ldrh r7, [r2, #0x4]
    and r7, r5
    mov r5, #0x3
    lsl r5, r5, #0xa
    orr r5, r7
    strh r5, [r2, #0x4]
    ldr r2, [r1, #0x4]
    ldr r5, =0xfffff3ff
    add r2, r2, r3
    ldr r2, [r2, #0x24]
    add r3, r3, #0x4
    ldrh r7, [r2, #0x4]
    and r5, r7
    orr r5, r0
    strh r5, [r2, #0x4]
    cmp r4, r6
    blt ov006_021f80c4_Lac
ov006_021f80c4_Ld8:
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
