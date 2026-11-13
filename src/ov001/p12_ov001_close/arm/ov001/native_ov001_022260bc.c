/* ov001 row 0x022260bc: 212 bytes.
 *
 * What it does: 53 instructions; 9 call(s) to 0x02008e0c, 0x021dbd30, 0x02226150, +6 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 9 calls (53 instructions, 9 calls, 2 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x94
 *   branch +0x50 -> +0x94
 *   branch +0x70 -> +0x94
 *   back edge +0x90 -> +0x54
 *   back edge +0xa0 -> +0x2c
 *   branch +0xb4 -> +0xc8
 *   test +0x30 cmp r0, #0
 *   test +0x4c cmp r1, #0
 *   test +0x6c cmp r0, #0
 *   test +0x7c cmp r8, r0
 *   test +0x8c cmp r8, r0
 *   test +0x98 cmp r7, #3
 *   test +0xb0 cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022260bc; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_0207b244(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_022260bc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r10, r1
    add r1, sp, #0
    mov r2, #12
    mov r11, r0
    bl native_fn_02008e0c
    mov r7, #0
    mov r4, r7
    add r6, sp, #0
    mov r5, r7
ov001_022260bc_L2c:
    ldr r0, [r6, r7, lsl #2]
    cmp r0, #0
    beq ov001_022260bc_L94
    mov r0, r10
    bl ov001_record_field_1f2_021dbd30
    ldrb r1, [r10, #0x323]
    mov r9, r0
    mov r8, r5
    cmp r1, #0
    ble ov001_022260bc_L94
ov001_022260bc_L54:
    add r0, r10, r8
    ldr r2, [r10, #0x1e8]
    ldrb r0, [r0, #0x35e]
    mov r1, r9
    add r2, r2, #70
    bl native_fn_0207b244
    cmp r0, #0
    bgt ov001_022260bc_L94
    ldrb r0, [r10, #0x323]
    sub r0, r0, #1
    cmp r8, r0
    streq r4, [r6, r7, lsl #2]
    ldrb r0, [r10, #0x323]
    add r8, r8, #1
    cmp r8, r0
    blt ov001_022260bc_L54
ov001_022260bc_L94:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_022260bc_L2c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022260bc_Lc8
    add r0, sp, #0
    mov r1, r11
    mov r2, #12
    bl native_fn_02008e0c
ov001_022260bc_Lc8:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
