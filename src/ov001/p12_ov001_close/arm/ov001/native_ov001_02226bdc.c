/* ov001 row 0x02226bdc: 212 bytes.
 *
 * What it does: 52 instructions; 7 call(s) to 0x02218368, 0x02008e0c, 0x02226764, +4 more; loops (back edge at +0x40); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (52 instructions, 7 calls, 2 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0xd0 -> native_data_0222e920 (image word 0x0222e920)
 *   back edge +0x40 -> +0x24
 *   branch +0x6c -> +0xb4
 *   branch +0xa0 -> +0xb4
 *   back edge +0xc0 -> +0x5c
 *   test +0x68 cmp r0, #0
 *   test +0x9c cmp r6, #0
 *   test +0xb8 cmp r5, #45
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02226bdc; the literal pool and
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

extern u8 native_data_0222e920[];
extern void native_fn_02218368(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02226764(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02226bdc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    ldr r4, =native_data_0222e920
    mov r8, r2
    add r3, sp, #0
    mov r10, r0
    mov r9, r1
    mov r6, #0
    mov r2, #22
ov001_02226bdc_L24:
    ldrb r1, [r4]
    ldrb r0, [r4, #0x1]
    add r4, r4, #2
    strb r1, [r3]
    strb r0, [r3, #0x1]
    add r3, r3, #2
    subs r2, r2, #1
    bne ov001_02226bdc_L24
    ldrb r0, [r4]
    add r7, sp, #0
    mov r5, #0
    strb r0, [r3]
    add r4, sp, #48
    mov r11, #12
ov001_02226bdc_L5c:
    ldrsb r1, [r7]
    mov r0, r8
    bl native_fn_02218368
    cmp r0, #0
    beq ov001_02226bdc_Lb4
    mov r0, r10
    mov r1, r4
    mov r2, r11
    bl native_fn_02008e0c
    ldrsb r2, [r7]
    mov r0, r4
    mov r1, r9
    bl native_fn_02226764
    mov r0, r4
    bl ov001_count_candidates_02223f20
    mov r6, r0
    cmp r6, #0
    ble ov001_02226bdc_Lb4
    mov r0, r4
    mov r1, r10
    mov r2, #12
    bl native_fn_02008e0c
ov001_02226bdc_Lb4:
    add r5, r5, #1
    cmp r5, #45
    add r7, r7, #1
    blt ov001_02226bdc_L5c
    mov r0, r6
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
