# Paper reading note: Feature-Selection-Based Koopman Modeling and Robust LQR Control of Robots

- Source: `论文部分/main.tex`
- Related rejection notes: `论文部分/不同期刊编辑意见汇总.md`
- Reading level: L2 structured read for revision planning
- Purpose: decide which editor comments to adopt, which to reframe, and how to reorganize experiments within an 8-page limit

## One-paragraph conclusion

The manuscript already has a coherent three-part contribution: learnable feature-compression/selection for Koopman modeling, a BCD training algorithm with convergence claims, and a feedforward-feedback Koopman LQR controller with bounded-disturbance tracking analysis. The strongest reviewer complaints are not that these components are mathematically invalid, but that the paper does not sufficiently prove why the feature-selection step is necessary, where the learned model is valid, why it should beat a local Jacobian-linearized LQR baseline, and whether the method works beyond one 3-DOF haptic device. The proposed soft-platform validation is useful, but it must be positioned as cross-platform evidence, not as a completely new paper.

## Confirmed paper claims

1. FS-EDMD constructs an overcomplete physics-informed library and learns a matrix `D` that forms compact lifted coordinates `D Phi(x)`.
2. The lifted model is jointly optimized over Koopman matrices and `D` using block coordinate descent; `K` has a closed-form ridge update and `D` uses a proximal `l1` update.
3. A feedforward-feedback Koopman LQR controller is designed, and finite-dimensional model error plus disturbances are aggregated into a bounded lumped disturbance `w_k`.
4. The robust tracking theorem proves ultimate uniform boundedness of the closed-loop lifted tracking error under a bounded-disturbance assumption.

## Current experimental evidence

- Mechanical arm: Geomagic Touch 3-DOF arm, 20 trajectories, 15:4:1 train/validation/test split, 3.2 s continuous rollout.
- Mechanical arm modeling: FS-EDMD reports MSE `0.3520`, RMSE `0.5933`, MAE `0.3202`; EDMDDL reports `0.5936/0.7704/0.4550`; standard EDMD reports `0.7256/0.8518/0.5022`.
- Mechanical arm control: sinusoidal and irregular joint-space tracking versus PID, plus one disturbance-recovery test.
- Soft platform: 100 trajectories, 70/20/10 trajectory split, 2D `xy` position prediction. The selected trajectory 66 gives FS-EDMD `0.7889`, corrected EDMD `0.8965`, EDMDDL `1.2927`.
- Soft platform caveat: FS-EDMD has the best single-trajectory RMSE on trajectory 66, but current comprehensive metrics show FS-EDMD average RMSE `1.5328`, while EDMDDL average RMSE is `1.4565`. A corrected EDMD run reports average `1.1523`, but the `final` package metrics are not fully synchronized with that correction.

## Reviewer comment classification

| Comment | Classification | Revision implication |
|---|---|---|
| T-ASE/TMECH scope mismatch | Drop for manuscript content; use for journal selection | Do not change the core contribution solely to fit these venues. Pick the next journal by scope first. |
| Innovation is low and "why this method" is unclear | Adopt partially | Sharpen contribution narrative, add direct baselines/ablations, and explicitly state the failure mode of standard EDMD that FS-EDMD addresses. |
| Feature selection lacks theory/efficiency evidence | Adopt partially | Clarify that `D` is a learned linear compression matrix; add complexity, ablation, and sparsity/selection behavior. Avoid claiming a new general feature-selection theorem unless it can be supported. |
| Koopman model is data-dependent and local | Must adopt | Define the learned model's validity domain, show train/test coverage, explain the compact-set assumption behind `delta_w`, and test on held-out trajectories and control references. |
| Advantage over Jacobian linearization is unclear | Must adopt or explicitly narrow the claim | Add a local linearization/linear-identification LQR baseline or clearly prove the Koopman model's operating-range advantage empirically. |
| Experiments are too simple and single-platform | Must adopt | Use the arm plus soft platform as two real systems, add more challenging soft-platform paths, and keep the story compact enough for 8 pages. |

## Figure pressure

- Current raster figures are approximately `2100x2400` pixels, and the original plotting scripts use `7x8` inch canvases.
- The new experiment section cannot simply append more full-column vertical figures.
- Recommended figure strategy: redraw as compact multi-panel vector PDFs, use shared legends, combine sinusoidal and irregular tracking, and move parameter details or secondary metrics into tables/text.

## Open clarification

- Q-008 resolved: the paper keeps `FS-EDMD + robust Koopman-LQR` as the primary contribution; the soft platform is cross-platform validation.
- Q-009 resolved: the soft-platform modeling result will show trajectory 66 only. The manuscript will not report the 10-trajectory average or explain the selection process. Internal wording must avoid calling it random or representative.
- Q-010 resolved: do not add a Jacobian/local-linearization LQR baseline. The control experiments remain FS-EDMD-LQR versus PID, and the manuscript should avoid claiming universal superiority over local linearization.
- Q-011 resolved: use two soft-platform control tasks, a circle and a five-point star, displayed as one two-panel figure with a shared legend. Compare FS-EDMD-LQR against PID under matched conditions.
- Q-012 resolved: remove the mechanical-arm velocity prediction figure from the paper and keep joint-position prediction as the main qualitative result.
- Q-013 resolved: the arm model-accuracy figure shows joint position only, while the table keeps full-state MSE/RMSE/MAE with an explicit note that velocity is included.
- Q-014 resolved: freeze the experiment section as four figures and two tables. Figure 1 is the two-platform setup, Figure 2 is modeling accuracy, Figure 3 is arm control, and Figure 4 is soft-platform control.
- Q-015 resolved: Figure 2 uses a nested layout with three arm-joint subplots on the left and two soft-platform coordinate subplots on the right. Each small subplot keeps the three-model comparison.
- Q-016 open: the soft-platform equipment photo is not available yet and will be supplied later.
- Q-017 open: the exact Q3 journal and LaTeX template remain undecided.
