/* ov001 row 0x021f5078: 420 bytes.
 *
 * What it does: 104 instructions; 14 call(s) to 0x021db8d0, 0x0220e3a8, 0x021d8dec, +11 more; loops (back edge at +0x40); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (104 instructions, 14 calls, 9 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x1a0 -> native_data_0222dfe4 (image word 0x0222dfe4)
 *   back edge +0x40 -> +0x24
 *   branch +0x50 -> +0x194
 *   branch +0x7c -> +0x9c
 *   branch +0xa0 -> +0x114
 *   branch +0xcc -> +0xdc
 *   branch +0xd8 -> +0xec
 *   branch +0xe0 -> +0x114
 *   branch +0xe8 -> +0x114
 *   branch +0xf0 -> +0x10c
 *   branch +0xf8 -> +0x10c
 *   branch +0x108 -> +0x114
 *   back edge +0x11c -> +0x64
 *   branch +0x124 -> +0x170
 *   branch +0x16c -> +0x194
 *   test +0x4c cmp r0, #0
 *   test +0x70 cmp r10, #0
 *   test +0x9c cmp r4, r6
 *   test +0xc8 cmp r1, #0
 *   test +0xd4 cmp r2, r0
 *   test +0xdc cmp r1, #0
 *   test +0xe4 cmp r2, r1
 *   test +0xec cmp r4, r6
 *   test +0xf4 cmp r5, r11
 *   test +0x104 cmp r0, #0
 *   test +0x118 cmp r8, #16
 *   test +0x120 cmp r5, #0
 *   test +0x144 cmp r2, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f5078; the literal pool and
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

extern u8 native_data_0222dfe4[];
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0220e3a8(void);
extern void native_fn_021d8dec(void);
extern void native_fn_0203d294(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021f949c(void);
extern void native_fn_021ee78c(void);


asm u32 native_ov001_021f5078 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    mov r10, r0
    mov r0, #0
    ldr r4, =native_data_0222dfe4
    add r3, sp, #8
    mov r9, r1
    str r0, [sp, #0x4]
    mov r2, #16
ov001_021f5078_L24:
    ldrb r1, [r4]
    ldrb r0, [r4, #0x1]
    add r4, r4, #2
    strb r1, [r3]
    strb r0, [r3, #0x1]
    add r3, r3, #2
    subs r2, r2, #1
    bne ov001_021f5078_L24
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f5078_L194
    mvn r5, #0
    mov r6, #4
    mov r8, #0
    mov r11, r5
ov001_021f5078_L64:
    add r0, sp, #8
    ldrb r1, [r0, r8, lsl #1]
    ldr r0, [r9, #0x1e8]
    cmp r10, #0
    add r0, r0, r1
    ldrb r4, [r0, #0x86]
    beq ov001_021f5078_L9c
    mov r2, #0
    mov r3, r2
    str r3, [sp]
    mov r0, r10
    mov r3, r4
    bl native_fn_0220e3a8
    mov r4, r0
ov001_021f5078_L9c:
    cmp r4, r6
    bgt ov001_021f5078_L114
    add r0, sp, #8
    add r0, r0, r8, lsl #1
    ldrb r7, [r0, #0x1]
    mov r0, r7
    bl native_fn_021d8dec
    ldrsb r1, [r0]
    add r2, r9, r7
    add r2, r2, #512
    ldrsb r2, [r2, #44]
    cmp r1, #0
    blt ov001_021f5078_Ldc
    ldrsb r0, [r0, #1]
    cmp r2, r0
    blt ov001_021f5078_Lec
ov001_021f5078_Ldc:
    cmp r1, #0
    bge ov001_021f5078_L114
    cmp r2, r1
    ble ov001_021f5078_L114
ov001_021f5078_Lec:
    cmp r4, r6
    bne ov001_021f5078_L10c
    cmp r5, r11
    beq ov001_021f5078_L10c
    mov r0, #2
    bl native_fn_0203d294
    cmp r0, #0
    beq ov001_021f5078_L114
ov001_021f5078_L10c:
    mov r5, r8
    mov r6, r4
ov001_021f5078_L114:
    add r8, r8, #1
    cmp r8, #16
    blt ov001_021f5078_L64
    cmp r5, #0
    blt ov001_021f5078_L170
    add r0, sp, #9
    ldrb r4, [r0, r5, lsl #1]
    mov r0, r4
    bl native_fn_021d8dec
    ldrsb r2, [r0]
    mov r3, #0
    mov r1, r4
    cmp r2, #0
    ldrgesb r2, [r0, #1]
    mov r0, r9
    str r3, [sp]
    bl native_fn_021dbf98
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
    mov r0, #1
    str r0, [sp, #0x4]
    b ov001_021f5078_L194
ov001_021f5078_L170:
    mov r0, #242
    mov r1, #1
    bl native_fn_021f949c
    mov r1, #0
    mov r0, r9
    mov r2, r1
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee78c
ov001_021f5078_L194:
    ldr r0, [sp, #0x4]
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
