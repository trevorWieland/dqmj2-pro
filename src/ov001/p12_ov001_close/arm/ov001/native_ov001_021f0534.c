/* ov001 row 0x021f0534: 56 bytes.
 *
 * What it does: 13 instructions; 2 call(s) to 0x0207afec, 0x021f0554; loops (back edge at +0x0c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (13 instructions, 2 calls, 1 branch, 1 back edge, 1 literal slot).
 *
 *   pool +0x34 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x18 -> +0x20
 *   branch +0x1c -> +0x24
 *   test +0x14 cmp r0, #0
 *   test +0x24 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f0534; the literal pool and
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

extern void native_fn_0207afec(void);


asm u32 native_ov001_021f0534 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    mov r0, r1
    bl native_fn_0207afec
    ldrsh r0, [r0, #28]
    cmp r0, #0
    ble ov001_021f0534_L20
    b ov001_021f0534_L24
ov001_021f0534_L20:
    ldr r0, =0x0000270f
ov001_021f0534_L24:
    cmp r4, r0
    movge r4, r0
    mov r0, r4
    ldmia sp!, {r4, pc}
}
