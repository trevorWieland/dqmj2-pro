/* ov006 row 0x021eb890: 84 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x4c -> native_data_0220d3b8 (image word 0x0220d3b8)
 *   pool +0x50 -> constant 0x02219290 (image word 0x02219290)
 *   branch +0x10 -> +0x44
 *   branch +0x24 -> +0x44
 *   back edge +0x40 -> +0x28
 *   test +0x0c cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x3c cmp r6, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eb890; the literal pool and
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

extern u8 native_data_0220d3b8[];
extern void native_fn_021e7608(void);


asm u32 native_ov006_021eb890 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r5, =native_data_0220d3b8
    ldr r0, [r5, #0x4]
    cmp r0, #0
    beq ov006_021eb890_L44
    ldr r4, =0x02219290
    mov r6, #0
    ldr r0, [r4, #0xc]
    cmp r0, #0
    ble ov006_021eb890_L44
ov006_021eb890_L28:
    ldr r0, [r5, #0x4]
    ldr r0, [r0, r6, lsl #3]
    bl native_fn_021e7608
    ldr r0, [r4, #0xc]
    add r6, r6, #1
    cmp r6, r0
    blt ov006_021eb890_L28
ov006_021eb890_L44:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
