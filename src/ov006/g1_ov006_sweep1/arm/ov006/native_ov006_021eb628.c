/* ov006 row 0x021eb628: 156 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> native_data_02208544 (image word 0x02208544)
 *   pool +0x84 -> native_data_022084fc (image word 0x022084fc)
 *   pool +0x88 -> native_data_02208548 (image word 0x02208548)
 *   pool +0x8c -> native_data_0220851c (image word 0x0220851c)
 *   pool +0x90 -> native_data_02208500 (image word 0x02208500)
 *   pool +0x94 -> constant 0x02219290 (image word 0x02219290)
 *   pool +0x98 -> native_data_0220d3b8 (image word 0x0220d3b8)
 *   branch +0x50 -> +0x74
 *   back edge +0x70 -> +0x58
 *   test +0x4c cmp r0, #0
 *   test +0x6c cmp r6, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eb628; the literal pool and
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

extern u8 native_data_02208544[];
extern void native_fn_021e767c(void);
extern u8 native_data_022084fc[];
extern u8 native_data_02208548[];
extern u8 native_data_0220851c[];
extern u8 native_data_02208500[];
extern u8 native_data_0220d3b8[];
extern void native_fn_021e7b64(void);
extern void native_fn_021eb240(void);


asm u32 native_ov006_021eb628 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r1, =native_data_02208544
    mov r0, #36
    bl native_fn_021e767c
    ldr r1, =native_data_022084fc
    mov r0, #37
    bl native_fn_021e767c
    ldr r1, =native_data_02208548
    mov r0, #38
    bl native_fn_021e767c
    ldr r1, =native_data_0220851c
    mov r0, #39
    bl native_fn_021e767c
    ldr r1, =native_data_02208500
    mov r0, #40
    bl native_fn_021e767c
    ldr r5, =0x02219290
    mov r6, #0
    ldr r0, [r5, #0xc]
    cmp r0, #0
    ble ov006_021eb628_L74
    ldr r4, =native_data_0220d3b8
ov006_021eb628_L58:
    ldr r0, [r4, #0x4]
    ldr r0, [r0, r6, lsl #3]
    bl native_fn_021e7b64
    ldr r0, [r5, #0xc]
    add r6, r6, #1
    cmp r6, r0
    blt ov006_021eb628_L58
ov006_021eb628_L74:
    mov r0, #0
    bl native_fn_021eb240
    ldmia sp!, {r4, r5, r6, pc}
}
