/* ov001 row 0x022217a4: 200 bytes.
 *
 * What it does: 49 instructions; 8 call(s) to 0x021db8d0, 0x0207b674, 0x02221820, +5 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (49 instructions, 8 calls, 3 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xc4 -> native_data_0222e118 (image word 0x0222e118)
 *   branch +0x28 -> +0x8c
 *   branch +0x38 -> +0x8c
 *   branch +0x58 -> +0x7c
 *   branch +0x78 -> +0x8c
 *   back edge +0x88 -> +0x44
 *   back edge +0x98 -> +0x1c
 *   branch +0xa0 -> +0xbc
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x80 cmp r5, #29
 *   test +0x90 cmp r4, #3
 *   test +0x9c cmp r7, #0
 *   test +0xb0 cmp r0, #5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022217a4; the literal pool and
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

extern void native_fn_021db8d0(void);
extern u8 native_data_0222e118[];
extern void native_fn_0207b674(void);
extern void native_fn_022189cc(void);
extern void native_fn_02026144(void);


asm u32 native_ov001_022217a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r6, #0
    ldr r11, [r0]
    ldr r8, [r0, #0xc]
    ldr r9, [r0, #0x8]
    mov r7, r6
    mov r4, r6
ov001_022217a4_L1c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022217a4_L8c
    add r0, r9, #512
    ldrsb r0, [r0, #97]
    cmp r0, #0
    bne ov001_022217a4_L8c
    ldr r10, =native_data_0222e118
    mov r5, #0
ov001_022217a4_L44:
    ldr r1, [r9, #0x1e8]
    ldrb r0, [r10]
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_022217a4_L7c
    mov r0, r11
    mov r1, r9
    mov r2, r8
    mov r3, #1
    bl native_fn_022189cc
    add r6, r6, r0
    add r7, r7, #1
    b ov001_022217a4_L8c
ov001_022217a4_L7c:
    add r5, r5, #1
    cmp r5, #29
    add r10, r10, #1
    blt ov001_022217a4_L44
ov001_022217a4_L8c:
    add r4, r4, #1
    cmp r4, #3
    add r9, r9, #1088
    blt ov001_022217a4_L1c
    cmp r7, #0
    ble ov001_022217a4_Lbc
    mov r0, r6
    mov r1, r7
    bl native_fn_02026144
    cmp r0, #5
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_022217a4_Lbc:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
