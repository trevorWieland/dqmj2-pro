/* ov001 row 0x0221a200: 248 bytes.
 *
 * What it does: 62 instructions; 11 call(s) to 0x021db8d0, 0x021e2b1c, 0x02218498, +8 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 11 calls (62 instructions, 11 calls, 5 branches, 10 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0xdc
 *   branch +0x38 -> +0x4c
 *   branch +0x48 -> +0xdc
 *   branch +0x5c -> +0xdc
 *   branch +0x7c -> +0xdc
 *   branch +0x94 -> +0xd0
 *   back edge +0xd8 -> +0x84
 *   back edge +0xe8 -> +0x18
 *   test +0x20 cmp r0, #0
 *   test +0x2c cmpne r0, r1
 *   test +0x34 cmp r6, #0
 *   test +0x44 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x74 cmp r9, #0
 *   test +0x90 tst r0, #2
 *   test +0xc0 cmp r4, r0
 *   test +0xd4 cmp r8, r9
 *   test +0xe0 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221a200; the literal pool and
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
extern void native_fn_021e2b1c(void);
extern void native_fn_02218498(void);
extern void native_fn_02218430(void);
extern void native_fn_022180e0(void);
extern void native_fn_021dbd30(void);
extern void native_fn_0207b244(void);


asm u32 native_ov001_0221a200 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #200
    ldr r11, [r0]
    ldr r6, [r0, #0x14]
    ldr r10, [r0, #0x4]
    mov r7, #0
ov001_0221a200_L18:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r1, [r10, #0x31f]
    ldrneb r0, [r11, #0x31f]
    cmpne r0, r1
    beq ov001_0221a200_Ldc
    cmp r6, #0
    beq ov001_0221a200_L4c
    ldrb r0, [r10, #0x31e]
    bl native_fn_021e2b1c
    cmp r0, #0
    bne ov001_0221a200_Ldc
ov001_0221a200_L4c:
    mov r0, r10
    mov r1, #2
    bl native_fn_02218498
    cmp r0, #0
    beq ov001_0221a200_Ldc
    add r1, sp, #0
    mov r0, r10
    mov r2, #200
    bl native_fn_02218430
    mov r9, r0
    cmp r9, #0
    mov r8, #0
    ble ov001_0221a200_Ldc
    add r5, sp, #0
ov001_0221a200_L84:
    ldr r0, [r5, r8, lsl #2]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r0, #2
    beq ov001_0221a200_Ld0
    mov r0, r10
    bl native_fn_021dbd30
    mov r4, r0
    mov r0, r10
    bl native_fn_021dbd30
    ldr r2, [r10, #0x1e8]
    mov r1, r0
    ldr r0, [r5, r8, lsl #2]
    add r2, r2, #70
    bl native_fn_0207b244
    cmp r4, r0
    addlt sp, sp, #200
    movlt r0, #1
    ldmltia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0221a200_Ld0:
    add r8, r8, #1
    cmp r8, r9
    blt ov001_0221a200_L84
ov001_0221a200_Ldc:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_0221a200_L18
    mov r0, #0
    add sp, sp, #200
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
