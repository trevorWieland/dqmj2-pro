/* ov000 row 0x021eb52c: 296 bytes.
 *
 * What it does: 70 instructions; 8 call(s) to 0x021ec290, 0x020c49e8, 0x021ebf34, +5 more; loops (back edge at +0x0c); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x118 -> constant 0x02236980 (image word 0x02236980)
 *   pool +0x11c -> native_data_0222b8ac (image word 0x0222b8ac)
 *   pool +0x120 -> constant 0x02236990 (image word 0x02236990)
 *   pool +0x124 -> native_data_0222b8b2 (image word 0x0222b8b2)
 *   branch +0x1c -> +0x38
 *   branch +0x24 -> +0x90
 *   branch +0x2c -> +0xd4
 *   test +0x18 cmp r0, #0
 *   test +0x20 cmp r0, #1
 *   test +0x28 cmp r0, #2
 *   test +0x60 cmp r0, #2
 *   5 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021eb52c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021ec290(void);
extern void native_fn_020c49e8(void);
extern void native_fn_021ebf34(void);
extern u8 native_data_0222b8ac[];
extern void native_fn_021ec154(void);
extern u8 native_data_0222b8b2[];


asm u32 native_ov000_021eb52c (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    bl native_fn_021ec290
    bl native_fn_020c49e8
    ldr r0, =0x02236980
    ldrsb r0, [r0, #32]
    cmp r0, #0
    beq ov000_021eb52c_L38
    cmp r0, #1
    beq ov000_021eb52c_L90
    cmp r0, #2
    beq ov000_021eb52c_Ld4
    add sp, sp, #12
    ldmia sp!, {pc}
ov000_021eb52c_L38:
    mov r0, #9
    mov r1, #4
    mov r2, #10
    bl native_fn_021ebf34
    ldr r0, =0x02236980
    ldr r2, =native_data_0222b8ac
    add r0, r0, #256
    ldrsb r0, [r0, #2]
    mov r1, #3
    mov r3, #1
    cmp r0, #2
    mov r0, #4
    str r0, [sp]
    mov r0, #12
    moveq r12, #1
    str r0, [sp, #0x4]
    movne r12, #0
    ldr r0, =0x02236990
    str r12, [sp, #0x8]
    bl native_fn_021ec154
    add sp, sp, #12
    ldmia sp!, {pc}
ov000_021eb52c_L90:
    mov r0, #9
    mov r1, #4
    mov r2, #0
    bl native_fn_021ebf34
    mov r0, #4
    str r0, [sp]
    mov r1, #12
    str r1, [sp, #0x4]
    mov r12, #0
    ldr r0, =0x02236990
    ldr r2, =native_data_0222b8b2
    mov r1, #3
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_021ec154
    add sp, sp, #12
    ldmia sp!, {pc}
ov000_021eb52c_Ld4:
    mov r0, #9
    mov r1, #4
    mov r2, #1
    bl native_fn_021ebf34
    mov r0, #4
    str r0, [sp]
    mov r1, #12
    ldr r0, =0x02236990
    ldr r2, =native_data_0222b8b2
    str r1, [sp, #0x4]
    mov r12, #0
    mov r1, #3
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_021ec154
    add sp, sp, #12
    ldmia sp!, {pc}
}
