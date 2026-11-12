/* ov000 row 0x021fc73c: 172 bytes.
 *
 * What it does: 42 instructions; 12 call(s) to 0x02215698, 0x020642dc, 0x02061260, +9 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa8 -> constant 0x022372a8 (image word 0x022372a8)
 *   branch +0x1c -> +0x2c
 *   branch +0x24 -> +0x4c
 *   branch +0x38 -> +0x44
 *   branch +0x80 -> +0x90
 *   branch +0x8c -> +0xa0
 *   test +0x18 cmp r0, #2
 *   test +0x20 cmp r0, #4
 *   test +0x30 cmp r0, #12
 *   test +0x34 cmpne r0, #13
 *   test +0x7c cmp r5, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fc73c; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_020642dc(void);
extern void native_fn_02061260(void);
extern void native_fn_022156d4(void);
extern void native_fn_020c4c58(void);
extern void native_fn_0204b61c(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_0206dcd0(void);


asm u32 native_ov000_021fc73c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl ov000_display_context_02215698
    ldr r1, =0x022372a8
    mov r5, r0
    ldr r4, [r1, #0xc]
    ldr r0, [r4]
    cmp r0, #2
    beq ov000_021fc73c_L2c
    cmp r0, #4
    beq ov000_021fc73c_L4c
    ldmia sp!, {r3, r4, r5, pc}
ov000_021fc73c_L2c:
    bl native_fn_020642dc
    cmp r0, #12
    cmpne r0, #13
    bne ov000_021fc73c_L44
    mov r0, #1
    bl native_fn_02061260
ov000_021fc73c_L44:
    bl native_fn_022156d4
    ldmia sp!, {r3, r4, r5, pc}
ov000_021fc73c_L4c:
    mov r0, #0
    mov r2, #1
    sub r1, r0, #1
    str r2, [r4, #0x4]
    bl native_fn_020c4c58
    add r0, r5, #16
    mov r1, #0
    bl native_fn_0204b61c
    mov r0, #1
    bl native_fn_020620b4
    ldr r5, [r4, #0xfc]
    bl native_fn_02062aa0
    cmp r5, r0
    bge ov000_021fc73c_L90
    mov r0, r5
    bl native_fn_02062a50
    b ov000_021fc73c_La0
ov000_021fc73c_L90:
    bl native_fn_02062aa0
    ldr r1, [r4, #0xfc]
    sub r0, r1, r0
    bl native_fn_02062a88
ov000_021fc73c_La0:
    bl native_fn_0206dcd0
    ldmia sp!, {r3, r4, r5, pc}
}
