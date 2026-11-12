/* ov006 row 0x021eb9a4: 176 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa8 -> native_data5_02219290 (image word 0x02219290)
 *   pool +0xac -> native_data_022087e4 (image word 0x022087e4)
 *   branch +0x14 -> +0xa0
 *   branch +0x24 -> +0x48
 *   branch +0x44 -> +0x98
 *   branch +0x60 -> +0x84
 *   branch +0x80 -> +0x98
 *   test +0x0c cmp r3, r0
 *   test +0x10 cmpeq r2, #0
 *   test +0x1c cmp r1, #0
 *   test +0x5c cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eb9a4; the literal pool and
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

extern u8 native_data5_02219290[];
extern void native_fn_021ebaf4(void);
extern u8 native_data_022087e4[];


asm u32 native_ov006_021eb9a4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r3, =native_data5_02219290
    ldr r3, [r3, #0x1c]
    cmp r3, r0
    cmpeq r2, #0
    beq ov006_021eb9a4_La0
    ldr r2, =native_data5_02219290
    cmp r1, #0
    str r0, [r2, #0x10]
    beq ov006_021eb9a4_L48
    mov r0, #0
    bl native_fn_021ebaf4
    ldr r0, =native_data5_02219290
    mov r1, #3
    str r1, [r0, #0x14]
    mov r1, #2
    str r1, [r0, #0x20]
    b ov006_021eb9a4_L98
ov006_021eb9a4_L48:
    mov r0, #12
    mul r1, r3, r0
    ldr r0, =native_data_022087e4
    ldr r0, [r0, r1]
    blx r0
    cmp r0, #0
    beq ov006_021eb9a4_L84
    ldr r0, =native_data5_02219290
    mov r2, #0
    ldr r3, [r0, #0x10]
    mov r1, #3
    str r3, [r0, #0x1c]
    str r2, [r0, #0x14]
    str r1, [r0, #0x20]
    b ov006_021eb9a4_L98
ov006_021eb9a4_L84:
    ldr r0, =native_data5_02219290
    mov r1, #2
    str r1, [r0, #0x14]
    mov r1, #3
    str r1, [r0, #0x20]
ov006_021eb9a4_L98:
    mov r0, #1
    ldmia sp!, {r3, pc}
ov006_021eb9a4_La0:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
