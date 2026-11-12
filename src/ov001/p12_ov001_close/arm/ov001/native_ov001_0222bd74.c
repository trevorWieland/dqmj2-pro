/* ov001 row 0x0222bd74: 208 bytes.
 *
 * What it does: 51 instructions; 11 call(s) to 0x02223fe8, 0x02225414, 0x02226bdc, +8 more; loops (back edge at +0x28); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (51 instructions, 11 calls, 1 branch, 11 back edges, 1 literal slot).
 *
 *   pool +0xcc -> native_data_0222e17c (image word 0x0222e17c)
 *   branch +0x9c -> +0xb4
 *   test +0x98 cmp r0, #0
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222bd74; the literal pool and
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

extern u8 native_data_0222e17c[];
extern void ov001_clear_free_candidate_slots_02223fe8(void);
extern void native_fn_02225414(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02224900(void);
extern void native_fn_02225bac(void);
extern void native_fn_02225ee4(void);
extern void native_fn_02225854(void);
extern void native_fn_02224804(void);
extern void ov001_pick_random_candidate_02224050(void);
extern void ov001_first_candidate_02226cb0(void);


asm u32 native_ov001_0222bd74 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e17c
    add r3, sp, #0
    mov r5, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r4, [r5, #0x4]
    mov r0, r3
    mov r1, r4
    bl ov001_clear_free_candidate_slots_02223fe8
    add r0, sp, #0
    mov r1, r4
    mov r2, #30
    mov r3, #1
    bl native_fn_02225414
    add r0, sp, #0
    mov r1, r5
    mov r2, #179
    bl native_fn_02226bdc
    add r0, sp, #0
    mov r1, r4
    bl native_fn_02224900
    add r0, sp, #0
    mov r1, r4
    mov r2, #55
    bl native_fn_02225bac
    add r0, sp, #0
    mov r1, r4
    mov r2, #54
    bl native_fn_02225bac
    add r0, sp, #0
    mov r1, r4
    mov r2, #1
    bl native_fn_02225ee4
    add r0, sp, #0
    mov r1, r4
    bl native_fn_02225854
    cmp r0, #0
    beq ov001_0222bd74_Lb4
    add r0, sp, #0
    mov r1, r4
    mov r2, #2
    mov r3, #5
    bl native_fn_02224804
ov001_0222bd74_Lb4:
    add r0, sp, #0
    bl ov001_pick_random_candidate_02224050
    add r0, sp, #0
    bl ov001_first_candidate_02226cb0
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
