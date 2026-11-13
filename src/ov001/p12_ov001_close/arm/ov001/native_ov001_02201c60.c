/* ov001 row 0x02201c60: 236 bytes.
 *
 * What it does: 57 instructions; 10 call(s) to 0x022068a0, 0x021db530, 0x02201c84, +7 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (57 instructions, 10 calls, 3 branches, 8 back edges, 2 literal slots).
 *
 *   pool +0xe4 -> constant 0x02239ca4 (image word 0x02239ca4)
 *   pool +0xe8 -> constant 0x02239c10 (image word 0x02239c10)
 *   back edge +0x3c -> +0x24
 *   branch +0x48 -> +0xc0
 *   branch +0x70 -> +0x90
 *   branch +0x8c -> +0xa8
 *   back edge +0xbc -> +0x58
 *   test +0x38 cmp r3, #3
 *   test +0x40 cmp r7, #0
 *   test +0x6c cmp r0, #0
 *   test +0xb0 cmp r7, r0, asr #24
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02201c60; the literal pool and
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

extern void native_fn_022068a0(void);
extern void ov001_mode_byte_021db530(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021fd074(void);
extern void native_fn_0206d114(void);
extern void native_fn_022068e0(void);
extern void native_fn_021e6754(void);


asm u32 native_ov001_02201c60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    bl native_fn_022068a0
    mov r6, r0
    mov r0, #0
    bl ov001_mode_byte_021db530
    mov r8, #0
    mov r7, r0
    mov r3, r8
    mvn r2, #0
ov001_02201c60_L24:
    add r0, r3, #1
    mov r0, r0, lsl #24
    add r1, r6, r3, lsl #2
    mov r3, r0, asr #24
    str r2, [r1, #0x84]
    cmp r3, #3
    blt ov001_02201c60_L24
    cmp r7, #0
    mov r10, #0
    ble ov001_02201c60_Lc0
    ldr r9, =0x02239ca4
    mov r11, r10
    mov r5, r10
ov001_02201c60_L58:
    mov r0, r5
    mov r1, r10
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    bne ov001_02201c60_L90
    mov r0, r11
    mov r1, r10
    bl native_fn_021fd074
    ldrsb r0, [r0, #12]
    mov r1, #0
    bl native_fn_0206d114
    b ov001_02201c60_La8
ov001_02201c60_L90:
    add r1, r6, r8, lsl #2
    add r0, r6, r8, lsl #5
    str r10, [r1, #0x84]
    str r4, [r0, #0x24]
    str r9, [r0, #0x28]
    add r8, r8, #1
ov001_02201c60_La8:
    add r0, r10, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    add r9, r9, #16
    mov r10, r0, asr #24
    bgt ov001_02201c60_L58
ov001_02201c60_Lc0:
    mov r0, r8
    bl native_fn_022068e0
    mov r0, #1
    bl native_fn_021e6754
    ldr r0, =0x02239c10
    mov r1, #17
    strb r1, [r0, #0xa]
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
