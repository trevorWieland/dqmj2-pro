/* ov001 row 0x021fcd14: 212 bytes.
 *
 * What it does: 50 instructions; 6 call(s) to 0x021db530, 0x0220269c, 0x021fd074, +3 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (50 instructions, 6 calls, 1 branch, 3 back edges, 3 literal slots).
 *
 *   pool +0xc8 -> native_data_0222edc4 (image word 0x0222edc4)
 *   pool +0xcc -> native_data_0222ed4c (image word 0x0222ed4c)
 *   pool +0xd0 -> constant 0x02239c10 (image word 0x02239c10)
 *   back edge +0xc0 -> +0x48
 *   test +0x28 cmp r8, #0
 *   test +0xb8 cmp r8, r0, asr #24
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fcd14; the literal pool and
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
extern void native_fn_0220269c(void);
extern u8 native_data_0222edc4[];
extern u8 native_data_0222ed4c[];
extern void native_fn_021fd074(void);
extern void native_fn_021fd098(void);
extern void native_fn_02204250(void);
extern void native_fn_0206cf44(void);


asm u32 native_ov001_021fcd14 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    bl native_fn_021db530
    mov r1, r0, lsl #24
    mov r0, r10
    mov r8, r1, asr #24
    bl native_fn_0220269c
    ldr r0, =native_data_0222edc4
    mov r7, #0
    ldrsb r0, [r0, r10]
    cmp r8, #0
    mov r0, r0, lsl #19
    mov r0, r0, asr #16
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r4, =native_data_0222ed4c
    ldr r11, =0x02239c10
    and r9, r10, #255
    and r5, r0, #255
ov001_021fcd14_L48:
    mov r0, r10
    mov r1, r7
    bl native_fn_021fd074
    mov r6, r0
    mov r0, r9
    and r1, r7, #255
    bl native_fn_021fd098
    bl native_fn_02204250
    strb r5, [r6, #0x4]
    mov r1, r0
    ldrsb r0, [r11, #6]
    add r0, r0, r0, lsl #1
    add r0, r4, r0
    ldrsb r0, [r7, r0]
    mov r0, r0, lsl #3
    strb r0, [r6, #0x5]
    and r2, r0, #255
    ldrsb r0, [r6, #12]
    ldrb r6, [r6, #0x4]
    ldrsh r3, [r1, #24]
    ldrsh r1, [r1, #26]
    add r3, r6, r3
    add r2, r2, r1
    and r1, r3, #255
    and r2, r2, #255
    bl native_fn_0206cf44
    add r0, r7, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    mov r7, r0, asr #24
    bgt ov001_021fcd14_L48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
