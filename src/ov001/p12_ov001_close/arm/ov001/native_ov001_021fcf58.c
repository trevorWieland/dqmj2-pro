/* ov001 row 0x021fcf58: 284 bytes.
 *
 * What it does: 67 instructions; 9 call(s) to 0x02204af8, 0x021fcf88, 0x021fcf70, +6 more; loops (back edge at +0x60); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (67 instructions, 9 calls, 4 branches, 6 back edges, 4 literal slots).
 *
 *   pool +0x10c -> constant 0x02239c9c (image word 0x02239c9c)
 *   pool +0x110 -> native_data_0222ed34 (image word 0x0222ed34)
 *   pool +0x114 -> constant 0x02239d6c (image word 0x02239d6c)
 *   pool +0x118 -> constant 0x02239ca4 (image word 0x02239ca4)
 *   branch +0x40 -> +0x4c
 *   back edge +0x60 -> +0x30
 *   back edge +0x74 -> +0x18
 *   branch +0x84 -> +0x9c
 *   branch +0xb0 -> +0xd4
 *   back edge +0xd0 -> +0xbc
 *   back edge +0x104 -> +0xec
 *   test +0x18 cmp r8, #0
 *   test +0x3c cmp r0, #127
 *   test +0x58 cmp r9, #3
 *   test +0x70 cmp r8, #2
 *   test +0x80 cmp r0, #127
 *   test +0x100 cmp r4, #10
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fcf58; the literal pool and
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

extern void native_fn_02204af8(void);
extern u8 native_data_0222ed34[];
extern void native_fn_02204250(void);
extern void native_fn_022042c4(void);
extern void native_fn_0206d7f8(void);
extern void native_fn_0206cc3c(void);
extern void native_fn_02204d24(void);


asm u32 native_ov001_021fcf58 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r8, #0
    ldr r5, =0x02239c9c
    mov r4, #127
    mov r11, #3
    mov r7, r8
ov001_021fcf58_L18:
    cmp r8, #0
    moveq r0, r7
    movne r0, r11
    mov r0, r0, lsl #24
    mov r9, #0
    mov r10, r0, asr #24
ov001_021fcf58_L30:
    mov r0, r10, lsl #24
    mov r6, r0, asr #24
    ldrsb r0, [r5, r6]
    cmp r0, #127
    beq ov001_021fcf58_L4c
    bl native_fn_02204af8
    strb r4, [r5, r6]
ov001_021fcf58_L4c:
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    cmp r9, #3
    add r10, r10, #1
    blt ov001_021fcf58_L30
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #2
    blt ov001_021fcf58_L18
    ldr r0, =native_data_0222ed34
    ldrsb r0, [r0, #3]
    cmp r0, #127
    beq ov001_021fcf58_L9c
    bl native_fn_02204250
    bl native_fn_022042c4
    ldr r0, =native_data_0222ed34
    mov r1, #127
    strb r1, [r0, #0x3]
ov001_021fcf58_L9c:
    ldr r0, =0x02239d6c
    ldrsb r0, [r0, #112]
    sub r0, r0, #1
    mov r0, r0, lsl #24
    movs r1, r0, asr #24
    bmi ov001_021fcf58_Ld4
    ldr r2, =0x02239ca4
    mov r3, #0
ov001_021fcf58_Lbc:
    sub r0, r1, #1
    add r1, r2, r1, lsl #4
    mov r0, r0, lsl #24
    strb r3, [r1, #0x9]
    movs r1, r0, asr #24
    bpl ov001_021fcf58_Lbc
ov001_021fcf58_Ld4:
    bl native_fn_0206d7f8
    mov r0, #2
    bl native_fn_0206cc3c
    ldr r0, =0x02239d6c
    mov r4, #0
    strb r4, [r0, #0x70]
ov001_021fcf58_Lec:
    mov r0, r4
    bl native_fn_02204d24
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #10
    blt ov001_021fcf58_Lec
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
