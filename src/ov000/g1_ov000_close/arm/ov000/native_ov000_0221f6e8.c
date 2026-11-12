/* ov000 row 0x0221f6e8: 236 bytes.
 *
 * What it does: 58 instructions; 8 call(s) to 0x0207cd98, 0x02062a10, 0x02062a10, +5 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> constant 0x022463b0 (image word 0x022463b0)
 *   branch +0x1c -> +0xc8
 *   branch +0x2c -> +0x54
 *   branch +0x3c -> +0x5c
 *   branch +0x50 -> +0x5c
 *   branch +0x58 -> +0xc4
 *   branch +0x84 -> +0xc4
 *   branch +0x90 -> +0xac
 *   branch +0xa8 -> +0xc4
 *   branch +0xd0 -> +0xdc
 *   back edge +0xd8 -> +0x20
 *   test +0x38 cmp r9, r0
 *   test +0x4c cmp r0, #2
 *   test +0x7c cmp r1, r0
 *   test +0x8c cmp r0, #2
 *   test +0xa0 cmp r0, #2
 *   test +0xbc cmp r0, #0
 *   test +0xcc cmp r5, r0
 *   test +0xd4 cmp r5, #100
 *   test +0xdc cmp r0, #100
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221f6e8; the literal pool and
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

extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_02220778(void);


asm u32 native_ov000_0221f6e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r6, #0
    mov r10, r0
    mov r9, r1
    mov r5, r6
    ldr r4, =0x022463b0
    mov r11, #132
    b ov000_0221f6e8_Lc8
ov000_0221f6e8_L20:
    mov r0, r5
    bl native_fn_0207cd98
    movs r7, r0
    beq ov000_0221f6e8_L54
    bl native_fn_02062a10
    ldrb r0, [r0, #0x1b]
    cmp r9, r0
    beq ov000_0221f6e8_L5c
    mov r0, r7
    bl native_fn_02062a10
    ldrb r0, [r0, #0x1b]
    cmp r0, #2
    beq ov000_0221f6e8_L5c
ov000_0221f6e8_L54:
    add r6, r6, #1
    b ov000_0221f6e8_Lc4
ov000_0221f6e8_L5c:
    ldr r0, [r4, #0xc]
    ldr r1, [r4, #0x1c]
    rsb r0, r0, #1
    mla r8, r0, r11, r1
    mov r0, r7
    bl native_fn_02062a10
    ldr r1, [r8, #0x14]
    ldr r0, [r0, #0x14]
    cmp r1, r0
    addeq r6, r6, #1
    beq ov000_0221f6e8_Lc4
    ldrb r0, [r8, #0x1b]
    cmp r0, #2
    bne ov000_0221f6e8_Lac
    mov r0, r7
    bl native_fn_02062a10
    ldrb r0, [r0, #0x1b]
    cmp r0, #2
    addeq r6, r6, #1
    beq ov000_0221f6e8_Lc4
ov000_0221f6e8_Lac:
    mov r0, r7
    bl native_fn_02062a10
    ldrsh r0, [r0, #24]
    bl native_fn_02220778
    cmp r0, #0
    addeq r6, r6, #1
ov000_0221f6e8_Lc4:
    add r5, r5, #1
ov000_0221f6e8_Lc8:
    add r0, r10, r6
    cmp r5, r0
    bgt ov000_0221f6e8_Ldc
    cmp r5, #100
    blt ov000_0221f6e8_L20
ov000_0221f6e8_Ldc:
    cmp r0, #100
    mvnge r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
