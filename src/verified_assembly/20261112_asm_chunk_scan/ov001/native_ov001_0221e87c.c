/* ov001 row 0x0221e87c: 204 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xc8 -> native_data_0222e138 (image word 0x0222e138)
 *   branch +0x64 -> +0xb0
 *   branch +0x78 -> +0xa4
 *   branch +0xa0 -> +0xb0
 *   back edge +0xac -> +0x6c
 *   back edge +0xb8 -> +0x58
 *   test +0x60 cmp r12, #0
 *   test +0x74 cmp r1, r0
 *   test +0x8c cmp r0, r7
 *   test +0xa8 cmp r3, r12
 *   test +0xb4 cmp r2, #8
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221e87c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0222e138[];
extern void native_fn_021dbd30(void);
extern void native_fn_0207b244(void);


asm u32 native_ov001_0221e87c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #32
    ldr r6, [r0]
    ldr r5, =native_data_0222e138
    add r4, sp, #0
    ldmia r5!, {r0, r1, r2, r3}
    stmia r4!, {r0, r1, r2, r3}
    ldmia r5, {r0, r1, r2, r3}
    stmia r4, {r0, r1, r2, r3}
    mov r0, r6
    bl native_fn_021dbd30
    ldr r1, [r6, #0x1e8]
    mov r4, r0
    add r2, r1, #70
    mov r0, #172
    mov r1, r4
    bl native_fn_0207b244
    mov r2, #0
    sub r7, r4, r0
    add r4, sp, #0
    mov r8, #8
    mov r5, r2
ov001_0221e87c_L58:
    ldrb r12, [r6, #0x323]
    mov r3, r5
    cmp r12, #0
    ble ov001_0221e87c_Lb0
    ldr r0, [r4, r2, lsl #2]
ov001_0221e87c_L6c:
    add r1, r6, r3
    ldrb r1, [r1, #0x35e]
    cmp r1, r0
    bne ov001_0221e87c_La4
    ldr r2, [r6, #0x1e8]
    mov r1, r7
    add r2, r2, #70
    bl native_fn_0207b244
    cmp r0, r7
    addle sp, sp, #32
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
    mov r2, r8
    b ov001_0221e87c_Lb0
ov001_0221e87c_La4:
    add r3, r3, #1
    cmp r3, r12
    blt ov001_0221e87c_L6c
ov001_0221e87c_Lb0:
    add r2, r2, #1
    cmp r2, #8
    blt ov001_0221e87c_L58
    mov r0, #0
    add sp, sp, #32
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
