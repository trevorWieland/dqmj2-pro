/* ov000 row 0x021fec54: 228 bytes.
 *
 * What it does: 55 instructions; 10 call(s) to 0x02215698, 0x02049ae4, 0x02049f24, +7 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xdc -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0xe0 -> constant 0x02237564 (image word 0x02237564)
 *   branch +0x38 -> +0xb8
 *   branch +0xb4 -> +0xbc
 *   branch +0xc4 -> +0xd0
 *   test +0x34 cmp r1, #3
 *   test +0xc0 cmp r1, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fec54; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02049ae4(void);
extern void native_fn_02049f24(void);
extern void native_fn_02049f30(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02046af4(void);
extern void native_fn_02049f14(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02217cf0(void);
extern void native_fn_020853c8(void);


asm u32 native_ov000_021fec54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    mov r6, #0
    bl ov000_display_context_02215698
    mov r5, r0
    ldr r7, =0x021c9698
    bl native_fn_02049ae4
    mov r8, r0
    bl native_fn_02049f24
    mov r4, r0
    bl native_fn_02049f30
    ldr r0, =0x02237564
    ldr r1, [r0]
    cmp r1, #3
    bne ov000_021fec54_Lb8
    ldr r9, [r0, #0xf8]
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    mov r1, #255
    ldr r3, [r0, #0x4]
    mov r0, r7
    str r4, [sp]
    str r1, [sp, #0x4]
    ldrb r2, [r3, #0x5e]
    ldr r1, [r3, #0x68]
    mov r3, r6
    bl native_fn_02046af4
    mov r0, r4
    bl native_fn_02049f14
    mov r1, #1
    and r0, r9, #255
    add r0, r0, #8
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    str r1, [sp]
    mov r0, #87
    str r0, [sp, #0x4]
    mov r0, r6
    mov r3, r1
    bl native_fn_02217bdc
    add r0, r5, #16
    bl native_fn_02217cf0
    b ov000_021fec54_Lbc
ov000_021fec54_Lb8:
    mov r6, #1
ov000_021fec54_Lbc:
    ldr r1, [r8]
    cmp r1, #0
    beq ov000_021fec54_Ld0
    ldr r0, [r8, #0x4]
    bl native_fn_020853c8
ov000_021fec54_Ld0:
    mov r0, r6
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
