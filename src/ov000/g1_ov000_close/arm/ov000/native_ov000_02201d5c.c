/* ov000 row 0x02201d5c: 348 bytes.
 *
 * What it does: 84 instructions; 13 call(s) to 0x02215698, 0x02049ae4, 0x02049f24, +10 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x150 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x154 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0x158 -> constant 0x02237f7c (image word 0x02237f7c)
 *   branch +0x38 -> +0x48
 *   branch +0x40 -> +0x130
 *   branch +0x44 -> +0x12c
 *   branch +0x74 -> +0xc8
 *   branch +0xc4 -> +0x118
 *   branch +0x128 -> +0x130
 *   branch +0x138 -> +0x144
 *   test +0x34 cmp r1, #1
 *   test +0x3c cmp r1, #3
 *   test +0x70 cmp r0, #127
 *   test +0x134 cmp r1, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02201d5c; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02049ae4(void);
extern void native_fn_02049f24(void);
extern void native_fn_02049f30(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02046af4(void);
extern void native_fn_02217bdc(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02217cf0(void);
extern void native_fn_02049f14(void);
extern void native_fn_020853c8(void);


asm u32 native_ov000_02201d5c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r6, #0
    bl native_fn_02215698
    mov r7, r0
    ldr r11, =0x021c9698
    bl native_fn_02049ae4
    mov r9, r0
    bl native_fn_02049f24
    mov r10, r0
    bl native_fn_02049f30
    ldr r0, =0x02237d94
    ldr r1, [r0]
    cmp r1, #1
    beq ov000_02201d5c_L48
    cmp r1, #3
    beq ov000_02201d5c_L130
    b ov000_02201d5c_L12c
ov000_02201d5c_L48:
    ldr r4, [r0, #0x8]
    add r0, r4, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r1, [r0]
    ldr r5, =0x02237f7c
    and r4, r4, #255
    ldrb r0, [r5, r4]
    ldr r8, [r1, #0x4]
    cmp r0, #127
    beq ov000_02201d5c_Lc8
    str r10, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldrb r2, [r8, #0x5e]
    ldr r1, [r8, #0x68]
    mov r0, r11
    mov r3, r6
    bl native_fn_02046af4
    mov r3, #1
    str r3, [sp]
    mov r0, #87
    str r0, [sp, #0x4]
    ldrb r2, [r5, r4]
    mov r0, #5
    mov r1, #7
    add r2, r2, #21
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_02217bdc
    b ov000_02201d5c_L118
ov000_02201d5c_Lc8:
    mov r0, #5
    mov r1, #7
    mov r2, #42
    bl native_fn_0205dc70
    mov r1, r0
    str r10, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldrb r2, [r8, #0x5e]
    mov r0, r11
    mov r3, r6
    bl native_fn_02046af4
    mov r3, #1
    str r3, [sp]
    mov r0, #87
    str r0, [sp, #0x4]
    mov r0, #5
    mov r1, #7
    mov r2, #42
    bl native_fn_02217bdc
ov000_02201d5c_L118:
    add r0, r7, #16
    bl native_fn_02217cf0
    mov r0, r10
    bl native_fn_02049f14
    b ov000_02201d5c_L130
ov000_02201d5c_L12c:
    mov r6, #1
ov000_02201d5c_L130:
    ldr r1, [r9]
    cmp r1, #0
    beq ov000_02201d5c_L144
    ldr r0, [r9, #0x4]
    bl native_fn_020853c8
ov000_02201d5c_L144:
    mov r0, r6
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
