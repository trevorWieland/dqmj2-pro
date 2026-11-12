/* ov001 row 0x0221967c: 148 bytes.
 *
 * What it does: 36 instructions; 4 call(s) to 0x021db8d0, 0x021f07dc, 0x021dbcbc, +1 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (36 instructions, 4 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0x90 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x2c -> +0x74
 *   back edge +0x80 -> +0x20
 *   test +0x28 cmp r0, #0
 *   test +0x64 cmp r5, r2
 *   test +0x78 cmp r9, #3
 *   1 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221967c; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021f07dc(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0221967c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r9, #0
    ldr r8, [r0]
    ldr r10, [r0, #0x8]
    ldr r4, =0x66666667
    mov r7, r9
    mov r6, #1
ov001_0221967c_L20:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221967c_L74
    str r7, [sp]
    mov r0, r8
    mov r1, r10
    mov r2, r7
    mov r3, r7
    stmib sp, {r6, r7}
    bl native_fn_021f07dc
    mov r5, r0
    mov r0, r10
    bl native_fn_021dbcbc
    smull r1, r2, r4, r0
    mov r0, r0, lsr #31
    add r2, r0, r2, asr #2
    cmp r5, r2
    addge sp, sp, #12
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
ov001_0221967c_L74:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #1088
    blt ov001_0221967c_L20
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
