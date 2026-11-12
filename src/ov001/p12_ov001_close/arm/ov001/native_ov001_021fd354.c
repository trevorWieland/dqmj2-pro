/* ov001 row 0x021fd354: 480 bytes.
 *
 * What it does: 105 instructions; 26 call(s) to 0x0201d444, 0x0201d444, 0x0201d444, +23 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, pc}; 15 literal slot(s) in the extent
 *
 * Decoded shape: loop with 26 calls (105 instructions, 26 calls, 11 branches, 25 back edges, 15 literal slots).
 *
 *   pool +0x1a4 -> native_data_0222ee50 (image word 0x0222ee50)
 *   pool +0x1a8 -> native_data_0222ee64 (image word 0x0222ee64)
 *   pool +0x1ac -> native_data_0222ee78 (image word 0x0222ee78)
 *   pool +0x1b0 -> native_data_0222ee8c (image word 0x0222ee8c)
 *   pool +0x1b4 -> native_data_0222eea4 (image word 0x0222eea4)
 *   pool +0x1b8 -> native_data_0222eebc (image word 0x0222eebc)
 *   pool +0x1bc -> native_data_0222eed4 (image word 0x0222eed4)
 *   pool +0x1c0 -> native_data_0222eee8 (image word 0x0222eee8)
 *   pool +0x1c4 -> native_data_0222eefc (image word 0x0222eefc)
 *   pool +0x1c8 -> native_data_0222ef14 (image word 0x0222ef14)
 *   pool +0x1cc -> native_data_0222ef28 (image word 0x0222ef28)
 *   pool +0x1d0 -> native_data_0222ef3c (image word 0x0222ef3c)
 *   pool +0x1d4 -> native_data_0222ed3e (image word 0x0222ed3e)
 *   pool +0x1d8 -> native_data_0222ed3c (image word 0x0222ed3c)
 *   pool +0x1dc -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x14 -> +0xc4
 *   branch +0x18 -> +0x28
 *   branch +0x1c -> +0x50
 *   branch +0x20 -> +0x78
 *   branch +0x24 -> +0xa0
 *   branch +0x4c -> +0xc4
 *   branch +0x74 -> +0xc4
 *   branch +0x9c -> +0xc4
 *   branch +0xd0 -> +0x114
 *   branch +0x120 -> +0x154
 *   branch +0x160 -> +0x198
 *   test +0x0c cmp r4, #3
 *   test +0xcc cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd354; the literal pool and
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

extern u8 native_data_0222ee50[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222ee64[];
extern u8 native_data_0222ee78[];
extern u8 native_data_0222ee8c[];
extern u8 native_data_0222eea4[];
extern u8 native_data_0222eebc[];
extern u8 native_data_0222eed4[];
extern u8 native_data_0222eee8[];
extern u8 native_data_0222eefc[];
extern u8 native_data_0222ef14[];
extern u8 native_data_0222ef28[];
extern u8 native_data_0222ef3c[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern u8 native_data_0222ed3e[];
extern u8 native_data_0222ed3c[];
extern void native_fn_0204820c(void);
extern void native_fn_0202a498(void);
extern void native_fn_02045490(void);
extern void native_fn_02008e0c(void);
extern void native_fn_022023c4(void);
extern void native_fn_02048308(void);


asm u32 native_ov001_021fd354 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #96
    mov r4, r0
    cmp r4, #3
    addls pc, pc, r4, lsl #2
    b ov001_021fd354_Lc4
    b ov001_021fd354_L28
    b ov001_021fd354_L50
    b ov001_021fd354_L78
    b ov001_021fd354_La0
ov001_021fd354_L28:
    ldr r1, =native_data_0222ee50
    add r0, sp, #0
    bl native_fn_0201d444
    ldr r1, =native_data_0222ee64
    add r0, sp, #32
    bl native_fn_0201d444
    ldr r1, =native_data_0222ee78
    add r0, sp, #64
    bl native_fn_0201d444
    b ov001_021fd354_Lc4
ov001_021fd354_L50:
    ldr r1, =native_data_0222ee8c
    add r0, sp, #0
    bl native_fn_0201d444
    ldr r1, =native_data_0222eea4
    add r0, sp, #32
    bl native_fn_0201d444
    ldr r1, =native_data_0222eebc
    add r0, sp, #64
    bl native_fn_0201d444
    b ov001_021fd354_Lc4
ov001_021fd354_L78:
    ldr r1, =native_data_0222eed4
    add r0, sp, #0
    bl native_fn_0201d444
    ldr r1, =native_data_0222eee8
    add r0, sp, #32
    bl native_fn_0201d444
    ldr r1, =native_data_0222eefc
    add r0, sp, #64
    bl native_fn_0201d444
    b ov001_021fd354_Lc4
ov001_021fd354_La0:
    ldr r1, =native_data_0222ef14
    add r0, sp, #0
    bl native_fn_0201d444
    ldr r1, =native_data_0222ef28
    add r0, sp, #32
    bl native_fn_0201d444
    ldr r1, =native_data_0222ef3c
    add r0, sp, #64
    bl native_fn_0201d444
ov001_021fd354_Lc4:
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov001_021fd354_L114
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r2, =native_data_0222ed3e
    mov r4, r4, lsl #2
    ldr r1, =native_data_0222ed3c
    ldrh r3, [r2, r4]
    ldrh r2, [r1, r4]
    mov r4, r0
    mov r1, r3, lsl #5
    add r0, r4, r3, lsl #5
    mov r2, r2, lsl #1
    bl native_fn_0204820c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov001_021fd354_L114:
    add r0, sp, #32
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov001_021fd354_L154
    add r0, sp, #32
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r1, r4
    mov r3, r5
    mov r0, #3
    mov r2, #0
    bl native_fn_02045490
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov001_021fd354_L154:
    add r0, sp, #64
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov001_021fd354_L198
    add r0, sp, #64
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02239c10
    mov r4, r0
    ldr r1, [r1, #0x40]
    mov r2, r5
    bl native_fn_02008e0c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    mov r0, #2
    bl native_fn_022023c4
ov001_021fd354_L198:
    bl native_fn_02048308
    add sp, sp, #96
    ldmia sp!, {r3, r4, r5, pc}
}
