/* ov000 row 0x021f5908: 812 bytes.
 *
 * What it does: 202 instructions; 31 call(s) to 0x02061c1c, 0x02223f24, 0x01ffb734, +28 more; loops (back edge at +0x2c); 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x328 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   branch +0x38 -> +0x90
 *   branch +0x44 -> +0x54
 *   branch +0x4c -> +0x74
 *   branch +0x50 -> +0x90
 *   branch +0x70 -> +0x90
 *   branch +0x98 -> +0xb4
 *   branch +0xbc -> +0xcc
 *   branch +0xc8 -> +0x118
 *   test +0x34 cmp r0, #3
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmp r0, #1
 *   test +0x94 cmp r0, #1
 *   test +0xb8 cmp r0, #1
 *   test +0xc4 cmp r0, #3
 *   2 block transfer(s), 38 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f5908; the literal pool and
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

extern void native_fn_02061c1c(void);
extern void native_fn_02223f24(void);
extern void native_fn_01ffb734(void);
extern void native_fn_01ffb50c(void);
extern void native_fn_01ffa84c(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_02048034(void);
extern void native_fn_021f65e4(void);
extern void native_fn_02045ed0(void);


asm u32 native_ov000_021f5908 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #6
    mov r1, #9
    mov r2, #4
    mov r3, #14
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    bl native_fn_02223f24
    cmp r0, #3
    bne ov000_021f5908_L90
    bl native_fn_01ffb734
    cmp r0, #0
    beq ov000_021f5908_L54
    cmp r0, #1
    beq ov000_021f5908_L74
    b ov000_021f5908_L90
ov000_021f5908_L54:
    mov r12, #1
    mov r0, #6
    mov r1, #15
    mov r2, #0
    mov r3, #11
    str r12, [sp]
    bl native_fn_01ffb50c
    b ov000_021f5908_L90
ov000_021f5908_L74:
    mov r12, #1
    mov r0, #6
    mov r1, #15
    mov r2, #0
    mov r3, #12
    str r12, [sp]
    bl native_fn_01ffb50c
ov000_021f5908_L90:
    bl native_fn_02223f24
    cmp r0, #1
    bne ov000_021f5908_Lb4
    mov r3, #1
    mov r0, #6
    mov r1, #16
    mov r2, #2
    str r3, [sp]
    bl native_fn_01ffb50c
ov000_021f5908_Lb4:
    bl native_fn_01ffb734
    cmp r0, #1
    bne ov000_021f5908_Lcc
    bl native_fn_02223f24
    cmp r0, #3
    beq ov000_021f5908_L118
ov000_021f5908_Lcc:
    bl native_fn_01ffa84c
    bl native_fn_01ffb4ec
    mov r1, #0
    bl native_fn_02048034
    mov r1, #2
    str r1, [sp]
    mov r3, #0
    str r3, [sp, #0x4]
    mov r0, #7
    mov r2, #8
    str r3, [sp, #0x8]
    mov r3, #24
    bl native_fn_02061c1c
    mov r3, #0
    str r3, [sp]
    mov r0, #7
    mov r1, #16
    mov r2, r1
    bl native_fn_01ffb50c
ov000_021f5908_L118:
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #8
    mov r1, #3
    mov r2, #11
    mov r3, #16
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    mov r1, #16
    mov r12, #0
    mov r2, r1
    mov r0, #8
    mov r3, #1
    str r12, [sp]
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #9
    mov r1, #24
    mov r2, #11
    mov r3, #3
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    ldr r1, =0x02236ee4
    mov r0, #9
    ldr r1, [r1, #0x14]
    mov r2, #3
    bl native_fn_021f65e4
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #10
    mov r1, #3
    mov r2, #14
    mov r3, #16
    bl native_fn_02061c1c
    mov r0, #0
    str r0, [sp]
    mov r0, #10
    mov r1, #16
    mov r2, r1
    mov r3, #2
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #11
    mov r1, #24
    mov r2, #14
    mov r3, #3
    bl native_fn_02061c1c
    mov r0, #11
    ldr r1, =0x02236ee4
    mov r2, #3
    ldr r1, [r1, #0x24]
    bl native_fn_021f65e4
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #12
    mov r1, #3
    mov r2, #17
    mov r3, #16
    bl native_fn_02061c1c
    mov r1, #16
    mov r12, #0
    mov r2, r1
    mov r0, #12
    mov r3, #3
    str r12, [sp]
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #13
    mov r1, #24
    mov r2, #17
    mov r3, #3
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    ldr r1, =0x02236ee4
    mov r0, #13
    ldr r1, [r1, #0x18]
    mov r2, #3
    bl native_fn_021f65e4
    mov r0, #2
    str r0, [sp]
    mov r1, #0
    str r1, [sp, #0x4]
    mov r0, #14
    str r1, [sp, #0x8]
    mov r1, #3
    mov r2, #20
    mov r3, #16
    bl native_fn_02061c1c
    mov r0, #0
    str r0, [sp]
    mov r0, #14
    mov r1, #16
    mov r2, r1
    mov r3, #4
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #15
    mov r1, #24
    mov r2, #20
    mov r3, #3
    bl native_fn_02061c1c
    mov r0, #15
    ldr r1, =0x02236ee4
    mov r2, #3
    ldr r1, [r1, #0x4]
    bl native_fn_021f65e4
    mov r0, #1
    bl native_fn_02045ed0
    add sp, sp, #12
    ldmia sp!, {pc}
}
