/* ov001 row 0x021e2078: 228 bytes.
 *
 * What it does: 56 instructions; 6 call(s) to 0x021db8d0, 0x021e1f5c, 0x020449d4, +3 more; loops (back edge at +0x18); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (56 instructions, 6 calls, 5 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xe0 -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x20 -> +0xb0
 *   branch +0x50 -> +0xb0
 *   branch +0x5c -> +0x6c
 *   branch +0x68 -> +0x90
 *   branch +0x8c -> +0xb0
 *   test +0x1c cmp r0, #0
 *   test +0x4c cmp r0, #1
 *   test +0x58 cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e2078; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021e1f5c(void);
extern void native_fn_020449d4(void);
extern void native_fn_020444a8(void);
extern void native_fn_021e1f74(void);


asm u32 native_ov001_021e2078 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r1, #0
    mov r5, r0
    str r1, [sp, #0x8]
    str r1, [sp, #0x4]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021e2078_Lb0
    mov r0, r5
    bl native_fn_021e1f5c
    ldr r1, [r5, #0x1e8]
    mov r4, r0
    ldrsh r0, [r1, #42]
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r0, r0, #255
    cmp r0, #1
    bne ov001_021e2078_Lb0
    ldrb r0, [r5, #0x31e]
    cmp r0, #0
    beq ov001_021e2078_L6c
    bl native_fn_020444a8
    cmp r0, #0
    beq ov001_021e2078_L90
ov001_021e2078_L6c:
    mov r0, #20
    mul r1, r4, r0
    mov r4, #1
    add r2, sp, #8
    add r3, sp, #4
    mov r0, r5
    str r4, [sp]
    bl native_fn_021e1f74
    b ov001_021e2078_Lb0
ov001_021e2078_L90:
    mov r0, #10
    mul r1, r4, r0
    mov r4, #1
    add r2, sp, #8
    add r3, sp, #4
    mov r0, r5
    str r4, [sp]
    bl native_fn_021e1f74
ov001_021e2078_Lb0:
    ldr r1, =0x022388ec
    ldr r4, [sp, #0x8]
    ldrb r0, [r1, #0x18]
    ldr r3, [sp, #0x4]
    add r0, r0, r4
    strb r0, [r1, #0x18]
    ldrb r2, [r1, #0x19]
    add r0, r4, r3
    add r2, r2, r3
    strb r2, [r1, #0x19]
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
