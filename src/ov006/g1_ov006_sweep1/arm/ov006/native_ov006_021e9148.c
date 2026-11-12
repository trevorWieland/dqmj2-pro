/* ov006 row 0x021e9148: 172 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x02218e60 (image word 0x02218e60)
 *   pool +0xa4 -> native_data3_02218d90 (image word 0x02218d90)
 *   pool +0xa8 -> constant 0x02218e18 (image word 0x02218e18)
 *   branch +0x10 -> +0x98
 *   branch +0x18 -> +0x30
 *   branch +0x2c -> +0x60
 *   branch +0x40 -> +0x60
 *   test +0x0c cmp r0, #0
 *   test +0x14 cmp r4, #0
 *   test +0x34 cmp r0, #0
 *   test +0x3c cmpne r2, #0
 *   test +0x70 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9148; the literal pool and
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

extern void native_fn_021e7e90(void);
extern void native_fn_0205fa4c(void);
extern void native_fn_021e90c0(void);
extern void native_fn_02049ae4(void);
extern u8 native_data3_02218d90[];
extern void native_fn_0204b61c(void);
extern void native_fn_021e8044(void);


asm u32 native_ov006_021e9148 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r1
    bl native_fn_021e7e90
    cmp r0, #0
    beq ov006_021e9148_L98
    cmp r4, #0
    bne ov006_021e9148_L30
    ldr r0, =0x02218e60
    mov r1, #1
    bl native_fn_0205fa4c
    bl native_fn_021e90c0
    b ov006_021e9148_L60
ov006_021e9148_L30:
    bl native_fn_02049ae4
    cmp r0, #0
    ldrne r2, [r0, #0x4]
    cmpne r2, #0
    beq ov006_021e9148_L60
    ldr r0, =native_data3_02218d90
    ldr r1, [r2, #0x80]
    ldr r0, [r0, #0x3c]
    bic r1, r1, #8
    mov r0, r0, lsl #31
    orr r0, r1, r0, lsr #28
    str r0, [r2, #0x80]
ov006_021e9148_L60:
    ldr r0, =0x02218e18
    mov r1, #0
    bl native_fn_0204b61c
    ldr r1, =native_data3_02218d90
    cmp r4, #0
    movne r0, #4
    ldr r1, [r1, #0x5c]
    moveq r0, #3
    bl native_fn_021e8044
    ldr r0, =native_data3_02218d90
    mov r1, #0
    str r1, [r0, #0x4]
    mov r0, #1
    ldmia sp!, {r4, pc}
ov006_021e9148_L98:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
