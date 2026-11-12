/* ov000 row 0x02225434: 344 bytes.
 *
 * What it does: 85 instructions; 12 call(s) to 0x022256fc, 0x022256e4, 0x02008e0c, +9 more; loops (back edge at +0x58); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x154 -> constant 0x02246aa8 (image word 0x02246aa8)
 *   branch +0x0c -> +0x2c
 *   branch +0x28 -> +0x44
 *   branch +0x98 -> +0x124
 *   branch +0x120 -> +0x134
 *   back edge +0x148 -> +0x90
 *   test +0x04 cmp r1, #0
 *   test +0x10 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0x144 cmp r8, #3
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02225434; the literal pool and
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

extern void native_fn_022256fc(void);
extern void native_fn_022256e4(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02008d78(void);
extern void native_fn_02223ce0(void);


asm u32 native_ov000_02225434 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    cmp r1, #0
    ldr r10, =0x02246aa8
    beq ov000_02225434_L2c
    cmp r0, #0
    movne r0, #68
    moveq r0, #24
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_022256fc
    b ov000_02225434_L44
ov000_02225434_L2c:
    cmp r0, #0
    movne r0, #68
    moveq r0, #24
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_022256e4
ov000_02225434_L44:
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r1, r10, #404
    mov r2, #68
    bl native_fn_02008e0c
    ldrb r2, [r10, #0x194]
    ldrb r1, [r10, #0x195]
    ldrb r0, [r10, #0x196]
    mov r8, #0
    strb r2, [r10, #0x18c]
    strb r1, [r10, #0x18d]
    strb r0, [r10, #0x192]
    mov r9, #3
    add r5, r10, #404
    mov r7, r8
    mov r6, #132
    mov r4, #16
    mov r11, #2
ov000_02225434_L90:
    ldrsh r0, [r10, #24]
    cmp r0, #0
    beq ov000_02225434_L124
    mov r0, r10
    mov r1, r7
    mov r2, r6
    bl native_fn_02008d78
    add r0, r5, r9
    mov r1, r10
    mov r2, r4
    bl native_fn_02008e0c
    add r0, r9, #16
    add r0, r5, r0
    add r1, r10, #24
    mov r2, r11
    bl native_fn_02008e0c
    add r0, r9, #18
    add r0, r5, r0
    add r1, r10, #26
    mov r2, #1
    bl native_fn_02008e0c
    add r0, r9, #19
    add r0, r5, r0
    add r1, r10, #48
    mov r2, #1
    bl native_fn_02008e0c
    add r0, r9, #20
    add r0, r5, r0
    add r1, r10, #27
    mov r2, #1
    bl native_fn_02008e0c
    mov r0, #1
    mov r1, r8
    mov r2, r10
    add r9, r9, #21
    bl native_fn_02223ce0
    b ov000_02225434_L134
ov000_02225434_L124:
    mov r0, #1
    mov r1, r8
    mov r2, #0
    bl native_fn_02223ce0
ov000_02225434_L134:
    add r10, r10, #132
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #3
    blt ov000_02225434_L90
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
