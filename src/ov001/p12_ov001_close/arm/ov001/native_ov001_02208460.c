/* ov001 row 0x02208460: 308 bytes.
 *
 * What it does: 76 instructions; 12 call(s) to 0x02207938, 0x020443ec, 0x020443ec, +9 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (76 instructions, 12 calls, 4 branches, 12 back edges, 1 literal slot).
 *
 *   pool +0x130 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x30 -> +0x4c
 *   branch +0x3c -> +0x4c
 *   branch +0x48 -> +0x98
 *   branch +0x58 -> +0x98
 *   test +0x2c cmp r0, #0
 *   test +0x38 cmp r0, #6
 *   test +0x44 cmp r0, #8
 *   test +0x50 cmp r0, #1
 *   test +0x54 cmpne r0, #3
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208460; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_020443ec(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02060434(void);
extern void native_fn_0204a858(void);
extern void native_fn_02202320(void);
extern void native_fn_021fe6b8(void);
extern void native_fn_0206006c(void);


asm u32 native_ov001_02208460 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    ldr r4, =0x021c9698
    bl native_fn_02207938
    ldr r5, [r0, #0x10]
    add r1, sp, #12
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    strh r0, [sp, #12]
    bl native_fn_020443ec
    cmp r0, #0
    beq ov001_02208460_L4c
    bl native_fn_020443ec
    cmp r0, #6
    beq ov001_02208460_L4c
    bl native_fn_020443ec
    cmp r0, #8
    bne ov001_02208460_L98
ov001_02208460_L4c:
    ldrb r0, [r5, #0x31e]
    cmp r0, #1
    cmpne r0, #3
    bne ov001_02208460_L98
    mov r0, #24
    ldr r4, [r5, #0x1e8]
    bl native_fn_02049ad0
    ldrsh r2, [sp, #14]
    mov r1, #1
    str r2, [sp]
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    ldrsh r1, [r4, #42]
    ldrb r2, [r4, #0x2c]
    ldrsh r3, [sp, #12]
    ldr r0, [r0]
    bl native_fn_02060434
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
ov001_02208460_L98:
    mov r0, #24
    ldr r6, [r5, #0x1e8]
    bl native_fn_02049ad0
    ldrsh r2, [sp, #14]
    mov r1, #1
    str r2, [sp]
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    ldrsh r1, [r6, #42]
    ldrb r2, [r6, #0x2c]
    ldrsh r3, [sp, #12]
    ldr r0, [r0]
    bl native_fn_02060434
    ldrsh r0, [sp, #14]
    mov r3, #1
    mov r1, r4
    add r0, r0, #16
    strh r3, [sp, #12]
    strh r0, [sp, #14]
    ldr r0, [r5, #0x1e8]
    add r2, sp, #12
    add r0, r0, #178
    str r0, [sp]
    mov r4, #0
    mov r0, #24
    str r4, [sp, #0x4]
    bl native_fn_0204a858
    mov r0, #31
    bl native_fn_02202320
    bl native_fn_021fe6b8
    mov r1, #4
    str r1, [sp]
    mov r1, #8
    mov r2, #3
    mov r3, #20
    bl native_fn_0206006c
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
