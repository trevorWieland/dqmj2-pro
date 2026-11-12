/* ov001 row 0x021f2120: 272 bytes.
 *
 * What it does: 66 instructions; 8 call(s) to 0x0205d790, 0x021db438, 0x021db8d0, +5 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (66 instructions, 8 calls, 4 branches, 7 back edges, 2 literal slots).
 *
 *   pool +0x108 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x10c -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x24 -> +0x40
 *   branch +0x60 -> +0xf0
 *   branch +0x70 -> +0xf0
 *   branch +0x78 -> +0x90
 *   branch +0x8c -> +0xf0
 *   back edge +0xfc -> +0x54
 *   test +0x18 cmp r9, #0
 *   test +0x40 cmp r5, #0
 *   test +0x5c cmp r0, #0
 *   test +0x6c cmp r8, r0
 *   test +0x74 cmp r4, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xf4 cmp r6, r5
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f2120; the literal pool and
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

extern void native_fn_0205d790(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021d8b4c(void);
extern void native_fn_021eedbc(void);


asm u32 native_ov001_021f2120 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #16
    mov r8, r1
    mov r9, r0
    mov r0, r8
    bl native_fn_0205d790
    cmp r9, #0
    mov r4, r0
    movne r5, #1
    bne ov001_021f2120_L40
    ldr r0, =0x0223989c
    mov r1, #0
    ldrb r0, [r0, #0x11]
    bl native_fn_021db438
    mov r9, r0
    mov r5, #3
ov001_021f2120_L40:
    cmp r5, #0
    mov r6, #0
    addle sp, sp, #16
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    mov r7, r9
ov001_021f2120_L54:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f2120_Lf0
    add r0, r7, #768
    ldrh r0, [r0, #74]
    cmp r8, r0
    bne ov001_021f2120_Lf0
    cmp r4, #0
    blt ov001_021f2120_L90
    mov r0, r8
    mov r1, r7
    mov r2, r4
    bl native_fn_021eec7c
    b ov001_021f2120_Lf0
ov001_021f2120_L90:
    add r0, r9, #30
    add r1, r6, r6, lsl #4
    add r5, r0, #768
    ldrb r0, [r5, r1, lsl #6]
    mov r4, r1, lsl #6
    add r1, sp, #4
    cmp r0, #0
    moveq r0, #3
    movne r0, #11
    bl native_fn_021d8b4c
    ldrb r1, [r5, r4]
    ldr r4, =0x66666667
    mov r0, r8
    str r1, [sp]
    ldr r2, [sp, #0xc]
    ldr r1, [sp, #0x4]
    mov r5, r2, lsl #3
    smull r2, r3, r4, r5
    mov r4, r5, lsr #31
    ldr r2, [sp, #0x8]
    add r3, r4, r3, asr #2
    bl native_fn_021eedbc
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_021f2120_Lf0:
    add r6, r6, #1
    cmp r6, r5
    add r7, r7, #1088
    blt ov001_021f2120_L54
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
