/* ov000 row 0x022245bc: 324 bytes.
 *
 * What it does: 81 instructions; 9 call(s) to 0x020894bc, 0x01ffb4ec, 0x02008d78, +6 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x60 -> +0x78
 *   back edge +0x8c -> +0x58
 *   branch +0xcc -> +0x12c
 *   branch +0xf8 -> +0x11c
 *   back edge +0x128 -> +0xec
 *   back edge +0x138 -> +0xb8
 *   test +0x14 tst r0, #536870912
 *   test +0x5c cmp r0, r9
 *   test +0x7c cmp r4, #6
 *   test +0xc8 cmp r1, r0
 *   test +0xf4 cmp r1, r0
 *   test +0x120 cmp r7, #6
 *   test +0x130 cmp r10, #6
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022245bc; the literal pool and
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

extern void native_fn_020894bc(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_01ffa5fc(void);


asm u32 native_ov000_022245bc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #324
    mov r8, r0
    bl native_fn_020894bc
    ldr r0, [r0]
    tst r0, #536870912
    addeq sp, sp, #324
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    and r0, r8, #255
    bl native_fn_01ffb4ec
    str r0, [sp, #0x4]
    add r0, sp, #12
    mov r1, #0
    mov r2, #312
    bl native_fn_02008d78
    ldr r5, [sp, #0x4]
    add r6, sp, #12
    mov r0, r5
    add r7, r0, #20
    mov r4, #0
    mov r10, #52
    mvn r9, #0
ov000_022245bc_L58:
    ldrsh r0, [r5, #24]
    cmp r0, r9
    beq ov000_022245bc_L78
    mov r0, r7
    mov r1, r6
    mov r2, r10
    bl native_fn_02008e0c
    strh r9, [r5, #24]
ov000_022245bc_L78:
    add r4, r4, #1
    cmp r4, #6
    add r5, r5, #52
    add r6, r6, #52
    add r7, r7, #52
    blt ov000_022245bc_L58
    mov r0, r8
    mov r1, #8
    bl native_fn_01ffa5fc
    str r0, [sp]
    ldr r0, [sp, #0x4]
    mov r10, #0
    add r8, r0, #20
    mvn r0, #0
    mov r11, #52
    str r0, [sp, #0x8]
ov000_022245bc_Lb8:
    ldr r0, [sp]
    add r6, r0, r10, lsl #2
    ldr r1, [r6, #0x4]
    ldr r0, [sp, #0x8]
    cmp r1, r0
    beq ov000_022245bc_L12c
    ldr r0, [sp, #0x4]
    mov r7, #0
    add r1, r0, r10, lsl #2
    ldr r0, [sp]
    add r9, sp, #12
    add r5, r0, r10, lsl #1
    add r4, r1, #256
ov000_022245bc_Lec:
    ldr r1, [r9]
    ldr r0, [r6, #0x4]
    cmp r1, r0
    bne ov000_022245bc_L11c
    ldrsh r2, [r5, #28]
    mov r0, r9
    mov r1, r8
    strh r2, [r4, #76]
    ldrsh r3, [r5, #40]
    mov r2, r11
    strh r3, [r4, #78]
    bl native_fn_02008e0c
ov000_022245bc_L11c:
    add r7, r7, #1
    cmp r7, #6
    add r9, r9, #52
    blt ov000_022245bc_Lec
ov000_022245bc_L12c:
    add r10, r10, #1
    cmp r10, #6
    add r8, r8, #52
    blt ov000_022245bc_Lb8
    add sp, sp, #324
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
