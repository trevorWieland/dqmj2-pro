/* ov001 row 0x02224ed0: 132 bytes.
 *
 * What it does: 33 instructions; 6 call(s) to 0x02008e0c, 0x021dbd30, 0x02224ef8, +3 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 6 calls (33 instructions, 6 calls, 1 branch, 5 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x44
 *   back edge +0x50 -> +0x28
 *   branch +0x64 -> +0x78
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x48 cmp r6, #3
 *   test +0x60 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224ed0; the literal pool and
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
extern void native_fn_021dbd30(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02224ed0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #12
    mov r7, r1
    add r1, sp, #0
    mov r2, #12
    mov r8, r0
    bl native_fn_02008e0c
    mov r6, #0
    mov r4, r6
    add r5, sp, #0
ov001_02224ed0_L28:
    ldr r0, [r5, r6, lsl #2]
    cmp r0, #0
    beq ov001_02224ed0_L44
    mov r0, r7
    bl native_fn_021dbd30
    cmp r0, #0
    streq r4, [r5, r6, lsl #2]
ov001_02224ed0_L44:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02224ed0_L28
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224ed0_L78
    add r0, sp, #0
    mov r1, r8
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224ed0_L78:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
