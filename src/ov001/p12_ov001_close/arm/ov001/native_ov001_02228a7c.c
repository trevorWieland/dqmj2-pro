/* ov001 row 0x02228a7c: 148 bytes.
 *
 * What it does: 36 instructions; 8 call(s) to 0x02223fe8, 0x02226bdc, 0x0207afec, +5 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (36 instructions, 8 calls, 0 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x90 -> native_data_0222e680 (image word 0x0222e680)
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02228a7c; the literal pool and
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

extern u8 native_data_0222e680[];
extern void ov001_clear_free_candidate_slots_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_0207afec(void);
extern void native_fn_02225534(void);
extern void ov001_filter_highest_priority_candidates_02224570(void);
extern void native_fn_0222463c(void);
extern void ov001_pick_random_candidate_02224050(void);
extern void ov001_first_candidate_02226cb0(void);


asm u32 native_ov001_02228a7c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e680
    add r3, sp, #0
    mov r6, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r4, [r6, #0x4]
    mov r0, r3
    mov r1, r4
    ldr r5, [r6, #0x8]
    bl ov001_clear_free_candidate_slots_02223fe8
    add r0, sp, #0
    mov r1, r6
    mov r2, #65
    bl native_fn_02226bdc
    mov r0, r5
    bl native_fn_0207afec
    ldrb r2, [r0, #0x1f]
    add r0, sp, #0
    mov r1, r4
    bl native_fn_02225534
    add r0, sp, #0
    mov r1, r4
    mov r2, #4
    bl ov001_filter_highest_priority_candidates_02224570
    mov r1, r4
    add r0, sp, #0
    mov r2, #0
    bl native_fn_0222463c
    add r0, sp, #0
    bl ov001_pick_random_candidate_02224050
    add r0, sp, #0
    bl ov001_first_candidate_02226cb0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
