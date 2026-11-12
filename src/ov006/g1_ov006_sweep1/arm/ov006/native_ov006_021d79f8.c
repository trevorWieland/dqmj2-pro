/* ov006 row 0x021d79f8: 216 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xcc -> native_data3_0220eb04 (image word 0x0220eb04)
 *   pool +0xd0 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0xd4 -> native_data_0220c8a0 (image word 0x0220c8a0)
 *   back edge +0x44 -> +0x2c
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021d79f8; the literal pool and
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

extern u8 native_data3_0220eb04[];
extern void native_fn_02049ffc(void);
extern void native_fn_02085284(void);
extern void native_fn_02046af4(void);
extern u8 native_data_0220c8a0[];
extern void native_fn_02087a48(void);
extern void native_fn_021d79d4(void);


asm u32 native_ov006_021d79f8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #264
    ldr r4, =native_data3_0220eb04
    mov r8, r0
    ldr r4, [r4, r8, lsl #2]
    mov r7, r1
    add r12, sp, #8
    mov r6, r2
    mov r5, r3
    mov r1, #32
    mov r0, #0
ov006_021d79f8_L2c:
    strh r0, [r12]
    strh r0, [r12, #2]
    strh r0, [r12, #4]
    strh r0, [r12, #6]
    add r12, r12, #8
    subs r1, r1, #1
    bne ov006_021d79f8_L2c
    ldr r0, =native_data3_0220eb04
    ldr r0, [r0, r8, lsl #2]
    bl native_fn_02049ffc
    mov r1, r7
    mov r2, r6
    mov r3, r5
    add r0, r4, #60
    bl native_fn_02085284
    add r1, sp, #8
    mov r0, #255
    str r1, [sp]
    str r0, [sp, #0x4]
    ldr r1, [r4, #0x68]
    ldr r0, =0x021c9698
    mov r2, #2
    mov r3, #0
    bl native_fn_02046af4
    ldr r0, =native_data_0220c8a0
    add r1, sp, #8
    ldr r2, [r0, #0x4]
    ldr r0, =native_data3_0220eb04
    str r2, [sp]
    str r1, [sp, #0x4]
    add r2, sp, #272
    mov r1, #0
    ldrsh r2, [r2, #16]
    ldr r0, [r0, r8, lsl #2]
    mov r3, r1
    bl native_fn_02087a48
    mov r0, #1
    bl native_fn_021d79d4
    add sp, sp, #264
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
