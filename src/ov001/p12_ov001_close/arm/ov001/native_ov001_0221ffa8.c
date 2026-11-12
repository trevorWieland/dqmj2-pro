/* ov001 row 0x0221ffa8: 164 bytes.
 *
 * What it does: 41 instructions; 7 call(s) to 0x021db8d0, 0x021dbd30, 0x02220030, +4 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: block load (41 instructions, 7 calls, 1 branch, 5 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x88
 *   branch +0x44 -> +0x88
 *   branch +0x60 -> +0x88
 *   back edge +0x84 -> +0x64
 *   back edge +0x94 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x30 cmpne r1, r0
 *   test +0x40 cmp r0, #200
 *   test +0x5c cmp r0, #0
 *   test +0x6c cmp r1, #1
 *   test +0x80 cmp r2, r0
 *   test +0x8c cmp r8, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221ffa8; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_02218430(void);


asm u32 native_ov001_0221ffa8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #200
    mov r8, #0
    ldmia r0, {r7, r9}
    add r6, sp, #0
    mov r5, #200
    mov r4, r8
ov001_0221ffa8_L1c:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    ldrneb r1, [r7, #0x31f]
    ldrneb r0, [r9, #0x31f]
    cmpne r1, r0
    beq ov001_0221ffa8_L88
    mov r0, r9
    bl ov001_record_field_1f2_021dbd30
    cmp r0, #200
    blt ov001_0221ffa8_L88
    mov r0, r9
    mov r1, r6
    mov r2, r5
    bl native_fn_02218430
    mov r2, r4
    cmp r0, #0
    ble ov001_0221ffa8_L88
ov001_0221ffa8_L64:
    ldr r1, [r6, r2, lsl #2]
    sub r1, r1, #52
    cmp r1, #1
    addls sp, sp, #200
    movls r0, #1
    ldmlsia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    add r2, r2, #1
    cmp r2, r0
    blt ov001_0221ffa8_L64
ov001_0221ffa8_L88:
    add r8, r8, #1
    cmp r8, #3
    add r9, r9, #1088
    blt ov001_0221ffa8_L1c
    mov r0, #0
    add sp, sp, #200
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
