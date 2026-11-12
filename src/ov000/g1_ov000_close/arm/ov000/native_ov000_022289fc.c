/* ov000 row 0x022289fc: 200 bytes.
 *
 * What it does: 50 instructions; 7 call(s) to 0x02229f38, 0x02229f38, 0x02229f38, +4 more; loops (back edge at +0xc4); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x4c -> +0x7c
 *   branch +0x60 -> +0x7c
 *   branch +0x8c -> +0xbc
 *   branch +0xa0 -> +0xbc
 *   back edge +0xc4 -> +0x24
 *   test +0x30 cmp r0, r4
 *   test +0x48 cmp r10, r0
 *   test +0x5c cmp r9, r0
 *   test +0x88 cmp r9, r0
 *   test +0x9c cmp r10, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022289fc; the literal pool and
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

extern void native_fn_02229f38(void);


asm u32 native_ov000_022289fc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r8, #0
    mov r10, r0
    mov r9, r1
    mov r5, #1
    mov r6, r8
    mov r11, r8
    mov r7, r8
    mvn r4, #0
ov000_022289fc_L24:
    mov r0, r8
    mov r1, r7
    bl native_fn_02229f38
    cmp r0, r4
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r8
    mov r1, r6
    bl native_fn_02229f38
    cmp r10, r0
    bne ov000_022289fc_L7c
    mov r0, r8
    mov r1, r5
    bl native_fn_02229f38
    cmp r9, r0
    bne ov000_022289fc_L7c
    mov r0, r8
    mov r1, #2
    bl native_fn_02229f38
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_022289fc_L7c:
    mov r0, r8
    mov r1, r11
    bl native_fn_02229f38
    cmp r9, r0
    bne ov000_022289fc_Lbc
    mov r0, r8
    mov r1, #1
    bl native_fn_02229f38
    cmp r10, r0
    bne ov000_022289fc_Lbc
    mov r0, r8
    mov r1, #2
    bl native_fn_02229f38
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_022289fc_Lbc:
    add r0, r8, #1
    and r8, r0, #255
    b ov000_022289fc_L24
}
