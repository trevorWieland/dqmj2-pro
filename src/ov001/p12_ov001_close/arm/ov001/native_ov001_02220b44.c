/* ov001 row 0x02220b44: 244 bytes.
 *
 * What it does: 61 instructions; 10 call(s) to 0x021db8d0, 0x02218430, 0x02220c1c, +7 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 10 calls (61 instructions, 10 calls, 5 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0xd8
 *   branch +0x40 -> +0xd8
 *   branch +0x5c -> +0xcc
 *   branch +0x78 -> +0xcc
 *   branch +0xa4 -> +0xc0
 *   branch +0xac -> +0xcc
 *   branch +0xbc -> +0xcc
 *   back edge +0xd4 -> +0x4c
 *   back edge +0xe4 -> +0x14
 *   test +0x1c cmp r0, #0
 *   test +0x38 cmp r8, #0
 *   test +0x58 cmp r0, #0
 *   test +0x74 cmp r0, #1
 *   test +0xa0 cmp r0, #1
 *   test +0xa8 cmp r2, #0
 *   test +0xb8 cmp r0, #1
 *   test +0xd0 cmp r7, r8
 *   test +0xdc cmp r11, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02220b44; the literal pool and
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
extern void native_fn_02218430(void);
extern void native_fn_0207b004(void);
extern void native_fn_0207afec(void);


asm u32 native_ov001_02220b44 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #200
    ldr r6, [r0]
    ldr r10, [r0, #0x8]
    mov r11, #0
ov001_02220b44_L14:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02220b44_Ld8
    add r1, sp, #0
    mov r0, r10
    mov r2, #200
    bl native_fn_02218430
    mov r8, r0
    cmp r8, #0
    mov r7, #0
    ble ov001_02220b44_Ld8
    add r5, sp, #0
    mov r4, #8
ov001_02220b44_L4c:
    ldr r0, [r5, r7, lsl #2]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02220b44_Lcc
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_02220b44_Lcc
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_0207afec
    ldrb r9, [r0, #0x1f]
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_0207afec
    ldr r1, [r6, #0x1e8]
    ldrb r2, [r0, #0x20]
    add r0, r1, r9
    ldrb r0, [r0, #0x86]
    cmp r0, #1
    bls ov001_02220b44_Lc0
    cmp r2, #0
    beq ov001_02220b44_Lcc
    add r0, r1, r2
    ldrb r0, [r0, #0x86]
    cmp r0, #1
    bhi ov001_02220b44_Lcc
ov001_02220b44_Lc0:
    add sp, sp, #200
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02220b44_Lcc:
    add r7, r7, #1
    cmp r7, r8
    blt ov001_02220b44_L4c
ov001_02220b44_Ld8:
    add r11, r11, #1
    cmp r11, #3
    add r10, r10, #1088
    blt ov001_02220b44_L14
    mov r0, #0
    add sp, sp, #200
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
