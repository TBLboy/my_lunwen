/*
 * Robot_Real_data.c
 *
 * Code generation for model "Robot_Real".
 *
 * Model version              : 1.12
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Fri Nov  7 13:04:05 2025
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "Robot_Real.h"
#include "Robot_Real_private.h"

/* Block parameters (default storage) */
P_Robot_Real_T Robot_Real_P = {
  /* Variable: seed1
   * Referenced by: '<Root>/Uniform Random Number'
   */
  964888.53519927652,

  /* Variable: seed2
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  157613.0816775483,

  /* Variable: seed3
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  970592.78176061565,

  /* Mask Parameter: Memory2_initial_condition
   * Referenced by: '<Root>/Memory2'
   */
  0.0,

  /* Mask Parameter: Memory1_initial_condition
   * Referenced by: '<Root>/Memory1'
   */
  0.0,

  /* Mask Parameter: Memory_initial_condition
   * Referenced by: '<Root>/Memory'
   */
  0.0,

  /* Expression: [0.3,0.29,0.2]
   * Referenced by: '<Root>/Saturation'
   */
  { 0.3, 0.29, 0.2 },

  /* Expression: [-0.3,-0.29,-0.2]
   * Referenced by: '<Root>/Saturation'
   */
  { -0.3, -0.29, -0.2 },

  /* Computed Parameter: TransferFcn_A
   * Referenced by: '<Root>/Transfer Fcn'
   */
  -10.0,

  /* Computed Parameter: TransferFcn_C
   * Referenced by: '<Root>/Transfer Fcn'
   */
  10.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain'
   */
  1.0,

  /* Computed Parameter: TransferFcn1_A
   * Referenced by: '<Root>/Transfer Fcn1'
   */
  -10.0,

  /* Computed Parameter: TransferFcn1_C
   * Referenced by: '<Root>/Transfer Fcn1'
   */
  10.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain1'
   */
  1.0,

  /* Computed Parameter: TransferFcn2_A
   * Referenced by: '<Root>/Transfer Fcn2'
   */
  -10.0,

  /* Computed Parameter: TransferFcn2_C
   * Referenced by: '<Root>/Transfer Fcn2'
   */
  10.0,

  /* Expression: 1
   * Referenced by: '<Root>/Gain2'
   */
  1.0,

  /* Expression: 20
   * Referenced by: '<Root>/Gain3'
   */
  20.0,

  /* Expression: -0.3
   * Referenced by: '<Root>/Uniform Random Number'
   */
  -0.3,

  /* Expression: 0.3
   * Referenced by: '<Root>/Uniform Random Number'
   */
  0.3,

  /* Expression: -0.29
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  -0.29,

  /* Expression: 0.29
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  0.29,

  /* Expression: -0.2
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  -0.2,

  /* Expression: 0.2
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  0.2
};
