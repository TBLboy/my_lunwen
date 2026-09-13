/*
 * QuarkRefer.h
 *
 * Code generation for model "QuarkRefer".
 *
 * Model version              : 1.35
 * Simulink Coder version : 8.14 (R2018a) 06-Feb-2018
 * C source code generated on : Sat Nov  8 19:36:23 2025
 *
 * Target selection: quarc_win64.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef RTW_HEADER_QuarkRefer_h_
#define RTW_HEADER_QuarkRefer_h_
#include <math.h>
#include <float.h>
#include <string.h>
#ifndef QuarkRefer_COMMON_INCLUDES_
# define QuarkRefer_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "rtw_extmode.h"
#include "sysran_types.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"
#include "dt_info.h"
#include "ext_work.h"
#include "quanser_phantom.h"
#include "quanser_messages.h"
#include "quanser_extern.h"
#endif                                 /* QuarkRefer_COMMON_INCLUDES_ */

#include "QuarkRefer_types.h"

/* Shared type includes */
#include "multiword_types.h"
#include "rtGetInf.h"
#include "rt_nonfinite.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetContStateDisabled
# define rtmGetContStateDisabled(rtm)  ((rtm)->contStateDisabled)
#endif

#ifndef rtmSetContStateDisabled
# define rtmSetContStateDisabled(rtm, val) ((rtm)->contStateDisabled = (val))
#endif

#ifndef rtmGetContStates
# define rtmGetContStates(rtm)         ((rtm)->contStates)
#endif

#ifndef rtmSetContStates
# define rtmSetContStates(rtm, val)    ((rtm)->contStates = (val))
#endif

#ifndef rtmGetContTimeOutputInconsistentWithStateAtMajorStepFlag
# define rtmGetContTimeOutputInconsistentWithStateAtMajorStepFlag(rtm) ((rtm)->CTOutputIncnstWithState)
#endif

#ifndef rtmSetContTimeOutputInconsistentWithStateAtMajorStepFlag
# define rtmSetContTimeOutputInconsistentWithStateAtMajorStepFlag(rtm, val) ((rtm)->CTOutputIncnstWithState = (val))
#endif

#ifndef rtmGetDerivCacheNeedsReset
# define rtmGetDerivCacheNeedsReset(rtm) ((rtm)->derivCacheNeedsReset)
#endif

#ifndef rtmSetDerivCacheNeedsReset
# define rtmSetDerivCacheNeedsReset(rtm, val) ((rtm)->derivCacheNeedsReset = (val))
#endif

#ifndef rtmGetFinalTime
# define rtmGetFinalTime(rtm)          ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetIntgData
# define rtmGetIntgData(rtm)           ((rtm)->intgData)
#endif

#ifndef rtmSetIntgData
# define rtmSetIntgData(rtm, val)      ((rtm)->intgData = (val))
#endif

#ifndef rtmGetOdeF
# define rtmGetOdeF(rtm)               ((rtm)->odeF)
#endif

#ifndef rtmSetOdeF
# define rtmSetOdeF(rtm, val)          ((rtm)->odeF = (val))
#endif

#ifndef rtmGetOdeY
# define rtmGetOdeY(rtm)               ((rtm)->odeY)
#endif

#ifndef rtmSetOdeY
# define rtmSetOdeY(rtm, val)          ((rtm)->odeY = (val))
#endif

#ifndef rtmGetPeriodicContStateIndices
# define rtmGetPeriodicContStateIndices(rtm) ((rtm)->periodicContStateIndices)
#endif

#ifndef rtmSetPeriodicContStateIndices
# define rtmSetPeriodicContStateIndices(rtm, val) ((rtm)->periodicContStateIndices = (val))
#endif

#ifndef rtmGetPeriodicContStateRanges
# define rtmGetPeriodicContStateRanges(rtm) ((rtm)->periodicContStateRanges)
#endif

#ifndef rtmSetPeriodicContStateRanges
# define rtmSetPeriodicContStateRanges(rtm, val) ((rtm)->periodicContStateRanges = (val))
#endif

#ifndef rtmGetRTWExtModeInfo
# define rtmGetRTWExtModeInfo(rtm)     ((rtm)->extModeInfo)
#endif

#ifndef rtmGetZCCacheNeedsReset
# define rtmGetZCCacheNeedsReset(rtm)  ((rtm)->zCCacheNeedsReset)
#endif

#ifndef rtmSetZCCacheNeedsReset
# define rtmSetZCCacheNeedsReset(rtm, val) ((rtm)->zCCacheNeedsReset = (val))
#endif

#ifndef rtmGetdX
# define rtmGetdX(rtm)                 ((rtm)->derivs)
#endif

#ifndef rtmSetdX
# define rtmSetdX(rtm, val)            ((rtm)->derivs = (val))
#endif

#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

#ifndef rtmGetStopRequested
# define rtmGetStopRequested(rtm)      ((rtm)->Timing.stopRequestedFlag)
#endif

#ifndef rtmSetStopRequested
# define rtmSetStopRequested(rtm, val) ((rtm)->Timing.stopRequestedFlag = (val))
#endif

#ifndef rtmGetStopRequestedPtr
# define rtmGetStopRequestedPtr(rtm)   (&((rtm)->Timing.stopRequestedFlag))
#endif

#ifndef rtmGetT
# define rtmGetT(rtm)                  (rtmGetTPtr((rtm))[0])
#endif

#ifndef rtmGetTFinal
# define rtmGetTFinal(rtm)             ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetTPtr
# define rtmGetTPtr(rtm)               ((rtm)->Timing.t)
#endif

/* Block signals (default storage) */
typedef struct {
  real_T Sum[3];                       /* '<Root>/Sum' */
  real_T Saturation[3];                /* '<Root>/Saturation' */
  real_T Gain;                         /* '<Root>/Gain' */
  real_T LeftDevice_o2[3];             /* '<S3>/Left Device' */
  real_T LeftDevice_o3[3];             /* '<S3>/Left Device' */
  real_T Derivative[3];                /* '<S3>/Derivative' */
  real_T Gain1;                        /* '<Root>/Gain1' */
  real_T Gain2;                        /* '<Root>/Gain2' */
  real_T TmpSignalConversionAtToWorkspac[6];/* '<Root>/Subsystem' */
  real_T Gain3[3];                     /* '<Root>/Gain3' */
  real_T Gain5;                        /* '<Root>/Gain5' */
  real_T Gain6;                        /* '<Root>/Gain6' */
  real_T Gain7;                        /* '<Root>/Gain7' */
  real_T UniformRandomNumber;          /* '<Root>/Uniform Random Number' */
  real_T UniformRandomNumber1;         /* '<Root>/Uniform Random Number1' */
  real_T UniformRandomNumber2;         /* '<Root>/Uniform Random Number2' */
  real_T Clock;                        /* '<Root>/Clock' */
  real_T tau[3];                       /* '<Root>/MATLAB Function' */
  int32_T LeftDevice_o1;               /* '<S3>/Left Device' */
  int32_T LeftDevice_o4;               /* '<S3>/Left Device' */
} B_QuarkRefer_T;

/* Block states (default storage) for system '<Root>' */
typedef struct {
  real_T Memory2_Value[3];             /* '<Root>/Memory2' */
  real_T Memory1_Value[3];             /* '<Root>/Memory1' */
  real_T Memory_Value[3];              /* '<Root>/Memory' */
  real_T TimeStampA;                   /* '<S3>/Derivative' */
  real_T LastUAtTimeA[3];              /* '<S3>/Derivative' */
  real_T TimeStampB;                   /* '<S3>/Derivative' */
  real_T LastUAtTimeB[3];              /* '<S3>/Derivative' */
  real_T UniformRandomNumber_NextOutput;/* '<Root>/Uniform Random Number' */
  real_T UniformRandomNumber1_NextOutput;/* '<Root>/Uniform Random Number1' */
  real_T UniformRandomNumber2_NextOutput;/* '<Root>/Uniform Random Number2' */
  t_phantom_properties LeftDevice_Phantom;/* '<S3>/Left Device' */
  struct {
    void *LoggedData;
  } Scope_PWORK;                       /* '<Root>/Scope' */

  struct {
    void *LoggedData;
  } Scope1_PWORK;                      /* '<Root>/Scope1' */

  struct {
    void *LoggedData;
  } Scope10_PWORK;                     /* '<Root>/Scope10' */

  struct {
    void *LoggedData;
  } Scope11_PWORK;                     /* '<Root>/Scope11' */

  struct {
    void *LoggedData;
  } Scope12_PWORK;                     /* '<Root>/Scope12' */

  struct {
    void *LoggedData;
  } Scope13_PWORK;                     /* '<Root>/Scope13' */

  struct {
    void *LoggedData;
  } Scope14_PWORK;                     /* '<Root>/Scope14' */

  struct {
    void *LoggedData;
  } Scope15_PWORK;                     /* '<Root>/Scope15' */

  struct {
    void *LoggedData;
  } Scope16_PWORK;                     /* '<Root>/Scope16' */

  struct {
    void *LoggedData;
  } Scope17_PWORK;                     /* '<Root>/Scope17' */

  struct {
    void *LoggedData;
  } Scope2_PWORK;                      /* '<Root>/Scope2' */

  struct {
    void *LoggedData;
  } Scope3_PWORK;                      /* '<Root>/Scope3' */

  struct {
    void *LoggedData;
  } Scope4_PWORK;                      /* '<Root>/Scope4' */

  struct {
    void *LoggedData;
  } Scope5_PWORK;                      /* '<Root>/Scope5' */

  struct {
    void *LoggedData;
  } Scope6_PWORK;                      /* '<Root>/Scope6' */

  struct {
    void *LoggedData;
  } Scope7_PWORK;                      /* '<Root>/Scope7' */

  struct {
    void *LoggedData;
  } Scope8_PWORK;                      /* '<Root>/Scope8' */

  struct {
    void *LoggedData;
  } Scope9_PWORK;                      /* '<Root>/Scope9' */

  struct {
    void *LoggedData;
  } ToWorkspace_PWORK;                 /* '<Root>/To Workspace' */

  struct {
    void *LoggedData;
  } ToWorkspace1_PWORK;                /* '<Root>/To Workspace1' */

  struct {
    void *LoggedData;
  } Scope_PWORK_p;                     /* '<S3>/Scope' */

  struct {
    void *LoggedData;
  } Scope1_PWORK_f;                    /* '<S3>/Scope1' */

  struct {
    void *LoggedData;
  } Scope2_PWORK_p;                    /* '<S3>/Scope2' */

  struct {
    void *LoggedData;
  } Scope3_PWORK_g;                    /* '<S3>/Scope3' */

  struct {
    void *LoggedData;
  } Scope4_PWORK_o;                    /* '<S3>/Scope4' */

  struct {
    void *LoggedData;
  } Scope5_PWORK_m;                    /* '<S3>/Scope5' */

  struct {
    void *LoggedData;
  } Scope6_PWORK_c;                    /* '<S3>/Scope6' */

  struct {
    void *LoggedData;
  } ToWorkspace2_PWORK;                /* '<Root>/To Workspace2' */

  int32_T Memory2_ValueDims;           /* '<Root>/Memory2' */
  int32_T Memory1_ValueDims;           /* '<Root>/Memory1' */
  int32_T Memory_ValueDims;            /* '<Root>/Memory' */
  uint32_T RandSeed;                   /* '<Root>/Uniform Random Number' */
  uint32_T RandSeed_o;                 /* '<Root>/Uniform Random Number1' */
  uint32_T RandSeed_g;                 /* '<Root>/Uniform Random Number2' */
} DW_QuarkRefer_T;

/* Continuous states (default storage) */
typedef struct {
  real_T TransferFcn_CSTATE;           /* '<Root>/Transfer Fcn' */
  real_T TransferFcn1_CSTATE;          /* '<Root>/Transfer Fcn1' */
  real_T TransferFcn2_CSTATE;          /* '<Root>/Transfer Fcn2' */
} X_QuarkRefer_T;

/* State derivatives (default storage) */
typedef struct {
  real_T TransferFcn_CSTATE;           /* '<Root>/Transfer Fcn' */
  real_T TransferFcn1_CSTATE;          /* '<Root>/Transfer Fcn1' */
  real_T TransferFcn2_CSTATE;          /* '<Root>/Transfer Fcn2' */
} XDot_QuarkRefer_T;

/* State disabled  */
typedef struct {
  boolean_T TransferFcn_CSTATE;        /* '<Root>/Transfer Fcn' */
  boolean_T TransferFcn1_CSTATE;       /* '<Root>/Transfer Fcn1' */
  boolean_T TransferFcn2_CSTATE;       /* '<Root>/Transfer Fcn2' */
} XDis_QuarkRefer_T;

#ifndef ODE3_INTG
#define ODE3_INTG

/* ODE3 Integration Data */
typedef struct {
  real_T *y;                           /* output */
  real_T *f[3];                        /* derivatives */
} ODE3_IntgData;

#endif

/* Parameters (default storage) */
struct P_QuarkRefer_T_ {
  real_T seed1;                        /* Variable: seed1
                                        * Referenced by: '<Root>/Uniform Random Number'
                                        */
  real_T seed2;                        /* Variable: seed2
                                        * Referenced by: '<Root>/Uniform Random Number1'
                                        */
  real_T seed3;                        /* Variable: seed3
                                        * Referenced by: '<Root>/Uniform Random Number2'
                                        */
  real_T Memory2_initial_condition[3]; /* Mask Parameter: Memory2_initial_condition
                                        * Referenced by: '<Root>/Memory2'
                                        */
  real_T Memory1_initial_condition;    /* Mask Parameter: Memory1_initial_condition
                                        * Referenced by: '<Root>/Memory1'
                                        */
  real_T Memory_initial_condition[3];  /* Mask Parameter: Memory_initial_condition
                                        * Referenced by: '<Root>/Memory'
                                        */
  real_T Saturation_UpperSat[3];       /* Expression: [0.3 0.29 0.2]
                                        * Referenced by: '<Root>/Saturation'
                                        */
  real_T Saturation_LowerSat[3];       /* Expression: [-0.3 -0.29 -0.2]
                                        * Referenced by: '<Root>/Saturation'
                                        */
  real_T TransferFcn_A;                /* Computed Parameter: TransferFcn_A
                                        * Referenced by: '<Root>/Transfer Fcn'
                                        */
  real_T TransferFcn_C;                /* Computed Parameter: TransferFcn_C
                                        * Referenced by: '<Root>/Transfer Fcn'
                                        */
  real_T Gain_Gain;                    /* Expression: 1.6
                                        * Referenced by: '<Root>/Gain'
                                        */
  real_T TransferFcn1_A;               /* Computed Parameter: TransferFcn1_A
                                        * Referenced by: '<Root>/Transfer Fcn1'
                                        */
  real_T TransferFcn1_C;               /* Computed Parameter: TransferFcn1_C
                                        * Referenced by: '<Root>/Transfer Fcn1'
                                        */
  real_T Gain1_Gain;                   /* Expression: 1.6
                                        * Referenced by: '<Root>/Gain1'
                                        */
  real_T TransferFcn2_A;               /* Computed Parameter: TransferFcn2_A
                                        * Referenced by: '<Root>/Transfer Fcn2'
                                        */
  real_T TransferFcn2_C;               /* Computed Parameter: TransferFcn2_C
                                        * Referenced by: '<Root>/Transfer Fcn2'
                                        */
  real_T Gain2_Gain;                   /* Expression: 1.5
                                        * Referenced by: '<Root>/Gain2'
                                        */
  real_T Gain3_Gain;                   /* Expression: 20
                                        * Referenced by: '<Root>/Gain3'
                                        */
  real_T Gain4_Gain;                   /* Expression: 1
                                        * Referenced by: '<Root>/Gain4'
                                        */
  real_T Gain5_Gain;                   /* Expression: 1
                                        * Referenced by: '<Root>/Gain5'
                                        */
  real_T Gain6_Gain;                   /* Expression: 1
                                        * Referenced by: '<Root>/Gain6'
                                        */
  real_T Gain7_Gain;                   /* Expression: 0.5
                                        * Referenced by: '<Root>/Gain7'
                                        */
  real_T Gain8_Gain;                   /* Expression: 1
                                        * Referenced by: '<Root>/Gain8'
                                        */
  real_T Gain9_Gain;                   /* Expression: 1
                                        * Referenced by: '<Root>/Gain9'
                                        */
  real_T UniformRandomNumber_Minimum;  /* Expression: -0.3
                                        * Referenced by: '<Root>/Uniform Random Number'
                                        */
  real_T UniformRandomNumber_Maximum;  /* Expression: 0.3
                                        * Referenced by: '<Root>/Uniform Random Number'
                                        */
  real_T UniformRandomNumber1_Minimum; /* Expression: -0.3
                                        * Referenced by: '<Root>/Uniform Random Number1'
                                        */
  real_T UniformRandomNumber1_Maximum; /* Expression: 0.3
                                        * Referenced by: '<Root>/Uniform Random Number1'
                                        */
  real_T UniformRandomNumber2_Minimum; /* Expression: -0.2
                                        * Referenced by: '<Root>/Uniform Random Number2'
                                        */
  real_T UniformRandomNumber2_Maximum; /* Expression: 0.2
                                        * Referenced by: '<Root>/Uniform Random Number2'
                                        */
};

/* Real-time Model Data Structure */
struct tag_RTM_QuarkRefer_T {
  const char_T *errorStatus;
  RTWExtModeInfo *extModeInfo;
  RTWSolverInfo solverInfo;
  X_QuarkRefer_T *contStates;
  int_T *periodicContStateIndices;
  real_T *periodicContStateRanges;
  real_T *derivs;
  boolean_T *contStateDisabled;
  boolean_T zCCacheNeedsReset;
  boolean_T derivCacheNeedsReset;
  boolean_T CTOutputIncnstWithState;
  real_T odeY[3];
  real_T odeF[3][3];
  ODE3_IntgData intgData;

  /*
   * Sizes:
   * The following substructure contains sizes information
   * for many of the model attributes such as inputs, outputs,
   * dwork, sample times, etc.
   */
  struct {
    uint32_T checksums[4];
    int_T numContStates;
    int_T numPeriodicContStates;
    int_T numSampTimes;
  } Sizes;

  /*
   * SpecialInfo:
   * The following substructure contains special information
   * related to other components that are dependent on RTW.
   */
  struct {
    const void *mappingInfo;
  } SpecialInfo;

  /*
   * Timing:
   * The following substructure contains information regarding
   * the timing information for the model.
   */
  struct {
    uint32_T clockTick0;
    uint32_T clockTickH0;
    time_T stepSize0;
    uint32_T clockTick1;
    uint32_T clockTickH1;
    uint32_T clockTick2;
    uint32_T clockTickH2;
    struct {
      uint8_T TID[3];
    } TaskCounters;

    time_T tFinal;
    SimTimeStep simTimeStep;
    boolean_T stopRequestedFlag;
    time_T *t;
    time_T tArray[3];
  } Timing;
};

/* Block parameters (default storage) */
extern P_QuarkRefer_T QuarkRefer_P;

/* Block signals (default storage) */
extern B_QuarkRefer_T QuarkRefer_B;

/* Continuous states (default storage) */
extern X_QuarkRefer_T QuarkRefer_X;

/* Block states (default storage) */
extern DW_QuarkRefer_T QuarkRefer_DW;

/* Model entry point functions */
extern void QuarkRefer_initialize(void);
extern void QuarkRefer_step(void);
extern void QuarkRefer_terminate(void);

/* Real-time Model object */
extern RT_MODEL_QuarkRefer_T *const QuarkRefer_M;

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'QuarkRefer'
 * '<S1>'   : 'QuarkRefer/MATLAB Function'
 * '<S2>'   : 'QuarkRefer/MATLAB Function1'
 * '<S3>'   : 'QuarkRefer/Subsystem'
 */
#endif                                 /* RTW_HEADER_QuarkRefer_h_ */
