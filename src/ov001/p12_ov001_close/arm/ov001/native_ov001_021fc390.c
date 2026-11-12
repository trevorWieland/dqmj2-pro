/* ov001 row 0x021fc390: 432 bytes.
 *
 * What it does: 101 instructions; 17 call(s) to 0x0205fd80, 0x020656f0, 0x02049ad0, +14 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (101 instructions, 17 calls, 1 branch, 14 back edges, 7 literal slots).
 *
 *   pool +0x194 -> constant 0x02239c64 (image word 0x02239c64)
 *   pool +0x198 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x19c -> native_data_0222ed34 (image word 0x0222ed34)
 *   pool +0x1a0 -> constant 0x02239d6c (image word 0x02239d6c)
 *   pool +0x1a4 -> constant 0x02239d04 (image word 0x02239d04)
 *   pool +0x1a8 -> native_data_0222edcc (image word 0x0222edcc)
 *   pool +0x1ac -> constant 0x02239c9c (image word 0x02239c9c)
 *   back edge +0x48 -> +0x20
 *   back edge +0x68 -> +0x54
 *   back edge +0xec -> +0xd4
 *   branch +0x110 -> +0x144
 *   back edge +0x140 -> +0x11c
 *   back edge +0x18c -> +0x178
 *   test +0x44 cmp r7, #36
 *   test +0x64 cmp r4, #4
 *   test +0xe8 cmp r4, #3
 *   test +0x108 cmp r5, #0
 *   test +0x134 cmp r5, r0, asr #24
 *   test +0x184 cmp r0, #6
 *   0 block transfer(s), 19 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fc390; the literal pool and
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

extern void native_fn_0205fd80(void);
extern void native_fn_020656f0(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02045680(void);
extern void ov001_table_f0_entry_02202360(void);
extern u8 native_data_0222ed34[];
extern void native_fn_0220409c(void);
extern void native_fn_021fd140(void);
extern void ov001_mode_byte_021db530(void);
extern u8 native_data_0222edcc[];
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_02048fac(void);
extern void native_fn_02045738(void);


asm u32 native_ov001_021fc390 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r0, #1
    bl native_fn_0205fd80
    bl native_fn_020656f0
    mov r7, #0
    mov r6, #127
    mov r4, r7
    mvn r5, #0
ov001_021fc390_L20:
    mov r0, r7
    bl native_fn_02049ad0
    strb r6, [r0, #0x4]
    add r1, r7, #1
    strb r6, [r0, #0x5]
    mov r1, r1, lsl #24
    str r4, [r0]
    mov r7, r1, asr #24
    strb r5, [r0, #0x6]
    cmp r7, #36
    blt ov001_021fc390_L20
    ldr r1, =0x02239c64
    mov r2, #32
ov001_021fc390_L54:
    add r0, r4, #1
    mov r0, r0, lsl #24
    str r2, [r1, r4, lsl #2]
    mov r4, r0, asr #24
    cmp r4, #4
    blt ov001_021fc390_L54
    ldr r1, =0x02239c10
    mov r2, #30720
    mov r0, #0
    str r2, [r1, #0x60]
    bl native_fn_02045680
    ldr r1, =0x02239c10
    mov r2, #8
    strb r2, [r1, #0x4]
    mov r0, #0
    strb r0, [r1, #0xc]
    strb r2, [r1, #0xd]
    strb r0, [r1, #0xa]
    mov r2, #4
    strb r2, [r1, #0xe]
    bl ov001_table_f0_entry_02202360
    mov r3, #0
    strb r3, [r0, #0x13]
    ldr r1, =0x02239c10
    ldr r0, =native_data_0222ed34
    sub r2, r3, #1
    strb r3, [r1]
    strb r2, [r0, #0x1]
    bl native_fn_0220409c
    ldr r0, =0x02239d6c
    mov r4, #0
    str r4, [r0]
ov001_021fc390_Ld4:
    mov r0, r4
    bl native_fn_021fd140
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #3
    blt ov001_021fc390_Ld4
    ldr r1, =0x02239d04
    mov r2, #127
    mov r0, #0
    strb r2, [r1]
    bl ov001_mode_byte_021db530
    mov r5, r0
    cmp r5, #0
    mov r7, #0
    ble ov001_021fc390_L144
    ldr r6, =native_data_0222edcc
    mov r4, r7
ov001_021fc390_L11c:
    mov r0, r4
    mov r1, r7
    bl ov001_side_slot_record_021db438
    ldrb r1, [r0, #0x1fe]
    add r0, r7, #1
    mov r0, r0, lsl #24
    cmp r5, r0, asr #24
    strb r1, [r6], #1
    mov r7, r0, asr #24
    bgt ov001_021fc390_L11c
ov001_021fc390_L144:
    mov r0, #0
    mov r1, #32
    bl native_fn_02048fac
    mov r0, #1
    mov r1, #33
    bl native_fn_02048fac
    mov r0, #1
    bl native_fn_02045738
    ldr r0, =0x02239d6c
    mov r1, #127
    str r1, [r0, #0x28]
    ldr r2, =0x02239c9c
    mov r0, #0
ov001_021fc390_L178:
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    cmp r0, #6
    strb r1, [r2], #1
    blt ov001_021fc390_L178
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
