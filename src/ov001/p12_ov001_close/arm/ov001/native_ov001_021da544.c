/* ov001 row 0x021da544: 420 bytes.
 *
 * What it does: 104 instructions; 26 call(s) to 0x021db438, 0x021dba58, 0x021da4f4, +23 more; loops (back edge at +0x44); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 26 calls (104 instructions, 26 calls, 10 branches, 12 back edges, 1 literal slot).
 *
 *   pool +0x1a0 -> constant 0x022355e4 (image word 0x022355e4)
 *   branch +0x14 -> +0x50
 *   branch +0x4c -> +0xd0
 *   branch +0x54 -> +0x88
 *   branch +0x84 -> +0xd0
 *   branch +0x8c -> +0xd0
 *   branch +0xdc -> +0x118
 *   branch +0x114 -> +0x198
 *   branch +0x11c -> +0x150
 *   branch +0x14c -> +0x198
 *   branch +0x154 -> +0x198
 *   test +0x10 cmp r0, #1
 *   test +0x34 cmp r0, #0
 *   test +0x50 cmp r0, #2
 *   test +0x88 cmp r0, #3
 *   test +0xd8 cmp r0, #1
 *   test +0xfc cmp r0, #0
 *   test +0x118 cmp r0, #2
 *   test +0x150 cmp r0, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021da544; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021dba58(void);
extern void native_fn_021da4f4(void);


asm u32 native_ov001_021da544 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x022355e4
    mov r4, #0
    ldrb r0, [r0, #0x3]
    cmp r0, #1
    bne ov001_021da544_L50
    mov r0, r4
    mov r1, r4
    bl native_fn_021db438
    mov r5, r0
    mov r0, r4
    mov r1, #2
    bl native_fn_021dba58
    cmp r0, #0
    movne r1, #7
    moveq r1, #3
    mov r0, r5
    bl native_fn_021da4f4
    add r4, r4, #1
    b ov001_021da544_Ld0
ov001_021da544_L50:
    cmp r0, #2
    bne ov001_021da544_L88
    mov r0, r4
    mov r1, r4
    bl native_fn_021db438
    mov r1, #5
    bl native_fn_021da4f4
    mov r0, r4
    mov r1, #1
    bl native_fn_021db438
    mov r1, #6
    bl native_fn_021da4f4
    add r4, r4, #2
    b ov001_021da544_Ld0
ov001_021da544_L88:
    cmp r0, #3
    bne ov001_021da544_Ld0
    mov r0, r4
    mov r1, r4
    bl native_fn_021db438
    mov r1, #2
    bl native_fn_021da4f4
    mov r0, r4
    mov r1, #1
    bl native_fn_021db438
    mov r1, #3
    bl native_fn_021da4f4
    mov r0, r4
    mov r1, #2
    bl native_fn_021db438
    mov r1, #4
    bl native_fn_021da4f4
    add r4, r4, #3
ov001_021da544_Ld0:
    ldr r0, =0x022355e4
    ldrb r0, [r0, #0x2]
    cmp r0, #1
    bne ov001_021da544_L118
    mov r0, #1
    mov r1, #0
    bl native_fn_021db438
    mov r5, r0
    mov r0, #1
    mov r1, #2
    bl native_fn_021dba58
    cmp r0, #0
    movne r1, #15
    moveq r1, #11
    mov r0, r5
    bl native_fn_021da4f4
    add r4, r4, #1
    b ov001_021da544_L198
ov001_021da544_L118:
    cmp r0, #2
    bne ov001_021da544_L150
    mov r0, #1
    mov r1, #0
    bl native_fn_021db438
    mov r1, #13
    bl native_fn_021da4f4
    mov r0, #1
    mov r1, r0
    bl native_fn_021db438
    mov r1, #14
    bl native_fn_021da4f4
    add r4, r4, #2
    b ov001_021da544_L198
ov001_021da544_L150:
    cmp r0, #3
    bne ov001_021da544_L198
    mov r0, #1
    mov r1, #0
    bl native_fn_021db438
    mov r1, #10
    bl native_fn_021da4f4
    mov r0, #1
    mov r1, r0
    bl native_fn_021db438
    mov r1, #11
    bl native_fn_021da4f4
    mov r0, #1
    mov r1, #2
    bl native_fn_021db438
    mov r1, #12
    bl native_fn_021da4f4
    add r4, r4, #3
ov001_021da544_L198:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
