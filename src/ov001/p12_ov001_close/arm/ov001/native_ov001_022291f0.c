/* ov001 row 0x022291f0: 260 bytes.
 *
 * What it does: 64 instructions; 13 call(s) to 0x02223fe8, 0x02226bdc, 0x02008e0c, +10 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (64 instructions, 13 calls, 2 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0x100 -> native_data_0222e5e4 (image word 0x0222e5e4)
 *   branch +0x80 -> +0xa4
 *   branch +0xa0 -> +0xe8
 *   test +0x7c cmp r0, #0
 *   2 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022291f0; the literal pool and
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

extern u8 native_data_0222e5e4[];
extern void native_fn_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02008e0c(void);
extern void native_fn_022240a4(void);
extern void native_fn_02225354(void);
extern void native_fn_02224570(void);
extern void native_fn_0207afec(void);
extern void native_fn_02225534(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_022291f0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #36
    ldr r1, =native_data_0222e5e4
    add r3, sp, #24
    mov r7, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r5, [r7, #0x4]
    mov r0, r3
    mov r1, r5
    ldr r4, [r7]
    ldr r6, [r7, #0x8]
    bl native_fn_02223fe8
    add r0, sp, #24
    mov r1, r7
    mov r2, #78
    bl native_fn_02226bdc
    add r0, sp, #24
    add r1, sp, #12
    mov r2, #12
    bl native_fn_02008e0c
    mov r0, #1
    str r0, [sp]
    add r2, sp, #8
    str r2, [sp, #0x4]
    mov r1, r4
    add r0, sp, #24
    mov r2, r5
    mov r3, r6
    bl native_fn_022240a4
    ldr r0, [sp, #0x8]
    cmp r0, #0
    beq ov001_022291f0_La4
    add r0, sp, #24
    mov r1, r5
    bl native_fn_02225354
    add r0, sp, #24
    mov r1, r5
    mov r2, #0
    bl native_fn_02224570
    b ov001_022291f0_Le8
ov001_022291f0_La4:
    add r0, sp, #12
    add r1, sp, #24
    mov r2, #12
    bl native_fn_02008e0c
    mov r0, r6
    bl native_fn_0207afec
    ldrb r2, [r0, #0x1f]
    add r0, sp, #24
    mov r1, r5
    bl native_fn_02225534
    add r0, sp, #24
    mov r1, r5
    bl native_fn_02225354
    add r0, sp, #24
    mov r1, r5
    mov r2, #0
    bl native_fn_02224570
ov001_022291f0_Le8:
    add r0, sp, #24
    bl native_fn_02224050
    add r0, sp, #24
    bl native_fn_02226cb0
    add sp, sp, #36
    ldmia sp!, {r4, r5, r6, r7, pc}
}
