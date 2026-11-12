/* ov001 row 0x021f4fa4: 212 bytes.
 *
 * What it does: 50 instructions; 4 call(s) to 0x021e1864, 0x021f5060, 0x021e1864, +1 more; loops (back edge at +0x4c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (50 instructions, 4 calls, 2 branches, 3 back edges, 3 literal slots).
 *
 *   pool +0xc8 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0xcc -> constant 0x0223995c (image word 0x0223995c)
 *   pool +0xd0 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x20 -> +0x58
 *   branch +0x54 -> +0xbc
 *   branch +0x68 -> +0xbc
 *   back edge +0xb8 -> +0x78
 *   test +0x1c cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0xb4 cmp r7, r1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f4fa4; the literal pool and
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

extern void native_fn_021e1864(void);


asm u32 native_ov001_021f4fa4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    ldr r4, =0x0223989c
    mov r5, r0
    ldrb r0, [r4, #0x10]
    mov r10, r1
    mov r9, r2
    cmp r0, #0
    bne ov001_021f4fa4_L58
    ldr r1, =0x0223989c
    moveq r3, #1
    ldrb r4, [r1, #0x29]
    movne r3, #0
    mov r0, r9
    str r4, [sp]
    mov r4, #0
    mov r1, r5
    mov r2, r10
    str r4, [sp, #0x4]
    bl native_fn_021e1864
    mov r6, r0
    b ov001_021f4fa4_Lbc
ov001_021f4fa4_L58:
    ldrsb r0, [r4, #43]
    mov r6, #0
    mov r7, r6
    cmp r0, #0
    ble ov001_021f4fa4_Lbc
    ldr r8, =0x0223995c
    ldr r5, =0x022399b8
    mov r11, #1
ov001_021f4fa4_L78:
    ldrb r0, [r4, #0x10]
    ldrb r1, [r4, #0x29]
    mov r2, r10
    cmp r0, #0
    str r1, [sp]
    ldrb r1, [r8], #1
    moveq r3, r11
    movne r3, #0
    str r1, [sp, #0x4]
    ldr r1, [r5, r7, lsl #2]
    mov r0, r9
    bl native_fn_021e1864
    ldrsb r1, [r4, #43]
    add r7, r7, #1
    add r6, r6, r0
    cmp r7, r1
    blt ov001_021f4fa4_L78
ov001_021f4fa4_Lbc:
    mov r0, r6
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
