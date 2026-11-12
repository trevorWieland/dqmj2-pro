/* ov001 row 0x0220bd30: 184 bytes.
 *
 * What it does: 46 instructions; 6 call(s) to 0x02065d88, 0x021db438, 0x021db438, +3 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 6 calls (46 instructions, 6 calls, 4 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0x44
 *   branch +0x40 -> +0x54
 *   branch +0x60 -> +0xb0
 *   branch +0x78 -> +0xa0
 *   branch +0x8c -> +0xa0
 *   back edge +0xac -> +0x70
 *   test +0x24 cmp r0, #1
 *   test +0x54 cmp r7, #0
 *   test +0x5c cmpgt r7, #0
 *   test +0x74 cmp r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0xa4 cmp r6, r7
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220bd30; the literal pool and
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

extern void native_fn_02065d88(void);
extern void native_fn_021db438(void);
extern void native_fn_0220bb7c(void);


asm u32 native_ov001_0220bd30 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r2
    mov r6, r0
    mov r0, r10
    mov r5, r1
    mov r4, r3
    mov r8, #0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x30]
    cmp r0, #1
    mov r0, r6
    bne ov001_0220bd30_L44
    mov r1, r8
    bl native_fn_021db438
    mov r9, r0
    mov r7, #3
    b ov001_0220bd30_L54
ov001_0220bd30_L44:
    mov r1, r5
    bl native_fn_021db438
    mov r9, r0
    mov r7, #1
ov001_0220bd30_L54:
    cmp r7, #0
    mov r6, #0
    cmpgt r7, #0
    ble ov001_0220bd30_Lb0
    and r5, r4, #255
    mov r4, r6
    mov r11, #1
ov001_0220bd30_L70:
    ldrb r0, [r9, #0x31c]
    cmp r0, #0
    beq ov001_0220bd30_La0
    mov r0, r9
    mov r1, r10
    bl native_fn_0220bb7c
    cmp r0, #0
    beq ov001_0220bd30_La0
    strb r5, [r9, #0x31d]
    add r0, r9, #768
    mov r8, r11
    strh r4, [r0, #32]
ov001_0220bd30_La0:
    add r6, r6, #1
    cmp r6, r7
    add r9, r9, #1088
    blt ov001_0220bd30_L70
ov001_0220bd30_Lb0:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
