/* ov001 row 0x022240a4: 308 bytes.
 *
 * What it does: 76 instructions; 8 call(s) to 0x02008e0c, 0x021dbd24, 0x02223f48, +5 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (76 instructions, 8 calls, 5 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0x130 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x4c -> +0x84
 *   back edge +0x90 -> +0x40
 *   branch +0xb4 -> +0xd0
 *   branch +0xbc -> +0xf4
 *   branch +0xcc -> +0xf4
 *   branch +0xd4 -> +0xe8
 *   back edge +0xfc -> +0xac
 *   branch +0x110 -> +0x124
 *   test +0x30 cmp r7, #0
 *   test +0x48 cmp r0, #0
 *   test +0x78 cmp r1, r5
 *   test +0x88 cmp r6, #3
 *   test +0xac cmp r8, #0
 *   test +0xb8 cmp r3, #0
 *   test +0xc4 cmp r3, r5
 *   test +0xd0 cmp r3, #0
 *   test +0xdc cmp r3, r5
 *   test +0xe0 cmpgt r3, #0
 *   test +0xec cmp r3, #0
 *   test +0xf8 cmp r1, #3
 *   test +0x10c cmp r4, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022240a4; the literal pool and
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
extern void native_fn_021dbd24(void);
extern void native_fn_02223f48(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_022240a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #32
    mov r10, r1
    mov r9, r2
    ldr r7, [sp, #0x4c]
    add r1, sp, #8
    mov r2, #12
    str r0, [sp]
    mov r11, r3
    ldr r8, [sp, #0x48]
    ldr r5, =0x0000270f
    bl native_fn_02008e0c
    cmp r7, #0
    addeq r7, sp, #4
    mov r6, #0
    str r6, [r7]
ov001_022240a4_L40:
    add r0, sp, #8
    ldr r0, [r0, r6, lsl #2]
    cmp r0, #0
    beq ov001_022240a4_L84
    mov r0, r9
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r10
    mov r1, r9
    mov r2, r11
    mov r3, #2
    bl native_fn_02223f48
    sub r1, r4, r0
    add r0, sp, #20
    cmp r1, r5
    str r1, [r0, r6, lsl #2]
    movlt r5, r1
ov001_022240a4_L84:
    add r6, r6, #1
    cmp r6, #3
    add r9, r9, #1088
    blt ov001_022240a4_L40
    mov r1, #0
    mov r4, r1
    add r9, sp, #20
    add r0, sp, #8
    mov r2, #1
    mov r6, r1
ov001_022240a4_Lac:
    cmp r8, #0
    ldr r3, [r0, r1, lsl #2]
    bne ov001_022240a4_Ld0
    cmp r3, #0
    beq ov001_022240a4_Lf4
    ldr r3, [r9, r1, lsl #2]
    cmp r3, r5
    strgt r6, [r0, r1, lsl #2]
    b ov001_022240a4_Lf4
ov001_022240a4_Ld0:
    cmp r3, #0
    beq ov001_022240a4_Le8
    ldr r3, [r9, r1, lsl #2]
    cmp r3, r5
    cmpgt r3, #0
    strgt r4, [r0, r1, lsl #2]
ov001_022240a4_Le8:
    ldr r3, [r9, r1, lsl #2]
    cmp r3, #0
    strle r2, [r7]
ov001_022240a4_Lf4:
    add r1, r1, #1
    cmp r1, #3
    blt ov001_022240a4_Lac
    add r0, sp, #8
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022240a4_L124
    ldr r1, [sp]
    add r0, sp, #8
    mov r2, #12
    bl native_fn_02008e0c
ov001_022240a4_L124:
    mov r0, r4
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
