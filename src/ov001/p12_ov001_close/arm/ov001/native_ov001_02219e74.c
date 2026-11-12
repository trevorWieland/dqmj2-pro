/* ov001 row 0x02219e74: 92 bytes.
 *
 * What it does: 23 instructions; 3 call(s) to 0x02219ec8, 0x0207b004, 0x02219e90; loops (back edge at +0x28); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 3 calls (23 instructions, 3 calls, 1 branch, 2 back edges, 0 literal slots).
 *
 *   branch +0x14 -> +0x54
 *   branch +0x30 -> +0x54
 *   back edge +0x50 -> +0x1c
 *   test +0x10 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r6, r0
 *   test +0x4c cmp r6, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219e74; the literal pool and
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

extern void native_fn_0207b004(void);


asm u32 native_ov001_02219e74 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r5, [r0]
    mov r6, #0
    ldrb r0, [r5, #0x323]
    cmp r0, #0
    ble ov001_02219e74_L54
    mov r4, #128
ov001_02219e74_L1c:
    add r0, r5, r6
    ldrb r0, [r0, #0x35e]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    bne ov001_02219e74_L54
    ldrb r1, [r5, #0x323]
    sub r0, r1, #1
    cmp r6, r0
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r6, r6, #1
    cmp r6, r1
    blt ov001_02219e74_L1c
ov001_02219e74_L54:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
