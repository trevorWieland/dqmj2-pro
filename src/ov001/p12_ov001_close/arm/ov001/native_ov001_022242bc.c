/* ov001 row 0x022242bc: 148 bytes.
 *
 * What it does: 37 instructions; 7 call(s) to 0x02008e0c, 0x021dbd3c, 0x021dbd8c, +4 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 7 calls (37 instructions, 7 calls, 1 branch, 6 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x54
 *   back edge +0x60 -> +0x2c
 *   branch +0x74 -> +0x88
 *   test +0x30 cmp r0, #0
 *   test +0x4c cmp r0, r10, lsl #1
 *   test +0x58 cmp r5, #3
 *   test +0x70 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022242bc; the literal pool and
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
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_022242bc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r7, r1
    mov r6, r2
    add r1, sp, #0
    mov r2, #12
    mov r8, r0
    bl native_fn_02008e0c
    mov r5, #0
    mov r9, r5
    add r4, sp, #0
ov001_022242bc_L2c:
    ldr r0, [r4, r5, lsl #2]
    cmp r0, #0
    beq ov001_022242bc_L54
    mov r0, r7
    bl native_fn_021dbd3c
    mov r10, r0
    mov r0, r6
    bl native_fn_021dbd8c
    cmp r0, r10, lsl #1
    strge r9, [r4, r5, lsl #2]
ov001_022242bc_L54:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_022242bc_L2c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022242bc_L88
    add r0, sp, #0
    mov r1, r8
    mov r2, #12
    bl native_fn_02008e0c
ov001_022242bc_L88:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
