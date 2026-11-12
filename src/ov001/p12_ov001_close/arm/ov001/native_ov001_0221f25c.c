/* ov001 row 0x0221f25c: 316 bytes.
 *
 * What it does: 77 instructions; 10 call(s) to 0x021db8d0, 0x021dbd3c, 0x0221f284, +7 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (77 instructions, 10 calls, 4 branches, 9 back edges, 2 literal slots).
 *
 *   pool +0x134 -> constant 0x0000270f (image word 0x0000270f)
 *   pool +0x138 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x34 -> +0x4c
 *   back edge +0x58 -> +0x28
 *   branch +0x78 -> +0xa4
 *   branch +0x88 -> +0x9c
 *   branch +0x98 -> +0xa4
 *   back edge +0xb0 -> +0x6c
 *   branch +0xbc -> +0x128
 *   back edge +0x124 -> +0xd4
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r0, r4
 *   test +0x50 cmp r9, #3
 *   test +0x74 cmp r0, #0
 *   test +0x84 cmp r0, r8
 *   test +0xa8 cmp r10, #3
 *   test +0xb4 cmp r7, #0
 *   test +0x10c cmp r4, r2
 *   test +0x120 cmp r10, r7
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221f25c; the literal pool and
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
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_02218c34(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0221f25c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r1, [r0, #0x8]
    mov r4, #0
    ldr r6, [r0, #0x4]
    ldr r8, =0x0000270f
    str r1, [sp]
    mov r7, r4
    mov r9, r4
    mov r10, r1
ov001_0221f25c_L28:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221f25c_L4c
    mov r0, r10
    bl native_fn_021dbd3c
    cmp r0, r4
    movge r5, r9
    movge r4, r0
ov001_0221f25c_L4c:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #1088
    blt ov001_0221f25c_L28
    mov r9, r6
    mov r10, #0
    add r4, sp, #4
    mov r11, #1
ov001_0221f25c_L6c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221f25c_La4
    mov r0, r9
    bl native_fn_021dbd8c
    cmp r0, r8
    bge ov001_0221f25c_L9c
    mov r7, r11
    mov r8, r0
    str r10, [sp, #0x4]
    b ov001_0221f25c_La4
ov001_0221f25c_L9c:
    streq r10, [r4, r7, lsl #2]
    addeq r7, r7, #1
ov001_0221f25c_La4:
    add r10, r10, #1
    cmp r10, #3
    add r9, r9, #1088
    blt ov001_0221f25c_L6c
    cmp r7, #0
    mov r10, #0
    ble ov001_0221f25c_L128
    ldr r0, [sp]
    add r1, r5, r5, lsl #4
    ldr r11, =0x66666667
    add r8, r0, r1, lsl #6
    add r5, sp, #4
ov001_0221f25c_Ld4:
    ldr r1, [r5, r10, lsl #2]
    mov r0, r8
    add r1, r1, r1, lsl #4
    add r9, r6, r1, lsl #6
    mov r1, r9
    mov r2, #0
    bl native_fn_02218c34
    mov r4, r0
    mov r0, r9
    bl native_fn_021dbcbc
    add r1, r0, r0, lsl #1
    smull r0, r2, r11, r1
    mov r0, r1, lsr #31
    add r2, r0, r2, asr #2
    cmp r4, r2
    addge sp, sp, #16
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r10, r10, #1
    cmp r10, r7
    blt ov001_0221f25c_Ld4
ov001_0221f25c_L128:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
