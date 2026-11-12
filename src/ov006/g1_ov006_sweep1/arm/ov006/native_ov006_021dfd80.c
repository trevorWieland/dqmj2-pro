/* ov006 row 0x021dfd80: 200 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xb4 -> native_data_02207940 (image word 0x02207940)
 *   pool +0xb8 -> constant 0x0220f614 (image word 0x0220f614)
 *   pool +0xbc -> native_data_0220d0c0 (image word 0x0220d0c0)
 *   pool +0xc0 -> constant 0x0220f72c (image word 0x0220f72c)
 *   pool +0xc4 -> constant 0x021c9698 (image word 0x021c9698)
 *   2 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dfd80; the literal pool and
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

extern u8 native_data_02207940[];
extern u8 native_data_0220d0c0[];
extern void native_fn_02049794(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_0204a808(void);


asm u32 native_ov006_021dfd80 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #92
    ldr r4, =native_data_02207940
    mov r5, r0
    ldrh r0, [r4, #14]
    ldr r12, =0x0220f614
    ldrh r6, [r4, #12]
    add r4, r12, r5, lsl #4
    strb r1, [r4, #0xc]
    strb r2, [r4, #0xd]
    strh r6, [sp, #24]
    strh r0, [sp, #26]
    strb r3, [r4, #0xe]
    stmia sp, {r1, r2, r3}
    mov r3, #2
    str r3, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldr r6, =native_data_0220d0c0
    str r0, [sp, #0x14]
    ldr r2, =0x0220f72c
    ldrsb r1, [r6, r5]
    ldrsb r2, [r2, #28]
    bl native_fn_02049794
    ldrb r1, [sp, #0x70]
    ldrh r2, [sp, #116]
    mov r0, #15
    bl native_fn_0205dc70
    mov r1, r0
    add r0, sp, #28
    mov r3, #0
    stmia sp, {r0, r3}
    ldr r0, =0x021c9698
    mov r2, #32
    bl native_fn_02046af4
    mov r2, #1
    str r2, [sp]
    mov r3, r0
    ldrsb r0, [r6, r5]
    add r1, sp, #24
    bl native_fn_0204a808
    mov r0, #1
    str r0, [r4, #0x4]
    add sp, sp, #92
    ldmia sp!, {r3, r4, r5, r6, pc}
}
