/* ov001 row 0x021fd9a8: 200 bytes.
 *
 * What it does: 49 instructions; 8 call(s) to 0x021db530, 0x021db438, 0x02063520, +5 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (49 instructions, 8 calls, 2 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0xc4 -> constant 0x02239f4c (image word 0x02239f4c)
 *   branch +0x48 -> +0xac
 *   back edge +0xbc -> +0x28
 *   test +0x18 cmp r7, #0
 *   test +0x44 cmp r0, #0
 *   test +0xb4 cmp r7, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd9a8; the literal pool and
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
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_02063520(void);
extern void native_fn_021fd074(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);
extern void native_fn_0206d250(void);
extern void native_fn_02065818(void);


asm u32 native_ov001_021fd9a8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r0, #1
    ldr r9, =0x02239f4c
    bl ov001_mode_byte_021db530
    mov r7, r0
    mov r8, #0
    cmp r7, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r11, #1
    mov r6, r11
ov001_021fd9a8_L28:
    mov r0, r6
    mov r1, r8
    bl ov001_side_slot_record_021db438
    ldr r1, [r0, #0x1e8]
    ldrsh r0, [r1, #42]
    ldrb r1, [r1, #0x2c]
    bl native_fn_02063520
    cmp r0, #0
    beq ov001_021fd9a8_Lac
    mov r0, r11
    mov r1, r8
    bl native_fn_021fd074
    mov r5, r0
    mov r0, #1
    bl native_fn_02202384
    mov r0, r0, asr #3
    add r0, r0, #4
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    mov r0, #1
    mov r1, r8
    bl native_fn_02202398
    mov r4, r0
    ldrsb r0, [r5, #12]
    bl native_fn_0206d250
    add r0, r0, r0, lsl #2
    add r0, r0, r4, asr #3
    add r0, r0, #3
    mov r0, r0, lsl #24
    mov r2, r0, asr #24
    mov r1, r10
    mov r0, r9
    bl native_fn_02065818
ov001_021fd9a8_Lac:
    add r0, r8, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    mov r8, r0, asr #24
    bgt ov001_021fd9a8_L28
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
