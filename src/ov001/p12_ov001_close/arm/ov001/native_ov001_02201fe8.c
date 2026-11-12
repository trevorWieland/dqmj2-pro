/* ov001 row 0x02201fe8: 164 bytes.
 *
 * What it does: 40 instructions; 12 call(s) to 0x022034e0, 0x02203228, 0x02201760, +9 more; loops (back edge at +0x1c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (40 instructions, 12 calls, 4 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xa0 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x0c -> +0x98
 *   branch +0x18 -> +0x30
 *   branch +0x2c -> +0x98
 *   branch +0x70 -> +0x8c
 *   test +0x08 cmp r0, #0
 *   test +0x14 cmp r0, #0
 *   test +0x6c cmp r0, #2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02201fe8; the literal pool and
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

extern void native_fn_022034e0(void);
extern void native_fn_02203228(void);
extern void native_fn_02201760(void);
extern void native_fn_02202360(void);
extern void native_fn_02202e08(void);
extern void native_fn_021fceb4(void);
extern void native_fn_02204590(void);
extern void native_fn_02041538(void);
extern void native_fn_021ff4f0(void);
extern void native_fn_02203320(void);
extern void native_fn_021e13a8(void);
extern void native_fn_021ff238(void);


asm u32 native_ov001_02201fe8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_022034e0
    cmp r0, #0
    beq ov001_02201fe8_L98
    bl native_fn_02203228
    cmp r0, #0
    beq ov001_02201fe8_L30
    bl native_fn_02201760
    ldr r0, =0x02239c10
    mov r1, #1
    strb r1, [r0, #0x5]
    b ov001_02201fe8_L98
ov001_02201fe8_L30:
    mov r0, #0
    bl native_fn_02202360
    mov r4, r0
    bl native_fn_02202e08
    bl native_fn_021fceb4
    add r0, r4, #24
    mov r1, #123
    bl native_fn_02204590
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    bl native_fn_021ff4f0
    mov r0, #1
    bl native_fn_02203320
    cmp r0, #2
    bne ov001_02201fe8_L8c
    mov r0, #4
    bl native_fn_021e13a8
    mov r0, #1
    bl native_fn_021ff238
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_02201fe8_L8c:
    ldr r0, =0x02239c10
    mov r1, #3
    strb r1, [r0, #0xa]
ov001_02201fe8_L98:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
