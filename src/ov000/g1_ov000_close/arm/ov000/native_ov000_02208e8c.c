/* ov000 row 0x02208e8c: 296 bytes.
 *
 * What it does: 70 instructions; 12 call(s) to 0x02003ba0, 0x02002d00, 0x020038a8, +9 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x118 -> constant 0x0400100a (image word 0x0400100a)
 *   pool +0x11c -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x120 -> constant 0x02238514 (image word 0x02238514)
 *   pool +0x124 -> native_data_0222f7d8 (image word 0x0222f7d8)
 *   branch +0x30 -> +0x48
 *   branch +0x44 -> +0x58
 *   branch +0x9c -> +0xc8
 *   branch +0xf8 -> +0x108
 *   test +0x28 cmp r5, #8
 *   test +0x98 cmp r5, #0
 *   test +0xf4 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02208e8c; the literal pool and
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

extern void native_fn_02003ba0(void);
extern void native_fn_02002d00(void);
extern void native_fn_020038a8(void);
extern void native_fn_02008d78(void);
extern u8 native_data_0222f7d8[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_0203cf9c(void);
extern void native_fn_020414c8(void);


asm u32 native_ov000_02208e8c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #24
    mov r1, #0
    mov r5, r0
    strh r1, [sp]
    bl native_fn_02003ba0
    mov r0, #0
    bl native_fn_02002d00
    mov r0, r5
    bl native_fn_020038a8
    cmp r5, #8
    ldr r1, =0x0400100a
    bhi ov000_02208e8c_L48
    ldrh r0, [r1]
    and r0, r0, #67
    orr r0, r0, #8
    strh r0, [r1]
    b ov000_02208e8c_L58
ov000_02208e8c_L48:
    ldrh r0, [r1]
    and r0, r0, #67
    orr r0, r0, #4
    strh r0, [r1]
ov000_02208e8c_L58:
    ldr r12, =0x0400100a
    mov r0, #102760448
    ldrh r3, [r12]
    mov r1, #0
    mov r2, #131072
    bic r3, r3, #3
    orr r3, r3, #1
    strh r3, [r12]
    bl native_fn_02008d78
    ldr r2, =0x04001000
    ldr r0, =0x02238514
    ldr r1, [r2]
    bic r1, r1, #7936
    orr r1, r1, #512
    str r1, [r2]
    ldr r5, [r0, #0x8]
    cmp r5, #0
    bne ov000_02208e8c_Lc8
    ldr r1, =native_data_0222f7d8
    add r0, sp, #2
    bl native_fn_0201d444
    add r0, sp, #2
    bl native_fn_0202a8e0
    mov r4, r0
    add r0, sp, #2
    mov r1, #1
    bl native_fn_0203cc2c
    mov r5, r0
ov000_02208e8c_Lc8:
    mov r0, r5
    mov r2, r4
    mov r1, #0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    ldr r0, =0x02238514
    ldr r0, [r0, #0x8]
    cmp r0, #0
    bne ov000_02208e8c_L108
    mov r1, r5
    mov r0, #1
    bl native_fn_0203cf9c
ov000_02208e8c_L108:
    mov r0, #63
    bl native_fn_020414c8
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, pc}
}
