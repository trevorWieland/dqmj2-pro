/* ov001 row 0x021fc9a4: 340 bytes.
 *
 * What it does: 82 instructions; 10 call(s) to 0x021db530, 0x021fcadc, 0x021fd074, +7 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (82 instructions, 10 calls, 2 branches, 6 back edges, 3 literal slots).
 *
 *   pool +0x148 -> constant 0x02239c9c (image word 0x02239c9c)
 *   pool +0x14c -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x150 -> constant 0x02239d6c (image word 0x02239d6c)
 *   branch +0x2c -> +0x138
 *   branch +0x10c -> +0x120
 *   back edge +0x134 -> +0x40
 *   test +0x10 cmp r10, #0
 *   test +0x20 cmp r7, #0
 *   test +0x40 cmp r10, #0
 *   test +0x108 cmp r0, #0
 *   test +0x12c cmp r7, r0, asr #24
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fc9a4; the literal pool and
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

extern void ov001_mode_byte_021db530(void);
extern void native_fn_021fd074(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_0206c88c(void);
extern void native_fn_0206ccb4(void);
extern void native_fn_02204aa0(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_022025a4(void);
extern void native_fn_021fcd14(void);


asm u32 native_ov001_021fc9a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    bl ov001_mode_byte_021db530
    mov r0, r0, lsl #24
    cmp r10, #0
    mov r7, r0, asr #24
    moveq r0, #0
    movne r0, #3
    cmp r7, #0
    mov r0, r0, lsl #24
    mov r6, #0
    ble ov001_021fc9a4_L138
    ldr r1, =0x02239c9c
    add r8, r1, r0, asr #24
    mov r0, r10, lsl #24
    mov r11, r0, asr #24
ov001_021fc9a4_L40:
    cmp r10, #0
    moveq r9, #6
    mov r0, r11
    mov r1, r6
    movne r9, #127
    bl native_fn_021fd074
    mov r5, r0
    mov r0, r10
    mov r1, r6
    bl ov001_side_slot_record_021db438
    mov r4, r0
    ldr r0, [r4, #0x1e8]
    mov r2, #1
    ldrsh r0, [r0, #42]
    mov r3, #32
    str r0, [r5]
    mov r0, #0
    strb r0, [r5, #0x6]
    strb r0, [r5, #0x7]
    strb r6, [r5, #0x8]
    mov r0, r2
    strb r0, [r5, #0x9]
    mov r0, #2
    str r0, [sp]
    ldr r1, [r4, #0x1e8]
    ldr r0, [r5]
    ldrb r1, [r1, #0x2c]
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_0206c88c
    strb r0, [r5, #0xc]
    and r1, r9, #255
    str r1, [sp]
    ldr r0, =0x02239c10
    ldrsb r1, [r5, #12]
    ldr r0, [r0, #0x24]
    mov r2, #3
    mov r3, #8
    bl native_fn_0206ccb4
    ldr r1, =0x02239d6c
    mov r0, r5
    ldrsb r2, [r1, #112]
    mov r1, r10
    add r3, r2, #1
    ldr r2, =0x02239d6c
    strb r3, [r2, #0x70]
    bl native_fn_02204aa0
    strb r0, [r8]
    mov r0, r4
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    bne ov001_021fc9a4_L120
    mov r0, r10
    mov r1, r6
    mov r2, #0
    bl native_fn_022025a4
ov001_021fc9a4_L120:
    add r8, r8, #1
    add r0, r6, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    mov r6, r0, asr #24
    bgt ov001_021fc9a4_L40
ov001_021fc9a4_L138:
    mov r0, r10, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021fcd14
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
