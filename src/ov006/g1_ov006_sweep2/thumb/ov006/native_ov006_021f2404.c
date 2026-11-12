/* ov006 row 0x021f2404: 96 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x50 -> constant 0x0221c008 (image word 0x0221c008)
 *   pool +0x54 -> native_data_0220b0e8 (image word 0x0220b0e8)
 *   pool +0x58 -> native_data_0220b0da (image word 0x0220b0da)
 *   pool +0x5c -> native_data_0220b0c4 (image word 0x0220b0c4)
 *   branch +0x20 -> +0x4c
 *   back edge +0x4a -> +0x24
 *   test +0x1e cmp r6, #0x0
 *   test +0x48 cmp r4, r6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2404; the literal pool and
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

extern u8 native_data_0220b0e8[];
extern void native_fn_02202eb0(void);
extern u8 native_data_0220b0da[];
extern u8 native_data_0220b0c4[];


asm u32 native_ov006_021f2404 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r7, r0, #0x0
    ldr r0, =0x0221c008
    add r3, r7, #0x0
    ldr r2, [r0, #0]
    ldr r0, =native_data_0220b0e8
    ldrb r1, [r2, #0x17]
    ldrb r6, [r0, r1]
    ldr r0, [r2, #0x8]
    mov r1, #0x0
    mvn r1, r1
    mov r2, #0x0
    bl native_fn_02202eb0
    mov r4, #0x0
    cmp r6, #0x0
    ble ov006_021f2404_L4c
    add r5, r4, #0x0
ov006_021f2404_L24:
    ldr r0, =0x0221c008
    mov r1, #0x0
    ldr r2, [r0, #0]
    mvn r1, r1
    ldr r0, [r2, r5]
    ldrb r2, [r2, #0x17]
    lsl r3, r2, #0x1
    ldr r2, =native_data_0220b0da
    add r2, r2, r3
    ldrb r2, [r4, r2]
    lsl r3, r2, #0x2
    ldr r2, =native_data_0220b0c4
    ldrh r2, [r2, r3]
    add r3, r7, #0x4
    bl native_fn_02202eb0
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, r6
    blt ov006_021f2404_L24
ov006_021f2404_L4c:
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
