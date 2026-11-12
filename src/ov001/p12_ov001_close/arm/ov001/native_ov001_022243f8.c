/* ov001 row 0x022243f8: 168 bytes.
 *
 * What it does: 42 instructions; 7 call(s) to 0x02008e0c, 0x021dbd24, 0x02223f48, +4 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 7 calls (42 instructions, 7 calls, 1 branch, 6 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x68
 *   back edge +0x74 -> +0x34
 *   branch +0x88 -> +0x9c
 *   test +0x38 cmp r0, #0
 *   test +0x60 cmp r5, r0
 *   test +0x6c cmp r7, #3
 *   test +0x84 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022243f8; the literal pool and
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


asm u32 native_ov001_022243f8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r10, r1
    mov r9, r2
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r8, r3
    bl native_fn_02008e0c
    mov r7, #0
    mov r4, r7
    add r6, sp, #4
    mov r11, #1
ov001_022243f8_L34:
    ldr r0, [r6, r7, lsl #2]
    cmp r0, #0
    beq ov001_022243f8_L68
    mov r0, r9
    bl native_fn_021dbd24
    mov r5, r0
    mov r0, r10
    mov r1, r9
    mov r2, r8
    mov r3, r11
    bl native_fn_02223f48
    cmp r5, r0
    strgt r4, [r6, r7, lsl #2]
ov001_022243f8_L68:
    add r7, r7, #1
    cmp r7, #3
    add r9, r9, #1088
    blt ov001_022243f8_L34
    add r0, sp, #4
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022243f8_L9c
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_022243f8_L9c:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
