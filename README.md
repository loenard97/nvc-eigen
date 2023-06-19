<div align="center">

# nvc-eigen
NV-center Hamiltonian library

![](https://img.shields.io/github/last-commit/loenard97/nvc-eigen?&style=for-the-badge&logo=github&color=3776AB)
![](https://img.shields.io/github/repo-size/loenard97/nvc-eigen?&style=for-the-badge&logo=github&color=3776AB)

</div>


# 📖 Library
This library contains helper functions for solving the NV-center Hamiltonian:
```math
H = H_{ss} + g_s H_B  = 
\left( \begin{matrix}
    D & 0 & E \\
    0 & 0 & 0 \\
    E & 0 & D \\
\end{matrix} \right) 
+
\left( \begin{matrix}
    B_z                              & \frac{1}{\sqrt{2}}(B_x + i B_y)  & 0                                \\
    \frac{1}{\sqrt{2}}(B_x - i B_y)  & 0                                & \frac{1}{\sqrt{2}}(B_x + i B_y)  \\
    0                                & \frac{1}{\sqrt{2}}(B_x - i B_y)  & -B_z                             \\
\end{matrix} \right)
```

## Usage
```python
from nveigen.solver import HSolver
from nveigen.vector import Vector3D

# create new solver (constants E, D and g can optionally be set via attributes)
solver = HSolver()

# solve Hamiltonian for given B-field, returns numpy array of resonances in MHz
b_field = Vector3D(7, -10, 9)
resonances = solver.solve_resonances(b_field)

# try to optimize Hamiltonian for given resonances and estimated B-field
meas_freq = [2444, 3347, 2614, 3274, 2942, 3054, 2833, 3142]
b_estimate = Vector(10, 30, -15)
meas_field = solver.solve_b_field(meas_freq, b_estimate)
```


# 🔍 Visualization tool
Additionally a visualization tool that plots the resulting ODMR spectrum is included and can be downloaded [here](https://github.com/loenard97/nvc-eigen/releases)

![](/screenshots/screenshot.png)
