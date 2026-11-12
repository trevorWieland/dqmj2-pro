/* ov006 row 0x021ddb28: 232 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xdc -> native_data5_0220f4e8 (image word 0x0220f4e8)
 *   pool +0xe0 -> native_data3_0220d060 (image word 0x0220d060)
 *   pool +0xe4 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x30 -> +0x68
 *   branch +0x88 -> +0xb4
 *   test +0x2c cmp r4, r0
 *   test +0x3c cmp r4, #6
 *   test +0x70 cmp r0, #1
 *   test +0x84 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ddb28; the literal pool and
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

extern u8 native_data5_0220f4e8[];
extern u8 native_data3_0220d060[];
extern void native_fn_021de618(void);
extern void native_fn_021dfa24(void);
extern void native_fn_020642cc(void);
extern void native_fn_021df5a4(void);
extern void native_fn_020851d4(void);
extern void native_fn_02085200(void);
extern void native_fn_0204176c(void);
extern void native_fn_021df4d8(void);


asm u32 native_ov006_021ddb28 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =native_data5_0220f4e8
    ldr r2, =native_data3_0220d060
    ldr r1, [r0, #0x4]
    mov r0, #12
    mla r5, r1, r0, r2
    ldr r0, [r5, #0x4]
    blx r0
    ldr r1, =native_data5_0220f4e8
    mov r4, r0
    ldr r0, [r1, #0x4]
    cmp r4, r0
    beq ov006_021ddb28_L68
    ldr r0, [r5, #0x8]
    blx r0
    cmp r4, #6
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    mov r0, #12
    mul r2, r4, r0
    ldr r3, =native_data3_0220d060
    ldr r0, =native_data5_0220f4e8
    ldr r1, [r3, r2]
    str r4, [r0, #0x4]
    add r5, r3, r2
    blx r1
ov006_021ddb28_L68:
    ldr r0, =native_data5_0220f4e8
    ldr r0, [r0, #0x4]
    cmp r0, #1
    moveq r0, #11
    ldmeqia sp!, {r3, r4, r5, pc}
    bl native_fn_021de618
    bl native_fn_021dfa24
    cmp r0, #0
    bne ov006_021ddb28_Lb4
    ldr r0, [r5, #0x8]
    blx r0
    mov r0, #37
    bl native_fn_020642cc
    ldr r0, =native_data3_0220d060
    ldr r1, =native_data5_0220f4e8
    mov r2, #2
    ldr r0, [r0, #0x18]
    str r2, [r1, #0x4]
    blx r0
ov006_021ddb28_Lb4:
    bl native_fn_021df5a4
    bl native_fn_020851d4
    bl native_fn_02085200
    ldr r0, =0x02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    bl native_fn_0204176c
    bl native_fn_021df4d8
    mov r0, #11
    ldmia sp!, {r3, r4, r5, pc}
}
