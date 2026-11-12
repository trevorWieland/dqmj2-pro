/* ov001 row 0x022064c0: 144 bytes.
 *
 * What it does: 36 instructions; 3 call(s) to 0x02213698, 0x02206520, 0x02206550; no back edge; returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: branched body (36 instructions, 3 calls, 1 branch, 0 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x60
 *   branch +0x5c -> +0x74
 *   test +0x20 cmp r5, r1
 *   test +0x34 cmp r1, r12
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022064c0; the literal pool and
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

extern void native_fn_02213698(void);
extern void native_fn_02206550(void);


asm u32 native_ov001_022064c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldr r0, [r6, #0x28]
    mov r5, r1
    mov r4, #0
    bl native_fn_02213698
    ldr r1, [r6, #0x34]
    ldr r3, [r6, #0x30]
    cmp r5, r1
    movgt r5, r1
    ldr r1, [r6, #0x38]
    ldr r12, [r0, r1, lsl #2]
    add r1, r5, r3
    cmp r1, r12
    blt ov001_022064c0_L60
    ldr r2, [r6, #0x34]
    sub r1, r12, r3
    sub r1, r2, r1
    str r1, [r6, #0x34]
    ldr r1, [r6, #0x38]
    mov r4, #1
    ldr r0, [r0, r1, lsl #2]
    str r0, [r6, #0x30]
    b ov001_022064c0_L74
ov001_022064c0_L60:
    add r0, r3, r5
    str r0, [r6, #0x30]
    ldr r0, [r6, #0x34]
    sub r0, r0, r5
    str r0, [r6, #0x34]
ov001_022064c0_L74:
    ldr r1, [r6, #0x30]
    ldr r2, [r6, #0x38]
    mov r0, r6
    mov r3, #1
    bl native_fn_02206550
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
