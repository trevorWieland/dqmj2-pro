/* ov001 row 0x021fd0bc: 80 bytes.
 *
 * What it does: 20 instructions; 2 call(s) to 0x0207afec, 0x0207afec; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 2 calls (20 instructions, 2 calls, 2 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x44
 *   branch +0x40 -> +0x48
 *   test +0x1c cmp r0, #2
 *   test +0x20 cmpne r0, #3
 *   test +0x3c cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd0bc; the literal pool and
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


asm u32 native_ov001_021fd0bc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r4, #0
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #2
    cmpne r0, #3
    beq ov001_021fd0bc_L44
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #2
    bne ov001_021fd0bc_L48
ov001_021fd0bc_L44:
    mov r4, #1
ov001_021fd0bc_L48:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
