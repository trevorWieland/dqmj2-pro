/* ov000 row 0x021e8b60: 168 bytes.
 *
 * What it does: 40 instructions; 6 call(s) to 0x021e07b8, 0x021e8b20, 0x021e7d18, +3 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0xa0 -> native_data_0222edb8 (image word 0x0222edb8)
 *   pool +0xa4 -> constant 0x0223526c (image word 0x0223526c)
 *   branch +0x3c -> +0x4c
 *   branch +0x54 -> +0x74
 *   test +0x10 cmp r1, #0
 *   test +0x38 cmp r0, #0
 *   test +0x50 cmp r0, #2
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8b60; the literal pool and
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

extern u8 native_data_0222edb8[];
extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_021e8b20(void);
extern void native_fn_021e7d18(void);
extern void native_fn_021e7d5c(void);
extern void native_fn_0202818c(void);
extern void native_fn_021e0b88(void);


asm u32 native_ov000_021e8b60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =native_data_0222edb8
    mov r0, #0
    ldrsb r1, [r1]
    cmp r1, #0
    ldmltia sp!, {r3, r4, r5, pc}
    bl ov000_saved_world_position_get_021e07b8
    ldr r1, =native_data_0222edb8
    ldr r3, =0x0223526c
    ldrsb r2, [r1]
    mov r1, #716
    mov r4, r0
    mla r5, r2, r1, r3
    ldrb r0, [r5, #0x276]
    cmp r0, #0
    beq ov000_021e8b60_L4c
    mov r0, r5
    ldmia r4, {r1, r2, r3}
    bl native_fn_021e8b20
ov000_021e8b60_L4c:
    ldrb r0, [r5, #0x2a9]
    cmp r0, #2
    beq ov000_021e8b60_L74
    mov r0, r5
    mov r1, #2
    mov r2, #0
    bl native_fn_021e7d18
    mov r0, r5
    mov r1, #3
    bl native_fn_021e7d5c
ov000_021e8b60_L74:
    mov r0, r4
    add r1, r5, #112
    bl native_fn_0202818c
    bl native_fn_021e0b88
    add r0, r5, #512
    mov r1, #30
    strh r1, [r0, #172]
    mov r1, #0
    strh r1, [r0, #174]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
