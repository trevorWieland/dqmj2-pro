/* ov001 row 0x021e2cdc: 356 bytes.
 *
 * What it does: 83 instructions; 20 call(s) to 0x021dba58, 0x021dba58, 0x021dba58, +17 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: loop with 20 calls (83 instructions, 20 calls, 10 branches, 20 back edges, 6 literal slots).
 *
 *   pool +0x14c -> native_data_0222ebd8 (image word 0x0222ebd8)
 *   pool +0x150 -> native_data_0222ebe0 (image word 0x0222ebe0)
 *   pool +0x154 -> native_data_0222ebe8 (image word 0x0222ebe8)
 *   pool +0x158 -> native_data_0222ebf0 (image word 0x0222ebf0)
 *   pool +0x15c -> native_data_0222ebf8 (image word 0x0222ebf8)
 *   pool +0x160 -> constant 0x02238ad0 (image word 0x02238ad0)
 *   branch +0x80 -> +0xa0
 *   branch +0x9c -> +0xd8
 *   branch +0xac -> +0xbc
 *   branch +0xb8 -> +0xd8
 *   branch +0xc0 -> +0xd0
 *   branch +0xcc -> +0xd8
 *   branch +0xe8 -> +0x108
 *   branch +0x104 -> +0x12c
 *   branch +0x114 -> +0x124
 *   branch +0x120 -> +0x12c
 *   test +0x7c cmp r4, #0
 *   test +0xa0 cmp r5, #0
 *   test +0xbc cmp r6, #0
 *   test +0xe4 cmp r8, #0
 *   test +0x108 cmp r7, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e2cdc; the literal pool and
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

extern void native_fn_021dba58(void);
extern void native_fn_021dbac8(void);
extern void native_fn_021d732c(void);
extern void native_fn_021d7d4c(void);
extern void native_fn_021d7574(void);
extern u8 native_data_0222ebd8[];
extern u8 native_data_0222ebe0[];
extern u8 native_data_0222ebe8[];
extern u8 native_data_0222ebf0[];
extern u8 native_data_0222ebf8[];
extern void native_fn_02041510(void);


asm u32 native_ov001_021e2cdc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r0, #0
    mov r1, r0
    bl native_fn_021dba58
    mov r0, #1
    mov r1, #0
    bl native_fn_021dba58
    mov r0, #0
    mov r1, #1
    bl native_fn_021dba58
    mov r6, r0
    mov r0, #1
    mov r1, r0
    bl native_fn_021dba58
    mov r7, r0
    mov r0, #0
    mov r1, #2
    bl native_fn_021dba58
    mov r5, r0
    mov r0, #1
    mov r1, #2
    bl native_fn_021dba58
    mov r0, #0
    bl native_fn_021dbac8
    mov r4, r0
    mov r0, #1
    bl native_fn_021dbac8
    mov r8, r0
    mov r0, #0
    mov r1, #2
    bl native_fn_021d732c
    cmp r4, #0
    beq ov001_021e2cdc_La0
    mov r0, r4
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #0
    mov r2, #1
    bl native_fn_021d7574
    b ov001_021e2cdc_Ld8
ov001_021e2cdc_La0:
    cmp r5, #0
    mov r0, #0
    mov r2, #1
    beq ov001_021e2cdc_Lbc
    ldr r1, =native_data_0222ebd8
    bl native_fn_021d7574
    b ov001_021e2cdc_Ld8
ov001_021e2cdc_Lbc:
    cmp r6, #0
    beq ov001_021e2cdc_Ld0
    ldr r1, =native_data_0222ebe0
    bl native_fn_021d7574
    b ov001_021e2cdc_Ld8
ov001_021e2cdc_Ld0:
    ldr r1, =native_data_0222ebe8
    bl native_fn_021d7574
ov001_021e2cdc_Ld8:
    mov r0, #1
    mov r1, #2
    bl native_fn_021d732c
    cmp r8, #0
    beq ov001_021e2cdc_L108
    mov r0, r8
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #1
    mov r2, #2
    bl native_fn_021d7574
    b ov001_021e2cdc_L12c
ov001_021e2cdc_L108:
    cmp r7, #0
    mov r0, #1
    mov r2, #2
    beq ov001_021e2cdc_L124
    ldr r1, =native_data_0222ebf0
    bl native_fn_021d7574
    b ov001_021e2cdc_L12c
ov001_021e2cdc_L124:
    ldr r1, =native_data_0222ebf8
    bl native_fn_021d7574
ov001_021e2cdc_L12c:
    mov r0, #0
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    ldr r1, =0x02238ad0
    mov r0, #1
    strb r0, [r1, #0x3]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
