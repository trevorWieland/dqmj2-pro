/* ov001 row 0x02224f54: 284 bytes.
 *
 * What it does: 70 instructions; 10 call(s) to 0x02008e0c, 0x021dbd30, 0x0207b244, +7 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (70 instructions, 10 calls, 2 branches, 9 back edges, 1 literal slot).
 *
 *   pool +0x118 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x58 -> +0xa4
 *   back edge +0xb0 -> +0x50
 *   branch +0xcc -> +0xdc
 *   back edge +0xe4 -> +0xc4
 *   branch +0xf8 -> +0x10c
 *   test +0x54 cmp r0, #0
 *   test +0x98 cmp r1, r6
 *   test +0xa8 cmp r5, #3
 *   test +0xc8 cmp r1, #0
 *   test +0xd4 cmp r1, r6
 *   test +0xe0 cmp r4, #3
 *   test +0xf4 cmp r4, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224f54; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_021dbd30(void);
extern void native_fn_0207b244(void);
extern void native_fn_021f0858(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02224f54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    mov r10, r1
    mov r9, r2
    add r1, sp, #16
    mov r2, #12
    str r0, [sp, #0xc]
    mov r8, r3
    ldr r6, =0x0000270f
    bl native_fn_02008e0c
    mov r0, r10
    bl native_fn_021dbd30
    ldr r2, [r10, #0x1e8]
    mov r1, r0
    add r2, r2, #70
    mov r0, r8
    bl native_fn_0207b244
    mov r7, r0
    mov r5, #0
    add r11, sp, #16
ov001_02224f54_L50:
    ldr r0, [r11, r5, lsl #2]
    cmp r0, #0
    beq ov001_02224f54_La4
    mov r0, r9
    bl native_fn_021dbd30
    mov r1, #0
    str r1, [sp]
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    mov r4, r0
    mov r0, r10
    mov r1, r9
    mov r2, r7
    mov r3, r8
    bl native_fn_021f0858
    sub r1, r4, r0
    add r0, sp, #28
    cmp r1, r6
    str r1, [r0, r5, lsl #2]
    movle r6, r1
ov001_02224f54_La4:
    add r5, r5, #1
    cmp r5, #3
    add r9, r9, #1088
    blt ov001_02224f54_L50
    mov r4, #0
    mov r0, r4
    add r2, sp, #28
    add r3, sp, #16
ov001_02224f54_Lc4:
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_02224f54_Ldc
    ldr r1, [r2, r4, lsl #2]
    cmp r1, r6
    strgt r0, [r3, r4, lsl #2]
ov001_02224f54_Ldc:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_02224f54_Lc4
    add r0, sp, #16
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224f54_L10c
    ldr r1, [sp, #0xc]
    add r0, sp, #16
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224f54_L10c:
    mov r0, r4
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
