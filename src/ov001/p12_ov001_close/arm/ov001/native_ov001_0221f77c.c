/* ov001 row 0x0221f77c: 264 bytes.
 *
 * What it does: 64 instructions; 8 call(s) to 0x021db8d0, 0x021dbd8c, 0x0221f794, +5 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block load (64 instructions, 8 calls, 4 branches, 8 back edges, 2 literal slots).
 *
 *   pool +0x100 -> constant 0x0000270f (image word 0x0000270f)
 *   pool +0x104 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x24 -> +0x3c
 *   back edge +0x48 -> +0x18
 *   branch +0x6c -> +0xe8
 *   branch +0x8c -> +0xe8
 *   branch +0xac -> +0xe8
 *   back edge +0xf4 -> +0x60
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r0, r6
 *   test +0x40 cmp r4, #3
 *   test +0x68 cmp r0, #0
 *   test +0x78 cmp r1, #0
 *   test +0x80 cmpeq r1, #0
 *   test +0x88 cmpeq r0, #0
 *   test +0xa8 cmp r0, #1
 *   test +0xdc cmp r5, r2
 *   test +0xec cmp r10, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221f77c; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_0207afec(void);
extern void native_fn_02218c34(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0221f77c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldmib r0, {r5, r8}
    ldr r7, [r0, #0xc]
    ldr r6, =0x0000270f
    mov r10, r5
    mov r4, #0
ov001_0221f77c_L18:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221f77c_L3c
    mov r0, r10
    bl native_fn_021dbd8c
    cmp r0, r6
    movle r9, r4
    movle r6, r0
ov001_0221f77c_L3c:
    add r4, r4, #1
    cmp r4, #3
    add r10, r10, #1088
    blt ov001_0221f77c_L18
    add r0, r9, r9, lsl #4
    mov r10, #0
    ldr r4, =0x66666667
    add r9, r5, r0, lsl #6
    mov r6, r10
ov001_0221f77c_L60:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221f77c_Le8
    add r0, r8, #512
    ldrsb r1, [r0, #63]
    cmp r1, #0
    ldreqsb r1, [r0, #64]
    cmpeq r1, #0
    ldreqsb r0, [r0, #65]
    cmpeq r0, #0
    bne ov001_0221f77c_Le8
    mov r0, r7
    bl native_fn_0207afec
    ldrb r0, [r0, #0x1f]
    ldr r1, [r8, #0x1e8]
    add r0, r1, r0
    ldrb r0, [r0, #0x86]
    cmp r0, #1
    bhi ov001_0221f77c_Le8
    mov r0, r8
    mov r1, r9
    mov r2, r6
    bl native_fn_02218c34
    mov r5, r0
    mov r0, r9
    bl native_fn_021dbcbc
    add r1, r0, r0, lsl #1
    smull r0, r2, r4, r1
    mov r0, r1, lsr #31
    add r2, r0, r2, asr #2
    cmp r5, r2
    movge r0, #1
    ldmgeia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_0221f77c_Le8:
    add r10, r10, #1
    cmp r10, #3
    add r8, r8, #1088
    blt ov001_0221f77c_L60
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
