/* ov001 row 0x022295cc: 248 bytes.
 *
 * What it does: 61 instructions; 14 call(s) to 0x02223fe8, 0x02226bdc, 0x022243f8, +11 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (61 instructions, 14 calls, 1 branch, 13 back edges, 1 literal slot).
 *
 *   pool +0xf4 -> native_data_0222e5a8 (image word 0x0222e5a8)
 *   branch +0x5c -> +0x94
 *   branch +0x90 -> +0xdc
 *   test +0x58 cmp r0, #0
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022295cc; the literal pool and
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

extern u8 native_data_0222e5a8[];
extern void ov001_clear_free_candidate_slots_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_022243f8(void);
extern void native_fn_02225354(void);
extern void native_fn_0222470c(void);
extern void ov001_filter_highest_priority_candidates_02224570(void);
extern void native_fn_0207afec(void);
extern void native_fn_02225534(void);
extern void ov001_pick_random_candidate_02224050(void);
extern void ov001_first_candidate_02226cb0(void);


asm u32 native_ov001_022295cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e5a8
    add r3, sp, #0
    mov r7, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r5, [r7, #0x4]
    mov r0, r3
    mov r1, r5
    ldr r4, [r7]
    ldr r6, [r7, #0x8]
    bl ov001_clear_free_candidate_slots_02223fe8
    add r0, sp, #0
    mov r1, r7
    mov r2, #83
    bl native_fn_02226bdc
    mov r1, r4
    add r0, sp, #0
    mov r2, r5
    mov r3, r6
    bl native_fn_022243f8
    cmp r0, #0
    ble ov001_022295cc_L94
    add r0, sp, #0
    mov r1, r5
    bl native_fn_02225354
    add r0, sp, #0
    mov r1, r5
    mov r2, #0
    mov r3, #4
    bl native_fn_0222470c
    add r0, sp, #0
    mov r1, r5
    mov r2, #4
    bl ov001_filter_highest_priority_candidates_02224570
    b ov001_022295cc_Ldc
ov001_022295cc_L94:
    mov r0, r6
    bl native_fn_0207afec
    ldrb r2, [r0, #0x1f]
    add r0, sp, #0
    mov r1, r5
    bl native_fn_02225534
    add r0, sp, #0
    mov r1, r5
    bl native_fn_02225354
    add r0, sp, #0
    mov r1, r5
    mov r2, #0
    mov r3, #4
    bl native_fn_0222470c
    mov r1, r5
    add r0, sp, #0
    mov r2, #4
    bl ov001_filter_highest_priority_candidates_02224570
ov001_022295cc_Ldc:
    add r0, sp, #0
    bl ov001_pick_random_candidate_02224050
    add r0, sp, #0
    bl ov001_first_candidate_02226cb0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
