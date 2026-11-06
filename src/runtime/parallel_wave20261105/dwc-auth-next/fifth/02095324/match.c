#include "context.h"
int native_main_02095324(tagACHOLD * hd)
{
  byte bVar1;
  int iVar2;
  uint uVar3;
  
  if (hd->overrideType == '\0') {
    bVar1 = hd->endType;
  }
  else {
    bVar1 = hd->overrideType;
  }
  uVar3 = (uint)bVar1;
  if (hd->endSequence < 10) {
    if (hd->endState == '\x03') {
      iVar2 = -0xc79c - uVar3;
    }
    else if (hd->endState == '\x04') {
      iVar2 = -0xc800 - uVar3;
    }
    else {
      iVar2 = -0xc864 - uVar3;
    }
  }
  else if (hd->endSequence < 0xd) {
    iVar2 = -52000 - uVar3;
  }
  else if (hd->errorTest == 0) {
    iVar2 = -50000 - uVar3;
  }
  else if (hd->errorTest == -1) {
    iVar2 = -0xcb84 - uVar3;
  }
  else if (hd->errorTest == -2) {
    iVar2 = -0xcbe8 - uVar3;
  }
  else if (hd->errorTest == -3) {
    iVar2 = -0xcc4c - uVar3;
  }
  else if (hd->errorTest == -4) {
    iVar2 = -53000 - uVar3;
  }
  else if (hd->errorTest == -5) {
    iVar2 = -0xcf6c - uVar3;
  }
  else if (hd->errorTest == -6) {
    iVar2 = -0xcfd0 - uVar3;
  }
  else {
    iVar2 = hd->errorTest;
  }
  return iVar2;
}