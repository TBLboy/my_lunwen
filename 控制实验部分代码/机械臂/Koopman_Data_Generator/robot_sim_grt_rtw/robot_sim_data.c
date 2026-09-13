/*
 * robot_sim_data.c
 *
 * Code generation for model "robot_sim".
 *
 * Model version              : 1.12
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Thu Nov  6 22:06:01 2025
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "robot_sim.h"
#include "robot_sim_private.h"

/* Block parameters (default storage) */
P_robot_sim_T robot_sim_P = {
  /* Variable: seed1
   * Referenced by: '<Root>/Uniform Random Number'
   */
  80741.718817737172,

  /* Variable: seed2
   * Referenced by: '<Root>/Uniform Random Number1'
   */
  382853.46700370213,

  /* Variable: seed3
   * Referenced by: '<Root>/Uniform Random Number2'
   */
  497223.33208966907,

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
