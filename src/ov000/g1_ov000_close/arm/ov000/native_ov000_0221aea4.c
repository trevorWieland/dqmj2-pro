/* ov000 row 0x0221aea4: 228 bytes.
 *
 * What it does: 55 instructions; 14 call(s) to 0x02041814, 0x02041814, 0x02041814, +11 more; loops (back edge at +0x38); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xdc -> constant 0x022460d4 (image word 0x022460d4)
 *   pool +0xe0 -> constant 0x02246090 (image word 0x02246090)
 *   branch +0x10 -> +0x28
 *   branch +0x18 -> +0x4c
 *   branch +0x20 -> +0x60
 *   branch +0x24 -> +0xd4
 *   branch +0x34 -> +0xd4
 *   branch +0x68 -> +0x78
 *   test +0x0c cmp r0, #1
 *   test +0x14 cmp r0, #6
 *   test +0x1c cmp r0, #7
 *   test +0x30 cmp r0, #7
 *   test +0x3c cmp r0, #1
 *   test +0x50 cmp r0, #1
 *   test +0x64 cmp r0, #1
 *   test +0x7c cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221aea4; the literal pool and
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

extern void native_fn_02041814(void);
extern void native_fn_0207e874(void);
extern void native_fn_0205fd70(void);
extern void native_fn_0207e948(void);
extern void native_fn_020c3e9c(void);
extern void native_fn_02048f1c(void);
extern void native_fn_02048f2c(void);
extern void native_fn_02048f3c(void);
extern void native_fn_02048f4c(void);
extern void native_fn_020c40e8(void);
extern void native_fn_020c3f94(void);
extern void native_fn_0221a8e8(void);


asm u32 native_ov000_0221aea4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x022460d4
    ldrsb r0, [r0, #16]
    cmp r0, #1
    beq ov000_0221aea4_L28
    cmp r0, #6
    beq ov000_0221aea4_L4c
    cmp r0, #7
    beq ov000_0221aea4_L60
    b ov000_0221aea4_Ld4
ov000_0221aea4_L28:
    ldr r0, =0x02246090
    ldrsb r0, [r0, #3]
    cmp r0, #7
    bne ov000_0221aea4_Ld4
    bl native_fn_02041814
    cmp r0, #1
    movne r0, #1
    moveq r0, #0
    ldmia sp!, {r3, pc}
ov000_0221aea4_L4c:
    bl native_fn_02041814
    cmp r0, #1
    movne r0, #1
    moveq r0, #0
    ldmia sp!, {r3, pc}
ov000_0221aea4_L60:
    bl native_fn_02041814
    cmp r0, #1
    bne ov000_0221aea4_L78
    bl native_fn_0207e874
    mov r0, #0
    ldmia sp!, {r3, pc}
ov000_0221aea4_L78:
    bl native_fn_0205fd70
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r3, pc}
    bl native_fn_0207e948
    bl native_fn_020c3e9c
    mov r0, #1
    mov r1, r0
    bl native_fn_02048f1c
    mov r0, #0
    mov r1, #1
    bl native_fn_02048f2c
    mov r0, #2
    mov r1, #1
    bl native_fn_02048f3c
    mov r0, #3
    mov r1, #1
    bl native_fn_02048f4c
    bl native_fn_020c40e8
    bl native_fn_020c3f94
    bl native_fn_0221a8e8
    mov r0, #1
    ldmia sp!, {r3, pc}
ov000_0221aea4_Ld4:
    mov r0, #1
    ldmia sp!, {r3, pc}
}
