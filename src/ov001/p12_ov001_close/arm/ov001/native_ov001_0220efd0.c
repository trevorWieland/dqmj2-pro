/* ov001 row 0x0220efd0: 200 bytes.
 *
 * What it does: 50 instructions; 3 call(s) to 0x02210ad0, 0x021dbcbc, 0x02210ad0; loops (back edge at +0x68); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 3 calls (50 instructions, 3 calls, 6 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0xa4
 *   branch +0x2c -> +0x50
 *   branch +0x60 -> +0xa0
 *   branch +0x7c -> +0xa0
 *   branch +0xa8 -> +0xc0
 *   back edge +0xbc -> +0x28
 *   test +0x28 cmp r0, #5
 *   test +0x44 cmp r0, #0
 *   test +0x5c cmp r0, #23
 *   test +0x78 cmp r2, r0, asr #2
 *   test +0x94 cmp r0, #0
 *   test +0xa4 cmp r7, #64
 *   test +0xb8 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220efd0; the literal pool and
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

extern void native_fn_02210ad0(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0220efd0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r7, #0
    mov r9, r2
    mov r8, r3
    add r4, r10, #256
    mov r6, #256
    mov r11, r7
    mov r5, #1
    b ov001_0220efd0_La4
ov001_0220efd0_L28:
    cmp r0, #5
    bne ov001_0220efd0_L50
    mov r9, r9, lsl #1
    mov r0, r10
    mov r1, r6
    mov r2, r9
    bl native_fn_02210ad0
    cmp r0, #0
    movne r8, r5
    moveq r8, r11
ov001_0220efd0_L50:
    ldr r0, [r10, #0x1e8]
    add r0, r0, r7
    ldrb r0, [r0, #0x46]
    cmp r0, #23
    bne ov001_0220efd0_La0
    mov r0, r10
    bl native_fn_021dbcbc
    mov r1, r0, asr #1
    ldrsh r2, [r4, #240]
    add r0, r0, r1, lsr #30
    cmp r2, r0, asr #2
    bgt ov001_0220efd0_La0
    mov r9, r9, lsl #4
    mov r0, r10
    mov r1, #256
    mov r2, r9
    bl native_fn_02210ad0
    cmp r0, #0
    movne r8, #1
    moveq r8, #0
ov001_0220efd0_La0:
    add r7, r7, #1
ov001_0220efd0_La4:
    cmp r7, #64
    bge ov001_0220efd0_Lc0
    ldr r0, [r10, #0x1e8]
    add r0, r0, r7
    ldrb r0, [r0, #0x46]
    cmp r0, #0
    bne ov001_0220efd0_L28
ov001_0220efd0_Lc0:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
