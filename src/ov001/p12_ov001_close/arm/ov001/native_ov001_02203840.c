/* ov001 row 0x02203840: 120 bytes.
 *
 * What it does: 29 instructions; 7 call(s) to 0x0206bc80, 0x020443ec, 0x0204458c, +4 more; loops (back edge at +0x10); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (29 instructions, 7 calls, 4 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0x74 -> constant 0x0223d8ec (image word 0x0223d8ec)
 *   branch +0x1c -> +0x60
 *   branch +0x28 -> +0x60
 *   branch +0x38 -> +0x60
 *   branch +0x48 -> +0x60
 *   test +0x18 cmp r0, #2
 *   test +0x24 cmp r0, #1
 *   test +0x34 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02203840; the literal pool and
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

extern void native_fn_0206bc80(void);
extern void native_fn_020443ec(void);
extern void native_fn_0204458c(void);
extern void native_fn_022035a0(void);
extern void native_fn_02203270(void);
extern void native_fn_02203b18(void);
extern void native_fn_02203558(void);


asm u32 native_ov001_02203840 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    add r0, sp, #4
    add r1, sp, #0
    bl native_fn_0206bc80
    bl native_fn_020443ec
    cmp r0, #2
    bne ov001_02203840_L60
    bl native_fn_0204458c
    cmp r0, #1
    bne ov001_02203840_L60
    add r0, sp, #4
    bl native_fn_022035a0
    cmp r0, #0
    beq ov001_02203840_L60
    add r0, sp, #4
    bl native_fn_02203270
    cmp r0, #0
    beq ov001_02203840_L60
    ldr r0, =0x0223d8ec
    mov r1, #6
    strb r1, [r0, #0x8]
    add sp, sp, #16
    ldmia sp!, {r3, pc}
ov001_02203840_L60:
    bl native_fn_02203b18
    mov r0, #0
    bl native_fn_02203558
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
