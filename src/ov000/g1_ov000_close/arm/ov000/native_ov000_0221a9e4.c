/* ov000 row 0x0221a9e4: 136 bytes.
 *
 * What it does: 34 instructions; 7 call(s) to 0x02221344, 0x02062a10, 0x02221358, +4 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0x28
 *   branch +0x38 -> +0x48
 *   back edge +0x70 -> +0x54
 *   test +0x0c cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x6c cmp r6, #3
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221a9e4; the literal pool and
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

extern void native_fn_02221344(void);
extern void native_fn_02062a10(void);
extern void native_fn_02221358(void);
extern void native_fn_0222131c(void);
extern void native_fn_0221d77c(void);


asm u32 native_ov000_0221a9e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    bl native_fn_02221344
    cmp r0, #0
    moveq r0, #0
    streqh r0, [sp, #6]
    beq ov000_0221a9e4_L28
    bl native_fn_02062a10
    ldrsh r0, [r0, #24]
    strh r0, [sp, #6]
ov000_0221a9e4_L28:
    bl native_fn_02221358
    cmp r0, #0
    moveq r0, #0
    streqh r0, [sp, #8]
    beq ov000_0221a9e4_L48
    bl native_fn_02062a10
    ldrsh r0, [r0, #24]
    strh r0, [sp, #8]
ov000_0221a9e4_L48:
    mov r6, #0
    add r5, sp, #6
    add r4, sp, #0
ov000_0221a9e4_L54:
    add r2, r6, #2
    mov r0, r6
    add r1, r5, r2, lsl #1
    add r2, r4, r2
    bl native_fn_0222131c
    add r6, r6, #1
    cmp r6, #3
    blt ov000_0221a9e4_L54
    add r0, sp, #6
    add r1, sp, #0
    bl native_fn_0221d77c
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
