/* ov001 row 0x021fcde8: 204 bytes.
 *
 * What it does: 48 instructions; 6 call(s) to 0x021db530, 0x02202720, 0x021db438, +3 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (48 instructions, 6 calls, 2 branches, 5 back edges, 3 literal slots).
 *
 *   pool +0xc0 -> native_data_0222edc4 (image word 0x0222edc4)
 *   pool +0xc4 -> native_data_0222ed4c (image word 0x0222ed4c)
 *   pool +0xc8 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x5c -> +0xa8
 *   back edge +0xb8 -> +0x48
 *   test +0x2c cmp r5, #0
 *   test +0x58 cmp r0, #0
 *   test +0xb0 cmp r5, r0, asr #24
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fcde8; the literal pool and
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

extern void native_fn_021db530(void);
extern void native_fn_02202720(void);
extern u8 native_data_0222edc4[];
extern u8 native_data_0222ed4c[];
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021fd074(void);
extern void native_fn_0206cf44(void);


asm u32 native_ov001_021fcde8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r7, r0
    bl native_fn_021db530
    mov r1, r0, lsl #24
    mov r0, r7
    mov r5, r1, asr #24
    mov r6, #0
    bl native_fn_02202720
    ldr r0, =native_data_0222edc4
    mov r4, r6
    ldrsb r0, [r0, r7]
    cmp r5, #0
    mov r0, r0, lsl #19
    mov r0, r0, asr #16
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    ldr r9, =native_data_0222ed4c
    ldr r8, =0x02239c10
    and r10, r0, #255
ov001_021fcde8_L48:
    mov r0, r7
    mov r1, r4
    bl native_fn_021db438
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021fcde8_La8
    mov r0, r7
    mov r1, r4
    bl native_fn_021fd074
    mov r1, r0
    strb r10, [r1, #0x4]
    ldrsb r0, [r8, #6]
    add r0, r0, r0, lsl #1
    add r0, r9, r0
    ldrsb r0, [r6, r0]
    mov r2, r0, lsl #3
    strb r2, [r1, #0x5]
    ldrsb r0, [r1, #12]
    ldrb r1, [r1, #0x4]
    and r2, r2, #255
    bl native_fn_0206cf44
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
ov001_021fcde8_La8:
    add r0, r4, #1
    mov r0, r0, lsl #24
    cmp r5, r0, asr #24
    mov r4, r0, asr #24
    bgt ov001_021fcde8_L48
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
