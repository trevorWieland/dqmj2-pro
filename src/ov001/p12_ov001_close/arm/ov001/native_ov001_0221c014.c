/* ov001 row 0x0221c014: 264 bytes.
 *
 * What it does: 66 instructions; 11 call(s) to 0x021db8d0, 0x021dbd3c, 0x021db8d0, +8 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 11 calls (66 instructions, 11 calls, 3 branches, 11 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x54
 *   branch +0x60 -> +0x74
 *   back edge +0x84 -> +0x2c
 *   branch +0xc8 -> +0xdc
 *   back edge +0xe8 -> +0xbc
 *   test +0x34 cmp r0, #0
 *   test +0x5c cmp r0, #0
 *   test +0x78 cmp r11, #3
 *   test +0xc4 cmp r0, #0
 *   test +0xe0 cmp r7, #3
 *   test +0xf8 cmp r6, r0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221c014; the literal pool and
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
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_02026144(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221c014 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r8, [r0, #0x8]
    mov r1, #0
    ldr r9, [r0, #0x4]
    str r1, [sp]
    mov r4, r1
    mov r5, r1
    mov r6, r1
    mov r7, r1
    mov r11, r1
    mov r10, r8
ov001_0221c014_L2c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221c014_L54
    mov r0, r9
    bl native_fn_021dbd3c
    ldr r1, [sp]
    add r6, r6, #1
    add r0, r1, r0
    str r0, [sp]
ov001_0221c014_L54:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221c014_L74
    mov r0, r10
    bl native_fn_021dbd8c
    add r4, r4, r0
    add r7, r7, #1
ov001_0221c014_L74:
    add r11, r11, #1
    cmp r11, #3
    add r9, r9, #1088
    add r10, r10, #1088
    blt ov001_0221c014_L2c
    ldr r0, [sp]
    mov r1, r6
    bl native_fn_02026144
    mov r6, r0
    mov r0, r4
    mov r1, r7
    bl native_fn_02026144
    add r0, r0, r0, lsl #1
    mov r4, #0
    add r1, r6, r6, lsl #1
    add r0, r0, r0, lsr #31
    mov r7, r4
    sub r6, r1, r0, asr #1
ov001_0221c014_Lbc:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221c014_Ldc
    mov r0, r8
    bl native_fn_021dbd24
    add r5, r5, r0
    add r4, r4, #1
ov001_0221c014_Ldc:
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #1088
    blt ov001_0221c014_Lbc
    mov r0, r5
    mov r1, r4
    bl native_fn_02026144
    cmp r6, r0
    movge r0, #1
    movlt r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
