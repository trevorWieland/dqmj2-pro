/* ov006 row 0x021e9484: 96 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> native_data_0220d114 (image word 0x0220d114)
 *   pool +0x5c -> constant 0x02218d90 (image word 0x02218d90)
 *   branch +0x14 -> +0x50
 *   test +0x10 cmp r0, r1
 *   test +0x1c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9484; the literal pool and
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

extern u8 native_data_0220d114[];
extern void native_fn_0205f45c(void);
extern void native_fn_0205e814(void);


asm u32 native_ov006_021e9484 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_0220d114
    mvn r1, #0
    ldr r0, [r0, #0x20]
    cmp r0, r1
    beq ov006_021e9484_L50
    bl native_fn_0205f45c
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r3, pc}
    ldr r0, =0x02218d90
    ldr r3, =native_data_0220d114
    ldr r1, [r0, #0x58]
    mvn r12, #0
    mov r0, #0
    mov r2, #30
    str r12, [r3, #0x20]
    bl native_fn_0205e814
    mov r0, #1
    ldmia sp!, {r3, pc}
ov006_021e9484_L50:
    mov r0, #1
    ldmia sp!, {r3, pc}
}
