/* ov001 row 0x021ff374: 380 bytes.
 *
 * What it does: 93 instructions; 23 call(s) to 0x02202360, 0x021db530, 0x020414c8, +20 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 23 calls (93 instructions, 23 calls, 3 branches, 14 back edges, 2 literal slots).
 *
 *   pool +0x174 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x178 -> constant 0x02239d04 (image word 0x02239d04)
 *   branch +0x2c -> +0x94
 *   branch +0xc0 -> +0xd4
 *   branch +0xe8 -> +0x114
 *   branch +0xf4 -> +0x110
 *   back edge +0x10c -> +0xf8
 *   back edge +0x148 -> +0x138
 *   test +0x28 cmp r0, #0
 *   test +0x98 cmp r0, #1
 *   test +0xa8 cmp r0, #1
 *   test +0xbc cmp r0, #0
 *   test +0xe4 cmp r0, #0
 *   test +0xec cmp r5, #0
 *   test +0x108 cmp r4, r5
 *   test +0x144 cmp r4, #3
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff374; the literal pool and
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

extern void ov001_table_f0_entry_02202360(void);
extern void ov001_mode_byte_021db530(void);
extern void native_fn_020414c8(void);
extern void native_fn_02041538(void);
extern void native_fn_021ff4f0(void);
extern void native_fn_0204b61c(void);
extern void native_fn_021fe3dc(void);
extern void native_fn_021fd858(void);
extern void native_fn_021e13b8(void);
extern void native_fn_02041814(void);
extern void native_fn_02204d24(void);
extern void native_fn_022028c8(void);
extern void native_fn_0220b70c(void);
extern void native_fn_021fe2b8(void);
extern void native_fn_021fd140(void);
extern void native_fn_02008d78(void);
extern void native_fn_0220345c(void);


asm u32 native_ov001_021ff374 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl ov001_table_f0_entry_02202360
    mov r4, r0
    mov r0, #0
    bl ov001_mode_byte_021db530
    ldr r1, =0x02239c10
    mov r5, r0
    ldrsb r0, [r1, #11]
    cmp r0, #0
    beq ov001_021ff374_L94
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #0
    mov r1, #2
    mov r2, #6
    bl native_fn_02041538
    ldr r0, =0x02239c10
    mov r1, #11
    strb r1, [r0, #0xa]
    mov r1, #0
    strb r1, [r0, #0xb]
    bl native_fn_021ff4f0
    add r0, r4, #24
    mov r1, #0
    bl native_fn_0204b61c
    mvn r0, #0
    str r0, [r4]
    ldr r2, =0x02239c10
    mov r0, #1
    mov r1, #0
    strb r0, [r2]
    bl native_fn_021fe3dc
    bl native_fn_021fd858
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_021ff374_L94:
    bl native_fn_021e13b8
    cmp r0, #1
    movne r0, #0
    ldmneia sp!, {r3, r4, r5, pc}
    bl native_fn_02041814
    cmp r0, #1
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r0, =0x02239c10
    ldrb r0, [r0]
    cmp r0, #0
    bne ov001_021ff374_Ld4
    mov r0, #0
    mov r1, #2
    mov r2, #6
    bl native_fn_02041538
ov001_021ff374_Ld4:
    mov r0, #0
    bl native_fn_02204d24
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #0
    bne ov001_021ff374_L114
    cmp r5, #0
    mov r4, #0
    ble ov001_021ff374_L110
ov001_021ff374_Lf8:
    mov r0, r4, lsl #24
    mov r0, r0, asr #24
    bl native_fn_022028c8
    add r4, r4, #1
    cmp r4, r5
    blt ov001_021ff374_Lf8
ov001_021ff374_L110:
    bl native_fn_021ff4f0
ov001_021ff374_L114:
    mov r0, #1
    bl native_fn_0220b70c
    ldr r2, =0x02239c10
    mov r3, #3
    mov r0, #2
    mov r1, #1
    strb r3, [r2, #0xa]
    bl native_fn_021fe2b8
    mov r4, #0
ov001_021ff374_L138:
    mov r0, r4
    bl native_fn_021fd140
    add r4, r4, #1
    cmp r4, #3
    blt ov001_021ff374_L138
    ldr r0, =0x02239d04
    mov r1, #0
    mov r2, #104
    bl native_fn_02008d78
    mov r0, #0
    bl native_fn_0220345c
    mov r0, #1
    bl native_fn_0220345c
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
