/* ov000 row 0x02215bc8: 164 bytes.
 *
 * What it does: 40 instructions; 8 call(s) to 0x02062aa0, 0x02062ad0, 0x02008d78, +5 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x0224575c (image word 0x0224575c)
 *   back edge +0x50 -> +0x2c
 *   branch +0x68 -> +0x78
 *   branch +0x74 -> +0x80
 *   back edge +0x98 -> +0x64
 *   test +0x4c cmp r9, #6
 *   test +0x5c cmp r4, #0
 *   test +0x64 cmp r10, r8
 *   test +0x94 cmp r10, r4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215bc8; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02008d78(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02215c6c(void);


asm u32 native_ov000_02215bc8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    bl native_fn_02062aa0
    mov r8, r0
    bl native_fn_02062ad0
    mov r9, #0
    ldr r6, =0x0224575c
    str r0, [sp]
    mov r5, r9
    mov r11, #32
    mov r10, r9
    mov r4, #100
ov000_02215bc8_L2c:
    mla r7, r9, r4, r6
    mov r0, r7
    mov r1, r5
    mov r2, r11
    bl native_fn_02008d78
    add r0, r9, #1
    and r9, r0, #255
    strb r10, [r7, #0x60]
    cmp r9, #6
    blo ov000_02215bc8_L2c
    ldr r0, [sp]
    add r4, r8, r0
    cmp r4, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02215bc8_L64:
    cmp r10, r8
    bge ov000_02215bc8_L78
    mov r0, r10
    bl native_fn_02062a50
    b ov000_02215bc8_L80
ov000_02215bc8_L78:
    sub r0, r10, r8
    bl native_fn_02062a88
ov000_02215bc8_L80:
    ldr r1, [r0, #0x14]
    mov r0, r10
    bl native_fn_02215c6c
    add r0, r10, #1
    and r10, r0, #255
    cmp r10, r4
    blt ov000_02215bc8_L64
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
