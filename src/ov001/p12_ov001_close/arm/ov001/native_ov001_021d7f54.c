/* ov001 row 0x021d7f54: 276 bytes.
 *
 * What it does: 69 instructions; 15 call(s) to 0x021db438, 0x021db8d0, 0x02044cdc, +12 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 15 calls (69 instructions, 15 calls, 12 branches, 10 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x68
 *   branch +0x44 -> +0x58
 *   back edge +0x74 -> +0x24
 *   branch +0x7c -> +0xa0
 *   branch +0x84 -> +0x94
 *   branch +0x90 -> +0xd8
 *   branch +0x9c -> +0xd8
 *   branch +0xa4 -> +0xb8
 *   branch +0xac -> +0xc4
 *   branch +0xb4 -> +0xd0
 *   branch +0xc0 -> +0xd8
 *   branch +0xcc -> +0xd8
 *   branch +0xe0 -> +0xfc
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r9, r0
 *   test +0x60 cmp r0, #0
 *   test +0x6c cmp r6, #3
 *   test +0x78 cmp r7, #0
 *   test +0x80 cmp r4, #1
 *   test +0xa0 cmp r9, #0
 *   test +0xa8 cmp r9, #1
 *   test +0xb0 cmp r9, #2
 *   test +0xd8 cmp r4, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d7f54; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021dbaac(void);
extern void native_fn_021d75d4(void);
extern void native_fn_021d77b0(void);
extern void native_fn_021d94cc(void);


asm u32 native_ov001_021d7f54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r9, #0
    mov r1, r9
    mov r4, r0
    mov r7, r9
    bl native_fn_021db438
    mov r8, r0
    mov r6, r9
    mov r5, #1
ov001_021d7f54_L24:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021d7f54_L68
    ldr r0, [r8, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r9, r0
    bgt ov001_021d7f54_L58
    ldr r0, [r8, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    mov r9, r0
ov001_021d7f54_L58:
    mov r0, r8
    bl native_fn_021dbaac
    cmp r0, #0
    movne r7, r5
ov001_021d7f54_L68:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    blt ov001_021d7f54_L24
    cmp r7, #0
    beq ov001_021d7f54_La0
    cmp r4, #1
    bne ov001_021d7f54_L94
    mov r0, #24
    bl native_fn_021d75d4
    b ov001_021d7f54_Ld8
ov001_021d7f54_L94:
    mov r0, #25
    bl native_fn_021d75d4
    b ov001_021d7f54_Ld8
ov001_021d7f54_La0:
    cmp r9, #0
    beq ov001_021d7f54_Lb8
    cmp r9, #1
    beq ov001_021d7f54_Lc4
    cmp r9, #2
    b ov001_021d7f54_Ld0
ov001_021d7f54_Lb8:
    mov r0, #21
    bl native_fn_021d75d4
    b ov001_021d7f54_Ld8
ov001_021d7f54_Lc4:
    mov r0, #22
    bl native_fn_021d75d4
    b ov001_021d7f54_Ld8
ov001_021d7f54_Ld0:
    mov r0, #23
    bl native_fn_021d75d4
ov001_021d7f54_Ld8:
    cmp r4, #0
    mvn r0, #0
    bne ov001_021d7f54_Lfc
    mov r1, #737280
    bl native_fn_021d77b0
    mov r0, #1
    mov r1, #0
    bl native_fn_021d94cc
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_021d7f54_Lfc:
    mov r1, #0
    bl native_fn_021d77b0
    mov r0, #0
    mov r1, #1
    bl native_fn_021d94cc
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
