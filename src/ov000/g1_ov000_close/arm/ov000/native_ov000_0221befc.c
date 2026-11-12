/* ov000 row 0x0221befc: 260 bytes.
 *
 * What it does: 63 instructions; 17 call(s) to 0x02062a10, 0x0206dcd0, 0x021ead88, +14 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xfc -> constant 0x02246090 (image word 0x02246090)
 *   pool +0x100 -> constant 0x00000159 (image word 0x00000159)
 *   branch +0x20 -> +0x4c
 *   branch +0x48 -> +0xf4
 *   branch +0x50 -> +0xd0
 *   branch +0x68 -> +0xf4
 *   branch +0x7c -> +0xb8
 *   branch +0x90 -> +0xc8
 *   branch +0xa0 -> +0xac
 *   branch +0xa8 -> +0xc8
 *   branch +0xb4 -> +0xc8
 *   test +0x1c cmp r2, r6
 *   test +0x4c cmp r6, #0
 *   test +0x64 cmp r1, #0
 *   test +0x78 cmp r0, #0
 *   test +0x8c cmp r5, #0
 *   test +0x9c cmp r6, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221befc; the literal pool and
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

extern void native_fn_02062a10(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_021ead88(void);
extern void native_fn_021eb030(void);
extern void native_fn_021eae18(void);
extern void native_fn_02072f48(void);
extern void native_fn_021eae04(void);


asm u32 native_ov000_0221befc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    bl native_fn_02062a10
    ldr r1, =0x02246090
    mov r4, r0
    ldr r2, [r1, #0x2c]
    cmp r2, r6
    beq ov000_0221befc_L4c
    str r6, [r1, #0x2c]
    mov r2, #10
    strb r2, [r1, #0x4]
    bl native_fn_0206dcd0
    mov r0, #0
    mov r1, r0
    bl native_fn_021ead88
    bl native_fn_021eb030
    bl native_fn_021eae18
    b ov000_0221befc_Lf4
ov000_0221befc_L4c:
    cmp r6, #0
    beq ov000_0221befc_Ld0
    ldrsb r2, [r1, #4]
    sub r2, r2, #1
    strb r2, [r1, #0x4]
    ldrsb r1, [r1, #4]
    cmp r1, #0
    bne ov000_0221befc_Lf4
    bl native_fn_0206dcd0
    ldrsh r0, [r4, #24]
    bl native_fn_02072f48
    cmp r0, #0
    bne ov000_0221befc_Lb8
    ldrsh r0, [r4, #24]
    ldrb r1, [r4, #0x1a]
    bl native_fn_021ead88
    cmp r5, #0
    beq ov000_0221befc_Lc8
    ldr r0, =0x02246090
    ldr r0, [r0, #0xc]
    cmp r6, r0
    bne ov000_0221befc_Lac
    bl native_fn_021eae04
    b ov000_0221befc_Lc8
ov000_0221befc_Lac:
    bl native_fn_021eb030
    bl native_fn_021eae18
    b ov000_0221befc_Lc8
ov000_0221befc_Lb8:
    ldr r0, =0x00000159
    mov r1, #0
    bl native_fn_021ead88
    bl native_fn_021eae18
ov000_0221befc_Lc8:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov000_0221befc_Ld0:
    mov r0, #0
    bl native_fn_0206dcd0
    mov r0, #0
    mov r1, r0
    bl native_fn_021ead88
    bl native_fn_021eb030
    bl native_fn_021eae18
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov000_0221befc_Lf4:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
