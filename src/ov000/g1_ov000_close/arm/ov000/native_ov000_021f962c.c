/* ov000 row 0x021f962c: 124 bytes.
 *
 * What it does: 31 instructions; 4 call(s) to 0x02215698, 0x021f96a0, 0x0206d250, +1 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x28 -> +0x74
 *   branch +0x4c -> +0x74
 *   back edge +0x70 -> +0x2c
 *   test +0x24 cmp r0, #0
 *   test +0x40 cmp r9, r0, asr #24
 *   test +0x64 cmp r2, r1, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f962c; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_0206d250(void);


asm u32 native_ov000_021f962c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r9, r0
    bl ov000_display_context_02215698
    mov r7, #0
    mov r5, r0
    add r4, r5, #1024
    ldrsb r0, [r4, #149]
    mov r8, r7
    mov r6, r7
    cmp r0, #0
    ble ov000_021f962c_L74
ov000_021f962c_L2c:
    add r0, r5, r6, lsl #3
    ldrsb r0, [r0, #166]
    bl native_fn_0206d250
    add r0, r8, r0
    mov r0, r0, lsl #24
    cmp r9, r0, asr #24
    mov r0, r0, asr #24
    movle r7, r6
    ble ov000_021f962c_L74
    ldrsb r2, [r4, #149]
    add r3, r0, #1
    add r0, r6, #1
    mov r1, r0, lsl #24
    mov r0, r3, lsl #24
    cmp r2, r1, asr #24
    mov r8, r0, asr #24
    mov r6, r1, asr #24
    bgt ov000_021f962c_L2c
ov000_021f962c_L74:
    mov r0, r7
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
