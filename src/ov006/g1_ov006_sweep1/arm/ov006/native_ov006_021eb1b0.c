/* ov006 row 0x021eb1b0: 144 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> native_data2_02219290 (image word 0x02219290)
 *   pool +0x8c -> native_data2_0220d3b8 (image word 0x0220d3b8)
 *   branch +0x1c -> +0x54
 *   branch +0x24 -> +0x54
 *   test +0x10 cmp r1, #0
 *   test +0x18 cmp r4, #0
 *   test +0x20 cmp r4, #64
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmpeq r0, #0
 *   test +0x4c cmpeq r0, #0
 *   test +0x5c cmp r0, r4
 *   test +0x64 cmp r0, #0
 *   test +0x68 cmpge r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eb1b0; the literal pool and
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

extern u8 native_data2_02219290[];
extern void native_fn_020685f0(void);
extern void native_fn_0206877c(void);
extern u8 native_data2_0220d3b8[];


asm u32 native_ov006_021eb1b0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =native_data2_02219290
    mov r4, r0
    ldr r1, [r1, #0x2c]
    cmp r1, #0
    ldmneia sp!, {r3, r4, r5, pc}
    cmp r4, #0
    blt ov006_021eb1b0_L54
    cmp r4, #64
    bge ov006_021eb1b0_L54
    bl native_fn_020685f0
    mov r5, r0
    mov r0, r4
    bl native_fn_0206877c
    ldr r0, [r5, #0x3c]
    cmp r0, #0
    ldreq r0, [r5, #0x40]
    cmpeq r0, #0
    ldreq r0, [r5, #0x44]
    cmpeq r0, #0
    mvneq r4, #0
ov006_021eb1b0_L54:
    ldr r0, =native_data2_0220d3b8
    ldr r0, [r0, #0x8]
    cmp r0, r4
    ldmeqia sp!, {r3, r4, r5, pc}
    cmp r0, #0
    cmpge r4, #0
    movlt r2, #2
    ldr r0, =native_data2_0220d3b8
    ldr r1, =native_data2_02219290
    movge r2, #3
    str r2, [r1, #0x2c]
    str r4, [r0, #0x8]
    ldmia sp!, {r3, r4, r5, pc}
}
