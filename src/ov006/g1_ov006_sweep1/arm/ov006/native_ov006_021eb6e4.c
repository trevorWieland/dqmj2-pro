/* ov006 row 0x021eb6e4: 428 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x194 -> native_data5_02219290 (image word 0x02219290)
 *   pool +0x198 -> native_data4_0220d3b8 (image word 0x0220d3b8)
 *   pool +0x19c -> native_fn_021eb6c4 (image word 0x021eb6c4)
 *   pool +0x1a0 -> native_data_022086bc (image word 0x022086bc)
 *   pool +0x1a4 -> native_fn_021eb628 (image word 0x021eb628)
 *   pool +0x1a8 -> native_data_02208550 (image word 0x02208550)
 *   branch +0x14 -> +0x2c
 *   branch +0x1c -> +0x118
 *   branch +0x24 -> +0x16c
 *   branch +0x28 -> +0x188
 *   branch +0x40 -> +0x68
 *   branch +0x48 -> +0x68
 *   branch +0x64 -> +0x80
 *   branch +0xa8 -> +0x100
 *   back edge +0xfc -> +0xbc
 *   branch +0x124 -> +0x154
 *   branch +0x134 -> +0x154
 *   back edge +0x150 -> +0x138
 *   test +0x10 cmp r0, #1
 *   test +0x18 cmp r0, #2
 *   test +0x20 cmp r0, #3
 *   test +0x3c cmp r2, #0
 *   test +0x44 cmp r2, #64
 *   test +0xa4 cmp r1, #0
 *   test +0xf4 cmp r5, r1
 *   test +0x120 cmp r0, #0
 *   test +0x130 cmp r0, #0
 *   test +0x14c cmp r6, r0
 *   1 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eb6e4; the literal pool and
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
extern u8 native_data4_0220d3b8[];
extern void native_fn_021eb6c4(void);
extern u8 native_data_022086bc[];
extern void native_fn_021eb628(void);
extern u8 native_data_02208550[];
extern void native_fn_021e6bdc(void);
extern void native_fn_02048f6c(void);
extern void native_fn_021e7ec4(void);
extern void native_fn_021e73ac(void);
extern void native_fn_021e7608(void);
extern void native_fn_021eb240(void);


asm u32 native_ov006_021eb6e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #16
    ldr r5, =native_data5_02219290
    ldr r0, [r5, #0x2c]
    cmp r0, #1
    beq ov006_021eb6e4_L2c
    cmp r0, #2
    beq ov006_021eb6e4_L118
    cmp r0, #3
    beq ov006_021eb6e4_L16c
    b ov006_021eb6e4_L188
ov006_021eb6e4_L2c:
    ldr r1, =native_data4_0220d3b8
    mvn r0, #0
    ldr r2, [r1, #0x8]
    ldr r4, =native_fn_021eb6c4
    cmp r2, #0
    blt ov006_021eb6e4_L68
    cmp r2, #64
    bge ov006_021eb6e4_L68
    ldr r2, =native_data_022086bc
    mov r0, #11
    str r2, [r1, #0x4]
    str r0, [r5, #0xc]
    mov r0, #6
    ldr r4, =native_fn_021eb628
    b ov006_021eb6e4_L80
ov006_021eb6e4_L68:
    ldr r5, =native_data_02208550
    ldr r2, =native_data4_0220d3b8
    ldr r1, =native_data5_02219290
    mov r3, #1
    str r5, [r2, #0x4]
    str r3, [r1, #0xc]
ov006_021eb6e4_L80:
    bl native_fn_021e6bdc
    mov r0, #0
    bl native_fn_02048f6c
    mov r1, r0
    mov r0, #0
    bl native_fn_021e7ec4
    ldr r8, =native_data5_02219290
    mov r5, #0
    ldr r1, [r8, #0xc]
    cmp r1, #0
    ble ov006_021eb6e4_L100
    ldr r7, =native_data4_0220d3b8
    mov r6, r5
    mov r10, #1
    mov r9, #16
ov006_021eb6e4_Lbc:
    ldr r12, [r7, #0x4]
    mov r1, r9
    add r3, r12, r6
    ldrsb r2, [r3, #6]
    str r2, [sp]
    ldrsb r2, [r3, #7]
    stmib sp, {r2, r10}
    str r0, [sp, #0xc]
    ldrsb r2, [r3, #4]
    ldrsb r3, [r3, #5]
    ldr r0, [r12, r6]
    bl native_fn_021e73ac
    ldr r1, [r8, #0xc]
    add r5, r5, #1
    cmp r5, r1
    add r6, r6, #8
    blt ov006_021eb6e4_Lbc
ov006_021eb6e4_L100:
    blx r4
    ldr r1, =native_data5_02219290
    mov r0, #0
    str r0, [r1, #0x2c]
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov006_021eb6e4_L118:
    ldr r4, =native_data4_0220d3b8
    ldr r0, [r4, #0x4]
    cmp r0, #0
    beq ov006_021eb6e4_L154
    ldr r0, [r5, #0xc]
    mov r6, #0
    cmp r0, #0
    ble ov006_021eb6e4_L154
ov006_021eb6e4_L138:
    ldr r0, [r4, #0x4]
    ldr r0, [r0, r6, lsl #3]
    bl native_fn_021e7608
    ldr r0, [r5, #0xc]
    add r6, r6, #1
    cmp r6, r0
    blt ov006_021eb6e4_L138
ov006_021eb6e4_L154:
    ldr r0, =native_data5_02219290
    mov r1, #1
    str r1, [r0, #0x2c]
    add sp, sp, #16
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov006_021eb6e4_L16c:
    mov r0, #1
    bl native_fn_021eb240
    mov r1, r5
    mov r0, #0
    str r0, [r1, #0x2c]
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov006_021eb6e4_L188:
    mov r0, #1
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
