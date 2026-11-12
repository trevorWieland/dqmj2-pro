/* ov000 row 0x02224fa4: 288 bytes.
 *
 * What it does: 69 instructions; 8 call(s) to 0x02008d78, 0x0222508c, 0x02008e0c, +5 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x114 -> constant 0x02246e18 (image word 0x02246e18)
 *   pool +0x118 -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0x11c -> constant 0x022468b8 (image word 0x022468b8)
 *   branch +0x48 -> +0xe8
 *   branch +0x64 -> +0xcc
 *   back edge +0xe4 -> +0x60
 *   test +0x44 cmp r0, #0
 *   test +0x60 cmp r10, #0
 *   test +0xd8 cmp r1, r0, asr #24
 *   test +0xec cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224fa4; the literal pool and
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
extern void native_fn_01ffa5ac(void);


asm u32 native_ov000_02224fa4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
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
    ble ov000_02224fa4_Le8
    mov r10, r7
    add r6, r7, #404
    mov r5, #16
    mov r4, #2
    mov r11, #1
ov000_02224fa4_L60:
    cmp r10, #0
    beq ov000_02224fa4_Lcc
    mov r0, r10
    mov r2, r5
    add r1, r6, r9
    bl native_fn_02008e0c
    add r1, r9, #16
    add r0, r10, #24
    add r1, r6, r1
    mov r2, r4
    bl native_fn_02008e0c
    add r1, r9, #18
    add r0, r10, #26
    add r1, r6, r1
    mov r2, r11
    bl native_fn_02008e0c
    add r1, r9, #19
    add r0, r10, #48
    add r1, r6, r1
    mov r2, #1
    bl native_fn_02008e0c
    add r1, r9, #20
    add r0, r10, #27
    add r1, r6, r1
    mov r2, #1
    bl native_fn_02008e0c
    add r9, r9, #21
ov000_02224fa4_Lcc:
    ldrb r1, [r7, #0x18d]
    add r0, r8, #1
    mov r0, r0, lsl #24
    cmp r1, r0, asr #24
    add r10, r10, #132
    mov r8, r0, asr #24
    bgt ov000_02224fa4_L60
ov000_02224fa4_Le8:
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
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
