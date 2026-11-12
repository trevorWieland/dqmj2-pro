/* ov006 row 0x021e9700: 140 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> native_data_02208394 (image word 0x02208394)
 *   pool +0x84 -> native_data2_02219280 (image word 0x02219280)
 *   pool +0x88 -> native_data_02208328 (image word 0x02208328)
 *   branch +0x1c -> +0x78
 *   branch +0x24 -> +0x78
 *   branch +0x44 -> +0x78
 *   branch +0x58 -> +0x70
 *   test +0x20 cmp r5, #0
 *   test +0x34 cmp r5, r0
 *   test +0x40 cmpne r0, r5
 *   test +0x54 cmp r1, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9700; the literal pool and
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

extern u8 native_data_02208394[];
extern void native_fn_021e8fc0(void);
extern void native_fn_021e8000(void);
extern u8 native_data2_02219280[];
extern u8 native_data_02208328[];
extern void native_fn_021e9da8(void);
extern void native_fn_021eb9a4(void);


asm u32 native_ov006_021e9700 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r1, =native_data_02208394
    mov r2, r5
    mov r0, #6
    bl native_fn_021e8fc0
    movs r4, r0
    bne ov006_021e9700_L78
    cmp r5, #0
    beq ov006_021e9700_L78
    bl native_fn_021e8000
    mov r5, r0
    mvn r0, #0
    cmp r5, r0
    ldrne r0, =native_data2_02219280
    ldrne r0, [r0]
    cmpne r0, r5
    beq ov006_021e9700_L78
    ldr r0, =native_data_02208328
    ldr r1, [r0, r5, lsl #3]
    add r0, r0, r5, lsl #3
    cmp r1, #0
    beq ov006_021e9700_L70
    bl native_fn_021e9da8
    mov r0, #4
    mov r1, #1
    mov r2, #0
    bl native_fn_021eb9a4
ov006_021e9700_L70:
    ldr r0, =native_data2_02219280
    str r5, [r0]
ov006_021e9700_L78:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
