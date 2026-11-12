/* ov001 row 0x022204d8: 164 bytes.
 *
 * What it does: 40 instructions; 7 call(s) to 0x0207afec, 0x0207afec, 0x021db8d0, +4 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (40 instructions, 7 calls, 2 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0xa0 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x38 -> +0x88
 *   branch +0x54 -> +0x88
 *   back edge +0x94 -> +0x2c
 *   test +0x34 cmp r0, #0
 *   test +0x50 cmp r0, #1
 *   test +0x7c cmp r5, r2
 *   test +0x8c cmp r8, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022204d8; the literal pool and
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

extern void native_fn_0207afec(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_022189cc(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_022204d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r9, [r0, #0xc]
    ldr r7, [r0]
    ldr r10, [r0, #0x8]
    mov r0, r9
    bl native_fn_0207afec
    mov r0, r9
    bl native_fn_0207afec
    ldr r4, =0x66666667
    mov r8, #0
    mov r6, #1
ov001_022204d8_L2c:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022204d8_L88
    mov r0, r7
    mov r1, r10
    mov r2, r9
    mov r3, r6
    bl native_fn_022189cc
    cmp r0, #1
    bgt ov001_022204d8_L88
    mov r0, r10
    bl native_fn_021dbd24
    mov r5, r0
    mov r0, r10
    bl native_fn_021dbcbc
    mov r1, r0, lsl #2
    smull r0, r2, r4, r1
    mov r0, r1, lsr #31
    add r2, r0, r2, asr #1
    cmp r5, r2
    movge r0, #1
    ldmgeia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_022204d8_L88:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_022204d8_L2c
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
