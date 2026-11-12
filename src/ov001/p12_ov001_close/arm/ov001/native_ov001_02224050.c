/* ov001 row 0x02224050: 84 bytes.
 *
 * What it does: 21 instructions; 4 call(s) to 0x02223f20, 0x02224080, 0x0203d294, +1 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 4 calls (21 instructions, 4 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x10 -> +0x30
 *   back edge +0x28 -> +0x18
 *   branch +0x2c -> +0x34
 *   back edge +0x4c -> +0x3c
 *   test +0x0c cmp r0, #0
 *   test +0x24 cmp r1, #0
 *   test +0x3c cmp r0, r2
 *   test +0x48 cmp r2, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224050; the literal pool and
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

extern void native_fn_02223f20(void);
extern void native_fn_0203d294(void);


asm u32 native_ov001_02224050 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_02223f20
    cmp r0, #0
    ble ov001_02224050_L30
    mov r4, #3
ov001_02224050_L18:
    mov r0, r4
    bl native_fn_0203d294
    ldr r1, [r5, r0, lsl #2]
    cmp r1, #0
    beq ov001_02224050_L18
    b ov001_02224050_L34
ov001_02224050_L30:
    mov r0, #0
ov001_02224050_L34:
    mov r2, #0
    mov r1, r2
ov001_02224050_L3c:
    cmp r0, r2
    strne r1, [r5, r2, lsl #2]
    add r2, r2, #1
    cmp r2, #3
    blt ov001_02224050_L3c
    ldmia sp!, {r3, r4, r5, pc}
}
