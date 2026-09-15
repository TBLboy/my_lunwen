# Reading Note: Feature-selection-based Koopman Modeling and Robust LQR Control of Robots

- Reading level: L2 (structured deep read, controller-focused)
- Purpose: extract the paper's controller design before transferring it to the soft-platform 2D xy system
- Source: `C:/Users/Windows/Desktop/论文材料/论文.txt`

## Conclusion

The paper designs a feedforward-feedback LQR controller in the learned Koopman
augmented state space. The feedforward term compensates the nominal lifted
reference dynamics, the LQR feedback gain corrects the lifted-state deviation,
and modeling/sensor/environment uncertainty is treated as a bounded disturbance
so the closed-loop tracking error is ultimately uniformly bounded (UUB).

## Controller Design

The learned model used by the controller is:

```text
z_{k+1} = A z_k + B u_k + w_k
```

where `z_k = [x_k; D * Phi(x_k)]`, `A` and `B` are the learned Koopman matrices,
and `w_k` is the lumped bounded disturbance with `||w_k|| <= delta_w`.

The reference trajectory in physical coordinates `x_ref` is lifted with the same
dictionary and selection matrix:

```text
z_ref = [x_ref; D * Phi(x_ref)]
```

The infinite-horizon LQR cost is:

```text
J = sum_k (z_k - z_ref)^T Q (z_k - z_ref) + u_k^T R u_k
```

with `Q = C^T Q_x C`, `C = [I_n, 0]`, and `R > 0`. Thus `Q` weights the original
physical state through the projection matrix.

The control law is:

```text
u_k = u_ff - K_lqr * (z_k - z_ref)
```

where:

```text
u_ff = B^dagger * (z_ref_{k+1} - A * z_ref_k)
```

The feedback gain `K_lqr` is obtained from standard discrete-time LQR after
assuming `(A, B)` is stabilizable. The closed-loop error satisfies:

```text
e_{k+1} = (A - B K_lqr) e_k + w_k
```

Since `A_cl = A - B K_lqr` is Schur stable, Lyapunov analysis gives UUB tracking
with `||x_k - x_ref|| <= R`, where `R` depends linearly on `delta_w`.

## Mapping to Current Soft-Platform Code

- Physical state: `x in R^2` (xy coordinate)
- Control input: `u in R^2`
- FS-EDMD lifted state: `z = [x; D * Phi(x)]`, matching the paper
- `A_model` / `B_model` in `OursKoopmanTrainer` correspond to `A` / `B`
- `D_model` corresponds to the learned feature selection matrix `D`
- `Phi(x)` is `SoftLift` in the current modeling code
- The paper's `C = [I_n, 0]` matches the current physical state extraction

## Open Questions Before Implementation

- Are the reference trajectories defined in raw physical xy units or normalized units?
- Should `Q_x` and `R` be tuned or fixed for the soft platform?
- Is `u` the raw cable/rod displacement command or a normalized control signal?
- Should the controller be simulated with `model.predict`, or is there a plant simulator available?
- Are there input/output saturation constraints that the paper's current LQR formulation does not handle?
