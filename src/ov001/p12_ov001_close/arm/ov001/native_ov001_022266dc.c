/* ov001 row 0x022266dc: 136 bytes.
 *
 * What it does: 34 instructions; 5 call(s) to 0x02008e0c, 0x02226708, 0x02223f20, +2 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (34 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x48
 *   back edge +0x54 -> +0x2c
 *   branch +0x68 -> +0x7c
 *   test +0x30 cmp r1, #0
 *   test +0x40 cmp r2, r1
 *   test +0x4c cmp r12, #3
 *   test +0x64 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022266dc; the literal pool and
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


asm u32 native_ov001_022266dc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    mov r5, r1
    mov r4, r2
    add r1, sp, #0
    mov r2, #12
    mov r6, r0
    bl native_fn_02008e0c
    mov r12, #0
    mov r0, r12
    add r3, sp, #0
ov001_022266dc_L2c:
    ldr r1, [r3, r12, lsl #2]
    cmp r1, #0
    beq ov001_022266dc_L48
    ldrb r2, [r5, #0x31f]
    ldrb r1, [r4, #0x31f]
    cmp r2, r1
    streq r0, [r3, r12, lsl #2]
ov001_022266dc_L48:
    add r12, r12, #1
    cmp r12, #3
    add r4, r4, #1088
    blt ov001_022266dc_L2c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022266dc_L7c
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_022266dc_L7c:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
