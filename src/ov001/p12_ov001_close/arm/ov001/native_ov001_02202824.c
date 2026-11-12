/* ov001 row 0x02202824: 164 bytes.
 *
 * What it does: 40 instructions; 6 call(s) to 0x021db530, 0x022028bc, 0x021db438, +3 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (40 instructions, 6 calls, 3 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0xa0 -> native_data_0222edc8 (image word 0x0222edc8)
 *   branch +0x28 -> +0x98
 *   branch +0x4c -> +0x80
 *   branch +0x5c -> +0x80
 *   back edge +0x94 -> +0x34
 *   test +0x1c cmp r6, #0
 *   test +0x48 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x74 cmp r0, #127
 *   test +0x88 cmp r6, r0, asr #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202824; the literal pool and
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
extern u8 native_data_0222edc8[];
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dc108(void);
extern void native_fn_0220459c(void);


asm u32 native_ov001_02202824 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r4, r0
    mov r0, #0
    mov r5, #16
    bl ov001_mode_byte_021db530
    mov r6, r0
    mov r0, #2
    cmp r6, #0
    orr r5, r5, r0, lsl r4
    mov r9, #0
    ble ov001_02202824_L98
    ldr r7, =native_data_0222edc8
    mov r4, r9
ov001_02202824_L34:
    mov r0, r4
    mov r1, r9
    bl ov001_side_slot_record_021db438
    mov r8, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02202824_L80
    mov r0, r8
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_02202824_L80
    mov r0, r9
    mov r1, r5
    bl native_fn_0220459c
    strb r0, [r7]
    ldrsb r0, [r7]
    cmp r0, #127
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_02202824_L80:
    add r0, r9, #1
    mov r0, r0, lsl #24
    cmp r6, r0, asr #24
    add r7, r7, #1
    mov r9, r0, asr #24
    bgt ov001_02202824_L34
ov001_02202824_L98:
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
