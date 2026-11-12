/* ov001 row 0x02202720: 160 bytes.
 *
 * What it does: 38 instructions; 7 call(s) to 0x021db530, 0x022027a4, 0x021db438, +4 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (38 instructions, 7 calls, 2 branches, 7 back edges, 2 literal slots).
 *
 *   pool +0x98 -> native_data_0222e044 (image word 0x0222e044)
 *   pool +0x9c -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x3c -> +0x84
 *   branch +0x54 -> +0x70
 *   back edge +0x80 -> +0x40
 *   test +0x2c cmp r4, #0
 *   test +0x50 cmp r0, #0
 *   test +0x78 cmp r4, r0, asr #24
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202720; the literal pool and
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
extern u8 native_data_0222e044[];
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021fd074(void);
extern void native_fn_0206d250(void);
extern void native_fn_021fcaf8(void);


asm u32 native_ov001_02202720 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r5, r0
    bl ov001_mode_byte_021db530
    ldr r1, =native_data_0222e044
    mov r0, r0, lsl #24
    ldrb r3, [r1]
    ldrb r2, [r1, #0x1]
    mov r4, r0, asr #24
    strb r3, [sp]
    strb r2, [sp, #0x1]
    ldrb r0, [r1, #0x2]
    cmp r4, #0
    add r7, sp, #0
    strb r0, [sp, #0x2]
    mov r6, #0
    ble ov001_02202720_L84
ov001_02202720_L40:
    mov r0, r5
    mov r1, r6
    bl ov001_side_slot_record_021db438
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02202720_L70
    mov r0, r5
    mov r1, r6
    bl native_fn_021fd074
    ldrsb r0, [r0, #12]
    bl native_fn_0206d250
    strb r0, [r7], #1
ov001_02202720_L70:
    add r0, r6, #1
    mov r0, r0, lsl #24
    cmp r4, r0, asr #24
    mov r6, r0, asr #24
    bgt ov001_02202720_L40
ov001_02202720_L84:
    add r0, sp, #0
    bl native_fn_021fcaf8
    ldr r1, =0x02239c10
    strb r0, [r1, #0x6]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
