/* ov000 row 0x02224420: 332 bytes.
 *
 * What it does: 80 instructions; 17 call(s) to 0x02224434, 0x01ffa8c8, 0x0203d2ec, +14 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x140 -> constant 0x0224677c (image word 0x0224677c)
 *   pool +0x144 -> native_data_0222fdf0 (image word 0x0222fdf0)
 *   pool +0x148 -> constant 0x02246720 (image word 0x02246720)
 *   back edge +0x20 -> +0x14
 *   back edge +0x60 -> +0x40
 *   back edge +0x6c -> +0x40
 *   back edge +0x7c -> +0x40
 *   back edge +0x8c -> +0x40
 *   branch +0xc0 -> +0x12c
 *   back edge +0x138 -> +0xb4
 *   test +0x18 cmp r1, #3
 *   test +0x5c cmp r0, r1
 *   test +0x68 cmp r0, r1
 *   test +0x78 cmp r0, #0
 *   test +0x84 cmp r10, #3
 *   test +0x98 cmp r0, #0
 *   test +0xbc cmp r0, #0
 *   test +0x124 cmp r7, #3
 *   test +0x134 cmp r8, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224420; the literal pool and
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

extern void native_fn_01ffa8c8(void);
extern void native_fn_0203d2ec(void);
extern u8 native_data_0222fdf0[];
extern void native_fn_0203d294(void);
extern void native_fn_022243ec(void);
extern void native_fn_01ffa8d8(void);
extern void native_fn_01ffa394(void);
extern void native_fn_0205dc70(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0222456c(void);


asm u32 native_ov000_02224420 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r7, #0
    ldr r2, =0x0224677c
    mov r1, r7
    mvn r0, #0
ov000_02224420_L14:
    add r1, r1, #1
    cmp r1, #3
    strb r0, [r2], #1
    blt ov000_02224420_L14
    bl native_fn_01ffa8c8
    bl native_fn_0203d2ec
    ldr r9, =0x0224677c
    ldr r5, =native_data_0222fdf0
    ldr r4, =0x02246720
    mov r10, #0
    mov r6, #20
ov000_02224420_L40:
    mov r0, r6
    bl native_fn_0203d294
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    add r2, r5, r8, lsl #3
    ldrh r1, [r4, #4]
    ldrsb r0, [r2, #6]
    cmp r0, r1
    bgt ov000_02224420_L40
    ldrsb r0, [r2, #7]
    cmp r0, r1
    blt ov000_02224420_L40
    mov r0, r8
    bl native_fn_022243ec
    cmp r0, #0
    beq ov000_02224420_L40
    add r10, r10, #1
    cmp r10, #3
    strb r8, [r9], #1
    blt ov000_02224420_L40
    mov r8, #0
    bl native_fn_01ffa8d8
    cmp r0, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r6, =0x0224677c
    mov r5, #16
    mov r4, #13
    mov r10, #20
    mov r11, #255
ov000_02224420_Lb4:
    mov r0, r8
    bl native_fn_01ffa394
    cmp r0, #0
    bne ov000_02224420_L12c
    ldrsb r2, [r6, r7]
    mov r0, r5
    mov r1, r4
    add r2, r2, #40
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_0205dc70
    mov r9, r0
    and r0, r8, #255
    bl native_fn_01ffb4ec
    mov r1, r0
    mov r0, r9
    mov r2, r10
    bl native_fn_02008e0c
    and r0, r8, #255
    bl native_fn_01ffb4ec
    ldrsb r1, [r6, r7]
    mov r9, r0
    bl native_fn_0222456c
    mov r0, r11
    bl native_fn_0203d294
    strb r0, [r9, #0x167]
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #3
    movhs r7, #0
ov000_02224420_L12c:
    add r8, r8, #1
    bl native_fn_01ffa8d8
    cmp r8, r0
    blt ov000_02224420_Lb4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
