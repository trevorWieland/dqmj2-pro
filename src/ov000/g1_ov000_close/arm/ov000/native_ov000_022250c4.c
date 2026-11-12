/* ov000 row 0x022250c4: 308 bytes.
 *
 * What it does: 74 instructions; 10 call(s) to 0x02008d78, 0x022251bc, 0x02008e0c, +7 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x128 -> constant 0x02246e18 (image word 0x02246e18)
 *   pool +0x12c -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0x130 -> constant 0x022468b8 (image word 0x022468b8)
 *   branch +0x4c -> +0xf8
 *   back edge +0xf4 -> +0x64
 *   test +0x48 cmp r0, #0
 *   test +0xf0 cmp r1, r0, asr #24
 *   test +0xfc cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022250c4; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02227cec(void);
extern void native_fn_020cf5e8(void);
extern void native_fn_01ffa5ac(void);


asm u32 native_ov000_022250c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #136
    str r0, [sp]
    ldr r0, =0x02246e18
    ldr r7, =0x02246c84
    mov r1, #0
    mov r2, #68
    bl native_fn_02008d78
    mov r1, r7
    ldrb r2, [r1, #0x18c]
    mov r9, #3
    ldr r0, =0x022468b8
    strb r2, [r1, #0x194]
    strb r9, [r1, #0x195]
    ldr r0, [r0, #0x4]
    mov r8, #0
    strb r0, [r1, #0x196]
    ldrb r0, [r1, #0x18d]
    cmp r0, #0
    ble ov000_022250c4_Lf8
    mov r10, r7
    add r4, r7, #404
    add r6, sp, #4
    mov r5, #132
    mov r11, #16
ov000_022250c4_L64:
    mov r0, r10
    mov r1, r6
    mov r2, r5
    bl native_fn_02008e0c
    mov r0, r6
    bl native_fn_02227cec
    ldrsh r0, [sp, #28]
    ldrb r1, [sp, #0x1e]
    bl native_fn_020cf5e8
    strh r0, [sp, #28]
    mov r0, r6
    add r1, r4, r9
    mov r2, r11
    bl native_fn_02008e0c
    add r1, r9, #16
    add r0, sp, #28
    add r1, r4, r1
    mov r2, #2
    bl native_fn_02008e0c
    add r1, r9, #18
    add r0, sp, #52
    add r1, r4, r1
    mov r2, #1
    bl native_fn_02008e0c
    add r1, r9, #19
    add r0, sp, #31
    add r1, r4, r1
    mov r2, #1
    bl native_fn_02008e0c
    add r0, r8, #1
    mov r0, r0, lsl #24
    ldrb r1, [r7, #0x18d]
    add r9, r9, #20
    add r10, r10, #132
    mov r8, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov000_022250c4_L64
ov000_022250c4_Lf8:
    ldr r0, [sp]
    cmp r0, #0
    movne r0, #68
    moveq r0, #24
    mov r1, r0, lsl #16
    mov r2, r1, lsr #16
    add r0, r7, #404
    mov r1, #68
    bl native_fn_01ffa5ac
    mov r0, #0
    add sp, sp, #136
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
