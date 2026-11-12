/* ov000 row 0x021f4dac: 212 bytes.
 *
 * What it does: 52 instructions; 10 call(s) to 0x01ffb698, 0x021f4db8, 0x01ffa394, +7 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd0 -> constant 0x021c9698 (image word 0x021c9698)
 *   back edge +0x20 -> +0x0c
 *   branch +0x54 -> +0x8c
 *   branch +0x88 -> +0xbc
 *   back edge +0xc4 -> +0x44
 *   test +0x1c cmp r4, #8
 *   test +0x4c cmp r0, #1
 *   test +0xc0 cmp r10, #8
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f4dac; the literal pool and
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

extern void native_fn_01ffb698(void);
extern void native_fn_01ffa394(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_02046af4(void);
extern void native_fn_01ffb648(void);
extern void native_fn_02008d78(void);
extern void native_fn_01ffb530(void);


asm u32 native_ov000_021f4dac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    mov r4, #1
ov000_021f4dac_Lc:
    add r0, r4, #6
    and r0, r0, #255
    bl native_fn_01ffb698
    add r4, r4, #1
    cmp r4, #8
    blt ov000_021f4dac_Lc
    mov r10, #0
    ldr r7, =0x021c9698
    mov r5, r10
    mov r4, #3
    add r9, sp, #8
    mov r8, #255
    mov r6, #31
    mov r11, r10
ov000_021f4dac_L44:
    mov r0, r10
    bl native_fn_01ffa394
    cmp r0, #1
    and r0, r10, #255
    bne ov000_021f4dac_L8c
    bl native_fn_01ffb4ec
    str r9, [sp]
    mov r1, r0
    mov r0, r7
    mov r2, r6
    mov r3, r11
    str r8, [sp, #0x4]
    bl native_fn_02046af4
    add r0, r10, #6
    and r0, r0, #255
    mov r1, r9
    bl native_fn_01ffb648
    b ov000_021f4dac_Lbc
ov000_021f4dac_L8c:
    bl native_fn_01ffb4ec
    mov r1, #0
    mov r2, #20
    bl native_fn_02008d78
    add r0, r10, #6
    str r5, [sp]
    and r0, r0, #255
    mov r1, #16
    mov r2, #2
    mov r3, #5
    str r4, [sp, #0x4]
    bl native_fn_01ffb530
ov000_021f4dac_Lbc:
    add r10, r10, #1
    cmp r10, #8
    blt ov000_021f4dac_L44
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
