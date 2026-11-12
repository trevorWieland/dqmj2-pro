/* ov001 row 0x021f1abc: 228 bytes.
 *
 * What it does: 54 instructions; 3 call(s) to 0x021f1aa8, 0x021f1a38, 0x021f1adc; loops (back edge at +0xac); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (54 instructions, 6 calls, 8 branches, 3 back edges, 3 literal slots).
 *
 *   pool +0xd8 -> native_data_0222df58 (image word 0x0222df58)
 *   pool +0xdc -> constant 0x02238f9c (image word 0x02238f9c)
 *   pool +0xe0 -> constant 0x020feae8 (image word 0x020feae8)
 *   branch +0x30 -> +0xb8
 *   branch +0x3c -> +0x54
 *   branch +0x44 -> +0x6c
 *   branch +0x4c -> +0xa8
 *   branch +0x50 -> +0xb8
 *   branch +0x68 -> +0xb8
 *   branch +0x84 -> +0xb8
 *   branch +0xa4 -> +0xb8
 *   back edge +0xc4 -> +0x20
 *   test +0x2c cmp r1, #127
 *   test +0x38 cmp r0, #0
 *   test +0x40 cmp r0, #1
 *   test +0x48 cmp r0, #2
 *   test +0x80 cmp r0, #0
 *   test +0xc0 cmp r9, #32
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1abc; the literal pool and
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

extern u8 native_data_0222df58[];
extern void native_fn_021f1aa8(void);
extern void native_fn_021f1a38(void);


asm u32 native_ov001_021f1abc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r7, =native_data_0222df58
    ldr r8, =0x02238f9c
    mov r9, #0
    mov r5, #2
    mov r6, #1
    mov r11, #12
    mov r4, #72
ov001_021f1abc_L20:
    mul r0, r9, r4
    ldr r1, [r8, r0]
    add r10, r8, r0
    cmp r1, #127
    beq ov001_021f1abc_Lb8
    ldr r0, [r10, #0x4]
    cmp r0, #0
    beq ov001_021f1abc_L54
    cmp r0, #1
    beq ov001_021f1abc_L6c
    cmp r0, #2
    beq ov001_021f1abc_La8
    b ov001_021f1abc_Lb8
ov001_021f1abc_L54:
    mul r0, r1, r11
    ldr r1, [r7, r0]
    mov r0, r10
    blx r1
    str r6, [r10, #0x4]
    b ov001_021f1abc_Lb8
ov001_021f1abc_L6c:
    mov r0, #12
    mla r0, r1, r0, r7
    ldr r1, [r0, #0x4]
    mov r0, r10
    blx r1
    cmp r0, #0
    beq ov001_021f1abc_Lb8
    ldr r2, [r10]
    mov r1, #12
    mla r1, r2, r1, r7
    ldr r1, [r1, #0x8]
    mov r0, r10
    blx r1
    str r5, [r10, #0x4]
    b ov001_021f1abc_Lb8
ov001_021f1abc_La8:
    mov r0, r10
    bl native_fn_021f1aa8
    mov r0, r10
    bl native_fn_021f1a38
ov001_021f1abc_Lb8:
    add r0, r9, #1
    and r9, r0, #255
    cmp r9, #32
    blo ov001_021f1abc_L20
    ldr r0, =0x020feae8
    mov r1, #1
    str r1, [r0, #0x540]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
