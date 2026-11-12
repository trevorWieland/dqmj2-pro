/* ov001 row 0x02211f78: 256 bytes.
 *
 * What it does: 64 instructions; 11 call(s) to 0x02211fe4, 0x0205f98c, 0x02211fd0, +8 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 11 calls (64 instructions, 11 calls, 2 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x6c
 *   branch +0x3c -> +0x58
 *   back edge +0x68 -> +0x24
 *   branch +0x8c -> +0xf0
 *   branch +0x9c -> +0xd4
 *   back edge +0xd0 -> +0xa8
 *   branch +0xec -> +0xf8
 *   test +0x14 cmp r0, #0
 *   test +0x38 cmp r1, #0
 *   test +0x64 cmp r7, r0
 *   test +0x88 cmp r0, #0
 *   test +0x98 cmp r0, #0
 *   test +0xcc cmp r6, r0
 *   test +0xd8 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02211f78; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_02048a6c(void);
extern void native_fn_02048a44(void);


asm u32 native_ov001_02211f78 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r9, r0
    ldrb r0, [r9, #0x22]
    mov r8, #0
    mov r7, r8
    cmp r0, #0
    bls ov001_02211f78_L6c
    mov r5, r8
    mvn r4, #0
ov001_02211f78_L24:
    ldr r0, [r9, #0x1c]
    mov r1, r7
    bl native_fn_0205f98c
    mov r6, r0
    ldr r1, [r6, #0x84]
    cmp r1, #0
    ble ov001_02211f78_L58
    mov r1, r5
    mov r2, r4
    bl native_fn_02048a6c
    ldr r0, [r6, #0x84]
    sub r0, r0, #1
    str r0, [r6, #0x84]
ov001_02211f78_L58:
    ldrb r0, [r9, #0x22]
    add r1, r7, #1
    and r7, r1, #255
    cmp r7, r0
    blo ov001_02211f78_L24
ov001_02211f78_L6c:
    ldr r0, [r9, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    add r0, r0, #8
    mov r1, #1
    bl native_fn_02048a44
    ldrsh r0, [r9, #38]
    cmp r0, #0
    bgt ov001_02211f78_Lf0
    ldrb r0, [r9, #0x22]
    mov r6, #0
    cmp r0, #0
    bls ov001_02211f78_Ld4
    mov r5, r6
    mvn r4, #0
ov001_02211f78_La8:
    ldr r0, [r9, #0x1c]
    mov r1, r6
    bl native_fn_0205f98c
    mov r1, r5
    mov r2, r4
    bl native_fn_02048a6c
    add r1, r6, #1
    ldrb r0, [r9, #0x22]
    and r6, r1, #255
    cmp r6, r0
    blo ov001_02211f78_La8
ov001_02211f78_Ld4:
    ldrsb r0, [r9, #36]
    cmp r0, #0
    ldrsb r0, [r9, #36]
    movle r8, #1
    sub r0, r0, #1
    strb r0, [r9, #0x24]
    b ov001_02211f78_Lf8
ov001_02211f78_Lf0:
    sub r0, r0, #2
    strh r0, [r9, #38]
ov001_02211f78_Lf8:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
