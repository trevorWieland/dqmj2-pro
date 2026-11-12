/* ov001 row 0x02213408: 120 bytes.
 *
 * What it does: 29 instructions; 1 call(s) to 0x0202a634; loops (back edge at +0x08); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (29 instructions, 3 calls, 2 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x74 -> native_data_0222f16c (image word 0x0222f16c)
 *   branch +0x1c -> +0x44
 *   branch +0x2c -> +0x44
 *   test +0x18 cmp r1, #0
 *   test +0x28 cmp r0, #0
 *   test +0x4c cmp r1, #1
 *   test +0x54 cmpne r1, #0
 *   test +0x5c cmp r2, #0
 *   test +0x68 cmp r1, #1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213408; the literal pool and
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

extern void native_fn_0202a634(void);
extern u8 native_data_0222f16c[];


asm u32 native_ov001_02213408 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_0202a634
    ldr r1, [r4, #0x2c]
    ldr r0, =native_data_0222f16c
    ldr r1, [r0, r1, lsl #2]
    cmp r1, #0
    beq ov001_02213408_L44
    mov r0, r4
    blx r1
    cmp r0, #0
    beq ov001_02213408_L44
    ldr r2, [r4, #0x2c]
    ldr r1, =native_data_0222f16c
    mov r0, r4
    ldr r1, [r1, r2, lsl #2]
    blx r1
ov001_02213408_L44:
    ldr r1, [r4, #0x2c]
    mov r0, #0
    cmp r1, #1
    mov r2, #1
    cmpne r1, #0
    movne r2, r0
    cmp r2, #0
    ldmeqia sp!, {r4, pc}
    ldr r1, [r4, #0x44]
    cmp r1, #1
    moveq r0, #1
    ldmia sp!, {r4, pc}
}
