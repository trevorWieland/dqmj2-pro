/* ov006 row 0x021e8f2c: 148 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x88 -> constant 0x02218d90 (image word 0x02218d90)
 *   pool +0x8c -> native_data2_02218f38 (image word 0x02218f38)
 *   pool +0x90 -> native_data2_02218ea8 (image word 0x02218ea8)
 *   branch +0x34 -> +0x44
 *   branch +0x5c -> +0x6c
 *   test +0x48 cmp r3, r0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e8f2c; the literal pool and
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

extern u8 native_data2_02218f38[];
extern u8 native_data2_02218ea8[];
extern void native_fn_021e8044(void);
extern void native_fn_021e648c(void);


asm u32 native_ov006_021e8f2c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r12, =0x2aaaaaab
    add lr, r0, #5
    smull r3, r0, r12, r14
    ldr r1, =0x02218d90
    add r0, r0, lr, lsr #31
    ldr r1, [r1, #0x5c]
    smull r4, r3, r12, r1
    mov r4, r2
    adds r3, r3, r1, lsr #31
    ldreq r2, =native_data2_02218f38
    ldreq r12, [r2, #0x7c]
    biceq r12, r12, #2
    beq ov006_021e8f2c_L44
    ldr r2, =native_data2_02218f38
    ldr r12, [r2, #0x7c]
    orr r12, r12, #2
ov006_021e8f2c_L44:
    sub r0, r0, #1
    cmp r3, r0
    ldrge r0, =native_data2_02218ea8
    str r12, [r2, #0x7c]
    ldrge r2, [r0, #0x7c]
    bicge r2, r2, #2
    bge ov006_021e8f2c_L6c
    ldr r0, =native_data2_02218ea8
    ldr r2, [r0, #0x7c]
    orr r2, r2, #2
ov006_021e8f2c_L6c:
    str r2, [r0, #0x7c]
    mov r0, #0
    bl native_fn_021e8044
    mov r0, r4
    bl native_fn_021e648c
    ldmia sp!, {r4, pc}
}
