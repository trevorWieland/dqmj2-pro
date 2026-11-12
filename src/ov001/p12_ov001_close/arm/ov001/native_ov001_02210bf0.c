/* ov001 row 0x02210bf0: 132 bytes.
 *
 * What it does: 30 instructions; 1 call(s) to 0x02008d78; loops (back edge at +0x10); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (30 instructions, 1 call, 3 branches, 1 back edge, 3 literal slots).
 *
 *   pool +0x78 -> native_data_0223e118 (image word 0x0223e118)
 *   pool +0x7c -> constant 0x04000048 (image word 0x04000048)
 *   pool +0x80 -> native_data2_0223e118 (image word 0x0223e118)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02210bf0; the literal pool and
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

extern u8 native_data_0223e118[];
extern void native_fn_02008d78(void);
extern u8 native_data2_0223e118[];


asm u32 native_ov001_02210bf0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_0223e118
    mov r1, #0
    mov r2, #2
    bl native_fn_02008d78
    ldr lr, =0x04000048
    mov r3, #255
    ldrh r0, [lr]
    mov r1, #192
    mov r2, #67108864
    bic r0, r0, #63
    orr r0, r0, #63
    strh r0, [lr]
    ldrh r12, [lr, #2]
    ldr r0, =native_data2_0223e118
    bic r12, r12, #63
    orr r12, r12, #62
    strh r12, [lr, #2]
    strh r3, [lr, #-8]
    strh r1, [lr, #-4]
    ldr r1, [r2]
    and r1, r1, #57344
    mov r3, r1, lsr #13
    str r3, [r0, #0x4]
    ldr r1, [r2]
    orr r0, r3, #1
    bic r1, r1, #57344
    orr r0, r1, r0, lsl #13
    str r0, [r2]
    ldmia sp!, {r3, pc}
}
