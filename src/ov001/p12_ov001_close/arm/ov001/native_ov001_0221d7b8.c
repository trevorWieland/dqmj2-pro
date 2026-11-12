/* ov001 row 0x0221d7b8: 248 bytes.
 *
 * What it does: 61 instructions; 6 call(s) to 0x021db8d0, 0x021db8d0, 0x021f07dc, +3 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (61 instructions, 6 calls, 3 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xf4 -> constant 0x00002710 (image word 0x00002710)
 *   branch +0x40 -> +0x9c
 *   branch +0x50 -> +0x9c
 *   back edge +0xa8 -> +0x34
 *   back edge +0xb8 -> +0x2c
 *   branch +0xc4 -> +0xe8
 *   test +0x3c cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x60 cmp r0, #0
 *   test +0x90 cmp r6, r7
 *   test +0xa0 cmp r5, #3
 *   test +0xb0 cmp r4, #3
 *   test +0xc0 cmp r8, r0
 *   test +0xd8 cmp r6, r0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221d7b8; the literal pool and
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
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221d7b8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r1, [r0, #0x4]
    ldr r0, [r0, #0x8]
    ldr r7, =0x00002710
    str r1, [sp, #0x10]
    str r0, [sp, #0xc]
    mov r9, r1
    mvn r8, #0
    mov r4, #0
    mov r11, #1
ov001_0221d7b8_L2c:
    ldr r10, [sp, #0xc]
    mov r5, #0
ov001_0221d7b8_L34:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221d7b8_L9c
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221d7b8_L9c
    ldrb r0, [r10, #0x356]
    mov r2, #0
    mov r1, r9
    cmp r0, #0
    streqb r11, [r10, #0x356]
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, r10
    str r2, [sp, #0x8]
    mov r3, r2
    bl native_fn_021f07dc
    ldrb r1, [r10, #0x356]
    mul r6, r1, r0
    cmp r6, r7
    movlt r7, r6
    movlt r8, r4
ov001_0221d7b8_L9c:
    add r5, r5, #1
    cmp r5, #3
    add r10, r10, #1088
    blt ov001_0221d7b8_L34
    add r4, r4, #1
    cmp r4, #3
    add r9, r9, #1088
    blt ov001_0221d7b8_L2c
    mvn r0, #0
    cmp r8, r0
    beq ov001_0221d7b8_Le8
    ldr r0, [sp, #0x10]
    add r1, r8, r8, lsl #4
    add r0, r0, r1, lsl #6
    bl native_fn_021dbd24
    cmp r6, r0
    addge sp, sp, #20
    movge r0, #1
    ldmgeia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0221d7b8_Le8:
    mov r0, #0
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
