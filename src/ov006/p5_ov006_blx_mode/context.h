#ifndef P5_OV006_BLX_MODE_CONTEXT_H
#define P5_OV006_BLX_MODE_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Four adjacent Thumb rows that call ARM functions through an R_ARM_THM_CALL
   relocation. The original linker expanded that relocation to a BLX immediate
   (second halfword bit 12 clear). mwccarm emits the BL placeholder for every
   interworking call, so the mode has to come from the target:
   docs/authoring/2026-11-11-blx-mode-fix.md. */

#endif
