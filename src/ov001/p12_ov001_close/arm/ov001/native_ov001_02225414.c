/* ov001 row 0x02225414: 144 bytes.
 *
 * What it does: 36 instructions; 5 call(s) to 0x02008e0c, 0x02225448, 0x02223f20, +2 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 5 calls (36 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x50
 *   back edge +0x5c -> +0x34
 *   branch +0x70 -> +0x84
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r0, r4
 *   test +0x54 cmp r3, #3
 *   test +0x6c cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225414; the literal pool and
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
extern void native_fn_02223f20(void);


asm u32 native_ov001_02225414 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r7, r1
    mov r6, r2
    add r1, sp, #0
    mov r2, #12
    mov r5, r0
    mov r4, r3
    bl native_fn_02008e0c
    mov r3, #0
    add r12, r7, r6
    mov r1, r3
    add r2, sp, #0
ov001_02225414_L34:
    ldr r0, [r2, r3, lsl #2]
    cmp r0, #0
    beq ov001_02225414_L50
    add r0, r12, #512
    ldrsb r0, [r0, #44]
    cmp r0, r4
    strge r1, [r2, r3, lsl #2]
ov001_02225414_L50:
    add r3, r3, #1
    cmp r3, #3
    add r12, r12, #1088
    blt ov001_02225414_L34
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225414_L84
    add r0, sp, #0
    mov r1, r5
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225414_L84:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
