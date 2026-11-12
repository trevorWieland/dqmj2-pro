/* ov001 row 0x02227264: 132 bytes.
 *
 * What it does: 32 instructions; 7 call(s) to 0x02223fe8, 0x02226bdc, 0x02224900, +4 more; loops (back edge at +0x28); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (32 instructions, 7 calls, 0 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0x80 -> native_data_0222e89c (image word 0x0222e89c)
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02227264; the literal pool and
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

extern u8 native_data_0222e89c[];
extern void ov001_clear_free_candidate_slots_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02224900(void);
extern void native_fn_02225bac(void);
extern void ov001_pick_random_candidate_02224050(void);
extern void ov001_first_candidate_02226cb0(void);


asm u32 native_ov001_02227264 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e89c
    add r3, sp, #0
    mov r5, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r4, [r5, #0x4]
    mov r0, r3
    mov r1, r4
    bl ov001_clear_free_candidate_slots_02223fe8
    add r0, sp, #0
    mov r1, r5
    mov r2, #20
    bl native_fn_02226bdc
    add r0, sp, #0
    mov r1, r4
    bl native_fn_02224900
    add r0, sp, #0
    mov r1, r4
    mov r2, #55
    bl native_fn_02225bac
    mov r1, r4
    add r0, sp, #0
    mov r2, #54
    bl native_fn_02225bac
    add r0, sp, #0
    bl ov001_pick_random_candidate_02224050
    add r0, sp, #0
    bl ov001_first_candidate_02226cb0
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
