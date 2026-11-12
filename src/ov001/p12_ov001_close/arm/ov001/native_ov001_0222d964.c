/* ov001 row 0x0222d964: 68 bytes.
 *
 * What it does: 17 instructions; 3 call(s) to 0x02025a28, 0x02025ab8, 0x020259b4; loops (back edge at +0x30); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 3 calls (17 instructions, 3 calls, 4 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x08 -> +0x20
 *   branch +0x10 -> +0x28
 *   branch +0x1c -> +0x2c
 *   branch +0x24 -> +0x2c
 *   test +0x04 cmp r0, #0
 *   test +0x0c cmp r0, #1
 *   test +0x14 cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222d964; the literal pool and
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

extern void native_fn_02025a28(void);
extern void native_fn_02025ab8(void);
extern void native_fn_020259b4(void);


asm u32 native_ov001_0222d964 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    cmp r0, #0
    beq ov001_0222d964_L20
    cmp r0, #1
    beq ov001_0222d964_L28
    cmp r0, #2
    moveq r4, #1073741824
    b ov001_0222d964_L2c
ov001_0222d964_L20:
    mov r4, #1065353216
    b ov001_0222d964_L2c
ov001_0222d964_L28:
    mov r4, #1069547520
ov001_0222d964_L2c:
    mov r0, r1
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    ldmia sp!, {r4, pc}
}
