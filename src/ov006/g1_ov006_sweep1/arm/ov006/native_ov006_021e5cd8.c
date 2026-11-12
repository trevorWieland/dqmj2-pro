/* ov006 row 0x021e5cd8: 136 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> native_data3_0220d108 (image word 0x0220d108)
 *   pool +0x84 -> constant 0x02218d70 (image word 0x02218d70)
 *   branch +0x10 -> +0x2c
 *   branch +0x18 -> +0x5c
 *   branch +0x28 -> +0x78
 *   branch +0x40 -> +0x50
 *   branch +0x4c -> +0x78
 *   branch +0x58 -> +0x78
 *   test +0x0c cmp r0, r2
 *   test +0x14 cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e5cd8; the literal pool and
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

extern void native_fn_021e65a4(void);
extern void native_fn_021e8000(void);
extern u8 native_data3_0220d108[];
extern void native_fn_021e3f28(void);
extern void native_fn_021e802c(void);
extern void native_fn_021e3cd8(void);


asm u32 native_ov006_021e5cd8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021e65a4
    mvn r2, #0
    cmp r0, r2
    beq ov006_021e5cd8_L2c
    cmp r0, #0
    bne ov006_021e5cd8_L5c
    bl native_fn_021e8000
    ldr r1, =native_data3_0220d108
    str r0, [r1, #0x4]
    b ov006_021e5cd8_L78
ov006_021e5cd8_L2c:
    ldr r0, =0x02218d70
    ldr r1, =native_data3_0220d108
    ldr r0, [r0, #0x8]
    str r2, [r1, #0x8]
    cmp r0, #0
    beq ov006_021e5cd8_L50
    mov r0, #21
    bl native_fn_021e3f28
    b ov006_021e5cd8_L78
ov006_021e5cd8_L50:
    mov r0, #2
    bl native_fn_021e3f28
    b ov006_021e5cd8_L78
ov006_021e5cd8_L5c:
    ldr r1, =native_data3_0220d108
    sub r2, r0, #1
    mov r0, #0
    str r2, [r1, #0x8]
    bl native_fn_021e802c
    mov r0, #91
    bl native_fn_021e3f28
ov006_021e5cd8_L78:
    bl native_fn_021e3cd8
    ldmia sp!, {r3, pc}
}
