/* ov001 row 0x02203ccc: 168 bytes.
 *
 * What it does: 42 instructions; 7 call(s) to 0x0220305c, 0x0206bc80, 0x0206bd24, +4 more; loops (back edge at +0x10); returns through pop {r4, r5, pc}
 *
 * Decoded shape: loop with 7 calls (42 instructions, 7 calls, 1 branch, 5 back edges, 0 literal slots).
 *
 *   branch +0x48 -> +0x74
 *   back edge +0x9c -> +0x80
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r5, #0
 *   test +0x98 cmp r12, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02203ccc; the literal pool and
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

extern void native_fn_0220305c(void);
extern void native_fn_0206bc80(void);
extern void native_fn_0206bd24(void);
extern void native_fn_022035a0(void);
extern void native_fn_0220b3e4(void);


asm u32 native_ov001_02203ccc (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #28
    mov r5, r0
    mov r0, #0
    bl native_fn_0220305c
    mov r4, r0
    add r0, sp, #16
    add r1, sp, #0
    bl native_fn_0206bc80
    add r0, sp, #4
    add r1, sp, #0
    bl native_fn_0206bd24
    add r0, sp, #16
    bl native_fn_022035a0
    cmp r0, #0
    addeq sp, sp, #28
    ldmeqia sp!, {r4, r5, pc}
    cmp r5, #0
    beq ov001_02203ccc_L74
    ldr r1, [sp, #0x10]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x18]
    mov r0, #0
    bl native_fn_0220b3e4
    ldr r1, [sp, #0x4]
    ldr r2, [sp, #0x8]
    ldr r3, [sp, #0xc]
    mov r0, #2
    bl native_fn_0220b3e4
ov001_02203ccc_L74:
    mov r12, #0
    add r3, sp, #16
    add r1, sp, #4
ov001_02203ccc_L80:
    ldr r0, [r3, r12, lsl #2]
    add r2, r4, r12, lsl #2
    str r0, [r2, #0x1c]
    ldr r0, [r1, r12, lsl #2]
    add r12, r12, #1
    str r0, [r2, #0x28]
    cmp r12, #3
    blt ov001_02203ccc_L80
    add sp, sp, #28
    ldmia sp!, {r4, r5, pc}
}
