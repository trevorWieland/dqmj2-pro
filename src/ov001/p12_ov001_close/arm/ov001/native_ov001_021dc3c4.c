/* ov001 row 0x021dc3c4: 264 bytes.
 *
 * What it does: 62 instructions; 7 call(s) to 0x021db578, 0x021dc4b0, 0x02008d78, +4 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (62 instructions, 7 calls, 3 branches, 4 back edges, 4 literal slots).
 *
 *   pool +0xf8 -> constant 0x022362ac (image word 0x022362ac)
 *   pool +0xfc -> constant 0x02237c2c (image word 0x02237c2c)
 *   pool +0x100 -> constant 0x02236f6c (image word 0x02236f6c)
 *   pool +0x104 -> constant 0x022355ec (image word 0x022355ec)
 *   branch +0x18 -> +0x28
 *   branch +0x34 -> +0xec
 *   branch +0x74 -> +0x88
 *   branch +0x90 -> +0xa4
 *   back edge +0xb4 -> +0x6c
 *   test +0x30 cmp r0, #0
 *   test +0x70 cmp r12, #0
 *   test +0x8c cmp r12, #0
 *   test +0xa8 cmp r0, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc3c4; the literal pool and
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

extern void native_fn_021db578(void);
extern void native_fn_02008d78(void);
extern void native_fn_0220b3e4(void);


asm u32 native_ov001_021dc3c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #24
    movs r7, r0
    ldrne r5, =0x022362ac
    ldrne r6, =0x02237c2c
    movne r4, #3
    bne ov001_021dc3c4_L28
    ldr r5, =0x02236f6c
    ldr r6, =0x022355ec
    mov r4, #2
ov001_021dc3c4_L28:
    mov r0, r4
    bl native_fn_021db578
    cmp r0, #0
    ble ov001_021dc3c4_Lec
    add r0, sp, #12
    mov r1, #0
    mov r2, #12
    bl native_fn_02008d78
    add r0, sp, #0
    mov r1, #0
    mov r2, #12
    bl native_fn_02008d78
    mov r1, #0
    mov r2, r1
    mov r0, r1
    add lr, sp, #0
    add r3, sp, #12
ov001_021dc3c4_L6c:
    ldrb r12, [r5, #0x31c]
    cmp r12, #0
    beq ov001_021dc3c4_L88
    ldr r12, [r5, #0x1e8]
    ldr r12, [r12]
    str r12, [lr, r2, lsl #2]
    add r2, r2, #1
ov001_021dc3c4_L88:
    ldrb r12, [r6, #0x31c]
    cmp r12, #0
    beq ov001_021dc3c4_La4
    ldr r12, [r6, #0x1e8]
    ldr r12, [r12]
    str r12, [r3, r1, lsl #2]
    add r1, r1, #1
ov001_021dc3c4_La4:
    add r0, r0, #1
    cmp r0, #3
    add r5, r5, #1088
    add r6, r6, #1088
    blt ov001_021dc3c4_L6c
    ldr r1, [sp, #0xc]
    ldr r2, [sp, #0x10]
    ldr r3, [sp, #0x14]
    mov r0, r7
    bl native_fn_0220b3e4
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, r4
    bl native_fn_0220b3e4
    add sp, sp, #24
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_021dc3c4_Lec:
    mov r0, #0
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
