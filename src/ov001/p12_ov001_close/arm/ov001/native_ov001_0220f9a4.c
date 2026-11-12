/* ov001 row 0x0220f9a4: 200 bytes.
 *
 * What it does: 50 instructions; 10 call(s) to 0x0207b674, 0x0220f9e4, 0x0203d294, +7 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 10 calls (50 instructions, 10 calls, 4 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x40
 *   branch +0x2c -> +0x40
 *   branch +0x50 -> +0x74
 *   branch +0x60 -> +0x74
 *   branch +0x84 -> +0xc0
 *   branch +0x9c -> +0xc0
 *   branch +0xac -> +0xc0
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #1
 *   test +0x4c cmp r0, #0
 *   test +0x5c cmp r0, #5
 *   test +0x80 cmp r0, #0
 *   test +0x98 cmp r0, #1
 *   test +0xa8 cmp r0, #2
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220f9a4; the literal pool and
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

extern void native_fn_0207b674(void);
extern void native_fn_0203d294(void);
extern void native_fn_02044414(void);


asm u32 native_ov001_0220f9a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r1, r5
    mov r0, #39
    mov r4, r2
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220f9a4_L40
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0220f9a4_L40
    mov r0, #39
    strb r0, [r4]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_0220f9a4_L40:
    mov r1, r5
    mov r0, #74
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220f9a4_L74
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0220f9a4_L74
    mov r0, #74
    strb r0, [r4]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_0220f9a4_L74:
    mov r1, r5
    mov r0, #75
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220f9a4_Lc0
    bl native_fn_02044414
    mov r1, r0, lsr #31
    rsb r0, r1, r0, lsl #31
    add r0, r1, r0, ror #31
    cmp r0, #1
    bne ov001_0220f9a4_Lc0
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #2
    bge ov001_0220f9a4_Lc0
    mov r0, #75
    strb r0, [r4]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_0220f9a4_Lc0:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
