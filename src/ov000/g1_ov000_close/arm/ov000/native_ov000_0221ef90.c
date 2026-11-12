/* ov000 row 0x0221ef90: 388 bytes.
 *
 * What it does: 95 instructions; 13 call(s) to 0x0221f070, 0x02049ad0, 0x02049ffc, +10 more; loops (back edge at +0x44); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x17c -> constant 0x022463a0 (image word 0x022463a0)
 *   pool +0x180 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x28 -> +0xe0
 *   branch +0x80 -> +0xcc
 *   back edge +0xdc -> +0x38
 *   test +0x18 cmp r0, #6
 *   test +0x24 cmp r7, #0
 *   test +0x7c cmp r0, r1
 *   test +0x9c cmp r2, #0
 *   test +0xd4 cmp r7, r0, asr #24
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221ef90; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_0221ee08(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_020877bc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02087a48(void);


asm u32 native_ov000_0221ef90 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #64
    ldr r1, =0x022463a0
    mov r10, r0
    ldrsb r0, [r1]
    mov r6, #0
    cmp r0, #6
    movgt r0, #6
    and r7, r0, #255
    cmp r7, #0
    ble ov000_0221ef90_Le0
    ldr r4, =0x022463a0
    mov r11, #5
    mov r5, #26
ov000_0221ef90_L38:
    add r9, r6, #10
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    add r8, r6, #20
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r0, [r10, #0x4]
    ldrh r1, [r10, #14]
    add r0, r6, r0
    cmp r0, r1
    bge ov000_0221ef90_Lcc
    ldr r1, [r4, #0xc]
    rsb r2, r0, r0, lsl #3
    add r2, r1, r2
    ldrb r2, [r2, #0x3]
    mov r9, r9, lsl #24
    mov r8, r8, lsl #24
    cmp r2, #0
    movne r3, r11
    rsb r2, r0, r0, lsl #3
    moveq r3, #1
    str r5, [sp]
    str r3, [sp, #0x4]
    add r0, r1, r2
    ldrb r2, [r1, r2]
    ldrb r3, [r0, #0x1]
    mov r0, r9, asr #24
    mov r1, r8, asr #24
    bl native_fn_0221ee08
ov000_0221ef90_Lcc:
    add r0, r6, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    mov r6, r0, asr #24
    bgt ov000_0221ef90_L38
ov000_0221ef90_Le0:
    mov r0, #1
    bl native_fn_02049ad0
    mov r4, r0
    ldr r0, [r4]
    ldr r5, [r0, #0x4]
    mov r0, r5
    bl native_fn_02049ffc
    mov r0, #9
    mov r1, #0
    mov r2, #19
    bl native_fn_0205dc70
    add r2, sp, #8
    mov r1, r0
    str r2, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    mov r2, #24
    mov r3, #0
    bl native_fn_02046af4
    ldr r0, =0x022463a0
    add r1, sp, #14
    ldrsb r0, [r0, #2]
    mov r2, #2
    mov r3, #1
    bl native_fn_020877bc
    mov r0, r4
    bl native_fn_02049f4c
    mov r1, #1
    str r1, [sp]
    add r2, sp, #8
    mov r1, #0
    str r2, [sp, #0x4]
    mov r0, r5
    mov r2, #16
    mov r3, r1
    bl native_fn_02087a48
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
