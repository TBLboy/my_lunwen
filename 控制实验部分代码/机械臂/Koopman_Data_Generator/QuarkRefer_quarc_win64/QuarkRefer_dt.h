/*
 * QuarkRefer_dt.h
 *
 * Code generation for model "QuarkRefer".
 *
 * Model version              : 1.35
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Sun Nov  9 21:16:39 2025
 *
 * Target selection: quarc_win64.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "ext_types.h"

/* data type size table */
static uint_T rtDataTypeSizes[] = {
  sizeof(real_T),
  sizeof(real32_T),
  sizeof(int8_T),
  sizeof(uint8_T),
  sizeof(int16_T),
  sizeof(uint16_T),
  sizeof(int32_T),
  sizeof(uint32_T),
  sizeof(boolean_T),
  sizeof(fcn_call_T),
  sizeof(int_T),
  sizeof(pointer_T),
  sizeof(action_T),
  2*sizeof(uint32_T),
  sizeof(t_phantom_properties)
};

/* data type name table */
static const char_T * rtDataTypeNames[] = {
  "real_T",
  "real32_T",
  "int8_T",
  "uint8_T",
  "int16_T",
  "uint16_T",
  "int32_T",
  "uint32_T",
  "boolean_T",
  "fcn_call_T",
  "int_T",
  "pointer_T",
  "action_T",
  "timer_uint32_pair_T",
  "t_phantom_properties"
};

/* data type transitions for block I/O structure */
static DataTypeTransition rtBTransitions[] = {
  { (char_T *)(&QuarkRefer_B.Sum[0]), 0, 0, 37 },

  { (char_T *)(&QuarkRefer_B.LeftDevice_o1), 6, 0, 2 }
  ,

  { (char_T *)(&QuarkRefer_DW.Memory2_Value[0]), 0, 0, 20 },

  { (char_T *)(&QuarkRefer_DW.LeftDevice_Phantom), 14, 0, 1 },

  { (char_T *)(&QuarkRefer_DW.Scope_PWORK.LoggedData), 11, 0, 28 },

  { (char_T *)(&QuarkRefer_DW.Memory2_ValueDims), 6, 0, 3 },

  { (char_T *)(&QuarkRefer_DW.RandSeed), 7, 0, 3 }
};

/* data type transition table for block I/O structure */
static DataTypeTransitionTable rtBTransTable = {
  7U,
  rtBTransitions
};

/* data type transitions for Parameters structure */
static DataTypeTransition rtPTransitions[] = {
  { (char_T *)(&QuarkRefer_P.seed1), 0, 0, 38 }
};

/* data type transition table for Parameters structure */
static DataTypeTransitionTable rtPTransTable = {
  1U,
  rtPTransitions
};

/* [EOF] QuarkRefer_dt.h */
