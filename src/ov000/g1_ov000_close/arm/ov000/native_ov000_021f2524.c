/* ov000 row 0x021f2524: 264 bytes.
 *
 * What it does: 65 instructions; 5 call(s) to 0x020d3f4c, 0x02008e0c, 0x02008d78, +2 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x104 -> constant 0x02236d98 (image word 0x02236d98)
 *   branch +0x48 -> +0x94
 *   branch +0x58 -> +0x94
 *   back edge +0xa0 -> +0x34
 *   branch +0xc0 -> +0xec
 *   back edge +0xf4 -> +0xb0
 *   test +0x44 cmp r1, #0
 *   test +0x54 cmp r0, #0
 *   test +0x98 cmp r8, #3
 *   test +0xbc cmp r1, #0
 *   test +0xf0 cmp r3, #3
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f2524; the literal pool and
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

extern void native_fn_020d3f4c(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02008d78(void);


asm u32 native_ov000_021f2524 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r8, #0
    add r7, sp, #4
    mov r6, #4
    ldr r4, =0x02236d98
    mov r10, r0
    str r1, [sp]
    mov r9, r8
    strh r8, [r7]
    strh r8, [r7, #2]
    mov r5, r8
    mov r11, r6
ov000_021f2524_L34:
    ldr r0, [r4, #0x8]
    add r0, r0, r8, lsl #2
    add r0, r0, #6400
    ldrsh r1, [r0, #12]
    cmp r1, #0
    beq ov000_021f2524_L94
    mov r0, r10
    bl native_fn_020d3f4c
    cmp r0, #0
    beq ov000_021f2524_L94
    ldr r0, [r4, #0x8]
    mov r1, r7
    add r0, r0, #268
    add r0, r0, #6144
    mov r2, r6
    add r0, r0, r9
    bl native_fn_02008e0c
    ldr r0, [r4, #0x8]
    mov r1, r5
    add r0, r0, #268
    add r0, r0, #6144
    add r0, r0, r9
    mov r2, r11
    bl native_fn_02008d78
ov000_021f2524_L94:
    add r8, r8, #1
    cmp r8, #3
    add r9, r9, #4
    blt ov000_021f2524_L34
    ldr r0, =0x02236d98
    mov r3, #0
    ldr r2, [r0, #0x8]
ov000_021f2524_Lb0:
    add r0, r2, r3, lsl #2
    add r0, r0, #6400
    ldrsh r1, [r0, #12]
    cmp r1, #0
    bne ov000_021f2524_Lec
    ldr r1, =0x02236d98
    strh r10, [r0, #12]
    ldr r0, [r1, #0x8]
    add r0, r0, r3, lsl #2
    add r1, r0, #4096
    ldr r0, [sp]
    strb r0, [r1, #0x90e]
    ldrsh r0, [sp, #4]
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021f2524_Lec:
    add r3, r3, #1
    cmp r3, #3
    blt ov000_021f2524_Lb0
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
