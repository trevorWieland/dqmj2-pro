/* ov001 row 0x021eedfc: 292 bytes.
 *
 * What it does: 71 instructions; 3 call(s) to 0x021eeab8, 0x021eeb60, 0x0205c904; loops (back edge at +0x40); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (71 instructions, 3 calls, 7 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0x11c -> constant 0x02238e54 (image word 0x02238e54)
 *   pool +0x120 -> native_data_0222ec88 (image word 0x0222ec88)
 *   branch +0x2c -> +0x64
 *   branch +0x54 -> +0x64
 *   branch +0x70 -> +0xa0
 *   branch +0x8c -> +0xc8
 *   branch +0x9c -> +0xc8
 *   branch +0xa4 -> +0xc8
 *   branch +0xd4 -> +0xfc
 *   test +0x10 cmp r1, #0
 *   test +0x28 cmp r1, #10
 *   test +0x44 cmp r0, #0
 *   test +0x6c cmp r1, #20
 *   test +0x88 cmp r0, #0
 *   test +0xa0 cmp r1, #30
 *   test +0xd0 cmp r1, #50
 *   test +0xe4 cmp r1, #19
 *   test +0x104 cmp r1, #100
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eedfc; the literal pool and
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

extern u8 native_data_0222ec88[];
extern void native_fn_021eeab8(void);
extern void native_fn_021eeb60(void);
extern void native_fn_0205c904(void);


asm u32 native_ov001_021eedfc (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x02238e54
    mov r4, #0
    ldrb r1, [r0]
    cmp r1, #0
    streqb r4, [r0, #0x1]
    moveq r1, #10
    streqb r1, [r0]
    ldr r0, =0x02238e54
    ldrb r1, [r0]
    cmp r1, #10
    bne ov001_021eedfc_L64
    ldrb r1, [r0, #0x1]
    ldr r0, =native_data_0222ec88
    mov r1, r1, lsl #1
    ldrh r0, [r0, r1]
    bl native_fn_021eeab8
    cmp r0, #0
    ldreq r0, =0x02238e54
    moveq r1, #50
    streqb r1, [r0]
    beq ov001_021eedfc_L64
    ldr r0, =0x02238e54
    mov r1, #20
    strb r1, [r0]
ov001_021eedfc_L64:
    ldr r0, =0x02238e54
    ldrb r1, [r0]
    cmp r1, #20
    bne ov001_021eedfc_La0
    ldrb r1, [r0, #0x1]
    ldr r0, =native_data_0222ec88
    mov r1, r1, lsl #1
    ldrh r0, [r0, r1]
    bl native_fn_021eeb60
    cmp r0, #0
    beq ov001_021eedfc_Lc8
    ldr r0, =0x02238e54
    mov r1, #30
    strb r1, [r0]
    b ov001_021eedfc_Lc8
ov001_021eedfc_La0:
    cmp r1, #30
    bne ov001_021eedfc_Lc8
    ldrb r1, [r0, #0x1]
    ldr r0, =native_data_0222ec88
    mov r1, r1, lsl #1
    ldrh r0, [r0, r1]
    bl native_fn_0205c904
    ldr r0, =0x02238e54
    mov r1, #50
    strb r1, [r0]
ov001_021eedfc_Lc8:
    ldr r0, =0x02238e54
    ldrb r1, [r0]
    cmp r1, #50
    bne ov001_021eedfc_Lfc
    ldrb r1, [r0, #0x1]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #19
    strb r2, [r0, #0x1]
    movhs r1, #100
    strhsb r1, [r0]
    movlo r1, #10
    strlob r1, [r0]
ov001_021eedfc_Lfc:
    ldr r0, =0x02238e54
    ldrb r1, [r0]
    cmp r1, #100
    moveq r1, #0
    moveq r4, #1
    streqb r1, [r0]
    mov r0, r4
    ldmia sp!, {r4, pc}
}
