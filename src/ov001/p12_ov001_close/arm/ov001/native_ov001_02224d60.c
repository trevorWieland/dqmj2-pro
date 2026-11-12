/* ov001 row 0x02224d60: 224 bytes.
 *
 * What it does: 56 instructions; 10 call(s) to 0x02008e0c, 0x021dbcf0, 0x021dbd30, +7 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 10 calls (56 instructions, 10 calls, 2 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x58
 *   back edge +0x64 -> +0x2c
 *   branch +0x7c -> +0xa0
 *   back edge +0xac -> +0x74
 *   branch +0xc0 -> +0xd4
 *   test +0x30 cmp r0, #0
 *   test +0x50 cmp r0, r8
 *   test +0x5c cmp r7, #3
 *   test +0x78 cmp r0, #0
 *   test +0x98 cmp r0, r8
 *   test +0xa4 cmp r7, #3
 *   test +0xbc cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224d60; the literal pool and
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
extern void native_fn_021dbcf0(void);
extern void native_fn_021dbd30(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02224d60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r4, r1
    add r1, sp, #0
    mov r2, #12
    mov r5, r0
    mov r8, #0
    bl native_fn_02008e0c
    mov r9, r4
    mov r7, r8
    add r6, sp, #0
ov001_02224d60_L2c:
    ldr r0, [r6, r7, lsl #2]
    cmp r0, #0
    beq ov001_02224d60_L58
    mov r0, r9
    bl native_fn_021dbcf0
    mov r10, r0
    mov r0, r9
    bl native_fn_021dbd30
    sub r0, r10, r0
    cmp r0, r8
    movgt r8, r0
ov001_02224d60_L58:
    add r7, r7, #1
    cmp r7, #3
    add r9, r9, #1088
    blt ov001_02224d60_L2c
    mov r7, #0
    mov r9, r7
    add r6, sp, #0
ov001_02224d60_L74:
    ldr r0, [r6, r7, lsl #2]
    cmp r0, #0
    beq ov001_02224d60_La0
    mov r0, r4
    bl native_fn_021dbcf0
    mov r10, r0
    mov r0, r4
    bl native_fn_021dbd30
    sub r0, r10, r0
    cmp r0, r8
    strlt r9, [r6, r7, lsl #2]
ov001_02224d60_La0:
    add r7, r7, #1
    cmp r7, #3
    add r4, r4, #1088
    blt ov001_02224d60_L74
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224d60_Ld4
    add r0, sp, #0
    mov r1, r5
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224d60_Ld4:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
