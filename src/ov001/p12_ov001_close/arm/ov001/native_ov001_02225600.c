/* ov001 row 0x02225600: 168 bytes.
 *
 * What it does: 42 instructions; 5 call(s) to 0x02008e0c, 0x02225630, 0x02223f20, +2 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 5 calls (42 instructions, 5 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x68
 *   branch +0x4c -> +0x60
 *   back edge +0x74 -> +0x30
 *   branch +0x88 -> +0x9c
 *   test +0x34 cmp r1, #0
 *   test +0x40 cmp r4, #0
 *   test +0x58 cmp lr, r1
 *   test +0x60 cmp lr, #5
 *   test +0x6c cmp r12, #3
 *   test +0x84 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225600; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02225600 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r6, r1
    mov r5, r2
    add r1, sp, #0
    mov r2, #12
    mov r7, r0
    mov r4, r3
    bl native_fn_02008e0c
    mov r12, #0
    mov r0, r12
    add r3, sp, #0
ov001_02225600_L30:
    ldr r1, [r3, r12, lsl #2]
    cmp r1, #0
    beq ov001_02225600_L68
    ldr r2, [r6, #0x1e8]
    cmp r4, #0
    add r1, r5, r2
    ldrb lr, [r1, #0x86]
    beq ov001_02225600_L60
    add r1, r4, r2
    ldrb r1, [r1, #0x86]
    cmp lr, r1
    movge lr, r1
ov001_02225600_L60:
    cmp lr, #5
    strge r0, [r3, r12, lsl #2]
ov001_02225600_L68:
    add r12, r12, #1
    cmp r12, #3
    add r6, r6, #1088
    blt ov001_02225600_L30
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225600_L9c
    add r0, sp, #0
    mov r1, r7
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225600_L9c:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
