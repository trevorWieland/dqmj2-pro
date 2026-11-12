/* ov006 row 0x021d7c1c: 268 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x100 -> native_data2_0220eb04 (image word 0x0220eb04)
 *   pool +0x104 -> constant 0x020dbc18 (image word 0x020dbc18)
 *   pool +0x108 -> constant 0x021c9698 (image word 0x021c9698)
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021d7c1c; the literal pool and
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

extern void native_fn_020449d4(void);
extern u8 native_data2_0220eb04[];
extern void native_fn_02049ffc(void);
extern void native_fn_02008be0(void);
extern void native_fn_02008d78(void);
extern void native_fn_020470fc(void);
extern void native_fn_02044ff4(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087a48(void);


asm u32 native_ov006_021d7c1c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #108
    mov r5, r1
    mov r6, r0
    mov r0, r5
    mov r4, r2
    bl native_fn_020449d4
    ldr r1, =native_data2_0220eb04
    mov r7, r0
    ldr r0, [r1, r6, lsl #2]
    add r2, sp, #8
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    bl native_fn_02049ffc
    mov r0, #0
    add r1, sp, #12
    mov r2, #64
    bl native_fn_02008be0
    add r0, sp, #76
    mov r1, #0
    mov r2, #32
    bl native_fn_02008d78
    ldrh r1, [r7, #4]
    ldr r2, =0x020dbc18
    add r0, sp, #12
    mov r1, r1, lsl #24
    mov r1, r1, lsr #28
    add r1, r1, #13
    mov r1, r1, lsl #16
    mov r1, r1, lsr #16
    add r1, r1, #123
    add r1, r1, #256
    mov r1, r1, lsl #1
    ldrh r1, [r2, r1]
    strh r1, [sp, #12]
    bl native_fn_020470fc
    mov r2, r4
    mov r4, r0
    mov r1, r5
    add r0, sp, #76
    bl native_fn_02044ff4
    add r1, sp, #12
    add r1, r1, r4, lsl #1
    str r1, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    add r1, sp, #76
    mov r2, #28
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    str r0, [sp]
    add r1, sp, #12
    str r1, [sp, #0x4]
    mov r1, #0
    ldr r0, =native_data2_0220eb04
    mov r2, r1
    ldr r0, [r0, r6, lsl #2]
    mov r3, r1
    bl native_fn_02087a48
    add sp, sp, #108
    ldmia sp!, {r4, r5, r6, r7, pc}
}
