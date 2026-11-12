/* ov001 row 0x02218fc0: 88 bytes.
 *
 * What it does: 22 instructions; 2 call(s) to 0x021dbec8, 0x0203d294; loops (back edge at +0x0c); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 2 calls (22 instructions, 2 calls, 3 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0x50
 *   branch +0x34 -> +0x48
 *   branch +0x44 -> +0x50
 *   test +0x18 cmp r2, #0
 *   test +0x20 cmpeq r2, #0
 *   test +0x28 cmpeq r1, #0
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r0, #9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02218fc0; the literal pool and
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

extern void native_fn_021dbec8(void);
extern void native_fn_0203d294(void);


asm u32 native_ov001_02218fc0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, [r0]
    mov r0, r4
    bl native_fn_021dbec8
    add r1, r4, #512
    ldrsb r2, [r1, #63]
    cmp r2, #0
    ldreqsb r2, [r1, #65]
    cmpeq r2, #0
    ldreqsb r1, [r1, #64]
    cmpeq r1, #0
    beq ov001_02218fc0_L50
    cmp r0, #0
    bne ov001_02218fc0_L48
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #9
    bge ov001_02218fc0_L50
ov001_02218fc0_L48:
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_02218fc0_L50:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
