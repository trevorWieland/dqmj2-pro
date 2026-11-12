/* ov000 row 0x02217d18: 164 bytes.
 *
 * What it does: 40 instructions; 6 call(s) to 0x02049ad0, 0x02049f24, 0x02046af4, +3 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x021c9698 (image word 0x021c9698)
 *   test +0x64 cmp r0, #6
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217d18; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02049f24(void);
extern void native_fn_02046af4(void);
extern void native_fn_02049f14(void);
extern void native_fn_02077860(void);
extern void native_fn_02217bdc(void);


asm u32 native_ov000_02217d18 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #8
    mov r4, r0
    add r0, r4, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r7, r1
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r6, [r0, #0x4]
    bl native_fn_02049f24
    mov r5, r0
    str r5, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldrb r2, [r6, #0x5e]
    ldr r0, =0x021c9698
    ldr r1, [r6, #0x68]
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r5
    bl native_fn_02049f14
    add r0, r7, r4, lsl #1
    ldrb r0, [r0, #0x7a]
    bl native_fn_02077860
    cmp r0, #6
    movhi r0, #1
    movls r0, #0
    mov r0, r0, lsl #16
    mov r3, #1
    mov r2, r0, lsr #16
    str r3, [sp]
    mov r4, #87
    mov r0, #12
    mov r1, #0
    str r4, [sp, #0x4]
    bl native_fn_02217bdc
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
