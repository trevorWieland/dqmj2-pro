/* ov001 row 0x021ff094: 356 bytes.
 *
 * What it does: 82 instructions; 12 call(s) to 0x021fc5c4, 0x0202a37c, 0x021fd354, +9 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (82 instructions, 12 calls, 1 branch, 13 back edges, 7 literal slots).
 *
 *   pool +0x148 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x14c -> native_data_0222efd8 (image word 0x0222efd8)
 *   pool +0x150 -> native_data_0222ed61 (image word 0x0222ed61)
 *   pool +0x154 -> constant 0x02239de0 (image word 0x02239de0)
 *   pool +0x158 -> constant 0x02239c64 (image word 0x02239c64)
 *   pool +0x15c -> native_data_0222ed88 (image word 0x0222ed88)
 *   pool +0x160 -> constant 0x02239f4c (image word 0x02239f4c)
 *   back edge +0x2c -> +0x14
 *   back edge +0xbc -> +0x78
 *   back edge +0x114 -> +0xd0
 *   test +0xb0 cmp r8, #13
 *   test +0x108 cmp r8, #19
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff094; the literal pool and
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

extern void native_fn_021fc5c4(void);
extern void native_fn_0202a37c(void);
extern void native_fn_021fd354(void);
extern u8 native_data_0222efd8[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222ed61[];
extern void native_fn_0205ffcc(void);
extern u8 native_data_0222ed88[];
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_021fec7c(void);
extern void native_fn_021feaa8(void);


asm u32 native_ov001_021ff094 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #36
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov001_021ff094_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov001_021ff094_L14
    bl native_fn_021fc5c4
    mov r0, #2
    mov r1, #2048
    mov r2, #4
    bl native_fn_0202a37c
    ldr r1, =0x02239c10
    str r0, [r1, #0x40]
    mov r0, #0
    bl native_fn_021fd354
    ldr r1, =native_data_0222efd8
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0205ff80
    ldr r5, =native_data_0222ed61
    ldr r6, =0x02239de0
    ldr r4, =0x02239c64
    mov r8, #0
ov001_021ff094_L78:
    ldrb r7, [r5, #0x2]
    mov r0, r6
    ldr r1, [r4, r7, lsl #2]
    mov r3, r7
    str r1, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    bl native_fn_0205ffcc
    add r1, r8, #1
    ldr r2, [r4, r7, lsl #2]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r8, r1, asr #24
    str r0, [r4, r7, lsl #2]
    cmp r8, #13
    add r5, r5, #3
    add r6, r6, #12
    blt ov001_021ff094_L78
    ldr r5, =native_data_0222ed88
    ldr r6, =0x02239f4c
    ldr r4, =0x02239c64
    mov r8, #0
ov001_021ff094_Ld0:
    ldrb r7, [r5, #0x2]
    mov r0, r6
    ldr r1, [r4, r7, lsl #2]
    mov r3, r7
    str r1, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    bl native_fn_02065730
    add r1, r8, #1
    ldr r2, [r4, r7, lsl #2]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r8, r1, asr #24
    str r0, [r4, r7, lsl #2]
    cmp r8, #19
    add r5, r5, #3
    add r6, r6, #12
    blt ov001_021ff094_Ld0
    bl native_fn_0205ff9c
    ldr r1, =0x02239f4c
    ldr r0, =0x02239c10
    ldr r1, [r1, #0x9c]
    str r1, [r0, #0x50]
    bl native_fn_021fec7c
    bl native_fn_021feaa8
    ldr r0, =0x02239c10
    mov r1, #1
    strb r1, [r0, #0xf]
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
