/* ov001 row 0x0221d510: 148 bytes.
 *
 * What it does: 36 instructions; 5 call(s) to 0x021dbd24, 0x021db8d0, 0x022189cc, +2 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (36 instructions, 5 calls, 2 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x90 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x44 -> +0x78
 *   branch +0x60 -> +0x78
 *   back edge +0x84 -> +0x38
 *   test +0x40 cmp r0, #0
 *   test +0x5c cmp r0, #3
 *   test +0x6c cmp r7, r0
 *   test +0x7c cmp r9, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221d510; the literal pool and
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

extern void native_fn_021dbd24(void);
extern void native_fn_021db8d0(void);
extern void native_fn_022189cc(void);


asm u32 native_ov001_0221d510 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r4, [r0]
    ldr r6, [r0, #0x8]
    ldr r5, [r0, #0xc]
    mov r0, r4
    bl native_fn_021dbd24
    mov r1, #6
    mul r1, r0, r1
    ldr r2, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r7, r2, r1
    add r7, r0, r7, asr #2
    mov r9, #0
    mov r8, #1
ov001_0221d510_L38:
    mov r0, r6
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221d510_L78
    mov r0, r4
    mov r1, r6
    mov r2, r5
    mov r3, r8
    bl native_fn_022189cc
    cmp r0, #3
    bgt ov001_0221d510_L78
    mov r0, r6
    bl native_fn_021dbd24
    cmp r7, r0
    movgt r0, #1
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_0221d510_L78:
    add r9, r9, #1
    cmp r9, #3
    add r6, r6, #1088
    blt ov001_0221d510_L38
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
