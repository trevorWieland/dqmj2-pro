/* ov001 row 0x021e259c: 416 bytes.
 *
 * What it does: 103 instructions; 16 call(s) to 0x021db438, 0x021db438, 0x020444ec, +13 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 16 calls (103 instructions, 16 calls, 9 branches, 15 back edges, 1 literal slot).
 *
 *   pool +0x19c -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x68 -> +0x84
 *   branch +0x80 -> +0x8c
 *   branch +0x88 -> +0x90
 *   branch +0x9c -> +0x148
 *   branch +0xac -> +0x148
 *   branch +0xbc -> +0x148
 *   branch +0xec -> +0x148
 *   branch +0xf8 -> +0x108
 *   branch +0x104 -> +0x12c
 *   branch +0x128 -> +0x148
 *   back edge +0x154 -> +0x60
 *   back edge +0x168 -> +0x38
 *   test +0x64 cmp r0, #0
 *   test +0x7c cmp r1, r0
 *   test +0x98 cmp r0, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xe8 cmp r0, #7
 *   test +0xf4 cmp r0, #0
 *   test +0x100 cmp r0, #0
 *   test +0x14c cmp r7, #3
 *   test +0x164 cmp r0, #2
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e259c; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_020444ec(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa84c(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021e2018(void);
extern void native_fn_021e1f5c(void);
extern void native_fn_020449d4(void);
extern void native_fn_020444a8(void);
extern void native_fn_021e1f74(void);


asm u32 native_ov001_021e259c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    mov r0, #0
    mov r1, r0
    str r0, [sp, #0x14]
    str r0, [sp, #0x10]
    bl native_fn_021db438
    str r0, [sp, #0x8]
    mov r0, #1
    mov r1, #0
    bl native_fn_021db438
    str r0, [sp, #0xc]
    mov r0, #0
    str r0, [sp, #0x4]
ov001_021e259c_L38:
    ldr r0, [sp, #0x4]
    mov r7, #0
    rsb r0, r0, #1
    add r1, sp, #8
    ldr r5, [r1, r0, lsl #2]
    ldr r0, [sp, #0x4]
    mov r10, r7
    ldr r6, [r1, r0, lsl #2]
    add r4, sp, #20
    add r11, sp, #16
ov001_021e259c_L60:
    bl native_fn_020444ec
    cmp r0, #0
    beq ov001_021e259c_L84
    bl native_fn_01ffa824
    mov r8, r0
    bl native_fn_01ffa84c
    and r1, r8, #255
    cmp r1, r0
    bhs ov001_021e259c_L8c
ov001_021e259c_L84:
    add r9, r6, r10
    b ov001_021e259c_L90
ov001_021e259c_L8c:
    add r9, r5, r10
ov001_021e259c_L90:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021e259c_L148
    mov r0, r9
    bl native_fn_021dbd24
    cmp r0, #0
    ble ov001_021e259c_L148
    mov r0, r9
    bl native_fn_021e2018
    cmp r0, #0
    bne ov001_021e259c_L148
    mov r0, r9
    bl native_fn_021e1f5c
    ldr r1, [r9, #0x1e8]
    mov r8, r0
    ldrsh r0, [r1, #42]
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r0, r0, #255
    cmp r0, #7
    bne ov001_021e259c_L148
    ldrb r0, [r9, #0x31e]
    cmp r0, #0
    beq ov001_021e259c_L108
    bl native_fn_020444a8
    cmp r0, #0
    beq ov001_021e259c_L12c
ov001_021e259c_L108:
    mov r0, #10
    mul r1, r8, r0
    mov r8, #7
    mov r0, r9
    mov r2, r4
    mov r3, r11
    str r8, [sp]
    bl native_fn_021e1f74
    b ov001_021e259c_L148
ov001_021e259c_L12c:
    add r1, r8, r8, lsl #2
    mov r8, #7
    mov r0, r9
    mov r2, r4
    mov r3, r11
    str r8, [sp]
    bl native_fn_021e1f74
ov001_021e259c_L148:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_021e259c_L60
    ldr r0, [sp, #0x4]
    add r0, r0, #1
    str r0, [sp, #0x4]
    cmp r0, #2
    blt ov001_021e259c_L38
    ldr r1, =0x022388ec
    ldr r4, [sp, #0x14]
    ldrb r0, [r1, #0x18]
    ldr r3, [sp, #0x10]
    add r0, r0, r4
    strb r0, [r1, #0x18]
    ldrb r2, [r1, #0x19]
    add r0, r4, r3
    add r2, r2, r3
    strb r2, [r1, #0x19]
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
