/* ov000 row 0x02224ee4: 192 bytes.
 *
 * What it does: 45 instructions; 7 call(s) to 0x020451c4, 0x0201d444, 0x0201d444, +4 more; loops (back edge at +0x38); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb4 -> native_data_0222ff40 (image word 0x0222ff40)
 *   pool +0xb8 -> native_data_0222ff54 (image word 0x0222ff54)
 *   pool +0xbc -> native_data_0222ff78 (image word 0x0222ff78)
 *   branch +0x14 -> +0x28
 *   branch +0x20 -> +0x44
 *   branch +0x24 -> +0x88
 *   branch +0x40 -> +0x88
 *   branch +0x4c -> +0x5c
 *   branch +0x58 -> +0x64
 *   branch +0x74 -> +0x88
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmp r0, #1
 *   test +0x1c cmpne r0, #2
 *   test +0x44 cmp r0, #1
 *   test +0x70 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224ee4; the literal pool and
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

extern u8 native_data_0222ff40[];
extern void native_fn_020451c4(void);
extern u8 native_data_0222ff54[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222ff78[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_02045994(void);
extern void native_fn_0202a498(void);


asm u32 native_ov000_02224ee4 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #68
    mov r1, #0
    str r1, [sp]
    cmp r0, #0
    beq ov000_02224ee4_L28
    cmp r0, #1
    cmpne r0, #2
    beq ov000_02224ee4_L44
    b ov000_02224ee4_L88
ov000_02224ee4_L28:
    mov r1, #2
    ldr r0, =native_data_0222ff40
    add r3, sp, #0
    mov r2, r1
    bl native_fn_020451c4
    mov r4, r0
    b ov000_02224ee4_L88
ov000_02224ee4_L44:
    cmp r0, #1
    add r0, sp, #4
    bne ov000_02224ee4_L5c
    ldr r1, =native_data_0222ff54
    bl native_fn_0201d444
    b ov000_02224ee4_L64
ov000_02224ee4_L5c:
    ldr r1, =native_data_0222ff78
    bl native_fn_0201d444
ov000_02224ee4_L64:
    add r0, sp, #4
    bl native_fn_0202a8e0
    str r0, [sp]
    cmp r0, #0
    beq ov000_02224ee4_L88
    add r0, sp, #4
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
ov000_02224ee4_L88:
    ldr r3, [sp]
    mov r1, r4
    mov r0, #1
    mov r2, #0
    bl native_fn_02045994
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    mov r0, #0
    add sp, sp, #68
    ldmia sp!, {r3, r4, pc}
}
