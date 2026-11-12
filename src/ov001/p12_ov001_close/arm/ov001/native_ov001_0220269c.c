/* ov001 row 0x0220269c: 132 bytes.
 *
 * What it does: 31 instructions; 5 call(s) to 0x021db530, 0x02202704, 0x021fd074, +2 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (31 instructions, 5 calls, 1 branch, 5 back edges, 2 literal slots).
 *
 *   pool +0x7c -> native_data_0222e044 (image word 0x0222e044)
 *   pool +0x80 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x34 -> +0x68
 *   back edge +0x64 -> +0x3c
 *   test +0x2c cmp r6, #0
 *   test +0x58 cmp r6, r1, asr #24
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220269c; the literal pool and
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

extern u8 native_data_0222e044[];
extern void native_fn_021db530(void);
extern void native_fn_021fd074(void);
extern void native_fn_0206d250(void);
extern void native_fn_021fcaf8(void);


asm u32 native_ov001_0220269c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r1, =native_data_0222e044
    mov r4, r0
    ldrb r3, [r1, #0x3]
    ldrb r2, [r1, #0x4]
    strb r3, [sp]
    strb r2, [sp, #0x1]
    ldrb r1, [r1, #0x5]
    strb r1, [sp, #0x2]
    bl native_fn_021db530
    mov r6, r0
    cmp r6, #0
    mov r5, #0
    ble ov001_0220269c_L68
    add r7, sp, #0
ov001_0220269c_L3c:
    mov r0, r4
    mov r1, r5
    bl native_fn_021fd074
    ldrsb r0, [r0, #12]
    bl native_fn_0206d250
    add r1, r5, #1
    mov r1, r1, lsl #24
    cmp r6, r1, asr #24
    strb r0, [r7], #1
    mov r5, r1, asr #24
    bgt ov001_0220269c_L3c
ov001_0220269c_L68:
    add r0, sp, #0
    bl native_fn_021fcaf8
    ldr r1, =0x02239c10
    strb r0, [r1, #0x6]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
