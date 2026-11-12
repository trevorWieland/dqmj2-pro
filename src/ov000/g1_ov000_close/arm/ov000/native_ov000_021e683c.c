/* ov000 row 0x021e683c: 516 bytes.
 *
 * What it does: 126 instructions; 14 call(s) to 0x021e6544, 0x020283dc, 0x021e6544, +11 more; loops (back edge at +0x18); returns through pop {r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1f8 -> constant 0x022350d8 (image word 0x022350d8)
 *   pool +0x1fc -> constant 0x0223508c (image word 0x0223508c)
 *   pool +0x200 -> constant 0x02235128 (image word 0x02235128)
 *   branch +0x20 -> +0x3c
 *   branch +0x4c -> +0x68
 *   branch +0x74 -> +0x104
 *   branch +0x128 -> +0x1ec
 *   branch +0x140 -> +0x180
 *   branch +0x190 -> +0x1d0
 *   test +0x1c cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x124 cmp r0, #2
 *   test +0x13c cmp r0, #0
 *   test +0x18c cmp r0, #0
 *   0 block transfer(s), 24 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e683c; the literal pool and
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

extern void native_fn_021e6544(void);
extern void native_fn_020283dc(void);
extern void native_fn_020283fc(void);
extern void native_fn_021e6654(void);
extern void native_fn_0202859c(void);
extern void native_fn_020285c8(void);
extern void native_fn_0203d0fc(void);


asm u32 native_ov000_021e683c (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r0, =0x022350d8
    add r1, sp, #0
    mov r4, #0
    ldr r5, =0x0223508c
    bl native_fn_021e6544
    cmp r0, #0
    beq ov000_021e683c_L3c
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, r5
    bl native_fn_020283dc
    orr r4, r4, #1
ov000_021e683c_L3c:
    add r1, sp, #0
    add r0, r5, #104
    bl native_fn_021e6544
    cmp r0, #0
    beq ov000_021e683c_L68
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, r5
    bl native_fn_020283fc
    orr r4, r4, #2
ov000_021e683c_L68:
    mov r0, #0
    bl native_fn_021e6654
    cmp r0, #0
    beq ov000_021e683c_L104
    add r1, sp, #0
    mov r0, r5
    bl native_fn_0202859c
    ldr r3, [sp]
    ldr r1, [r5, #0x84]
    ldr r2, [sp, #0x4]
    add r1, r3, r1
    ldr r0, [r5, #0x88]
    ldr r12, [sp, #0x8]
    add r2, r2, r0
    ldr r3, [r5, #0x8c]
    mov r0, r5
    add r3, r12, r3
    str r1, [sp]
    str r2, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_020283dc
    add r1, sp, #0
    mov r0, r5
    bl native_fn_020285c8
    ldr r1, [sp]
    ldr r0, [r5, #0x90]
    ldr r2, [sp, #0x4]
    add r1, r1, r0
    ldr r0, [r5, #0x94]
    ldr r12, [sp, #0x8]
    add r2, r2, r0
    ldr r3, [r5, #0x98]
    mov r0, r5
    add r3, r12, r3
    str r1, [sp]
    str r2, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_020283fc
    orr r4, r4, #4
ov000_021e683c_L104:
    mov r0, #0
    str r0, [r5, #0x84]
    str r0, [r5, #0x88]
    str r0, [r5, #0x8c]
    str r0, [r5, #0x90]
    str r0, [r5, #0x94]
    str r0, [r5, #0x98]
    bl native_fn_0203d0fc
    cmp r0, #2
    bne ov000_021e683c_L1ec
    ldr r5, =0x02235128
    add r1, sp, #0
    add r0, r5, #76
    bl native_fn_021e6544
    cmp r0, #0
    beq ov000_021e683c_L180
    ldr r3, [sp]
    ldr r1, [r5, #0x84]
    ldr r2, [sp, #0x4]
    ldr r0, [r5, #0x88]
    add r1, r3, r1
    add r2, r2, r0
    ldr r12, [sp, #0x8]
    ldr r3, [r5, #0x8c]
    mov r0, r5
    add r3, r12, r3
    str r1, [sp]
    str r2, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_020283dc
    orr r4, r4, #1
ov000_021e683c_L180:
    add r1, sp, #0
    add r0, r5, #104
    bl native_fn_021e6544
    cmp r0, #0
    beq ov000_021e683c_L1d0
    ldr r3, [sp]
    ldr r1, [r5, #0x90]
    ldr r2, [sp, #0x4]
    ldr r0, [r5, #0x94]
    add r1, r3, r1
    add r2, r2, r0
    ldr r12, [sp, #0x8]
    ldr r3, [r5, #0x98]
    mov r0, r5
    add r3, r12, r3
    str r1, [sp]
    str r2, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_020283fc
    orr r4, r4, #2
ov000_021e683c_L1d0:
    mov r0, #0
    str r0, [r5, #0x84]
    str r0, [r5, #0x88]
    str r0, [r5, #0x8c]
    str r0, [r5, #0x90]
    str r0, [r5, #0x94]
    str r0, [r5, #0x98]
ov000_021e683c_L1ec:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
