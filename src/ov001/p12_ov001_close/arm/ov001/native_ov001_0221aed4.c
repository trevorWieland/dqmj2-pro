/* ov001 row 0x0221aed4: 208 bytes.
 *
 * What it does: 52 instructions; 9 call(s) to 0x021db8d0, 0x021dbd3c, 0x021db8d0, +6 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 9 calls (52 instructions, 9 calls, 2 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x44
 *   branch +0x50 -> +0x70
 *   back edge +0x80 -> +0x24
 *   test +0x2c cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x74 cmp r8, #3
 *   test +0xc0 cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221aed4; the literal pool and
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
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_021dbd24(void);
extern void native_fn_02026144(void);


asm u32 native_ov001_0221aed4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r11, #0
    ldr r9, [r0, #0x8]
    ldr r10, [r0, #0x4]
    mov r4, r11
    mov r5, r11
    mov r6, r11
    mov r7, r11
    mov r8, r11
ov001_0221aed4_L24:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221aed4_L44
    mov r0, r9
    bl native_fn_021dbd3c
    add r11, r11, r0
    add r7, r7, #1
ov001_0221aed4_L44:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221aed4_L70
    mov r0, r10
    bl native_fn_021dbd8c
    add r4, r4, r0
    mov r0, r10
    bl native_fn_021dbd24
    add r5, r5, r0
    add r6, r6, #1
ov001_0221aed4_L70:
    add r8, r8, #1
    cmp r8, #3
    add r9, r9, #1088
    add r10, r10, #1088
    blt ov001_0221aed4_L24
    mov r0, r11
    mov r1, r7
    bl native_fn_02026144
    mov r7, r0
    mov r0, r4
    mov r1, r6
    bl native_fn_02026144
    mov r4, r0
    mov r0, r5
    mov r1, r6
    bl native_fn_02026144
    add r1, r4, r4, lsl #1
    add r2, r7, r7, lsl #1
    add r1, r1, r1, lsr #31
    sub r1, r2, r1, asr #1
    cmp r1, r0
    movge r0, #1
    movlt r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
