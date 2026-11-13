/* ov001 row 0x0222602c: 144 bytes.
 *
 * What it does: 36 instructions; 6 call(s) to 0x02008e0c, 0x021e81d0, 0x02226058, +3 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 6 calls (36 instructions, 6 calls, 1 branch, 5 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x50
 *   back edge +0x5c -> +0x2c
 *   branch +0x70 -> +0x84
 *   test +0x30 cmp r0, #0
 *   test +0x48 cmp r0, r6
 *   test +0x54 cmp r5, #3
 *   test +0x6c cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222602c; the literal pool and
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
extern void native_fn_021e81d0(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_0222602c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
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
ov001_0222602c_L2c:
    ldr r0, [r4, r5, lsl #2]
    cmp r0, #0
    beq ov001_0222602c_L50
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    bl native_fn_021e81d0
    ldrh r0, [r0]
    cmp r0, r6
    streq r9, [r4, r5, lsl #2]
ov001_0222602c_L50:
    add r5, r5, #1
    cmp r5, #3
    add r7, r7, #1088
    blt ov001_0222602c_L2c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_0222602c_L84
    add r0, sp, #0
    mov r1, r8
    mov r2, #12
    bl native_fn_02008e0c
ov001_0222602c_L84:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
