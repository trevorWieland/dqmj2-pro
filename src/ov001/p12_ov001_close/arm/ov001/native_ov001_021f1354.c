/* ov001 row 0x021f1354: 164 bytes.
 *
 * What it does: 40 instructions; 5 call(s) to 0x02085284, 0x02086b14, 0x02086b24, +2 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (40 instructions, 5 calls, 2 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0xa0 -> constant 0x02238f58 (image word 0x02238f58)
 *   branch +0x64 -> +0x7c
 *   branch +0x78 -> +0x8c
 *   test +0x20 cmp r0, #2
 *   test +0x60 cmp r4, #1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1354; the literal pool and
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

extern void native_fn_02085284(void);
extern void native_fn_02086b14(void);
extern void native_fn_02086b24(void);
extern void native_fn_02085420(void);


asm u32 native_ov001_021f1354 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =0x02238f58
    mov r5, r0
    ldr r12, [r4, #0x4]
    mov r4, r3
    ldr r0, [r12, #0x18]
    mov lr, r1
    and r0, r0, #2
    cmp r0, #2
    ldmeqia sp!, {r3, r4, r5, pc}
    mov r3, r2, lsl #16
    add r0, r12, #60
    and r1, r5, #255
    and r2, lr, #255
    mov r3, r3, lsr #16
    bl native_fn_02085284
    ldr r0, =0x02238f58
    mov r1, #22
    ldr r3, [r0, #0x4]
    ldr r2, [r3, #0x18]
    orr r2, r2, #2
    str r2, [r3, #0x18]
    ldr r0, [r0, #0x4]
    bl native_fn_02086b14
    cmp r4, #1
    bne ov001_021f1354_L7c
    ldr r0, =0x02238f58
    mov r1, #24
    ldr r0, [r0, #0x4]
    bl native_fn_02086b24
    b ov001_021f1354_L8c
ov001_021f1354_L7c:
    ldr r0, =0x02238f58
    mov r1, #4
    ldr r0, [r0, #0x4]
    bl native_fn_02086b24
ov001_021f1354_L8c:
    ldr r0, =0x02238f58
    mov r1, #0
    ldr r0, [r0, #0x4]
    bl native_fn_02085420
    ldmia sp!, {r3, r4, r5, pc}
}
