/* ov001 row 0x02220484: 84 bytes.
 *
 * What it does: 21 instructions; 4 call(s) to 0x021e29e8, 0x02220430, 0x02218924, +1 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 4 calls (21 instructions, 4 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x14 -> +0x4c
 *   test +0x10 tst r0, #4
 *   test +0x20 cmp r0, #0
 *   test +0x40 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02220484; the literal pool and
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

extern void native_fn_021e29e8(void);
extern void native_fn_02220430(void);
extern void native_fn_02218924(void);


asm u32 native_ov001_02220484 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldr r5, [r4, #0x8]
    bl native_fn_021e29e8
    tst r0, #4
    beq ov001_02220484_L4c
    mov r0, r4
    bl native_fn_02220430
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
    ldr r0, [r4, #0x4]
    bl native_fn_02218924
    mov r4, r0
    mov r0, r5
    bl native_fn_02218924
    cmp r4, r0
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, pc}
ov001_02220484_L4c:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
