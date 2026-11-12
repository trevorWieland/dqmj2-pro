/* ov001 row 0x0221fe5c: 332 bytes.
 *
 * What it does: 83 instructions; 11 call(s) to 0x02218430, 0x0221ff88, 0x0207afec, +8 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 11 calls (83 instructions, 11 calls, 5 branches, 10 back edges, 0 literal slots).
 *
 *   branch +0x40 -> +0x12c
 *   branch +0x60 -> +0x11c
 *   branch +0x7c -> +0xcc
 *   branch +0x98 -> +0xb8
 *   back edge +0xc4 -> +0x8c
 *   branch +0xc8 -> +0x11c
 *   branch +0xe8 -> +0x100
 *   back edge +0x10c -> +0xdc
 *   back edge +0x128 -> +0x44
 *   test +0x38 cmp r0, #0
 *   test +0x5c cmp r0, #1
 *   test +0x94 cmp r0, #0
 *   test +0xac cmp r0, r6
 *   test +0xbc cmp r9, #3
 *   test +0xe4 cmp r0, #0
 *   test +0x104 cmp r9, #3
 *   test +0x110 cmp r10, r6
 *   test +0x124 cmp r5, r0
 *   test +0x138 cmp r0, r1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221fe5c; the literal pool and
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

extern void native_fn_02218430(void);
extern void native_fn_0207afec(void);
extern void native_fn_021db8d0(void);
extern void native_fn_02218c34(void);


asm u32 native_ov001_0221fe5c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #212
    ldr r2, [r0, #0x8]
    ldr r4, [r0]
    ldr r0, [r0, #0xc]
    mov r6, #0
    str r2, [sp, #0x8]
    str r0, [sp, #0x4]
    add r1, sp, #12
    mov r0, r4
    mov r2, #200
    mov r7, r6
    bl native_fn_02218430
    str r0, [sp]
    cmp r0, #0
    mov r5, r6
    ble ov001_0221fe5c_L12c
ov001_0221fe5c_L44:
    add r0, sp, #12
    ldr r0, [r0, r5, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_0221fe5c_L11c
    add r0, sp, #12
    ldr r0, [r0, r5, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    bne ov001_0221fe5c_Lcc
    ldr r10, [sp, #0x8]
    mov r9, #0
    add r8, sp, #12
ov001_0221fe5c_L8c:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221fe5c_Lb8
    ldr r2, [r8, r5, lsl #2]
    mov r0, r4
    mov r1, r10
    bl native_fn_02218c34
    cmp r0, r6
    movge r6, r0
    movge r7, r5
ov001_0221fe5c_Lb8:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #1088
    blt ov001_0221fe5c_L8c
    b ov001_0221fe5c_L11c
ov001_0221fe5c_Lcc:
    mov r10, #0
    ldr r8, [sp, #0x8]
    mov r9, r10
    add r11, sp, #12
ov001_0221fe5c_Ldc:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221fe5c_L100
    ldr r2, [r11, r5, lsl #2]
    mov r0, r4
    mov r1, r8
    bl native_fn_02218c34
    add r10, r10, r0
ov001_0221fe5c_L100:
    add r9, r9, #1
    cmp r9, #3
    add r8, r8, #1088
    blt ov001_0221fe5c_Ldc
    cmp r10, r6
    movge r6, r10
    movge r7, r5
ov001_0221fe5c_L11c:
    ldr r0, [sp]
    add r5, r5, #1
    cmp r5, r0
    blt ov001_0221fe5c_L44
ov001_0221fe5c_L12c:
    add r0, sp, #12
    ldr r1, [r0, r7, lsl #2]
    ldr r0, [sp, #0x4]
    cmp r0, r1
    moveq r0, #1
    movne r0, #0
    add sp, sp, #212
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
